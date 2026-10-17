---
name: awareness-git-sync
description: QwenWork 记忆(awareness)与自研技能同步到 GitHub 私有仓库、并生成换机恢复包的可复用流程。这是本用户管理"记忆/技能与 GitHub 私有库(seailnzq/*)跨机双向同步"的默认技能——凡此主题默认走本技能，无需打英文技能名。Use when 用户说"同步远端git到本机""从git拉回本机""换机恢复""做个换机/迁移恢复包""新机怎么还原记忆技能配置""同步记忆/技能到 git""push awareness 到 GitHub""备份自研技能""周期性同步""备份 cron/凭据清单"，或直接 /awareness-git-sync。方向语义："同步远端git到本机/拉回/恢复"=还原(git→本机)；"同步记忆/技能到 git/push"=上传(本机→git)。
version: 1.3.0
---

# awareness-git-sync

将 QwenWork 的 awareness 记忆文件和自研技能同步推送到 GitHub 私有仓库，并可进一步产出一个**换机恢复包（portable/）**，让新机 clone 后一键还原记忆/技能/配置结构/自动化骨架。

一句话触发："同步记忆到 git"；换机时："做/恢复迁移包"。恢复包各文件的**具体模板**见同目录 `reference/migration-package.md`（bootstrap.ps1 骨架、RESTORE.md 大纲、CRON.md / SECRETS.manifest 字段表、mcp.json 脱敏规则）。

## Steps

### 1. 技能分类与过滤

**目标**: 区分"用户自研技能"与"官方/DWS 市场安装技能"。

1. 读取 `~/.qwenworkcn/skills/.dws-skill-state.json`，获取 `skillNames` 数组 → DWS 市场技能列表。
2. 技能目录中若有 `_meta.json` 且带发布 slug/ownerId（如 `a-stock-realtime` → `a-stock-analysis-litiao`）→ 视为市场发布技能，排除。
3. 硬编码排除列表（官方内置）:
   - `dingtalk-*`（所有前缀匹配）
   - `docx`, `pptx`, `xlsx`, `pdf`, `media-generation`, `media-generation-premium`
   - `find-skills`, `create-skill`, `customize-qwenwork`, `qwenwork-guidance`
   - `plugin-creator`, `generate-pptx`, `ppt-visual-designer`
   - `wps-*`（所有前缀匹配）
4. 扫描 `~/.qwenworkcn/skills/` 下所有目录，减去上述排除集 → 剩余为自研技能。
5. 自研技能中排除 `.temp`、以 `.` 开头的隐藏目录、含 `.bak` 后缀的文件。
6. **权威口径**: frontmatter 里的 `official:` 标记是运行时注入的，不可靠；以仓库 `SKILLS-INDEX.md` 为准（每技能 = 顶层目录 + 索引表一行）。
7. 注意：系统提示的 available_skills 列表可能已包含市场技能（如 dingtalk-*），不能只按它判断自研。

### 2. Awareness 文件选取与 .gitignore

**源目录**: `~/.qwenworkcn/awareness/main/`

**纳入**:
- `MEMORY.md`, `USER.md`, `AGENTS.md`（根目录人读 markdown）
- `memory/*.md`（每日笔记）

**排除（写入 .gitignore）**:
```
.index.sqlite*
.hash-state.json
.memory_meta.json
*.reflection-bak
.memory_evicted.log
.DS_Store
```

**本地 git 仓库路径约定**: `~/github-repos/awareness/`（若不存在则 `git init`）。

**桥接库原则（重要）**:
- **不要在 `~/.qwenworkcn/awareness/main/` 实时源里 git init**——避免污染 awareness 运行时。
- 在 `~/github-repos/awareness/` 建**快照式镜像库**（桥接副本）：每次同步重新复制最新 md 进来再 commit。
- 库内 `README.md` 写明：这是镜像快照、权威源是本机 `~/.qwenworkcn/awareness/main/`、下次刷新方法（重刷 md → commit → 远端有备份提交则先 rebase → push）。
- awareness 库是快照镜像，memory 工具持续改实时源文件，不必追求 git 与实时逐秒一致。

### 3. 隐私扫描（推送前必做）

> ⚠️ 判据以 §8 两轴为准：**金额/仓位数字在私有库属预期允许、不是要清除的命中**；本节真正要拦的只有真凭据（`github_pat_`/`ghp_`/`sk-`/密钥行）。下面的金额/股票代码模式仅作"万一误推到公开库"的兜底提示，私有库命中可放行。

在 awareness 和 skills 仓库中 grep 以下模式:
- 金额数字: `\d{6,}`（6 位以上连续数字，可能是持仓金额）
- 仓位百分比: `仓位.*\d+%`
- 股票代码: `600\d{4}`、`688\d{3}`、`300\d{3}`、`002\d{3}`
- 私密政策关键词: `亲锁`、`退休锚` 等
- Token/密码: `ghp_`, `github_pat_`, `password`, `secret`, `token`
- API Key: `sk-`, `api_key`, `apikey`

**输出规则**: 命中项只打印 ASCII 摘要（文件名 + 行号 + 匹配规则标签），不输出实际内容。
- 命中项逐条人工判读分类（政策语言本身、"亲锁/锚"、公开示例代码 600519 属误报），真命中才拦截。

**PowerShell 编码规避**:
- 将扫描结果写入临时文件（UTF-8），再用 Read tool 读取。
- `.ps1` 脚本中字面量只用 ASCII，避免 PowerShell 5.1 以 GBK 解析 UTF-8 导致字符串终止符报错。
- 不要在命令行内联包含 `$` 的复杂脚本（被 shell wrapper 吞变量），改为写入 `.ps1` 文件后 `powershell -File` 执行。

### 4. 私有性核查

本机无 `gh` CLI 时用 `curl.exe`:
```bash
curl.exe -s -o NUL -w "%{http_code}" https://api.github.com/repos/<owner>/<repo>
```
- 返回 `404` = 仓库私有（或不存在）；`200` = 公开。
- 带 PAT 时加 `-H "Authorization: Bearer <token>"` 区分真正的 404。

### 5. 建仓与推送

**PAT 复用技巧**: 新库 origin 的 token 无需用户提供——从已授权库（如 `~/github-repos/skills`）的 `git config remote.origin.url` 提取内嵌 PAT（`https://github_pat_XXX@github.com/...` 格式），`git remote set-url` 或 `add` 时复用。显示/记录 URL 时必须打码: `-replace '://[^@]+@','://***@'`。

**PAT 权限不足时（403 建仓）**:
1. fine-grained PAT 无 Administration 权限，**不能 API 建库**。告知用户需在 GitHub 网页手工创建空私有仓库（不勾选 README/.gitignore/license）。
2. 等用户确认已建好后，配置 origin 并推送:
   ```bash
   git remote add origin https://<PAT>@github.com/<owner>/<repo>.git
   git push -u origin master
   ```
3. 若 origin 已存在，用 `git remote set-url origin ...` 更新。

**新库白名单（push 报 `Write access to repository not granted` 时）**:
- fine-grained PAT 按仓库逐个授权（Only select repositories）。新建仓库默认不在白名单。
- 让用户在 https://github.com/settings/personal-access-tokens 编辑 token，把新仓库加入 Repository access 白名单。
- 备选方案: 并入已授权库（如在 wiki-life 下开 `awareness/` 子目录），避免动 token。

**日常同步提交**:
```bash
# 推送前先重刷: 重新复制最新 MEMORY.md/USER.md/AGENTS.md + memory/*.md 到 git 目录
# （可捕获当天 memory 工具的增量更新）
git add -A
git commit -m "sync: $(date +%Y-%m-%d)"
git push origin master
```

### 5b. Skills 库增量同步

1. 复制新增/更新的自研技能目录（排除 `.bak` 脏文件）到 `~/github-repos/skills/`。
2. 更新 `SKILLS-INDEX.md`：加增量说明 + 每技能一行表格。
3. 推送前检查各技能体积 <40KB、无大数据 blob；重点核查含持仓/行情代码的技能是否把真实数据写死（运行时外部文件读写则安全）。
4. 复制前对技能内容跑一遍隐私扫描（第 3 节）。

### 6. 分叉与冲突处理

**常见场景**: 远端有 Obsidian/vault-backup 自动提交，本地有手动 sync → `push rejected`。

处理流程:
1. `git fetch origin`
2. 用 `git log --oneline origin/master..HEAD` / `HEAD..origin/master` 确认 AHEAD/BEHIND。
3. `git rebase origin/master`
4. 若 `SKILLS-INDEX.md`（或类似索引文件）冲突:
   - 保留 HEAD（远端）新增行 + 本地新增行，删除 `<<<<<<<`/`=======`/`>>>>>>>` 标记。
   - 不要丢弃任何一方的条目。
5. `git add <冲突文件>` → `$env:GIT_EDITOR='true'; git rebase --continue`
6. `git push origin master`

**stderr 误报**: PowerShell 将 git push 的进度输出（stderr）显示为 `NativeCommandError`/`RemoteException`，这是表面错误，实际推送成功。通过 `git log --oneline -3` 确认 HEAD 已前进即可。

### 7. 导出 cron → CRON.md

换机时"自动化骨架"也要能还原。用连接器工具拉取定时任务清单（**key 是 `qwenwork.cron`，不是 `qwenwork.tasks`**）：

```
qw_query  key = "qwenwork.cron"
```

把返回结果**手工重写**成 `portable/CRON.md`，每个任务保留这些字段，构成可重建的"施工图"（**不要**逐字抄超长 payload，减小泄漏面）：
- 状态（enabled/disabled）、schedule（expr + tz 或 every/at）、model
- 用途（一句话）、依赖（contextDirs / 依赖的 skill / 投递目标会话）
- **骨架 prompt**（先按第 8 节脱敏再落盘）

> mcp.json 与凭据的真实值**不在** cron 里；token/env 在应用登录态与环境变量，故 CRON.md 可安全入库（前提：金额/仓位已脱敏）。

### 8. 敏感值处理（两轴，2026-10-17 修订）

**别再把"落不落 git"当唯一轴——真正的红线是"这台机器的磁盘"。**

- **轴①·私有库无明文问题**：seailnzq/* 均 GitHub **私有**库，仓库访问控制即边界。退休/财务金额、个股仓位比例**可明文入库**（本人 2026-10-17 裁定，覆盖 09-22 的"金额不留明文"清洗；每次此类覆盖记进 wiki-life `log.md`）。→ 因此 git 里已有的金额/仓位**不需要**再去扫描清除，那是过度处理。
- **轴②·本机 DLP 才是红线**：这台是华为公司机、Trellix 文件面实时取证磁盘内容。**别把敏感明文写到本机磁盘**（outputs、临时 md、.ps1 都算），与"将来推去哪个库"无关——落盘即暴露。要往私有库存明文金额，就在**干净的备用机**上编辑后 push。
- **唯一永远不进任何 git（含私有库）**：真实凭据（GitHub PAT、API Key、token、`ghp_`/`github_pat_`/`sk-`）。这是"可用即仿冒 + 云端历史不可抹"的独立风险，非"明文"问题。

**因此"推送前隐私扫描"的目标收窄为：只拦真凭据，不误删金额。** 扫描命中金额/仓位数字属**预期允许**（私有库明文 OK），仅命中下列真凭据模式才必须处理：

```
github_pat_  ghp_  sk-[A-Za-z0-9]  api[_-]?key\s*[:=]  password\s*[:=]
```
- 命中真凭据 → 打码（URL 用 `-replace '://[^@]+@','://***@'`）或移除后再提交。
- 命中金额/仓位 → 保留（除非本会话是要推到**公开**库，那才走占位）。

**`{{私密:见线下账}}` 占位的新语义**：它标的不再是"私有库不能放"，而是 (a) 该值只在本人离线账、**助手从未取得**，或 (b) 回填动作因轴②须留到干净机做。换机到干净机后向本人取值、明文替换并 push（CRON.md 顶部已挂此待办）。

### 9. 换机恢复包 portable/

在 awareness 镜像库内新建 `portable/`，产出**五件套**（各文件的模板骨架见本技能 `reference/migration-package.md`）：

```
awareness/portable/
  RESTORE.md            # 换机恢复 SOP：clone 四库 → 跑 bootstrap → 手工补凭据/私密账/cron → 验证清单
  bootstrap.ps1         # 半自动引导脚本：默认 DRY-RUN，加 -Apply 才写盘；ASCII-only
  CRON.md               # 第 7/8 节产出的自动化施工图（金额/仓位可明文；只扫真凭据）
  SECRETS.manifest.md   # 需在新机重新置备的凭据/登录态清单（只列条目，不含值）
  config/mcp.json       # 脱敏后的 mcp.json 快照（只留结构，无敏感值）
```

**bootstrap.ps1 行为约定**（换机可靠性的核心）：
- 默认 **DRY RUN**，仅打印将执行的动作；显式 `-Apply` 才写盘。参数 `-ReposRoot`、`-QwHome`；靠自身所在目录的 `..` 定位 awareness 库。
- awareness 人读文件（MEMORY/USER/AGENTS + memory/*.md）→ 复制到 `$QwHome\awareness\main`。
- 自研技能目录 → 复制到 `$QwHome\skills`（**排除** `.git`、`SKILLS-INDEX.md`、迁移用的 `.json`）。
- `config/mcp.json` → 仅当 `$QwHome\mcp.json` **不存在**时放置，存在则不覆盖。
- 所有将写入的已存在目标先备份为 `.bak-<timestamp>`，**永不删除**用户文件。
- 结尾打印一份"手工补凭据/私密账/重建 cron"的检查清单。
- **脚本全文 ASCII**（PS 5.1 用 GBK 读含中文的 .ps1 会报"字符串缺少终止符"）。生成后**务必真跑一次 dry-run** 验证语法。

在 awareness 库 `README.md` 加一节 `## portable/ —— 换机恢复工具` 指向并说明这五件套。

## Pitfalls

- **不要同步运行时文件**: `.index.sqlite`、`.hash-state.json` 等是内存索引/缓存，无意义且体积大。
- **不要同步 DWS 市场技能**: 它们由平台管理，版本随时更新，入 git 会产生持续噪声。
- **PowerShell 中文输出**: `Get-ChildItem` 对中文文件名的输出可能 mojibake；用 Glob tool 代替。
- **Read tool 二进制判定**: 如果文件含 `\0` 字节（部分 SQLite 残留），Read 报二进制错误；用 `Select-String` 或 `Get-Content -Encoding UTF8` 处理。
- **`.ps1` 脚本只写 ASCII**: 含中文时 PS 5.1 按 GBK 解析 UTF-8 文件，报"字符串缺少终止符"。
- **不用 `-Command` 内联脚本**: Bash 工具执行 `powershell -Command "...$var..."` 时 `$` 变量被外壳吞掉；改为写 `.ps1` 文件后 `powershell -NoProfile -ExecutionPolicy Bypass -File xxx.ps1`。
- **git/CJK 输出落文件再读**: 含中文的命令输出重定向到文件（`Out-File -Encoding ascii`）后用 Read 工具读，避免被判为二进制或乱码挤掉真实错误。
- **首次 commit 作者信息**: 若全局 git config 未设 user.name/email，需先配置:
  ```bash
  git config user.name "<name>"
  git config user.email "<email>"
  ```
- **Out-File UTF-8 的 BOM 陷阱**: `Set-Content`/`Out-File -Encoding utf8` 会加 BOM，使 Read 工具把该文件判为"二进制"而拒绝。扫描/命令输出改**只写 ASCII 摘要行**（文件名+行号+类别标签，路径本就是 ASCII）再读；或直接 `Get-Content -Encoding UTF8` 读原文件。
- **cron 拉取用 `qwenwork.cron` 不是 `qwenwork.tasks`**: 键写错会得到会话/任务列表而非定时任务清单。
- **别把"金额脱敏"当红线**：私有库允许金额/仓位明文（2026-10-17 裁定），复扫只为抓真凭据。反 pattern 有两个：①把私有库里可留的金额误扫掉、毁了日后可读性；②反过来——在这台 DLP 监控机上把敏感明文写进磁盘（轴②才是真红线），或把真凭据提交进任何 git。放行门槛 = **真凭据残留为 0**（金额/仓位不在此列）。

## Verification

1. `git log --oneline -3` — 确认最新 commit hash 存在。
2. `git status` — 应为 `nothing to commit, working tree clean`。
3. `git remote -v` — 确认 origin URL 指向正确私有仓库。
4. 可选: `curl.exe` 无认证访问仓库 API 确认返回 404（私有）。
5. 在 GitHub 网页确认文件列表与预期一致（自研技能目录、awareness 的 md 文件）。

**换机恢复包专项**:
6. `portable/` 五件套齐全（RESTORE.md / bootstrap.ps1 / CRON.md / SECRETS.manifest.md / config/mcp.json）。
7. `powershell -NoProfile -ExecutionPolicy Bypass -File bootstrap.ps1`（**不带 -Apply**）dry-run 退出码 0、无语法报错，且打印动作符合预期。
8. 第 8 节 `git grep -nE` **真凭据**残留扫描为空（`github_pat_`/`ghp_`/`sk-` 无一命中）；金额/仓位明文属预期、无需为空。
9. `git log` 确认 HEAD 已前进；本地与远端 `git rev-list --left-right --count` 为 `0 0`。

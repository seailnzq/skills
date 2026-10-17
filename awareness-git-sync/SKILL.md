---
name: awareness-git-sync
description: QwenWork 记忆(awareness)与自研技能同步到 GitHub 私有仓库的可复用流程。Use when 用户要求"把记忆/技能同步到 git""push awareness 到 GitHub""备份自研技能""周期性同步"。
version: 1.0.0
---

# awareness-git-sync

将 QwenWork 的 awareness 记忆文件和自研技能同步推送到 GitHub 私有仓库。

## Steps

### 1. 技能分类与过滤

**目标**: 区分"用户自研技能"与"官方/DWS 市场安装技能"。

1. 读取 `~/.qwenworkcn/skills/.dws-skill-state.json`，获取 `skillNames` 数组 → DWS 市场技能列表。
2. 硬编码排除列表（官方内置）:
   - `dingtalk-*`（所有前缀匹配）
   - `docx`, `pptx`, `xlsx`, `pdf`, `media-generation`, `media-generation-premium`
   - `find-skills`, `create-skill`, `customize-qwenwork`, `qwenwork-guidance`
   - `plugin-creator`, `generate-pptx`, `ppt-visual-designer`
   - `wps-*`（所有前缀匹配）
3. 扫描 `~/.qwenworkcn/skills/` 下所有目录，减去上述排除集 → 剩余为自研技能。
4. 自研技能中排除 `.temp`、以 `.` 开头的隐藏目录、含 `.bak` 后缀的文件。

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

### 3. 隐私扫描（推送前必做）

在 awareness 和 skills 仓库中 grep 以下模式:
- 金额数字: `\d{6,}`（6 位以上连续数字，可能是持仓金额）
- Token/密码: `ghp_`, `github_pat_`, `password`, `secret`, `token`
- API Key: `sk-`, `api_key`, `apikey`

**输出规则**: 命中项只打印 ASCII 摘要（文件名 + 行号 + 匹配规则标签），不输出实际内容。

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

**PAT 权限不足时（403 建仓）**:
1. 告知用户需在 GitHub 网页手工创建空私有仓库（不勾选 README/.gitignore/license）。
2. 等用户确认已建好后，配置 origin 并推送:
   ```bash
   git remote add origin https://<PAT>@github.com/<owner>/<repo>.git
   git push -u origin master
   ```
3. 若 origin 已存在，用 `git remote set-url origin ...` 更新。

**日常同步提交**:
```bash
# awareness 仓库
# 重新 copy MEMORY.md/USER.md/memory/*.md 到 git 目录
git add -A
git commit -m "sync: $(date +%Y-%m-%d)"
git push origin master
```

### 6. 分叉与冲突处理

**常见场景**: 远端有 Obsidian/vault-backup 自动提交，本地有手动 sync → `push rejected`。

处理流程:
1. `git fetch origin`
2. `git rebase origin/master`
3. 若 `SKILLS-INDEX.md`（或类似索引文件）冲突:
   - 保留 HEAD（远端）新增行 + 本地新增行，删除 `<<<<<<<`/`=======`/`>>>>>>>` 标记。
   - 不要丢弃任何一方的条目。
4. `git add <冲突文件>` → `git rebase --continue`
5. `git push origin master`

**stderr 误报**: PowerShell 将 git push 的进度输出（stderr）显示为 `NativeCommandError`/`RemoteException`，这是表面错误，实际推送成功。通过 `git log --oneline -3` 确认 HEAD 已前进即可。

## Pitfalls

- **不要同步运行时文件**: `.index.sqlite`、`.hash-state.json` 等是内存索引/缓存，无意义且体积大。
- **不要同步 DWS 市场技能**: 它们由平台管理，版本随时更新，入 git 会产生持续噪声。
- **PowerShell 中文输出**: `Get-ChildItem` 对中文文件名的输出可能 mojibake；用 Glob tool 代替。
- **Read tool 二进制判定**: 如果文件含 `\0` 字节（部分 SQLite 残留），Read 报二进制错误；用 `Select-String` 或 `Get-Content -Encoding UTF8` 处理。
- **首次 commit 作者信息**: 若全局 git config 未设 user.name/email，需先配置:
  ```bash
  git config user.name "<name>"
  git config user.email "<email>"
  ```

## Verification

1. `git log --oneline -3` — 确认最新 commit hash 存在。
2. `git status` — 应为 `nothing to commit, working tree clean`。
3. `git remote -v` — 确认 origin URL 指向正确私有仓库。
4. 可选: `curl.exe` 无认证访问仓库 API 确认返回 404（私有）。
5. 在 GitHub 网页确认文件列表与预期一致（自研技能目录、awareness 的 md 文件）。

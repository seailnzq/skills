---
name: wiki-research-sync
description: "将深度研究主题归档进 wiki-knowledge 知识库的完整闭环：外部检索+库内引用→按 WIKI-SCHEMA 建 synthesis 综合页（双向链接）→更新 index/log→校验链接→git commit+push，并处理代理未开与远端 vault backup 冲突（按时间序保留双方）；也支持对已有综合页追加章节的深化归档。Use when 用户要求深度研究某主题并归档/入库到 wiki、回写综合分析到知识库、对已有综合页追问深化补新章节，或对 wiki-knowledge 做 git 同步与冲突处理。"
version: 1.1.0
---

# Wiki Research Sync — 深度研究归档闭环

将一次外部深度研究落成知识库综合页，并安全同步到远端的流水线；亦覆盖对已有综合页追问深化时的"追加章节"变体（见下文变体一节）。

**与 llm-wiki 的分工**：llm-wiki 定义建库/ingest/query/lint 的通用规范；本技能聚焦"外部研究 → synthesis 归档 → git 同步与冲突处理"闭环。两者配合使用，结构规范以库内 WIKI-SCHEMA.md 为准。

## 固定路径与前提

- 知识库：`C:\Users\l17405\github-repos\wiki-knowledge`（git 仓库，分支 `master`，远端 GitHub）
- 宪法文件：仓库根 `WIKI-SCHEMA.md`（结构、模板、分类体系如有演进，以它为准）
- 结构：`raw/`（不可变原文）＋ `wiki/`（`index.md`、`log.md`、`papers/`、`concepts/`、`entities/`、`synthesis/`）
- 网络：访问 GitHub 依赖本机代理（全局 git config `http.proxy=127.0.0.1:7897`）；该代理可能未开启
- 远端是多端同步仓库（其他机器/会话的 Obsidian vault backup 会推送提交），**push 前永远假设远端有新提交**

## 工作流

### Step 1 预检

```bash
cd "C:/Users/l17405/github-repos/wiki-knowledge" && git status --short && git fetch && git log --oneline HEAD..origin/master | head -5
```

- 读 `WIKI-SCHEMA.md`，确认页面模板与分类体系没有演进。
- 若远端已有新提交，先 `git pull --no-rebase --no-edit` 拿到最新基线再开工，避免收尾时大面积冲突。

### Step 2 外部研究

- WebSearch 中英文双语检索（中文财经媒体与外媒覆盖角度不同，各取所长）。
- 对关键文章用 WebFetch 提取具体数据点。
- 边查边记：关键数字＋日期＋出处，供综合页"数据来源"节使用。

### Step 3 库内引用

- 读 `wiki/index.md` 定位相关 `papers/`、`synthesis/`、`concepts/` 页面。
- 通读每个相关页面。新综合页必须**站在库内已有框架之上**（引用其模型、更新其变量打分、验证其预警），而不是另起炉灶。

### Step 4 撰写综合页

路径：`wiki/synthesis/<年份>-<主题>.md`。模板：

```markdown
---
title: "<主题>（<年-月>）"
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2, ...]
---

# <主题>（YYYY-MM-DD）

> **一句话结论**：……（带 [[库内引用]] 的核心判断）

## 一、现状快照（数据表格）
## 二~N、分析章节（历史复盘 / 机制 / 情景推演 / 对持仓含义……）
## 数据来源（YYYY-MM-DD ~ YYYY-MM-DD）
- 逐条列出：来源 + 日期 + 关键数据点
## See Also
- [[papers/...]] / [[synthesis/...]]
```

所有引用一律用 `[[类别/页面名]]` 或唯一时的 `[[页面名]]`。

### Step 5 双向链接

- 在每个被引用页面的"与已有知识的关系"或"See Also"补一行回链（写明回链理由/日期）。
- 若新证据与既有结论矛盾，显式标注：`> ⚠️ 与 [[xxx]] 的结论相矛盾：...`。
- 更新被引用页时同步其 frontmatter `updated` 字段（当日新建页无需改）。

### Step 6 更新 index / log

- `index.md`：
  - 综合页区追加 `- [[synthesis/页面名]] — 一句话摘要（YYYY-MM-DD 新增）`；
  - 更新底部统计行 `*统计：来源 N 篇 · 概念 N 个 · 实体 N 个 · 综合页 N 个*`；
  - 顺手核对 `synthesis/` 目录，补录已存在但 index 未收录的页面。
- `log.md` 末尾追加（格式统一，便于 `grep "^## \[" log.md | tail -5`）：

```markdown
## [YYYY-MM-DD] synthesis ×1 | <主题>
- 新建综合页：synthesis/xxx（要点……）
- 双向链接已建：<被回链页面清单>
- 更新 index（分类 + 统计 A→B）
```

### Step 7 链接校验

对新页所有 `[[链接]]` 逐一确认目标文件存在（全部 OK 才可提交）：

```bash
cd "C:/Users/l17405/github-repos/wiki-knowledge/wiki" && grep -o "\[\[[^]|]*\]\]" "synthesis/<新页文件名>.md" | sed 's/\[\[//;s/\]\]//' | sort -u | while read p; do case "$p" in papers/*|concepts/*|entities/*|synthesis/*) f="$p.md";; *) f=$(find . -name "$p.md" | head -1);; esac; if [ -f "$f" ]; then echo "OK   $p"; else echo "MISS $p"; fi; done
```

### Step 8 提交

```bash
cd "C:/Users/l17405/github-repos/wiki-knowledge" && git add <本次改动的全部文件> && git commit -m "$(cat <<'EOF'
synthesis: <主题>（YYYY-MM-DD）

- 要点1
- 要点2
EOF
)"
```

`git add` 逐个列出具体文件（中文文件名加引号），不用 `-A`。

### Step 9 推送与冲突处理

1. `git push`。成功即闭环。
2. **被拒（non-fast-forward）** —— 远端 vault backup 有新提交，属常态：

```bash
git fetch && git log --oneline HEAD..origin/master && git log --oneline origin/master..HEAD
git pull --no-rebase --no-edit
```

3. 冲突几乎总在 `index.md` 与 `log.md`（双方各自追加）。解决原则——**双方内容全部保留**：
   - 列表型冲突：两边条目都留，按日期时间序排列（早的在前）；
   - 统计行冲突：采用远端最新统计基数，再叠加本次新增量；
   - log 条目冲突：按日期先后排列两边全部条目。
4. 校验并提交合并：

```bash
grep -rn "<<<<<<<\|>>>>>>>" wiki/index.md wiki/log.md; echo "---markers checked---"
git add wiki/index.md wiki/log.md && git commit --no-edit && git push
```

5. **绝不 `git push --force`**。

### Step 10 网络降级（代理未开）

- 报 `Failed to connect ... over proxy 127.0.0.1` → 先试直连：`git -c http.proxy= -c https.proxy= push`
- 直连也失败 → 提交已安全留在本地；记录 commit hash，告知用户"待代理恢复后补推"，用户确认代理已开后重试 `git push`（重试时按 Step 9 处理可能出现的新提交）。

### Step 11 汇报

告知用户：归档页面路径、建立的双向链接清单、index/log 更新点、推送状态（未推送时明确"本地已提交 + 待补推"事项）。

## 变体：对已有综合页追加章节

用户对既有综合页追问深化时，不新建页面：

1. `Read` 目标页 → 在"数据来源"章节前 `Edit` 插入新编号章节，标题注明追加日期（如 `## 八、<章节标题>（YYYY-MM-DD 追加）`）；
2. "数据来源"章节补新数据行；更新 frontmatter 的 `updated`；
3. log.md 末尾追加 `## [YYYY-MM-DD] update | <页面> · <章节名>`；
4. 若引入新 `[[链接]]` 走 Step 7 校验；按 Step 8-10 提交推送，commit 消息以 `synthesis更新: <标题>——<章节主题>` 开头。

## 常见坑

- **Edit 报 "File has not been read yet"**：本会话用 Write 创建的文件，之后 Edit 也必须先 Read 一次。
- 更新 index 统计行前先数一遍实际目录文件数，历史统计可能已滞后。
- 综合页中的关键数字必须能追溯到 Step 2 的采集记录，不可编造。
- Windows 下 `LF will be replaced by CRLF` 警告无害，忽略。
- `raw/` 是不可变区：除非任务本身包含归档原文，不要动它，也不要误提交。
- 合并冲突后务必 `grep` 校验无残留 `<<<<<<<` / `>>>>>>>` 再提交。
- push 失败时不要反复重试或改动 git 配置：本地提交已是安全状态，降级链走完即止，等用户确认后再补推。

## 验证清单

- [ ] 链接校验脚本输出全部 `OK`，无 `MISS`
- [ ] 新页面 frontmatter 完整、"一句话结论"/See Also/数据来源齐备
- [ ] index.md 有新条目且统计行已更新；log.md 有当日记录
- [ ] 被引用页面均已回链（双向性）
- [ ] `git log --oneline -1` 有本次提交；`git status` 干净
- [ ] `git log --oneline HEAD..origin/master` 为空（与远端一致）

## 辅助文件

`reference.md`：页面骨架模板、index 与 log 条目格式、链接校验脚本、git 提交/降级/冲突处理命令速查。

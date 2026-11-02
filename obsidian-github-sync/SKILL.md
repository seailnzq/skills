---
name: obsidian-github-sync
description: "双向同步 Obsidian vault 与 GitHub 备份仓库：检查状态、拉取远程新增、提交本地改动、推送，并处理浅克隆损坏、packed-refs 无法更新、CRLF 噪音等常见故障。Use when the user asks to sync/backup an Obsidian vault with GitHub, or when git operations in a vault repo behave oddly (refs not updating, bad object HEAD, mysterious mass deletions)."
description_zh: "Obsidian 库与 GitHub 双向同步，含常见 git 故障修复"
description_en: "Two-way sync between Obsidian vaults and GitHub backup repos, with git failure recovery"
allowed-tools: Read,Write,Bash,Grep,Glob
display_name: "Obsidian ↔ GitHub 同步"
display_name_en: "Obsidian ↔ GitHub Sync"
visibility: "private"
---

# Obsidian ↔ GitHub 同步

把 Obsidian vault 与 GitHub 备份仓库拉到一致：**远程的新内容落到本地，本地的新改动推到远程**。

## 核心原则

1. **先诊断再动手。** vault 仓库常年在 Windows + 插件环境下运行，`.git` 可能早已半损坏。
2. **绝不直接在损坏仓库上 rebase。** 会让 `.git/refs` 整个消失（见故障 1）。
3. **远程领先时，先恢复文件再提交。** 否则会把远程新增内容误判成"删除"推上去（见故障 3）。
4. **删除要确认。** 涉及远程文件删除时，先在报告里列清单。

## 标准流程

```bash
cd <vault>
git remote -v                      # 确认仓库
ssh -T git@github.com              # 确认 SSH 可用
git rev-parse --is-shallow-repository
git fetch origin
git status -sb
git ls-remote origin master        # 远程真实状态（别只信本地 ref）
```

### A. 远程领先（behind N）

本地工作区缺少远程新增文件，git 会显示成一堆 `D`。**先恢复，再提交本机改动**：

```bash
# 看远程新提交动了哪些文件
git log --oneline -N origin/master
git diff --name-status HEAD

# 把「远程新增/更新、本地没改过」的文件拉回工作区
git checkout HEAD -- <这些文件>

# 只留本地真实改动，再提交
git add -A && git commit -m "vault backup: $(date '+%Y-%m-%d %H:%M:%S') <摘要>"
git push origin master
git ls-remote origin master        # 验证推送真的生效
```

区分"用户真的删了"和"本地缺远程文件"：对照 `git log --stat` 里远程提交改过的路径。

### B. 本地领先（ahead N）

直接提交 + push。风格沿用仓库既有提交信息（如 `vault backup: YYYY-MM-DD HH:MM:SS …`）。

### C. 两端都有改动

提交本地 → `git rebase origin/master` → push。**前提是仓库健康**；若 `.git` 有损坏迹象，先走故障 1 的修复。

## 故障处理

### 1. `.git` 损坏（bad object HEAD / missing blob / refs 目录消失）

症状：`git status` 报 `bad object HEAD`、`not a git repository`、fsck 报大量 `missing blob`。
**不要**继续 rebase/commit。最安全的修复路径 —— 只换元数据，不动工作区文件：

```bash
mv .git .git.broken-$(date +%Y%m%d)        # 备份（先移出仓库，否则会被 git add 进去！）
git clone git@github.com:<user>/<repo>.git /tmp/reclone
mv /tmp/reclone/.git .git
rm -rf /tmp/reclone
git config user.name "<name>"; git config user.email "<email>"
git status                                  # 自动 diff 出本地改动
```

> 坑：备份的 `.git.broken-*` **必须放到仓库目录外**，否则 `git add -A` 会把它整目录提交上去。

### 2. `packed-refs` 无法更新（fetch/push 成功但 ref 不变）

Windows 上 git 用 write+rename 更新 `packed-refs`，rename 会被静默拦截。表现：`git push` 报 `master -> master` 成功，但 `git status` 仍显示 `ahead 1`。

```bash
git ls-remote origin master                          # 查远程真实值
mkdir -p .git/refs/remotes/origin
git rev-parse HEAD > .git/refs/remotes/origin/master # 写 loose ref（优先级高于 packed）
git status -sb
```

### 3. 浅克隆（depth=1）导致 rebase 失败

`git rev-parse --is-shallow-repository` 为 true 时，先补全历史：

```bash
git fetch --unshallow origin
```

补完后务必再确认 ref 是否真的更新了（故障 2）。

### 4. `.obsidian/*.json` 的 CRLF 噪音

`git status` 显示 `M` 但 `git diff` 无实质内容时，是行尾符问题：

```bash
git config core.autocrlf input
git add --renormalize <file>
```

设置一次即可，之后不再产生噪音提交。

### 5. 提交身份缺失

`fatal: unable to auto-detect email address` → 新 clone 的仓库要显式配置：

```bash
git config user.name "<name>"
git config user.email "<email>"
```

## 收尾检查

```bash
git status -sb                     # 应与 origin/master 一致
git ls-remote origin master        # 远程真实值 == 本地 HEAD
```

# wiki-research-sync 参考模板与命令速查

仓库路径以 `REPO=C:\Users\l17405\github-repos\wiki-knowledge` 为例。

## 1. Synthesis 页 frontmatter 模板

```yaml
---
title: "主题名（YYYY-MM）"
type: synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2, 标签3]
---
```

## 2. 页面骨架

```markdown
# 主题名（YYYY-MM-DD）

> **一句话结论**：……（核心判断，内嵌关键 [[链接]]，引用库内框架时点名页面）

## 一、现状快照（数据表格）
| 维度 | 数据 | 位置/备注 |
|------|------|-----------|
| … | … | … |

## 二、机制/框架分析
（引用库内既有框架页并做增量更新，如"变量打分更新"）

## 三、历史复盘
（表格承载历史案例对比）

## N、情景推演 / 对持仓含义
（主观概率标注清楚，如 ~50%）

## See Also
- [[papers/2026-XX研报]] — 一句话说明关系
- [[synthesis/相关综合页]] — 一句话说明关系

## 数据来源（YYYY-MM-DD ~ YYYY-MM-DD）
- WebSearch/WebFetch：主题（来源，日期）
- 关键数据点：数据1、数据2、数据3……
```

追加章节变体：章节标题写成 `## 八、新章节标题（YYYY-MM-DD 追加）`，插在"数据来源"章节之前；数据来源章节内补一行 `- 追加数据：……`。

## 3. index.md 条目格式

综合页区（`## 综合页（synthesis/）`）条目：

```markdown
- [[synthesis/页面标题]] — 一句话说明，含核心结论要素（YYYY-MM-DD 新增）
```

补录旧页时日期标注写 `（YYYY-MM-DD 补录）`。

底部统计行（先用 `ls` 核对实际数量，历史统计可能滞后）：

```markdown
*统计：来源 182 篇 · 概念 18 个 · 实体 42 个 · 综合页 8 个*
```

## 4. log.md 条目格式

```markdown
## [YYYY-MM-DD] synthesis ×1 | 页面标题
- 新建综合页：synthesis/页面标题（核心结论一句话）
- 引用库内既有页面：×N 篇（点名）
- 双向链接已建：页面A、页面B 回链本页
- 更新 index（分类 + 统计 A→B）

## [YYYY-MM-DD] update | 页面标题·章节名
- 用户追问"……"，追加第 N 节：要点
- 数据来源补录；推送状态
```

注意：只追加到文件末尾，不改历史条目；一天内多次操作用独立条目区分。

## 5. 链接校验脚本

```bash
cd "<REPO>/wiki" && grep -o "\[\[[^]|]*\]\]" "<页面相对路径>.md" | sed 's/\[\[//;s/\]\]//' | sort -u | while read p; do
  case "$p" in
    papers/*|concepts/*|entities/*|synthesis/*) f="$p.md";;
    *) f=$(find . -name "$p.md" | head -1);;
  esac
  if [ -f "$f" ]; then echo "OK   $p"; else echo "MISS $p"; fi
done
```

有 `MISS` 时：修链接拼写，或确认是否漏建了页面。

## 6. Git 提交与推送命令

提交（add 具体文件并加引号，消息用 heredoc）：

```bash
cd "<REPO>" && git add "<文件1>" "<文件2>" ... && git commit -m "$(cat <<'EOF'
synthesis: 页面标题（YYYY-MM-DD）

- 要点一
- 要点二
- 要点三
EOF
)" && git push 2>&1 | tail -3
```

追加章节用 `synthesis更新: 标题——章节主题` 开头。

推送降级链（按序尝试，勿跳步；绝不 `--force`）：

```bash
# 1) 代理失败后，绕代理直连试一次
git -c http.proxy= -c https.proxy= push 2>&1 | tail -3

# 2) 仍失败：保留本地提交，记录 hash，告知用户启动 SoCloud 后补推
git log --oneline -1

# 3) （补推时）被拒 non-fast-forward：看分叉再合并
git fetch && git log --oneline HEAD..origin/master && git log --oneline origin/master..HEAD
git pull --no-rebase --no-edit 2>&1 | tail -5

# 4) 解决冲突后校验无残留标记，再提交推送
grep -rn "<<<<<<<\|>>>>>>>" wiki/index.md wiki/log.md; echo "---markers checked---"
git add wiki/index.md wiki/log.md && git commit --no-edit && git push 2>&1 | tail -3
```

## 7. 追加型冲突解决要领

- index.md 列表冲突：两边条目全保留，按日期先后排序（补录条目注明补录日期）。
- index.md 统计行冲突：采用远端最新统计基数，再叠加本次新增页面的计数；备注行（`>` 引用块）两边全留。
- log.md 冲突：两边条目全保留，按日期先后排序，同日条目按操作先后。
- 原则：**任何一侧的内容都不允许丢失**。

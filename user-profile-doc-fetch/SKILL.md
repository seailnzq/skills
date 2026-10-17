---
name: user-profile-doc-fetch
name_en: User Profile Doc Fetch
name_zh: 用户画像档案调取与时效体检
description: Locate and deliver the "cognition/profile of me" user-profile document (e.g. 认知体系与个人画像.md) by searching across historical session outputs folders and the wiki-life repo, pick the authoritative version by mtime, then audit its claims against the freshest MEMORY/USER/daily-note decisions and report stale items for the user to adjudicate. Use when the user asks to pull up "your cognition of me", "show me your profile of me", "how well do you understand me", or to update such profile documents with recent information.
description_en: Locate and deliver the "cognition/profile of me" user-profile document across historical session outputs and the wiki-life repo, pick the authoritative version by mtime, then audit its claims against the freshest MEMORY/USER decisions and report stale items.
description_zh: 调取"对我的认知/画像"类用户档案文档（如《认知体系与个人画像.md》）：跨历史会话 outputs 与 wiki-life 库定位权威版、按 mtime 选新版、复制交付，再逐项比对 MEMORY/USER/近几日日记的最新定调做时效体检，列出滞后条目请用户裁定是否回写。用于用户说"把对我的认知的文档调出来我看看""看看你对我的画像""根据这几天新增信息更新画像"等场景。
argument-hint: 直接说"把对我的认知的文档调出来我看看"，或指定画像文档名
argument-hint-en: Say "pull up the document about your cognition of me", or name the profile document
argument-hint-zh: 直接说"把对我的认知的文档调出来我看看"，或指定画像文档名
user-invocable: true
---

# 用户画像档案调取与时效体检

一句话定位：把"对我的认知/画像"类档案文档的**最新权威版**找出来交付，并当场体检其口径是否滞后于用户最新定调——体检报告往往比文档本身更有价值。

## 固定路径与前提

- 会话工作区根：`C:\Users\l17405\.qwenworkcn\workspace\`，每个历史会话有 `{chatId}/outputs/`
- 画像库（git）：`C:\Users\l17405\github-repos\wiki-life\wiki\`，含 `认知体系与个人画像.md`、`个人需求与性格剖析-2026.md`、`framework/认知提升计划-2026-2031.md` 等
- USER.md 中形如"详见 outputs/xxx.md"的相对路径**指向的是生成它时那个历史会话的 outputs 目录，不是当前会话**
- MEMORY.md 中已有纪律可交叉印证："改综合/画像页先取 github-repos 库内文件（outputs 同名件常是旧拷贝）"

## Step 1 定位文档（Glob 会漏，必须 find）

Glob 工具只搜默认工作目录，跨会话档案一律搜不到。直接用 Bash find 两个位置：

```bash
find /c/Users/l17405/.qwenworkcn/workspace -maxdepth 3 -iname "*认知*" 2>/dev/null
find /c/Users/l17405/github-repos/wiki-life -iname "*.md" -path "*认知*" 2>/dev/null
```

关键词按用户措辞替换（认知/画像/性格/剖析等），并顺带列出同目录伴页（个人需求与性格剖析、认知提升计划等），供 Step 5 提示用户一并调取。

## Step 2 多副本比对，选权威新版

同名文档往往有多份拷贝（历史会话旧版 + 库内持续修订版）。用 mtime 判定，不靠文件名猜：

```bash
ls -lt <各副本路径>
```

**优先级规则**：mtime 更新者胜；mtime 相近时 wiki-life 库内文件优先（库是权威源，outputs 同名件默认视为旧拷贝）。读其 frontmatter 的 `updated:` 字段二次确认版本。

## Step 3 交付

复制选定版到**当前会话** outputs，再用 present_files 交付：

```bash
mkdir -p "C:\Users\l17405\.qwenworkcn\workspace\<当前chatId>\outputs" && cp "<权威版路径>" "<当前会话outputs>/<文件名>.md"
```

## Step 4 时效体检（核心价值步骤）

拿着最新定调的现取来源，逐项比对文档口径与记忆层的最新定调。现取来源：

1. `mcp__qw-builtin__memory_get` 读近 3-7 天日记层（`memory/YYYY-MM-DD.md`）
2. 当前注入的 MEMORY.md / USER.md 全文

固定三个体检维度（维度是模板，**数值每次现取，禁止硬编码进技能**）：

| 维度 | 体检问题 | 典型滞后形态 |
|------|----------|--------------|
| 重大决策口径（如退休触发） | 文档写的触发条件 vs 用户最近改判后的定调 | 旧文档仍写"45岁退休、财务自洽为终局"，而新定调可能是"翻倍降为参考权重、50岁雇佣红线才是硬边界"（示例为 2026-09 时点） |
| 持仓结构与比例 | 文档中的标的/占比语气 vs 记忆层最近确认的持仓事实 | 文档仍是"观察名单"式分散列表，实际已高度集中于单一链条 |
| 随日递减的量化锚点 | 文档中的天数/倒计时是否为固定值 | "剩余约 9800 天"按日递减，引用时必须按当日重算且自带终点说明，禁止当固定常数抄 |

## Step 5 输出格式（固定五段）

1. **文档链接**：present_files 后给 file:// 链接，注明版本号与更新日期（如"9-06 版 v2"）
2. **结构速览**：一两段概括章节，不复述正文
3. **滞后条目清单**：每条三小段——文档原口径 / 最新定调（带日期）/ 建议改法
4. **伴页提示**：列出 Step 1 找到的配套页，问是否一并调出
5. **回写询问**：滞后条目是否由我改回库内权威版

## 回写分支（用户确认后执行）

改库内文件走版本管理流程：旧版备份到工作目录 → 编辑 `github-repos/wiki-life` 库内文件（git 仓库，免额外备份纪律）→ 更新 `wiki/index.md` 条目与 `wiki/log.md` 追加日志 → `git add` + commit → push。push 依赖 SoCloud 代理（127.0.0.1:7897），直连被 reset 且代理未开时如实在结尾告知"本地已 commit、push 挂起待代理开启后补推"，不要反复重试超过 2 次。

## 口径冲突处理纪律

文档内部或文档与记忆之间出现两套矛盾口径（如年龄两套反推口径、两个天数锚点）时：**不代为裁定、不替用户选一个写进去**。在文档就地打 `⚠️ 待修正（需本人裁定）` 标注，并列出连带影响，等用户一句话再统一改。

## Pitfalls

- 用 Glob 搜跨会话档案 → 必然搜不到，直接上 find
- 拿 outputs 里的同名件当最新 → 常是历史旧拷贝，必须 ls -lt 比对且库内优先
- 把 2026-09 时点的持仓、退休口径等具体数值当永久事实写死 → 这些本身就是体检对象，每次从记忆层现取
- 天数类锚点原样引用 → 随日递减，引用须按当日重算并自带终点
- 体检只挑文档的错却替用户改口径 → 只列差异给裁定，冲突处打待修正标注

## Verification

- present_files 成功返回且文件在**当前会话** outputs 下
- 交付的版本 mtime 不早于所有其它副本（ls -lt 留痕）
- 每条滞后条目都带"最新定调的来源日期"
- 若执行了回写：git log 有本轮 commit，push 结果（成功/挂起原因）已如实告知

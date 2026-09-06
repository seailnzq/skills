---
name: wiki-life-plan-authoring
name_en: Wiki-Life Long-Term Planning Doc
name_zh: 长期人生规划文档编撰与年审
description: Author or annually review a long-term (20+ year) directional life-plan grounded in the user's wiki-life Obsidian vault. Build a real-data profile from the library, confirm placement/horizon/bridging via AskUserQuestion, then produce a directional main doc (phases + triggers + failure list) plus an argumentation appendix; on each new fact judge what it overturns; cross-check every number with nominal-vs-real framing; verify objective facts with WebSearch; iterate in the workspace and never write to the vault before approval; finally ingest per WIKI-SCHEMA with bidirectional links, log, and git. Use when the user asks to draft/revise/audit a comprehensive or 20-year life plan, supplies new facts requiring re-evaluation, or asks to calibrate the plan each year / do a five-year review.
description_en: Author or annually review a 20+ year directional life-plan grounded in the wiki-life vault: build a profile, output a directional main doc plus argumentation appendix, iterate by judging what each new fact overturns, cross-check numbers, verify facts via WebSearch, then ingest after approval.
description_zh: 在用户的 Obsidian 库 wiki-life 上编撰或复核人生规划类长文档（长期/多年期方向性规划、养老退休测算、年度复核）。当用户要求制定/修订/审视人生规划、编撰多年期规划文档、提供新事实要求重估规划、要求批判性检查规划盲区，或要求把审定后的规划入库时使用。覆盖读库顺序、先问落点与跨度、方向层+论证层双文件结构、财务口径四查（名义/实际折现、结构通胀分化、方差三档、可逆窗口）、审视报告五分法（区分客观规律与价值判断）、审视式迭代、客观事实必须 WebSearch 核实、审定前不写库、WIKI-SCHEMA 入库与年度复核流程。
argument-hint: New plan or annual/five-year review? Point to the wiki-life vault (or let me auto-detect it).
argument-hint-en: New plan or annual/five-year review? Point to the wiki-life vault (or let me auto-detect it).
argument-hint-zh: 说明是新建长期规划，还是年度（默认 9 月）校准 / 五年复盘；给出 wiki-life 库路径，或让我自动探测。
user-invocable: true
version: 1.3.0
---

# wiki-life 人生规划类长文档编撰与复核

在用户的 `wiki-life` Obsidian 库（git 仓库）上编撰人生规划类长文档的稳定流程。核心原则：**规划建立在库内真实数据之上；草稿在 workspace 迭代，用户审定前绝不写库；每轮新事实先判断推翻了什么；数字必须换算并声明口径；客观事实必须核实来源。**

主文档只给**方向层**（往哪走、每阶段核心命题、触发器、红线），把测算/政策/专题论证拆到**附录（论证层）**，两文件互相引用。规划含健康、财务、家庭等私密事实，全程按保密约定处理。隐私数字**"只留线不留账"**：方向层只保留判据阈值与数字**带宽**（如"覆盖倍数≥X""缓冲金落在 A–B 区间"），把构成这些数字的账户、持仓、收支明细等"账"留在附录，且附录仅在私有库中呈现；正文不无谓扩散具体姓名/金额。

## 定位库（不要写死路径）

`wiki-life` 常位于 `~/.workbuddy/wiki-life`（Windows：`C:\Users\<user>\.workbuddy\wiki-life`；VM/容器可能不同）。先尝试该约定路径；若不存在或无访问权限，用 `mcp__workspace_request_directory` 请求用户选择该 vault 目录后再读。**同一用户往往还有一个 `wiki-knowledge`（对外研报库），二者互不混合——本技能只操作内在系统库 `wiki-life`。**

## 阶段 1：读库建立画像（固定顺序）

先 `memory_search` 查已有画像，但记忆不足时**以库内文件为准**。读全再动笔，按此顺序：

1. `wiki/overview.md` — 库全景（中心主题 + 五要素模型）
2. `wiki/认知体系与个人画像.md` — 画像底座（含十六字箴言等核心框架）
3. `wiki/framework/人生阶段与目标.md` + `framework/` 其余（第一性原理、思维工具、心性箴言、投资纪律、投资认知复盘）
4. `wiki/elements/` 七要素全部：心与认知、身与健康、关系、价值、时间、工作、投资
5. `wiki/execution/`：养老退休测算、医保退休规划、持仓假设清单、年度事项提醒等（真实数字与时间敏感事项）

读完，规划应能完全引用库内真实数据与**用户自己的概念框架**（用 `[[wiki链接]]` 指回库内页面），不引入库外假设。

## 阶段 2：动笔前用 AskUserQuestion 确认三件事

1. **落点**：直接按 WIKI-SCHEMA 入库 / 先出草稿审阅（推荐默认后者）/ 只要对话内容
2. **时间跨度**：给具体锚点选项（如"到 2053（约 69 岁，对齐用户自己的 9000 天锚点）"vs"严格 20 年"），锚点优先复用库内已有概念
3. **近期衔接**：是否包含与当前 1–3 年执行层的简短衔接段

三问齐了再动笔。

## 阶段 3：双文件产出（方向层 + 论证层）

骨架见 [template.md](template.md)。

- **主文档（方向层）**：`type: framework`。只回答三件事——多年往哪走、每阶段核心命题、哪些红线不能碰，不承载执行细节。必备构件：
  - **五要素速览表**（行=要素，列=阶段）
  - **触发器而非日历**：关键节点写成"若 X 则启动 Y"的条件触发，不写固定日程
  - **失败清单**（"XX 死法"条目）：主动列出不想发生的路径
  - **事实确认状态节**：集中列出尚未证实/待本人确认的事实（政策、价格、意愿、外部依赖），每条标注状态（已核实/待确认/已推翻）与来源时点；**每轮迭代都要回来更新此节**，清空即代表该版可进入审定
  - **§编号**：正文用 §一/§8.4 式编号，便于跨文档互相引用与审阅定位
  - 近期衔接表：主线下挂到 `[[execution/...]]` 页面
- **附录（论证层）**：`type: synthesis`。承载测算过程、政策条款、专题分析（通胀、保险精析、尾部风险等）。方向层只写结论，判断依据与反面证据放附录；**结论被推翻时先改附录再改主文档**。

两文件 frontmatter 均含：
```yaml
status: 草稿 v0.N 待审（未入库）
created / updated: YYYY-MM-DD
source: 基于 wiki-life 全库综合整理 + YYYY-MM-DD 第 N 轮审视修订（列出各版本变更要点）；由 LLM 起草，待本人审定
```
命名建议：`<跨度>人生规划-<起年>-<止年>-草稿.md` 与 `规划附录-<主题>.md`。用 `qwenwork_file_present_files` 呈现两个文件，回复中逐条对应"用户批示 → 落点章节"。

## 财务口径四项必查（起草与每轮迭代都要过一遍）

1. **名义 vs 实际折现**：任何跨期对比（如 2047 年名义养老金 vs 按 2026 年物价的生活预算）必须折现到同一口径再算缺口。发现错配要明确说"这是口径错配"并给出修正值——这类错误普遍偏乐观，是历史上实际踩过的坑（"A 缺口 1240"实为约 2860）。
2. **结构通胀分化**：综合 CPI 锚之外，医疗照护（长期 5–8%）、人工服务（4–6%）、工业品（0–1%）等分项单列各自假设，不用单一通胀率扫平；分项假设标注时点与依据（WebSearch）。
3. **方差按低/中/高三档**：教育、父母照护这类高方差项不写单点值——按三档给区间并注明触发条件（如"40W 是公办下限口径，不是期望值；民办/国际/留学量级差 10–50 倍"）；只有低方差项才允许单点值。
4. **可逆/不可逆窗口**：给每个动作标注窗口属性。商业保险可保期（如 45 岁前）、政策试点资格等属"过窗永久关闭"，必须给 deadline 并进近期衔接表；可逆/可推迟动作标注相应低优先级。

## 阶段 4：审视式迭代（每轮收到新事实时）

1. **先判定冲击面**：新事实是否推翻既有结论？回复里明确说"这条推翻了我上一版的 X"，并给出改写后的更精确结论。推翻一处，顺着 grep 找联动处（表格、速览、失败清单、附录通常各有一份同源表述）。
2. **数字口径校验**：所有金额/比率换算后讲清口径——尤其**名义 vs 实际（通胀调整后）**；历史遗留数字（如早年"拍"的基准）要重述其名义/实际属性并给出与新区间的关系；覆盖倍数等判据写明分母取值。
3. **客观事实必须核实**：通胀数据、保险条款与费率、长护险/医保政策、地方性政策（如加装电梯补贴与表决门槛）、产品价格——一律 WebSearch（必要时 WebFetch 一手来源）后再写入，标注时点。不得凭记忆写条款数字。
4. **版本升级**：每轮修订升 v0.N，同步更新 frontmatter source 串与各节标题中的版本标记（见 Pitfalls）。
5. 用户自述与库内框架冲突时，以用户当下自述为准，但要指出与其自己框架（如"事上练"）的呼应或矛盾。

## 审视报告五分法（用户要求"再审视/找盲区/批判性检查"时）

审视时强制区分两类内容，**只改客观规律可校验的部分；价值判断明确声明不动**（四阶段划分、五要素结构、终局定义、集中押注、家人相处原则等属用户价值领域，只评估其自洽性，不替用户做判断）。报告按五类组织，逐条给"结论 + 依据 + 建议动作"：

1. **客观硬伤**：方法论错误——口径错配、经典风险缺席（如规划了长寿风险却缺失能照护风险）、硬时间窗口未标注；
2. **方差低估**：被写成单点值的高方差变量（教育、父母照护、伴侣保障等外部依赖）；
3. **结构性盲区**：规划视角的结构性缺席——如单人视角掩盖双人决策（退休是夫妻共同决策）、他人意愿不在自己单方规划内；
4. **框架可商榷点**：触发器设计（财务/健康变量之外缺"意愿类"触发器）、缺中间解（全有全无之间）、年龄触发不如客观检验触发——给替代方案但不强推；
5. **内容性缺席**：完全没覆盖的维度（居住安排、知识库系统 27 年可维护性等）。

审视结论经用户认可后合入草稿，走阶段 4 迭代。

## 阶段 5：入库（仅在用户明确审定后）

未审定前所有迭代只发生在 workspace `outputs/`，**绝不写库**。用户确认后，按 [reference.md](reference.md) 的 WIKI-SCHEMA 细则执行：

1. 主文档 → `wiki/framework/`，附录 → `wiki/synthesis/`（库无 synthesis 层则并入 framework 或就近放置并说明），文件名去"草稿"字样
2. 按 WIKI-SCHEMA 补 frontmatter（status 改为"已入库"，私密页加 `tags: [私密]`），正文补 `[[双链]]`，确保被 index 或 overview 可达
3. 更新 `wiki/index.md`，在 `wiki/log.md` **追加**一条（日期 + 变更摘要）
4. `git add <具体文件> && git commit`（该库为 git 仓库，无需另备份）；仅当远程为**私有仓库**时才 push

## 阶段 6：年度校准与五年复盘（复用流程）

规划自带"年度校准"节（默认每年 9 月、规划日跑一次）与五年复盘锚点（如 2029/2035/2041/2046）。校准走简化回路：读该节触发器 → 只收增量事实 → 按阶段 4 迭代 → 涉及政策/价格类条目重新 WebSearch 核时效 → 输出增量修订（改对应 §，不重写全文）→ 审后入库。每年规划日自评项（如"今年哪件事磨了我"）先问再改。五年复盘以阶段为单位回看"假设 vs 现实"，把结论回灌 `framework/人生阶段与目标` 与主文档，产出仍是同一份主文档的新版本 + 附录，不另起体系。

## Pitfalls（实踩过的坑）

- **Edit/Write 前必须在同一轮会话完整 Read 目标文件**；上下文压缩或换轮后 read 状态会失效，报 "File has not been read yet" 时先完整 Read 再编辑。
- **old_string 不匹配是常态**：多轮编辑后凭记忆写 old_string 极易失败。先 `Grep -n` 定位、按实际文件文本复制再替换；失败一次就 grep 核对，不要盲改。
- **成段替换后检查重复与残留**：插入新版段落后，旧版同主题条目（bullet、表格行、附录序号）会残留成重复；每轮结束用 Grep 搜关键词确认无重复序号/重复行。
- **版本标记三处联动**：升版时 frontmatter status、主文档各节标题 "(v0.N ...)"、附录对应节三处都要同步，否则出现 §十 标题 v0.3、正文 v0.4 的错位。
- **数字联动清单**：缓冲金、带宽、覆盖倍数分母这类数字通常出现在主文档 ≥4 处（阶段条目、§表格、结论、衔接表）+ 附录 ≥2 处；改一处先 Grep 该数字找齐全部出现点。
- 不要把 WebSearch 结果写成无来源的确断；条款类写"截至 YYYY-MM 公开资料"。
- **用户重复发同一消息多为 UI 重发**：接着当前任务继续做，不要当新指令重开流程或重复执行一遍。

## Verification（每轮交付前自检）

1. 版本号：frontmatter、节标题、附录三处一致
2. 数字：本轮改动的每个数字，Grep 旧值确认无残留；名义/实际口径已声明
3. 结构：五要素速览、失败清单、触发器节仍在且与新结论一致
4. 无重复段落/重复序号
5. 未审定的草稿没有写入 wiki-life 库；outputs/ 内两文件已 present
6. 本轮涉及的客观事实均有 WebSearch/WebFetch 来源与时点标注

## 参考文件

- [reference.md](reference.md)：wiki-life 库结构、跨平台定位 vault、WIKI-SCHEMA 入库细则（双链、frontmatter 私密标记、index/log、git/私有库）。
- [template.md](template.md)：方向层主文档 + 论证层附录的骨架模板。

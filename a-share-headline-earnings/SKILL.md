---
name: a-share-headline-earnings
title: A股头部企业财报跟踪与行业全景分析
description: 跟踪 A 股各行业头部企业（98家清单）的定期报告（半年报/年报），批量下载 PDF、解析财务数据、生成 wiki 简要页、深度分析每行业头部企业，并生成行业景气矩阵与产业预测全景报告。适用于半年报/年报披露季的分批次跟踪（下载→分析→全景预测）。
agent_created: true
tags: [财报, A股, 行业分析, 全景预测, 巨潮, 知识库]
---

# A股头部企业财报跟踪与行业全景分析

## 适用场景
- 半年报/年报披露季，跟踪 98 家 A 股各行业头部企业（18 个行业）
- 分批下载 PDF → 解析财务数据 → 生成 wiki 页 → 每行业深度分析一家头部
- 披露截止后生成「半年报全景分析与产业预测」（景气矩阵 + AI 产业链传导 + 产业预测）
- 已落地为 8/25 + 8/31 两个定时自动化任务

## 数据文件（工作区根目录）
| 文件 | 内容 |
|---|---|
| `all_a_head_manifest.json` | 98 家头部公司清单（code/name/industry/board/orgId） |
| `all_a_head_links.json` | 下载结果（status: full/no_ann/exists） |
| `all_a_head_data.json` | 解析后财务数据（table: 营收/净利/扣非/现金流/ROE） |
| `all_a_head_focus.json` | 每行业重点分析标的（营收最高者） |
| `A股行业头部企业梳理_2026H1.md` | 行业头部梳理基准报告（98家/18行业） |

## 管线脚本
1. **`all_a_head_fetch.py`** — 下载半年报 PDF（增量）
   - 输入：`all_a_head_manifest.json`；输出 PDF → `~/.workbuddy/wiki-knowledge/raw/2026/半年报/全A头部/{code}-{name}/`
   - 支持沪深京三地：board → column/plate（sh→sse/sh，sz→szse/sz）
   - 运行：`cd C:/Users/sealin/WorkBuddy/Claw && python all_a_head_fetch.py`
2. **`all_a_head_process.py`** — 解析 + 生成 wiki 页 + 输出聚焦清单
   - 运行：`python all_a_head_process.py`
   - 输出：`all_a_head_data.json`、wiki 页 `wiki/papers/2026-H1A-{code}-{name}-半年报.md`、`all_a_head_focus.json`

## 巨潮接口（复用 cninfo-financial-reports）
1. orgId：`POST cninfo.com.cn/new/information/topSearch/query`，body `keyWord={代码}&maxNum=10`，匹配 `category=='A股'`
2. 公告：`POST cninfo.com.cn/new/hisAnnouncement/query`，body 含 `column/plate/stock={code},{orgId}/seDate=2026-07-01~2026-08-31`
3. 下载：`http://static.cninfo.com.cn{adjunctUrl}`，带 UA + `Referer: http://www.cninfo.com.cn/`，校验 `%PDF` 头且 >5KB

## 解析关键点（重要坑，已踩过）
1. **字段名带单位后缀**：沪深主板/深市摘要字段名为 `营业收入（元）`/`营业收入（千元）`，正则需同时匹配裸名和带后缀形式
2. **单位换算**：文本里 `单位：千元`/`（千元）`/`（百万元）`/`（万元）` 各异，用 `detect_unit()` 取**最早出现**的单位声明换算成元（坑：茅台正文后部"销售情况"表格有"单位：万元"会干扰，必须取最早）
3. **字段+单位跨行**：宁德时代"归属于上市公司股东的净利润"+"（千元）"拆两行，`find_field_row` 必须**优先 3 行拼接**匹配（k 从 2 往下）
4. **排除干扰标题**：下载时过滤 `英文版/更正/修订/废止`；解析时跳过目录页（点线+页码）
5. **保险/银行报表特殊**：平安用"（货币单位：人民币百万元）"，归母净利字段名可能是"归属于母公司股东的净利润"，解析不到时降级处理

## 知识库入库（llm-wiki 规范）
- PDF → `raw/2026/半年报/全A头部/{code}-{name}/`（.gitignore 排除）
- 每公司一页：`wiki/papers/2026-H1A-{code}-{name}-半年报.md`
  - frontmatter：title/industry/code/date/tags
  - 数据表 + 「关键信号」区块（LLM 精读全文后回填：营收利润趋势/竞争力行业地位/行业景气/风险展望）
- 综合报告：`A股头部半年报行业简析_{MMDD}.md`（批次数）+ `A股头部半年报全景分析与产业预测_{MMDD}.md`（最终）

## 分析框架（对齐 sealin 投资思路）
每行业头部企业深度分析必须落到：
- **高成长叙事五条件**（高成长/高毛利/可复制/可持续/龙头集中）
- **半导体周期 / 端侧算力 / 反内卷 / K型通胀**
- 明确营收利润同比、核心驱动、行业地位、与 AI 技术革命的关系
- 全景报告含：分行业景气矩阵 / AI 产业链传导（算力芯片→光模块→服务器→应用→端侧）/ 下半年及明年预测 / 可跟踪验证指标 / 风险清单

## 定时任务参考
```json
// 8/25 批次（下载+行业分析）
{"name":"A股头部半年报下载与行业分析（8/25）","scheduleType":"once","scheduledAt":"2026-08-25T20:30:00"}
// 8/31 批次（补全+全景预测）
{"name":"A股头部半年报全景分析（8/31）","scheduleType":"once","scheduledAt":"2026-08-31T20:30:00"}
```
注意：automation 的 cwds 会被指向独立目录，prompt 里必须显式 `cd C:/Users/sealin/WorkBuddy/Claw`。

## 注意事项
- 限频：orgId 查询间隔 0.15s、公告查询 0.1s；限频时报错等 30s 重试
- 披露季节奏：8/15 前仅少数公司披露，8/25 处理先行者，8/31 披露截止日补全
- 重新生成 wiki 页前先删旧页（脚本跳过已存在页面）
- 数据以 PDF 原文为准，westock（腾讯自选股 MCP）可做二次校验（营收/净利/市值）

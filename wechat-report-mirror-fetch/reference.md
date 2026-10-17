# 微信研报镜像采集 — 固定坑位与模板

## 收藏目录判定

- 目录：`WPSDrive/276687336/WPS云盘/应用/金山收藏助手/`（若用户 WPS 账号不同需调整中间数字段）。
- 命令：`ls -lt` 取当天时间戳条目；文件名通常含文章标题片段，可直接用于 Reportify 匹配。
- `.otl.wpsonline` 后缀：金山云指针文件，仅含元数据，不包含正文。联网内容一律走 Reportify。

## Reportify 固定地址

- 郭磊宏观茶座频道页：`https://reportify.cn/channels/S10740353838202886/documents`
- 文章详情页：`https://reportify.cn/social-media/<文章ID>`（如 846695993029463）
- 频道页按时间倒序列出文章标题与日期，用于当日匹配；详情页内"查看原文链接"给出 mp.weixin.qq.com 直链。
- 局限：只有要点式摘要，缺环比拆分、量价拆分、汇率分析、逐月展望等散文段落；原文链接常被抹去参数。

## 微信直链降级策略

1. 直抓 `mp.weixin.qq.com/s/...` → 大概率返回验证页/风控页。
2. 改抓同域名下 `js_content` 容器内链或缓存页，提取正文文本。
3. 仍失败 → Reportify 摘要兜底 + 镜像补全文；长图类正文标注"正文未获取"。

## 镜像站点检索模板

按标题关键词分组，以下模板中 `<kw>` 为提取的关键词，`<title>` 为标题核心短语：

| 站点 | 检索入口 |
|------|----------|
| 新浪财经 | `https://search.sina.com.cn/?q=<kw>&c=news&sort=time`；研报栏目 `sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/<id>/index.phtml` |
| 新浪研报登记页 | `https://stock.finance.sina.com.cn/stock/go.php/vReport_Show/kind/lastest/rptid/<id>/index.phtml`（取标题/作者/日期/摘要，稳定） |
| 老虎社区 laohu8 | `https://www.laohu8.com/news/<id>`（研报镜像全文，本会话实测可直取正文） |
| 东方财富 | 文章 `https://finance.eastmoney.com/a/<date><id>.html`；股吧 `https://guba.eastmoney.com/news,...html`；财富号 `https://caifuhao.eastmoney.com/news/<id>` |
| 同花顺财经 | `http://news.10jqka.com.cn/<date>/c<id>.shtml`（市场定价/期货口径常用） |
| 网易财经 | `https://www.163.com/search?keyword=<kw>` |
| 搜狐 | `https://search.sohu.com/?keyword=<kw>` |
| 慧博投研 | `https://www.hibor.com.cn/` 站内检索 `<kw>`（wap 详情页易 `fetch failed`，不稳） |
| 华尔街见闻 | `https://wallstreetcn.com/search?q=<kw>` |

**稳定性分层（超时即换源、不重试同源）**：
- 优先稳源：`laohu8.com`、`finance/guba/caifuhao.eastmoney`、`news.10jqka.com.cn`(同花顺)、新浪研报登记页 `stock.finance.sina.com.cn`。
- 超时/失败高发，命中即弃、只作次选补漏：`news.qq.com`、`guancha.cn`(观察者网)、`www.163.com`、`wap.hibor.org`、部分英文站(nextfin/morningstar)。`WebFetch timed out after 120000ms` / `fetch failed` 与风控同级处理。

## 子代理并行分组建议

- 每篇文章提取 2-4 个关键词（主题词 + 数据词，如"出口" + "8月"）。
- 每组一个子代理，任务书内写明：目标文章标题、关键词、可尝试的镜像站点清单、"取到全文段落原文返回，取不到明确说明"。
- 子代理返回后与 Reportify 摘要交叉核对，缺失段落（环比、量价、汇率、逐月展望）确认补齐情况。

## 输出五要素固定格式

```
## <标题>（<公众号名> <发布日期>）
> 前作/关联：<如适用>

### 核心论点
- ...

### 带日期数字的论据
- <统计期> <指标> = <数值>（来源：<URL>）

### 资产定价含义
- ...

### 来源URL
- 原文：<mp.weixin.qq.com 链接或"被风控未取到">
- Reportify：<reportify.cn/social-media/<id>>
- 镜像：<逐条列出>

### 未核实项
- <取不到/推断的内容>（或"无"）
```

## 市场定价类口径提取模板（step 6 可选扩展）

用于宏观事件/市场定价类追问，采集对象是卖方**会后点评**（非会前预判）。每条数字必须带三要素：口径、时点、来源。

```
### 会后市场定价（<机构/作者> <点评发布日期>，口径时点：<盘中快照/收盘 + 具体时区时刻>）
- <时点> 10月加息概率 = <X%>（FedWatch/期货隐含，来源：<URL>）
- <时点> 12月加息概率 = <Y%>（来源：<URL>）
- 至2026年底累计隐含加息 = <Z>bp（**口径：相对当前区间的累计隐含幅度**，非利率水平；换算成利率区间须标[推算]）
- 至2027 <时点>累计隐含 = <bp>，较会前 <±bp>
- 收益率读数：2Y=<..>% / 10Y=<..>% / 30Y=<..>%（注明盘中 vs 收盘）
- 三方对照：期货定价 vs 点阵图中值 vs 机构中位数（谁更鹰一档）
```

口径与坑位：
- "累计隐含加息幅度(bp)" 与 "利率区间/水平(%)" 是两回事，混用会得出错误终端利率；换算项一律标[推算]。
- 盘中快照与收盘读数常有 1‑6bp 差异，属时点差异不是数据冲突，别误记为未核实。
- 会前点评（"预计/或将"）不得当作会后市场定价引用；单一来源读数（某商品价格、某政策细节）入未核实项。
- 完整的"决议事实→会后定价→四方对照→充分/超额/不足判定"核查流水线属专用技能 `fed-rate-pricing-check`，本模板只负责把采集到的数字按口径整理清楚。

## 采集结果回写衔接（step 7）

- 用户目的为"分析学习入库"时，把本流水线输出直接喂 `wiki-research-sync`：建 paper/concept/synthesis 页、双向链接、更新 index/log、链接校验、commit+push，不重复提炼。
- 市场定价类结论优先回写库内"月度利率与通胀跟踪"类锚点页（FOMC 检验块），并顺手清零因口径/时点混淆而挂起的[待核实]。

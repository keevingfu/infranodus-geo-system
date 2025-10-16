# INITIAL: InfraNodus + Neo4j GEO Knowledge Graph System

## FEATURE

构建一个完整的"InfraNodus + Neo4j"知识图谱驱动的GEO（Generative Engine Optimization）系统，用于SweetNight内容生产和知识管理。

### 核心目标

将"内容堆栈"升级为"问题—知识—内容—引用 飞轮"：
- **InfraNodus**：发现话题结构洞、共现网络、关键词社群
- **Neo4j**：存储可查询的知识图谱、支持版本化和可追溯引用
- **自动化**：通过n8n编排数据采集、分析、内容生成、发布全流程

### 1. 数据采集与分析层

**输入源**：
- Reddit (r/Mattress, r/sleep)
- Amazon Reviews (SweetNight + 竞品)
- YouTube 评论和字幕
- Quora 问答

**处理流程**：
```
原始数据 → Firecrawl抓取 → 文本清洗 → InfraNodus分析 → Neo4j存储
```

**InfraNodus输出**：
- 关键词共现网络（Co-occurrence Graph）
- 话题社群模块（Topic Clusters）
- 结构洞识别（Content Gaps）
- 桥接关键词（Bridging Keywords）
- 叙事骨架（Narrative Structures）

### 2. 知识图谱层（Neo4j Schema）

#### 核心节点类型

```cypher
// 关键词与共现
(:Keyword {name, betweenness, degree, community})
(:TopicCluster {name, modularity, size})

// 人群-场景-痛点
(:Persona {name, description, priority})
(:Scenario {name, description, frequency})
(:PainPoint {name, description, severity, evidence_count})
(:Feature {name, description, category})
(:Product {name, brand, price_range, rating})

// 内容与提示
(:Prompt {text, type, priority, gap_score})
(:Brief {title, outline, target_persona, target_scenario})
(:Gap {topic_a, topic_b, opportunity_score, discovered_at})

// 证据与声明
(:Claim {text, confidence, verification_status})
(:Evidence {source, url, date, quote, credibility_score})

// 内容资产
(:Asset {type, channel, url, published_at, citation_ready_score})
```

#### 核心关系类型

```cypher
// 共现与聚类
(:Keyword)-[:CO_OCCURS_WITH {weight}]->(:Keyword)
(:Keyword)-[:BELONGS_TO]->(:TopicCluster)
(:TopicCluster)-[:BRIDGES]->(:TopicCluster)

// 人群与场景
(:Persona)-[:OCCURS_IN]->(:Scenario)
(:Scenario)-[:SUFFERS]->(:PainPoint)
(:PainPoint)-[:RELIEVED_BY]->(:Feature)
(:Feature)-[:IMPLEMENTED_IN]->(:Product)

// 内容生产
(:Prompt)-[:ADDRESSES]->(:PainPoint)
(:Prompt)-[:TARGETS]->(:Persona)
(:Gap)-[:SUGGESTS]->(:Prompt)
(:Brief)-[:COVERS]->(:TopicCluster)
(:Brief)-[:GENERATED_FROM]->(:Prompt)

// 证据链
(:Claim)-[:ABOUT]->(:Feature | :Product | :PainPoint)
(:Claim)-[:SUPPORTED_BY]->(:Evidence)
(:Asset)-[:DERIVES_FROM]->(:Brief | :Prompt | :Claim)
(:Asset)-[:MENTIONS]->(:Product | :Feature | :PainPoint)
```

### 3. 十大赋能功能

#### 3.1 Prompt宇宙构建
- 从VOC生成Prompt模板
- 映射Prompt到PainPoint
- 优先级排序

#### 3.2 结构洞选题
- 识别话题空白（Gap）
- 评估机会值（opportunity_score）
- 生成选题建议

#### 3.3 人群-场景-痛点三维细分
- Persona × Scenario × PainPoint矩阵
- 内容覆盖度分析
- FAQ自动排序

#### 3.4 证据驱动的可引用知识
- Claim + Evidence链接
- 来源追溯
- 可信度评分

#### 3.5 内容简报生成
- Narrative结构提取
- 多渠道脚本模板
- 锚文本规划

#### 3.6 跨渠道话语一致
- 术语标准化
- 同义词管理
- Framing一致性

#### 3.7 竞争差异分析
- 竞品话题对比
- 差异化机会
- 对比内容脚本

#### 3.8 引用就绪度评分
- Citation-Ready Score算法
- 覆盖度 × 证据强度 × 问题映射
- 发布前质量门控

#### 3.9 话题权重与演进
- 时间序列分析
- 热度迁移追踪
- 下周优先列表

#### 3.10 Graph-RAG问答
- 结构化查询
- 可追溯答案
- 官网/客服/ChatGPT插件

### 4. 自动化流水线（n8n编排）

#### Pipeline 1: 采集流水线（Acquire）
```
Firecrawl抓取 → 文本清洗 → InfraNodus API → Neo4j写入
频率: 每天
输出: 共现网络、关键词、社群、结构洞
```

#### Pipeline 2: 洞察流水线（Insight）
```
定时Cypher查询 → 结构洞分析 → 优先级排序 → Feishu推送
频率: 每周一
输出: Top 10空白选题 + Brief模板
```

#### Pipeline 3: 内容流水线（Generate & Publish）
```
读取Brief/Prompt → Claude生成内容 → 质量评分 → 发布（X/Reddit/Medium）
触发: 手动/定时
输出: 多渠道内容 + Citation追踪
```

#### Pipeline 4: 追踪流水线（Track）
```
Google Search Console → 关键词排名 → Citation监控 → Neo4j更新
频率: 每天
输出: (:Metric)节点更新
```

#### Pipeline 5: 闭环流水线（Optimize）
```
低分内容识别 → 缺陷分析 → 增强建议 → 行动清单
频率: 每周
输出: 优化任务列表
```

### 5. KPI看板指标

| 指标类别 | 具体指标 | 目标值 |
|---------|---------|--------|
| **结构洞转化** | Gap → Brief → Asset → Citation | 30% |
| **引用就绪度** | Citation-Ready Score | >80 |
| **问题覆盖度** | 高频Prompt覆盖率 | >70% |
| **证据密度** | 平均Evidence数/Asset | >5 |
| **术语一致性** | 同义词归一后分歧率 | <10% |
| **人群命中率** | Persona×Scenario点击转化 | >15% |

## EXAMPLES

### Example 1: InfraNodus API集成

参考：
- InfraNodus REST API文档：http://localhost:3000/api
- 现有InfraNodus实例：`/Users/cavin/infranodus-web`
- Neo4j Python Driver示例：`neo4j-driver` package

### Example 2: Neo4j知识图谱查询

参考现有Neo4j数据：
- 当前数据库：64 nodes, 231 relationships
- 现有标签：Brand, Product, Feature, Problem, Scenario, UserGroup, Context, Statement, Concept

### Example 3: n8n工作流

参考已配置的MCP服务器：
- n8n MCP: `/Users/cavin/.mcp.json`
- 可用工具：create_workflow, list_workflows, run_webhook

## DOCUMENTATION

### InfraNodus API文档
- **API端点**: http://localhost:3000/api
- **认证**: Session-based (需要登录demo_user)
- **关键接口**:
  - `/api/graph` - 获取共现图
  - `/api/concepts` - 获取关键词列表
  - `/api/statements` - 获取语句列表
  - `/api/gaps` - 获取结构洞

### Neo4j连接信息
- **URI**: `neo4j://localhost:7688`
- **用户**: `neo4j`
- **密码**: `claude_neo4j_2025`
- **数据库**: `neo4j`
- **Browser**: http://localhost:7475

### Neo4j Python Driver
- **包**: `neo4j-driver` (v5.x)
- **文档**: https://neo4j.com/docs/python-manual/current/

### n8n自动化
- **MCP配置**: `/Users/cavin/.mcp.json`
- **服务**: n8n via MCP
- **文档**: n8n.io/workflows

### Firecrawl抓取
- **Self-hosted**: http://localhost:3002
- **API Key**: `fs-test`
- **MCP集成**: `mcp__firecrawl__*` tools

## OTHER CONSIDERATIONS

### 技术栈
- **InfraNodus**: Node.js app at localhost:3000
- **Neo4j 5**: Docker container `neo4j-claude-mcp`
- **Python**: For data processing and Neo4j integration
- **n8n**: Via MCP for workflow automation
- **Firecrawl**: For web scraping (self-hosted)

### 数据隐私与安全
- 所有VOC数据脱敏处理
- 用户评论匿名化
- API密钥存储在`~/.mcp.env`
- 图谱数据定期备份

### 性能优化
- Neo4j索引优化（Keyword.name, Claim.text）
- InfraNodus批量处理（避免频繁API调用）
- n8n工作流错误重试机制
- 增量更新（避免全量重建）

### 可扩展性
- 支持多品牌扩展（不限于SweetNight）
- 多语言支持（EN/CN/ES/DE）
- 自定义节点类型（可扩展schema）
- 插件化架构（独立模块）

### 已知限制
- InfraNodus API可能需要会话管理（Cookie）
- Neo4j社区版限制（单实例）
- n8n MCP集成为beta功能
- Firecrawl速率限制（需控制频率）

## SUCCESS CRITERIA

1. ✅ Neo4j图谱schema创建完成（10+节点类型，20+关系类型）
2. ✅ InfraNodus集成脚本可工作（共现网络导入Neo4j）
3. ✅ 至少3个核心Cypher查询模板可用（结构洞/优先级/评分）
4. ✅ 1条n8n采集流水线运行成功（Firecrawl → InfraNodus → Neo4j）
5. ✅ Graph-RAG问答原型可演示（输入问题 → Neo4j查询 → 结构化答案）
6. ✅ Citation-Ready Score算法实现并测试
7. ✅ KPI看板可视化（至少3个关键指标）
8. ✅ 系统文档完整（README + API文档 + 使用指南）

## IMPLEMENTATION PLAN

### Phase 1: 基础设施（第1-3天）

**目标**: 建立最小可行系统

- [ ] 创建Neo4j图谱schema（Cypher脚本）
- [ ] 实现InfraNodus API客户端（Python）
- [ ] 导入测试数据（SweetNight 3个核心品类）
- [ ] 验证数据流：原始文本 → InfraNodus → Neo4j

**交付物**:
- `neo4j-schema.cypher` - 图谱初始化脚本
- `infranodus_client.py` - API客户端库
- `import_pipeline.py` - 数据导入脚本
- 测试数据集（冷感/混合/记忆棉语料各100条）

### Phase 2: 核心查询与算法（第4-7天）

**目标**: 实现10大赋能功能中的前5个

- [ ] 结构洞识别查询（Cypher）
- [ ] Prompt生成与优先级算法
- [ ] Persona-Scenario-PainPoint映射
- [ ] Claim-Evidence关联与验证
- [ ] Citation-Ready Score算法

**交付物**:
- `cypher_queries.py` - 核心查询库
- `scoring_engine.py` - 评分算法
- `gap_analyzer.py` - 结构洞分析
- 单元测试覆盖率 >80%

### Phase 3: 自动化流水线（第8-14天）

**目标**: n8n编排3条关键流水线

- [ ] 采集流水线（acquire）
- [ ] 洞察流水线（insight）
- [ ] 内容流水线（generate）

**交付物**:
- n8n workflow JSON（3个workflow）
- 流水线监控脚本
- Feishu通知模板
- 周报自动生成

### Phase 4: RAG与看板（额外1周）

**目标**: Graph-RAG问答 + KPI可视化

- [ ] Graph-RAG查询引擎
- [ ] 答案生成与引用追溯
- [ ] KPI看板（Grafana/自定义）
- [ ] 系统部署与文档

**交付物**:
- `graph_rag.py` - RAG查询引擎
- `dashboard.py` - 看板数据API
- 完整文档（README + 使用指南）
- 部署脚本（Docker Compose）

## RISKS & MITIGATION

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|------|------|---------|
| InfraNodus API不稳定 | 高 | 中 | 实现重试机制 + 缓存 |
| Neo4j性能瓶颈 | 中 | 低 | 索引优化 + 分批写入 |
| n8n MCP集成限制 | 中 | 中 | 备用方案：直接HTTP调用 |
| 数据质量问题 | 高 | 高 | 多层清洗 + 人工审核 |
| 时间预算超支 | 中 | 中 | MVP优先 + 敏捷迭代 |

## NOTES

- 使用Context Engineering方法论（INITIAL → PRP → 实施）
- 所有代码使用英文命名，注释使用中文
- 遵循已有项目的代码规范（scripts/common.sh模式）
- 优先使用现有工具（MCP服务器）而非重复造轮子
- 每个阶段结束进行验证和演示

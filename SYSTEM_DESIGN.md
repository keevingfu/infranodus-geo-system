# GEO系统完整应用设计方案

**文档版本**: 1.0
**创建时间**: 2025-10-16
**系统名称**: Generative Engine Optimization (GEO) Knowledge Graph Platform

---

## 📋 目录

1. [系统概述](#系统概述)
2. [系统架构](#系统架构)
3. [核心功能模块](#核心功能模块)
4. [技术栈](#技术栈)
5. [数据流设计](#数据流设计)
6. [API接口设计](#api接口设计)
7. [前端界面设计](#前端界面设计)
8. [自动化工作流](#自动化工作流)
9. [部署方案](#部署方案)
10. [安全与权限](#安全与权限)
11. [监控与运维](#监控与运维)
12. [扩展性设计](#扩展性设计)

---

## 系统概述

### 🎯 系统目标

构建一个智能化的内容优化和生成平台，通过知识图谱技术和AI能力，帮助企业：

1. **自动发现内容机会** - 通过结构洞分析识别市场空白
2. **生成优质内容** - 基于证据和数据生成高质量内容
3. **优化搜索排名** - 针对生成式搜索引擎（ChatGPT、Perplexity等）优化内容
4. **追踪内容表现** - 监控内容效果和系统健康

### 🔑 核心价值

- **数据驱动**: 基于真实用户数据和竞品分析
- **AI增强**: 利用Graph-RAG和LLM生成内容
- **自动化**: 从数据采集到内容发布全流程自动化
- **可追溯**: 所有内容都有证据链和引用来源

### 👥 目标用户

- **内容营销团队** - SEO/GEO专家
- **产品经理** - 需要市场洞察
- **数据分析师** - 需要可视化分析工具
- **企业决策者** - 需要战略性内容规划

---

## 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户界面层 (Frontend)                     │
├─────────────────────────────────────────────────────────────┤
│  Web Dashboard  │  Mobile App  │  Chrome Extension  │  API  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    应用服务层 (Backend API)                    │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Gateway  │  GraphQL API  │  WebSocket Server       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     核心业务层 (Services)                      │
├─────────────────────┬───────────────┬───────────────────────┤
│  Data Acquisition   │  Analysis     │  Content Generation   │
│  - Web Scraping     │  - Structure  │  - Prompt Engine      │
│  - API Integration  │    Holes      │  - Brief Generator    │
│  - File Upload      │  - Graph RAG  │  - Asset Creator      │
│                     │  - Citation   │                       │
├─────────────────────┼───────────────┼───────────────────────┤
│  Monitoring         │  Workflow     │  User Management      │
│  - Health Check     │  - n8n Flows  │  - Auth & Permissions │
│  - Metrics          │  - Scheduling │  - Team Collaboration │
│  - Reporting        │  - Triggers   │                       │
└─────────────────────┴───────────────┴───────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      数据层 (Data Layer)                       │
├─────────────────────┬───────────────┬───────────────────────┤
│  Neo4j              │  PostgreSQL   │  Redis                │
│  - Knowledge Graph  │  - Users      │  - Cache              │
│  - Relationships    │  - Projects   │  - Sessions           │
│  - Cypher Queries   │  - Tasks      │  - Job Queue          │
├─────────────────────┼───────────────┼───────────────────────┤
│  MinIO              │  MongoDB      │  ElasticSearch        │
│  - Media Files      │  - Logs       │  - Full-text Search   │
│  - Documents        │  - Analytics  │  - Content Index      │
│  - Backups          │  - Audit      │                       │
└─────────────────────┴───────────────┴───────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    外部集成层 (Integrations)                   │
├─────────────────────┬───────────────┬───────────────────────┤
│  InfraNodus API     │  OpenAI API   │  Firecrawl            │
│  Anthropic Claude   │  n8n Webhooks │  GitHub/GitLab        │
│  Slack/Feishu       │  Analytics    │  CMS (WordPress, etc) │
└─────────────────────┴───────────────┴───────────────────────┘
```

### 微服务架构

#### 核心服务

1. **API Gateway Service** (`api-gateway`)
   - 请求路由和负载均衡
   - 身份认证和授权
   - 速率限制和配额管理
   - 日志和监控

2. **Data Acquisition Service** (`data-acquisition`)
   - Web抓取调度
   - InfraNodus集成
   - 数据清洗和标准化
   - 增量更新管理

3. **Graph Processing Service** (`graph-processor`)
   - Neo4j CRUD操作
   - Cypher查询优化
   - 图算法执行（结构洞、社区发现等）
   - 实时图更新

4. **RAG Service** (`rag-engine`)
   - Graph-RAG问答
   - LLM集成（OpenAI、Claude、本地模型）
   - 上下文检索和排序
   - 引用追踪

5. **Content Generation Service** (`content-generator`)
   - 提示词生成
   - 简报创建
   - 资产生成（文章、社媒内容等）
   - 内容评分和优化建议

6. **Workflow Service** (`workflow-orchestrator`)
   - n8n工作流集成
   - 定时任务调度
   - 事件驱动触发器
   - 工作流监控

7. **Analytics Service** (`analytics`)
   - 系统健康监控
   - 使用统计分析
   - 性能指标追踪
   - 自定义报告生成

8. **Notification Service** (`notification`)
   - 邮件通知
   - Slack/Feishu消息
   - Webhook触发
   - 推送通知

---

## 核心功能模块

### 1. 数据采集模块 (Data Acquisition)

#### 功能特性

##### 1.1 多源数据采集
- **网页抓取**
  - 竞品网站内容
  - 行业资讯和博客
  - 用户评论和反馈
  - 社交媒体内容

- **API集成**
  - Google Search Console
  - Google Analytics
  - Social Media APIs (Twitter, LinkedIn, Reddit)
  - E-commerce平台 (Amazon, Shopify)

- **文件导入**
  - CSV/Excel表格
  - PDF文档
  - Word文档
  - 研究报告

- **数据库连接**
  - CRM系统 (Salesforce, HubSpot)
  - Support Tickets (Zendesk, Intercom)
  - Product Analytics (Mixpanel, Amplitude)

##### 1.2 InfraNodus集成
- **文本网络分析**
  - 自动生成共现网络
  - 识别关键主题
  - 发现话题聚类
  - 计算网络指标

- **API调用流程**
  ```python
  # InfraNodus工作流
  text → POST /api/graph →
  分析 → GET /api/graph/{id}/metrics →
  导出 → GET /api/graph/{id}/export
  ```

##### 1.3 数据处理流程
```
原始数据 → 清洗 → 标准化 → InfraNodus分析 → Neo4j导入
    ↓
验证规则检查 → 去重处理 → 实体识别 → 关系抽取
```

#### 数据模型

```python
class DataSource:
    id: UUID
    name: str
    type: SourceType  # WEB, API, FILE, DATABASE
    url: Optional[str]
    config: Dict[str, Any]
    schedule: CronExpression
    last_run: datetime
    status: SourceStatus

class DataImport:
    id: UUID
    source_id: UUID
    started_at: datetime
    completed_at: Optional[datetime]
    records_processed: int
    records_imported: int
    errors: List[ImportError]
    status: ImportStatus
```

### 2. 知识图谱模块 (Knowledge Graph)

#### Neo4j Schema设计

##### 节点类型 (12种)

```cypher
// 1. Keyword - 关键词节点
(:Keyword {
    name: String,              // 关键词
    frequency: Integer,        // 出现频率
    betweenness: Float,        // 介数中心性
    degree: Integer,           // 度中心性
    created_at: DateTime
})

// 2. TopicCluster - 主题集群
(:TopicCluster {
    name: String,              // 集群名称
    size: Integer,             // 包含关键词数量
    density: Float,            // 集群密度
    keywords: [String]         // 关键词列表
})

// 3. Persona - 用户画像
(:Persona {
    name: String,              // 角色名称
    description: String,       // 描述
    pain_points: [String],     // 痛点列表
    goals: [String],           // 目标列表
    demographics: Map          // 人口统计
})

// 4. PainPoint - 用户痛点
(:PainPoint {
    description: String,       // 痛点描述
    severity: Integer,         // 严重程度 (1-10)
    frequency: Integer,        // 出现频率
    evidence: [String]         // 证据来源
})

// 5. Feature - 产品功能
(:Feature {
    name: String,              // 功能名称
    description: String,       // 详细描述
    benefit: String,           // 用户收益
    technical_spec: Map        // 技术规格
})

// 6. Product - 产品
(:Product {
    name: String,              // 产品名称
    brand: String,             // 品牌
    category: String,          // 类别
    price: Float,              // 价格
    rating: Float,             // 评分
    url: String                // 链接
})

// 7. Claim - 声明/主张
(:Claim {
    text: String,              // 声明内容
    claim_type: String,        // 类型 (BENEFIT, FEATURE, etc)
    confidence: Float,         // 置信度
    created_at: DateTime
})

// 8. Evidence - 证据
(:Evidence {
    text: String,              // 证据内容
    source: String,            // 来源
    source_url: String,        // 源链接
    credibility: Float,        // 可信度
    date: DateTime             // 发布日期
})

// 9. Gap - 结构洞/内容空白
(:Gap {
    cluster_a: String,         // 集群A
    cluster_b: String,         // 集群B
    opportunity_score: Float,  // 机会分数
    keywords_a: [String],      // 集群A关键词
    keywords_b: [String],      // 集群B关键词
    identified_at: DateTime
})

// 10. Prompt - 内容提示
(:Prompt {
    text: String,              // 提示内容
    prompt_type: String,       // 类型
    target_persona: String,    // 目标人群
    priority: Integer,         // 优先级
    status: String             // 状态
})

// 11. Brief - 内容简报
(:Brief {
    title: String,             // 标题
    summary: String,           // 摘要
    key_points: [String],      // 关键点
    target_keywords: [String], // 目标关键词
    word_count: Integer,       // 字数要求
    status: String,            // 状态
    created_at: DateTime
})

// 12. Asset - 内容资产
(:Asset {
    title: String,             // 标题
    content: String,           // 内容
    asset_type: String,        // 类型 (BLOG, SOCIAL, etc)
    format: String,            // 格式 (MD, HTML, etc)
    status: String,            // 状态
    published_url: String,     // 发布链接
    citation_score: Float,     // 引用分数
    created_at: DateTime,
    published_at: DateTime
})
```

##### 关系类型

```cypher
// 关键词关系
(:Keyword)-[:CO_OCCURS_WITH {weight: Float}]->(:Keyword)
(:Keyword)-[:BELONGS_TO]->(:TopicCluster)

// 用户关系
(:Persona)-[:HAS_PAIN_POINT]->(:PainPoint)
(:Persona)-[:INTERESTED_IN]->(:Feature)
(:Persona)-[:CONSIDERS]->(:Product)

// 产品关系
(:Product)-[:HAS_FEATURE]->(:Feature)
(:Product)-[:ADDRESSES]->(:PainPoint)
(:Feature)-[:SOLVES]->(:PainPoint)

// 证据链
(:Claim)-[:SUPPORTED_BY]->(:Evidence)
(:Feature)-[:CLAIMED_AS]->(:Claim)
(:Product)-[:MAKES_CLAIM]->(:Claim)

// 内容生成链
(:Gap)-[:GENERATES]->(:Prompt)
(:Prompt)-[:CREATES]->(:Brief)
(:Brief)-[:PRODUCES]->(:Asset)
(:Asset)-[:CITES]->(:Evidence)
(:Asset)-[:TARGETS]->(:Persona)
(:Asset)-[:COVERS]->(:Keyword)
```

#### 关键算法

##### 2.1 结构洞检测算法

```python
def find_structure_holes(
    min_opportunity_score: float = 0.5,
    limit: int = 10
) -> List[Gap]:
    """
    结构洞检测算法

    算法步骤：
    1. 识别所有主题集群
    2. 计算集群间的连接强度
    3. 找到连接弱但相关性高的集群对
    4. 计算机会分数

    机会分数 = (1 - 连接强度) × 语义相关性
    """
    query = """
    MATCH (c1:TopicCluster), (c2:TopicCluster)
    WHERE id(c1) < id(c2)

    // 计算集群间关键词连接
    OPTIONAL MATCH path = (c1)<-[:BELONGS_TO]-(k1:Keyword)
                         -[:CO_OCCURS_WITH]-(k2:Keyword)
                         -[:BELONGS_TO]->(c2)
    WITH c1, c2, count(path) AS connections,
         collect(DISTINCT k1.name) AS keywords_a,
         collect(DISTINCT k2.name) AS keywords_b

    // 计算连接强度和机会分数
    WITH c1, c2, connections, keywords_a, keywords_b,
         (c1.size + c2.size) AS total_keywords,
         1.0 - (connections * 1.0 / total_keywords) AS gap_strength

    WHERE gap_strength >= $min_score

    RETURN c1.name AS cluster_a,
           c2.name AS cluster_b,
           gap_strength AS opportunity_score,
           keywords_a[0..5] AS keywords_a,
           keywords_b[0..5] AS keywords_b
    ORDER BY opportunity_score DESC
    LIMIT $limit
    """
    return execute_query(query, {
        'min_score': min_opportunity_score,
        'limit': limit
    })
```

##### 2.2 Citation-Ready评分算法

```python
def calculate_citation_score(asset_id: UUID) -> float:
    """
    Citation-Ready评分算法

    评分维度：
    1. 证据连接度 (40%) - 引用的证据数量和质量
    2. 知识图谱连接度 (30%) - 与图谱实体的连接强度
    3. 内容完整性 (20%) - 是否覆盖关键主题
    4. 新鲜度 (10%) - 证据和内容的时效性
    """
    query = """
    MATCH (a:Asset {id: $asset_id})

    // 1. 证据连接度
    OPTIONAL MATCH (a)-[:CITES]->(e:Evidence)
    WITH a, count(e) AS evidence_count,
         avg(e.credibility) AS avg_credibility

    // 2. 知识图谱连接度
    OPTIONAL MATCH (a)-[:COVERS]->(k:Keyword)
    WITH a, evidence_count, avg_credibility,
         count(k) AS keyword_coverage,
         avg(k.betweenness) AS avg_importance

    // 3. 目标人群覆盖
    OPTIONAL MATCH (a)-[:TARGETS]->(p:Persona)
    WITH a, evidence_count, avg_credibility,
         keyword_coverage, avg_importance,
         count(p) AS persona_coverage

    // 4. 计算综合评分
    WITH a,
         (evidence_count * avg_credibility / 10.0) AS evidence_score,
         (keyword_coverage * avg_importance / 10.0) AS connectivity_score,
         (persona_coverage / 3.0) AS completeness_score

    RETURN 0.4 * evidence_score +
           0.3 * connectivity_score +
           0.2 * completeness_score +
           0.1 AS citation_score
    """
    return execute_query(query, {'asset_id': asset_id})[0]['citation_score']
```

### 3. Graph-RAG问答模块

#### 架构设计

```python
class GraphRAG:
    """Graph-RAG问答系统"""

    def answer_question(self, question: str) -> Answer:
        """
        Graph-RAG回答流程：

        1. 问题分类 → 识别问题类型
        2. 实体识别 → 提取关键实体
        3. 图谱检索 → 查询相关子图
        4. 上下文组装 → 构建提示词
        5. LLM生成 → 生成答案
        6. 引用追踪 → 添加来源
        7. 置信度评估 → 评估答案质量
        """
        # 1. 问题分类
        question_type = self._classify_question(question)

        # 2. 实体识别
        entities = self._extract_entities(question)

        # 3. 图谱检索
        subgraph = self._retrieve_subgraph(
            question_type, entities
        )

        # 4. 上下文组装
        context = self._build_context(subgraph)

        # 5. LLM生成
        answer_text = self._generate_answer(
            question, context
        )

        # 6. 引用追踪
        citations = self._extract_citations(
            answer_text, subgraph
        )

        # 7. 置信度评估
        confidence = self._calculate_confidence(
            answer_text, citations, subgraph
        )

        return Answer(
            question=question,
            answer_text=answer_text,
            citations=citations,
            confidence=confidence,
            graph_path=subgraph.paths
        )
```

#### 问题类型分类

```python
class QuestionType(Enum):
    FEATURE = "feature"        # 功能相关
    PAIN_POINT = "pain_point"  # 痛点相关
    PRODUCT = "product"        # 产品相关
    EVIDENCE = "evidence"      # 证据相关
    COMPARISON = "comparison"  # 比较相关
    GENERAL = "general"        # 通用问题

# 问题分类规则
CLASSIFICATION_RULES = {
    "feature": [
        "what is", "what are", "how does", "explain",
        "feature", "function", "capability"
    ],
    "pain_point": [
        "problem", "issue", "solve", "fix", "pain",
        "difficulty", "challenge", "struggle"
    ],
    "product": [
        "which product", "best product", "recommend",
        "top", "comparison", "vs"
    ],
    "evidence": [
        "proof", "evidence", "research", "study",
        "data", "statistics", "support"
    ]
}
```

#### Cypher查询模板

```python
QUERY_TEMPLATES = {
    "feature": """
        MATCH (f:Feature)
        WHERE f.name CONTAINS $keyword
        OPTIONAL MATCH (f)-[:SOLVES]->(pp:PainPoint)
        OPTIONAL MATCH (p:Product)-[:HAS_FEATURE]->(f)
        OPTIONAL MATCH (f)-[:CLAIMED_AS]->(c:Claim)-[:SUPPORTED_BY]->(e:Evidence)
        RETURN f, collect(DISTINCT pp) AS pain_points,
               collect(DISTINCT p) AS products,
               collect(DISTINCT e) AS evidence
    """,

    "pain_point": """
        MATCH (pp:PainPoint)
        WHERE pp.description CONTAINS $keyword
        OPTIONAL MATCH (f:Feature)-[:SOLVES]->(pp)
        OPTIONAL MATCH (p:Product)-[:ADDRESSES]->(pp)
        OPTIONAL MATCH (persona:Persona)-[:HAS_PAIN_POINT]->(pp)
        RETURN pp, collect(DISTINCT f) AS solutions,
               collect(DISTINCT p) AS products,
               persona
        ORDER BY pp.severity DESC, pp.frequency DESC
    """,

    "product": """
        MATCH (p:Product)
        WHERE p.name CONTAINS $keyword
        OPTIONAL MATCH (p)-[:HAS_FEATURE]->(f:Feature)
        OPTIONAL MATCH (p)-[:ADDRESSES]->(pp:PainPoint)
        OPTIONAL MATCH (p)-[:MAKES_CLAIM]->(c:Claim)-[:SUPPORTED_BY]->(e:Evidence)
        RETURN p, collect(DISTINCT f) AS features,
               collect(DISTINCT pp) AS pain_points,
               collect(DISTINCT e) AS evidence
        ORDER BY p.rating DESC
    """,

    "evidence": """
        MATCH (e:Evidence)
        WHERE e.text CONTAINS $keyword
        OPTIONAL MATCH (c:Claim)-[:SUPPORTED_BY]->(e)
        OPTIONAL MATCH (f:Feature)-[:CLAIMED_AS]->(c)
        RETURN e, collect(DISTINCT c) AS claims,
               collect(DISTINCT f) AS features
        ORDER BY e.credibility DESC, e.date DESC
    """
}
```

### 4. 内容生成模块

#### 生成流程

```
结构洞 → 提示词生成 → 简报创建 → 资产生成 → 发布
   ↓          ↓           ↓           ↓         ↓
 Gap      Prompt      Brief       Asset    Published
 识别      模板        大纲        内容      内容
```

#### 4.1 提示词生成引擎

```python
class PromptEngine:
    """提示词生成引擎"""

    def generate_from_gap(self, gap: Gap) -> List[Prompt]:
        """
        从结构洞生成内容提示词

        生成策略：
        1. 桥接策略 - 连接两个集群的内容
        2. 深挖策略 - 深入探讨单个集群
        3. 对比策略 - 对比两个集群的差异
        """
        prompts = []

        # 策略1: 桥接内容
        bridge_prompt = self._create_bridge_prompt(gap)
        prompts.append(bridge_prompt)

        # 策略2: 深挖集群A
        deep_dive_a = self._create_deep_dive_prompt(
            gap.cluster_a, gap.keywords_a
        )
        prompts.append(deep_dive_a)

        # 策略3: 对比分析
        comparison = self._create_comparison_prompt(gap)
        prompts.append(comparison)

        return prompts

    def _create_bridge_prompt(self, gap: Gap) -> Prompt:
        """创建桥接提示词"""
        template = """
        Create content that bridges {cluster_a} and {cluster_b}.

        Context:
        - Cluster A focuses on: {keywords_a}
        - Cluster B focuses on: {keywords_b}
        - Opportunity Score: {score}

        Content should:
        1. Explain how {cluster_a} relates to {cluster_b}
        2. Provide practical examples
        3. Include evidence-based recommendations
        4. Target users interested in both topics
        """

        return Prompt(
            text=template.format(
                cluster_a=gap.cluster_a,
                cluster_b=gap.cluster_b,
                keywords_a=", ".join(gap.keywords_a),
                keywords_b=", ".join(gap.keywords_b),
                score=gap.opportunity_score
            ),
            prompt_type="BRIDGE",
            priority=self._calculate_priority(gap),
            status="PENDING"
        )
```

#### 4.2 简报生成器

```python
class BriefGenerator:
    """内容简报生成器"""

    def create_brief(self, prompt: Prompt) -> Brief:
        """
        生成内容简报

        简报包含：
        1. 标题和摘要
        2. 关键要点
        3. 目标关键词
        4. 内容大纲
        5. 证据要求
        6. SEO/GEO建议
        """
        # 1. 检索相关知识
        knowledge = self._retrieve_knowledge(prompt)

        # 2. 生成标题选项
        titles = self._generate_titles(prompt, knowledge)

        # 3. 创建内容大纲
        outline = self._create_outline(prompt, knowledge)

        # 4. 识别证据需求
        evidence_needs = self._identify_evidence_needs(outline)

        # 5. SEO/GEO优化建议
        seo_recommendations = self._generate_seo_recommendations(
            prompt, knowledge
        )

        return Brief(
            title=titles[0],  # 选择最佳标题
            title_alternatives=titles[1:],
            summary=self._generate_summary(outline),
            key_points=outline.main_points,
            outline=outline,
            target_keywords=self._extract_keywords(prompt, knowledge),
            evidence_requirements=evidence_needs,
            seo_recommendations=seo_recommendations,
            word_count=self._estimate_word_count(outline),
            tone="professional",
            target_persona=prompt.target_persona,
            status="DRAFT"
        )
```

#### 4.3 资产生成器

```python
class AssetGenerator:
    """内容资产生成器"""

    def generate_asset(
        self,
        brief: Brief,
        asset_type: AssetType = AssetType.BLOG_POST
    ) -> Asset:
        """
        生成最终内容资产

        支持类型：
        - BLOG_POST: 博客文章
        - SOCIAL_POST: 社交媒体帖子
        - EMAIL: 邮件内容
        - LANDING_PAGE: 落地页
        - FAQ: 常见问题
        """
        # 1. 准备上下文
        context = self._prepare_context(brief)

        # 2. 根据类型选择模板
        template = self._get_template(asset_type)

        # 3. 生成内容
        content = self._generate_content(
            brief, context, template
        )

        # 4. 添加引用
        content_with_citations = self._add_citations(
            content, context.evidence
        )

        # 5. 优化和格式化
        final_content = self._optimize_content(
            content_with_citations, asset_type
        )

        # 6. 计算评分
        citation_score = self._calculate_citation_score(
            final_content, context.evidence
        )

        return Asset(
            title=brief.title,
            content=final_content,
            asset_type=asset_type,
            format="MARKDOWN",
            status="READY_FOR_REVIEW",
            citation_score=citation_score,
            metadata={
                "word_count": len(final_content.split()),
                "keywords": brief.target_keywords,
                "evidence_count": len(context.evidence),
                "target_persona": brief.target_persona
            }
        )
```

### 5. 监控与报告模块

#### 5.1 实时监控面板

```python
class MonitoringDashboard:
    """监控面板"""

    def get_real_time_metrics(self) -> DashboardMetrics:
        """获取实时指标"""
        return DashboardMetrics(
            system_health=self.check_system_health(),
            graph_metrics=self.get_graph_metrics(),
            pipeline_metrics=self.get_pipeline_metrics(),
            content_performance=self.get_content_performance(),
            user_activity=self.get_user_activity()
        )

    def check_system_health(self) -> SystemHealth:
        """系统健康检查"""
        checks = {
            "neo4j": self._check_neo4j(),
            "api": self._check_api_availability(),
            "queue": self._check_queue_length(),
            "storage": self._check_storage_usage()
        }

        health_score = sum(
            1.0 for check in checks.values() if check.status == "ok"
        ) / len(checks) * 100

        return SystemHealth(
            health_score=health_score,
            checks=checks,
            last_check=datetime.now()
        )
```

#### 5.2 周报生成器

```python
class WeeklyReportGenerator:
    """周报生成器"""

    def generate_report(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> WeeklyReport:
        """生成周报"""

        # 1. 收集数据
        data = self._collect_weekly_data(start_date, end_date)

        # 2. 分析趋势
        trends = self._analyze_trends(data)

        # 3. 生成见解
        insights = self._generate_insights(data, trends)

        # 4. 制定建议
        recommendations = self._create_recommendations(
            data, trends, insights
        )

        # 5. 格式化报告
        report = self._format_report(
            data, trends, insights, recommendations
        )

        return report
```

---

## 技术栈

### 后端技术

#### 核心框架
```python
# API Framework
FastAPI 0.104.0            # 现代化Web框架
Pydantic 2.5.0            # 数据验证
Python 3.12+              # 编程语言

# 异步和并发
asyncio                   # 异步IO
aiohttp                   # 异步HTTP客户端
celery 5.3.0              # 分布式任务队列
redis 5.0.0               # 消息队列和缓存
```

#### 数据库和存储
```python
# 图数据库
neo4j 5.14.0              # 知识图谱存储
py2neo 2021.2.4           # Neo4j Python驱动

# 关系数据库
PostgreSQL 15             # 用户和元数据
SQLAlchemy 2.0            # ORM框架
alembic 1.12.0            # 数据库迁移

# 文档数据库
MongoDB 7.0               # 日志和分析
pymongo 4.5.0             # MongoDB驱动

# 对象存储
MinIO                     # S3兼容对象存储
boto3                     # AWS SDK

# 缓存
Redis 7.2                 # 缓存和会话
```

#### AI和机器学习
```python
# LLM集成
openai 1.3.0              # OpenAI API
anthropic 0.7.0           # Claude API
langchain 0.1.0           # LLM工具链

# NLP
spacy 3.7.0               # 实体识别
transformers 4.35.0       # 预训练模型
sentence-transformers     # 向量嵌入

# 图算法
networkx 3.2              # 图分析
python-louvain            # 社区发现
```

#### 数据处理
```python
# Web抓取
playwright 1.40.0         # 浏览器自动化
beautifulsoup4 4.12.0    # HTML解析
firecrawl                 # Web数据提取

# 数据分析
pandas 2.1.0              # 数据处理
numpy 1.26.0              # 数值计算
scipy 1.11.0              # 科学计算
```

### 前端技术

#### 核心框架
```javascript
// React生态
React 18.2.0              // UI框架
Next.js 14.0.0            // React框架
TypeScript 5.2.0          // 类型安全

// 状态管理
Zustand 4.4.0             // 状态管理
React Query 5.0.0         // 数据获取

// 路由
React Router 6.20.0       // 客户端路由
```

#### UI组件库
```javascript
// 组件库
shadcn/ui                 // UI组件
Radix UI                  // 无样式组件
Tailwind CSS 3.3.0        // CSS框架
Lucide React              // 图标库

// 数据可视化
D3.js 7.8.0               // 数据可视化
Recharts 2.9.0            // React图表
Cytoscape.js 3.27.0       // 图可视化
```

#### 开发工具
```javascript
// 构建工具
Vite 5.0.0                // 构建工具
ESLint 8.54.0             // 代码检查
Prettier 3.1.0            // 代码格式化

// 测试
Vitest 1.0.0              // 单元测试
Playwright 1.40.0         // E2E测试
```

### DevOps和基础设施

#### 容器化
```yaml
# Docker
Docker 24.0.0
Docker Compose 2.23.0

# 容器编排
Kubernetes 1.28
Helm 3.13.0
```

#### CI/CD
```yaml
# 持续集成
GitHub Actions
GitLab CI/CD

# 代码质量
SonarQube
CodeCov
```

#### 监控和日志
```yaml
# 监控
Prometheus              # 指标收集
Grafana                # 可视化面板
Sentry                 # 错误追踪

# 日志
ELK Stack              # 日志收集和分析
  - Elasticsearch
  - Logstash
  - Kibana
```

#### 部署平台
```yaml
# 云服务商
AWS / Azure / GCP

# 服务
- EC2 / Compute Engine  # 虚拟机
- S3 / Blob Storage     # 对象存储
- RDS / Cloud SQL       # 托管数据库
- CloudFront / CDN      # 内容分发
```

---

## 数据流设计

### 完整数据流图

```
┌─────────────────┐
│  Data Sources   │  外部数据源
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Data Acquisition│  数据采集
│  - Web Scraping │
│  - API Calls    │
│  - File Upload  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Data Processing │  数据处理
│  - Cleaning     │
│  - Validation   │
│  - Enrichment   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   InfraNodus    │  文本网络分析
│  - Co-occurrence│
│  - Clustering   │
│  - Metrics      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│    Neo4j        │  知识图谱存储
│  - Nodes        │
│  - Relationships│
│  - Indexes      │
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┐
         ↓                 ↓                 ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Structure Hole│  │  Graph-RAG   │  │ Monitoring   │
│  Analysis    │  │   Q&A        │  │  Dashboard   │
└──────┬───────┘  └──────┬───────┘  └──────────────┘
       │                 │
       ↓                 ↓
┌──────────────┐  ┌──────────────┐
│   Prompt     │  │   Answer     │
│  Generation  │  │  Delivery    │
└──────┬───────┘  └──────────────┘
       │
       ↓
┌──────────────┐
│    Brief     │
│  Creation    │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│    Asset     │
│  Generation  │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│  Publishing  │
│  - CMS       │
│  - Social    │
│  - Email     │
└──────────────┘
```

### 关键数据流

#### 1. 数据采集流
```python
# 输入: URL/File/API
raw_data = acquire_data(source)

# 清洗和验证
cleaned_data = clean_and_validate(raw_data)

# InfraNodus分析
infranodus_data = analyze_with_infranodus(cleaned_data)

# Neo4j导入
import_to_neo4j(infranodus_data)

# 输出: 知识图谱更新
```

#### 2. 内容生成流
```python
# 输入: 触发条件（定时/手动/事件）
gaps = find_structure_holes()

# 生成提示词
prompts = generate_prompts(gaps)

# 创建简报
for prompt in prompts:
    brief = create_brief(prompt)

    # 生成资产
    asset = generate_asset(brief)

    # 计算评分
    score = calculate_citation_score(asset)

    # 发布（如果评分>阈值）
    if score > THRESHOLD:
        publish_asset(asset)
```

#### 3. 问答流
```python
# 输入: 用户问题
question = user_input

# Graph-RAG处理
answer = graph_rag.answer_question(question)

# 输出: 答案+引用+置信度
return {
    "answer": answer.answer_text,
    "citations": answer.citations,
    "confidence": answer.confidence
}
```

---

## API接口设计

### RESTful API

#### 基础URL
```
Production:  https://api.geo-platform.com/v1
Development: http://localhost:8000/v1
```

#### 认证
```http
Authorization: Bearer <JWT_TOKEN>
```

### 核心API端点

#### 1. 认证相关
```http
POST   /auth/register          # 用户注册
POST   /auth/login             # 用户登录
POST   /auth/refresh           # 刷新Token
POST   /auth/logout            # 登出
GET    /auth/me                # 获取当前用户
```

#### 2. 数据采集
```http
# 数据源管理
GET    /data-sources           # 列表
POST   /data-sources           # 创建
GET    /data-sources/:id       # 详情
PUT    /data-sources/:id       # 更新
DELETE /data-sources/:id       # 删除
POST   /data-sources/:id/run   # 立即执行

# 导入任务
GET    /imports                # 导入历史
GET    /imports/:id            # 导入详情
POST   /imports/:id/retry      # 重试失败的导入
```

#### 3. 知识图谱
```http
# 实体操作
GET    /entities               # 实体列表
POST   /entities               # 创建实体
GET    /entities/:id           # 实体详情
PUT    /entities/:id           # 更新实体
DELETE /entities/:id           # 删除实体

# 关系操作
GET    /relationships          # 关系列表
POST   /relationships          # 创建关系
DELETE /relationships/:id      # 删除关系

# 图谱查询
POST   /graph/query            # Cypher查询
POST   /graph/search           # 全文搜索
GET    /graph/neighbors/:id    # 获取邻居节点
GET    /graph/path             # 查找路径

# 统计分析
GET    /graph/stats            # 图谱统计
GET    /graph/metrics          # 图谱指标
```

#### 4. 结构洞分析
```http
GET    /gaps                   # 结构洞列表
POST   /gaps/analyze           # 执行分析
GET    /gaps/:id               # 详情
POST   /gaps/:id/generate      # 生成提示词
```

#### 5. Graph-RAG问答
```http
POST   /rag/ask                # 提问
GET    /rag/history            # 历史记录
GET    /rag/answers/:id        # 答案详情
POST   /rag/feedback           # 答案反馈
```

#### 6. 内容生成
```http
# 提示词
GET    /prompts                # 提示词列表
POST   /prompts                # 创建提示词
GET    /prompts/:id            # 详情
PUT    /prompts/:id/priority   # 更新优先级

# 简报
GET    /briefs                 # 简报列表
POST   /briefs                 # 创建简报
GET    /briefs/:id             # 详情
PUT    /briefs/:id             # 更新
POST   /briefs/:id/approve     # 批准

# 资产
GET    /assets                 # 资产列表
POST   /assets                 # 创建资产
GET    /assets/:id             # 详情
PUT    /assets/:id             # 更新
POST   /assets/:id/publish     # 发布
GET    /assets/:id/preview     # 预览
```

#### 7. 监控和报告
```http
GET    /monitoring/health      # 系统健康
GET    /monitoring/metrics     # 实时指标
GET    /monitoring/dashboard   # 面板数据

GET    /reports/weekly         # 周报
GET    /reports/monthly        # 月报
POST   /reports/custom         # 自定义报告
```

#### 8. 工作流
```http
GET    /workflows              # 工作流列表
POST   /workflows              # 创建工作流
GET    /workflows/:id          # 详情
PUT    /workflows/:id          # 更新
POST   /workflows/:id/trigger  # 触发执行
GET    /workflows/:id/runs     # 执行历史
```

### GraphQL API

```graphql
type Query {
  # 知识图谱查询
  entities(
    type: EntityType
    limit: Int = 10
    offset: Int = 0
    search: String
  ): [Entity!]!

  entity(id: ID!): Entity

  # Graph-RAG
  answer(question: String!): Answer!

  # 内容生成
  gaps(minScore: Float = 0.5): [Gap!]!
  prompts(status: PromptStatus): [Prompt!]!
  assets(status: AssetStatus): [Asset!]!

  # 监控
  systemHealth: SystemHealth!
  graphMetrics: GraphMetrics!
}

type Mutation {
  # 数据采集
  createDataSource(input: DataSourceInput!): DataSource!
  runDataSource(id: ID!): Import!

  # 实体操作
  createEntity(input: EntityInput!): Entity!
  updateEntity(id: ID!, input: EntityInput!): Entity!
  deleteEntity(id: ID!): Boolean!

  # 内容生成
  generatePrompts(gapId: ID!): [Prompt!]!
  createBrief(promptId: ID!): Brief!
  generateAsset(briefId: ID!): Asset!
  publishAsset(id: ID!): Asset!
}

type Subscription {
  # 实时更新
  importProgress(importId: ID!): ImportProgress!
  systemHealthUpdates: SystemHealth!
}
```

### WebSocket API

```javascript
// 连接
const ws = new WebSocket('wss://api.geo-platform.com/ws')

// 订阅实时更新
ws.send(JSON.stringify({
  type: 'subscribe',
  channel: 'imports',
  importId: '123'
}))

// 接收更新
ws.onmessage = (event) => {
  const update = JSON.parse(event.data)
  // 处理更新
}
```

---

## 前端界面设计

### 主要页面

#### 1. 仪表板 (Dashboard)
```
┌─────────────────────────────────────────────────────┐
│  GEO Platform Dashboard                    [User ▼] │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ System Health│  │ Total Nodes  │  │ New Gaps  │ │
│  │     80%      │  │     1,250    │  │    5      │ │
│  └──────────────┘  └──────────────┘  └───────────┘ │
│                                                      │
│  ┌───────────────────────────────────────────────┐  │
│  │ Content Pipeline                              │  │
│  │                                               │  │
│  │  Prompts [====    ] 12                       │  │
│  │  Briefs  [======  ] 8                        │  │
│  │  Assets  [========] 4                        │  │
│  └───────────────────────────────────────────────┘  │
│                                                      │
│  ┌───────────────────────────────────────────────┐  │
│  │ Recent Activity                               │  │
│  │  • Import completed: competitor-analysis      │  │
│  │  • New gap identified: tech_features ↔ price │  │
│  │  • Asset published: mattress-buying-guide    │  │
│  └───────────────────────────────────────────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 2. 知识图谱浏览器 (Graph Explorer)
```
┌─────────────────────────────────────────────────────┐
│  Knowledge Graph Explorer                  [Search] │
├───────────┬─────────────────────────────────────────┤
│ Filters   │                                         │
│           │     [Interactive Graph Visualization]   │
│ □ Keywords│                                         │
│ □ Topics  │           ⚫ ── ⚫                       │
│ □ Products│          /  \  /  \                     │
│ □ Features│         ⚫ ── ⚫ ── ⚫                    │
│ □ Claims  │          \  /  \  /                     │
│ □ Evidence│           ⚫ ── ⚫                       │
│           │                                         │
│ [Analyze] │     Click node for details →           │
│           │                                         │
│           │  Selected: "memory_foam"                │
│           │  Type: Keyword                          │
│           │  Frequency: 142                         │
│           │  Related: 8 nodes                       │
│           │  [View Details] [Expand]                │
└───────────┴─────────────────────────────────────────┘
```

#### 3. 结构洞分析 (Structure Holes)
```
┌─────────────────────────────────────────────────────┐
│  Structure Hole Analysis            [Run Analysis]  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  Content Opportunities (5 found)                    │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ #1  comfort_tech ↔ sleep_problems            │   │
│  │     Score: 0.700                 [Generate]  │   │
│  │                                               │   │
│  │     Keywords:                                 │   │
│  │     cooling_gel, memory_foam ↔ hot_sleeper  │   │
│  │                                               │   │
│  │     Recommendation:                           │   │
│  │     Create content bridging comfort          │   │
│  │     technologies and sleep solutions         │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ #2  health_issues ↔ sleep_problems           │   │
│  │     Score: 0.615                 [Generate]  │   │
│  │     ...                                       │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 4. Graph-RAG问答 (Ask Question)
```
┌─────────────────────────────────────────────────────┐
│  Ask a Question                                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ What evidence supports cooling gel?         │   │
│  │                                    [Ask] ✓  │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Answer (Confidence: 85%)                           │
│  ────────────────────────────────────────────       │
│  Multiple studies support cooling gel               │
│  effectiveness:                                     │
│                                                      │
│  1. Temperature regulation [1]                      │
│  2. Improved sleep quality [2]                      │
│  3. User satisfaction 92% [3]                       │
│                                                      │
│  Citations:                                         │
│  [1] Sleep Foundation Study 2023                    │
│  [2] Journal of Sleep Research                     │
│  [3] Product Review Analysis (n=1,245)             │
│                                                      │
│  [👍 Helpful] [👎 Not Helpful] [Copy] [Share]      │
│                                                      │
│  Related Questions:                                 │
│  • How does cooling gel compare to memory foam?    │
│  • Which products have the best cooling gel?       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 5. 内容生成工作流 (Content Pipeline)
```
┌─────────────────────────────────────────────────────┐
│  Content Pipeline                    [New Content]  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────┬────────┬──────────┬──────────┐        │
│  │ Prompts │ Briefs │  Assets  │ Published│        │
│  └─────────┴────────┴──────────┴──────────┘        │
│                                                      │
│  Prompts (12)                    [Sort ▼] [Filter] │
│  ────────────────────────────────────────────       │
│  ┌──────────────────────────────────────────────┐   │
│  │ Bridge: comfort_tech ↔ sleep_problems        │   │
│  │ Priority: High • Created: 2 hours ago        │   │
│  │ Status: Pending                              │   │
│  │ [Create Brief] [Edit] [Delete]               │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │ Deep Dive: cooling_gel effectiveness         │   │
│  │ Priority: Medium • Created: 1 day ago        │   │
│  │ Status: Brief Created                        │   │
│  │ [View Brief] [Edit]                          │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

#### 6. 简报编辑器 (Brief Editor)
```
┌─────────────────────────────────────────────────────┐
│  Brief Editor                      [Save] [Generate]│
├─────────────────────────────────────────────────────┤
│                                                      │
│  Title                                              │
│  ┌──────────────────────────────────────────────┐   │
│  │ Complete Guide: Cooling Gel Technology      │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  Target Keywords                                    │
│  [cooling gel] [temperature regulation] [sleep]    │
│                                                      │
│  Outline                                            │
│  1. Introduction                                    │
│     • What is cooling gel                           │
│     • Why it matters                                │
│  2. How It Works                                    │
│     • Technology explanation                        │
│     • Science behind it                             │
│  3. Benefits                                        │
│     • Temperature control                           │
│     • Sleep quality                                 │
│  4. Evidence                                        │
│     • Research studies                              │
│     • User testimonials                             │
│                                                      │
│  Evidence Requirements                              │
│  ⚠️ Need 3 more citations for section 2            │
│  ✓ Section 3 fully supported                       │
│                                                      │
│  SEO Recommendations                                │
│  • Add FAQ section                                  │
│  • Include comparison table                         │
│  • Target featured snippet                          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### UI组件库

#### 核心组件

```typescript
// 按钮组件
<Button
  variant="primary" | "secondary" | "outline"
  size="sm" | "md" | "lg"
  loading={boolean}
  icon={IconComponent}
>
  Label
</Button>

// 图谱可视化组件
<GraphVisualization
  data={graphData}
  onNodeClick={handleNodeClick}
  layout="force" | "circular" | "hierarchical"
  filters={activeFilters}
/>

// 指标卡片
<MetricCard
  title="System Health"
  value={80}
  unit="%"
  trend="up" | "down" | "stable"
  change={5}
  icon={HealthIcon}
/>

// 内容卡片
<ContentCard
  type="prompt" | "brief" | "asset"
  title="Content Title"
  status="pending" | "in_progress" | "completed"
  priority="high" | "medium" | "low"
  actions={[...]}
/>

// 结构洞卡片
<GapCard
  clusterA="comfort_tech"
  clusterB="sleep_problems"
  score={0.700}
  keywordsA={["cooling_gel", "memory_foam"]}
  keywordsB={["hot_sleeper"]}
  onGenerate={handleGenerate}
/>
```

---

## 自动化工作流

### n8n工作流设计

#### 工作流1: 每日数据采集

```yaml
name: Daily Data Acquisition
trigger: Cron (0 2 * * *)  # 每天凌晨2点

nodes:
  - id: trigger
    type: n8n-nodes-base.cron

  - id: fetch_competitors
    type: n8n-nodes-base.httpRequest
    action: POST /api/v1/data-sources/bulk-run
    parameters:
      sources: ["competitor-1", "competitor-2", "competitor-3"]

  - id: wait_completion
    type: n8n-nodes-base.wait
    parameters:
      amount: 30
      unit: minutes

  - id: check_status
    type: n8n-nodes-base.httpRequest
    action: GET /api/v1/imports?status=completed&date=today

  - id: analyze_structure_holes
    type: n8n-nodes-base.httpRequest
    action: POST /api/v1/gaps/analyze

  - id: send_notification
    type: n8n-nodes-base.slack
    parameters:
      channel: "#content-team"
      message: "Daily data acquisition completed. {{$json.records_imported}} records imported."
```

#### 工作流2: 内容生成流水线

```yaml
name: Content Generation Pipeline
trigger: Manual / Webhook / Gap Identified

nodes:
  - id: gap_identified
    type: n8n-nodes-base.webhook

  - id: generate_prompts
    type: n8n-nodes-base.httpRequest
    action: POST /api/v1/gaps/{{$json.gap_id}}/generate

  - id: create_briefs
    type: n8n-nodes-base.code
    code: |
      const prompts = $input.all();
      const briefs = [];

      for (const prompt of prompts) {
        const brief = await fetch('/api/v1/briefs', {
          method: 'POST',
          body: JSON.stringify({ promptId: prompt.id })
        });
        briefs.push(brief);
      }

      return briefs;

  - id: send_for_review
    type: n8n-nodes-base.slack
    parameters:
      channel: "#content-review"
      message: "New briefs ready for review"
      blocks: [...]

  - id: wait_for_approval
    type: n8n-nodes-base.wait
    parameters:
      webhook: true

  - id: generate_assets
    type: n8n-nodes-base.httpRequest
    action: POST /api/v1/assets

  - id: publish_if_score_high
    type: n8n-nodes-base.if
    parameters:
      condition: "{{$json.citation_score}} > 0.7"
    branches:
      true: publish_to_cms
      false: send_for_manual_review
```

#### 工作流3: 周报生成和发送

```yaml
name: Weekly Report Generation
trigger: Cron (0 9 * * 1)  # 每周一早上9点

nodes:
  - id: trigger
    type: n8n-nodes-base.cron

  - id: generate_report
    type: n8n-nodes-base.httpRequest
    action: GET /api/v1/reports/weekly
    parameters:
      format: html

  - id: format_email
    type: n8n-nodes-base.emailTemplate
    template: |
      Subject: GEO Weekly Report - {{$json.week}}

      <h1>GEO System Weekly Report</h1>
      <p>Health Score: {{$json.health_score}}%</p>

      <h2>Key Insights</h2>
      <ul>
        {{#each $json.insights}}
        <li>{{this}}</li>
        {{/each}}
      </ul>

      <h2>Content Pipeline</h2>
      <ul>
        <li>Prompts Generated: {{$json.prompts_count}}</li>
        <li>Briefs Created: {{$json.briefs_count}}</li>
        <li>Assets Published: {{$json.assets_count}}</li>
      </ul>

      <h2>Recommendations</h2>
      <ul>
        {{#each $json.recommendations}}
        <li>{{this}}</li>
        {{/each}}
      </ul>

  - id: send_email
    type: n8n-nodes-base.gmail
    parameters:
      to: ["team@company.com"]
      attachments: [...]

  - id: post_to_slack
    type: n8n-nodes-base.slack
    parameters:
      channel: "#weekly-reports"
      blocks: [...]

  - id: archive_to_notion
    type: n8n-nodes-base.notion
    action: Create Page
    database: "Reports"
```

### Celery定时任务

```python
from celery import Celery
from celery.schedules import crontab

app = Celery('geo_platform')

# 定时任务配置
app.conf.beat_schedule = {
    # 每小时检查系统健康
    'health-check-hourly': {
        'task': 'tasks.monitoring.check_health',
        'schedule': crontab(minute=0),
    },

    # 每天凌晨2点数据采集
    'daily-data-acquisition': {
        'task': 'tasks.acquisition.run_daily_sources',
        'schedule': crontab(hour=2, minute=0),
    },

    # 每天凌晨3点结构洞分析
    'daily-gap-analysis': {
        'task': 'tasks.analysis.find_structure_holes',
        'schedule': crontab(hour=3, minute=0),
    },

    # 每周一生成周报
    'weekly-report': {
        'task': 'tasks.reporting.generate_weekly_report',
        'schedule': crontab(
            day_of_week=1,
            hour=9,
            minute=0
        ),
    },

    # 每月清理旧数据
    'monthly-cleanup': {
        'task': 'tasks.maintenance.cleanup_old_data',
        'schedule': crontab(
            day_of_month=1,
            hour=0,
            minute=0
        ),
    },
}

# 任务定义
@app.task
def check_health():
    """健康检查任务"""
    dashboard = MonitoringDashboard()
    health = dashboard.check_system_health()

    if health.health_score < 70:
        send_alert("System health below threshold")

    return health

@app.task
def run_daily_sources():
    """每日数据采集"""
    sources = get_active_sources()
    results = []

    for source in sources:
        result = source.run()
        results.append(result)

    return results

@app.task
def find_structure_holes():
    """结构洞分析"""
    queries = GEOQueries()
    gaps = queries.find_structure_holes(min_opportunity_score=0.5)

    # 自动生成提示词
    for gap in gaps:
        create_prompts_from_gap(gap)

    return len(gaps)
```

---

## 部署方案

### Docker Compose部署 (开发/测试)

```yaml
version: '3.8'

services:
  # API Gateway
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "8000:8000"
    environment:
      - NEO4J_URI=neo4j://neo4j:7687
      - POSTGRES_URL=postgresql://user:pass@postgres:5432/geo
      - REDIS_URL=redis://redis:6379
    depends_on:
      - neo4j
      - postgres
      - redis

  # Neo4j
  neo4j:
    image: neo4j:5.14.0
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs

  # PostgreSQL
  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=geo_user
      - POSTGRES_PASSWORD=geo_pass
      - POSTGRES_DB=geo_platform
    volumes:
      - postgres-data:/var/lib/postgresql/data

  # Redis
  redis:
    image: redis:7.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  # MongoDB
  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=geo_user
      - MONGO_INITDB_ROOT_PASSWORD=geo_pass
    volumes:
      - mongodb-data:/data/db

  # MinIO
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
    command: server /data --console-address ":9001"
    volumes:
      - minio-data:/data

  # Celery Worker
  celery-worker:
    build: ./services/api-gateway
    command: celery -A app.celery worker -l info
    environment:
      - NEO4J_URI=neo4j://neo4j:7687
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
      - neo4j

  # Celery Beat
  celery-beat:
    build: ./services/api-gateway
    command: celery -A app.celery beat -l info
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  # n8n
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n-data:/home/node/.n8n

  # Frontend
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - api-gateway

volumes:
  neo4j-data:
  neo4j-logs:
  postgres-data:
  redis-data:
  mongodb-data:
  minio-data:
  n8n-data:
```

### Kubernetes部署 (生产)

#### Namespace
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: geo-platform
```

#### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: geo-config
  namespace: geo-platform
data:
  NEO4J_URI: "neo4j://neo4j-service:7687"
  POSTGRES_URL: "postgresql://geo-user@postgres-service:5432/geo"
  REDIS_URL: "redis://redis-service:6379"
  MINIO_ENDPOINT: "minio-service:9000"
```

#### Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: geo-secrets
  namespace: geo-platform
type: Opaque
stringData:
  NEO4J_PASSWORD: "your-password"
  POSTGRES_PASSWORD: "your-password"
  OPENAI_API_KEY: "your-api-key"
  ANTHROPIC_API_KEY: "your-api-key"
```

#### Deployment - API Gateway
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-gateway
  namespace: geo-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-gateway
  template:
    metadata:
      labels:
        app: api-gateway
    spec:
      containers:
      - name: api
        image: geo-platform/api-gateway:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: geo-config
        - secretRef:
            name: geo-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-gateway-service
  namespace: geo-platform
spec:
  selector:
    app: api-gateway
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

#### Ingress
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: geo-ingress
  namespace: geo-platform
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.geo-platform.com
    secretName: geo-tls
  rules:
  - host: api.geo-platform.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway-service
            port:
              number: 80
```

#### StatefulSet - Neo4j
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: neo4j
  namespace: geo-platform
spec:
  serviceName: neo4j
  replicas: 1
  selector:
    matchLabels:
      app: neo4j
  template:
    metadata:
      labels:
        app: neo4j
    spec:
      containers:
      - name: neo4j
        image: neo4j:5.14.0
        ports:
        - containerPort: 7474
          name: http
        - containerPort: 7687
          name: bolt
        env:
        - name: NEO4J_AUTH
          valueFrom:
            secretKeyRef:
              name: geo-secrets
              key: NEO4J_AUTH
        - name: NEO4J_PLUGINS
          value: '["apoc", "graph-data-science"]'
        volumeMounts:
        - name: neo4j-data
          mountPath: /data
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
  volumeClaimTemplates:
  - metadata:
      name: neo4j-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi
```

### CI/CD Pipeline (GitHub Actions)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker build -t geo-platform/api:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker push geo-platform/api:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          namespace: 'geo-platform'
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            geo-platform/api:${{ github.sha }}
```

---

## 安全与权限

### 认证方式

#### JWT Token认证
```python
# 登录获取Token
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "password"
}

# 响应
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600
}

# 使用Token
GET /api/v1/entities
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 权限模型

#### RBAC (基于角色的访问控制)

```python
class Role(Enum):
    ADMIN = "admin"              # 系统管理员
    CONTENT_MANAGER = "content_manager"  # 内容管理员
    ANALYST = "analyst"          # 数据分析师
    EDITOR = "editor"            # 编辑
    VIEWER = "viewer"            # 只读用户

class Permission(Enum):
    # 数据源
    DATA_SOURCE_CREATE = "data_source:create"
    DATA_SOURCE_READ = "data_source:read"
    DATA_SOURCE_UPDATE = "data_source:update"
    DATA_SOURCE_DELETE = "data_source:delete"
    DATA_SOURCE_RUN = "data_source:run"

    # 知识图谱
    GRAPH_READ = "graph:read"
    GRAPH_WRITE = "graph:write"
    GRAPH_DELETE = "graph:delete"

    # 内容生成
    CONTENT_CREATE = "content:create"
    CONTENT_EDIT = "content:edit"
    CONTENT_APPROVE = "content:approve"
    CONTENT_PUBLISH = "content:publish"

    # 系统管理
    SYSTEM_CONFIG = "system:config"
    USER_MANAGE = "user:manage"
    REPORT_VIEW = "report:view"

# 角色权限映射
ROLE_PERMISSIONS = {
    Role.ADMIN: [*Permission],  # 所有权限

    Role.CONTENT_MANAGER: [
        Permission.DATA_SOURCE_READ,
        Permission.DATA_SOURCE_RUN,
        Permission.GRAPH_READ,
        Permission.CONTENT_CREATE,
        Permission.CONTENT_EDIT,
        Permission.CONTENT_APPROVE,
        Permission.CONTENT_PUBLISH,
        Permission.REPORT_VIEW,
    ],

    Role.ANALYST: [
        Permission.DATA_SOURCE_READ,
        Permission.GRAPH_READ,
        Permission.REPORT_VIEW,
    ],

    Role.EDITOR: [
        Permission.GRAPH_READ,
        Permission.CONTENT_EDIT,
        Permission.REPORT_VIEW,
    ],

    Role.VIEWER: [
        Permission.GRAPH_READ,
        Permission.REPORT_VIEW,
    ],
}
```

#### 权限检查装饰器

```python
from functools import wraps
from fastapi import HTTPException, Depends

def require_permission(permission: Permission):
    """权限检查装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取当前用户
            current_user = kwargs.get('current_user')

            # 检查权限
            if not has_permission(current_user, permission):
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission denied: {permission.value}"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@router.post("/data-sources")
@require_permission(Permission.DATA_SOURCE_CREATE)
async def create_data_source(
    data: DataSourceInput,
    current_user: User = Depends(get_current_user)
):
    """创建数据源 - 需要DATA_SOURCE_CREATE权限"""
    return create_source(data)
```

### 数据安全

#### 敏感数据加密
```python
from cryptography.fernet import Fernet

class SecureConfig:
    """安全配置存储"""

    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY')
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """加密敏感数据"""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """解密敏感数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# API密钥存储
config = SecureConfig()
api_key_encrypted = config.encrypt("sk-...")
# 存储到数据库: api_key_encrypted

# 使用时解密
api_key = config.decrypt(api_key_encrypted)
```

#### 审计日志
```python
class AuditLog:
    """审计日志"""

    @staticmethod
    async def log_action(
        user_id: UUID,
        action: str,
        resource_type: str,
        resource_id: UUID,
        details: Dict[str, Any] = None
    ):
        """记录用户操作"""
        await mongodb.audit_logs.insert_one({
            "user_id": str(user_id),
            "action": action,
            "resource_type": resource_type,
            "resource_id": str(resource_id),
            "details": details,
            "timestamp": datetime.utcnow(),
            "ip_address": request.client.host,
            "user_agent": request.headers.get("user-agent")
        })

# 使用示例
@router.delete("/entities/{entity_id}")
async def delete_entity(
    entity_id: UUID,
    current_user: User = Depends(get_current_user)
):
    # 删除实体
    entity = await get_entity(entity_id)
    await delete_entity_from_graph(entity_id)

    # 记录审计日志
    await AuditLog.log_action(
        user_id=current_user.id,
        action="DELETE",
        resource_type="Entity",
        resource_id=entity_id,
        details={"entity_name": entity.name}
    )

    return {"message": "Entity deleted"}
```

---

## 监控与运维

### Prometheus指标

```python
from prometheus_client import Counter, Histogram, Gauge

# 请求计数
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# 请求延迟
request_latency = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# 系统指标
graph_nodes = Gauge(
    'neo4j_nodes_total',
    'Total nodes in Neo4j'
)

graph_relationships = Gauge(
    'neo4j_relationships_total',
    'Total relationships in Neo4j'
)

content_pipeline_queue = Gauge(
    'content_pipeline_queue_size',
    'Content pipeline queue size',
    ['stage']
)

# 业务指标
gaps_identified = Counter(
    'structure_holes_identified_total',
    'Total structure holes identified'
)

prompts_generated = Counter(
    'prompts_generated_total',
    'Total prompts generated'
)

assets_published = Counter(
    'assets_published_total',
    'Total assets published'
)

# 中间件记录指标
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    # 记录请求
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    # 记录延迟
    request_latency.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(time.time() - start_time)

    return response
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "GEO Platform Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time (p95)",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Knowledge Graph Size",
        "type": "stat",
        "targets": [
          {
            "expr": "neo4j_nodes_total"
          }
        ]
      },
      {
        "title": "Content Pipeline Queue",
        "type": "graph",
        "targets": [
          {
            "expr": "content_pipeline_queue_size",
            "legendFormat": "{{stage}}"
          }
        ]
      }
    ]
  }
}
```

### 告警规则

```yaml
groups:
  - name: geo_platform_alerts
    interval: 30s
    rules:
      # 系统健康告警
      - alert: SystemHealthLow
        expr: system_health_score < 70
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "System health below threshold"
          description: "Health score is {{ $value }}%"

      # API响应时间告警
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "API response time high"
          description: "P95 latency is {{ $value }}s"

      # Neo4j连接告警
      - alert: Neo4jDown
        expr: neo4j_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Neo4j is down"
          description: "Cannot connect to Neo4j database"

      # 队列积压告警
      - alert: QueueBacklog
        expr: content_pipeline_queue_size > 100
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Content pipeline queue backlog"
          description: "Queue size is {{ $value }}"
```

---

## 扩展性设计

### 水平扩展

#### 无状态服务扩展
```yaml
# API Gateway - 根据CPU/内存自动扩展
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-gateway-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

#### Celery Worker扩展
```yaml
# Celery Worker - 根据队列长度扩展
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: celery-worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: celery-worker
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: External
    external:
      metric:
        name: redis_queue_length
      target:
        type: AverageValue
        averageValue: "30"
```

### 插件系统

```python
class PluginInterface:
    """插件接口"""

    def on_data_imported(self, data: Dict[str, Any]):
        """数据导入后钩子"""
        pass

    def on_gap_identified(self, gap: Gap):
        """结构洞识别后钩子"""
        pass

    def on_content_generated(self, asset: Asset):
        """内容生成后钩子"""
        pass

    def on_asset_published(self, asset: Asset):
        """内容发布后钩子"""
        pass

# 插件示例: Slack通知插件
class SlackNotificationPlugin(PluginInterface):
    """Slack通知插件"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def on_gap_identified(self, gap: Gap):
        """发送Slack通知"""
        message = f"""
        🔍 New Content Opportunity Identified!

        Clusters: {gap.cluster_a} ↔ {gap.cluster_b}
        Score: {gap.opportunity_score:.3f}
        Keywords: {', '.join(gap.keywords_a[:3])} | {', '.join(gap.keywords_b[:3])}
        """
        send_slack_message(self.webhook_url, message)

    def on_asset_published(self, asset: Asset):
        """发送发布通知"""
        message = f"""
        ✅ Content Published!

        Title: {asset.title}
        Type: {asset.asset_type}
        Citation Score: {asset.citation_score:.2f}
        URL: {asset.published_url}
        """
        send_slack_message(self.webhook_url, message)

# 插件注册
plugin_manager = PluginManager()
plugin_manager.register(SlackNotificationPlugin(
    webhook_url="https://hooks.slack.com/services/..."
))
```

### 多租户支持

```python
class Tenant:
    """租户模型"""
    id: UUID
    name: str
    slug: str
    plan: str  # free, pro, enterprise
    limits: TenantLimits
    settings: Dict[str, Any]

class TenantLimits:
    """租户限制"""
    max_nodes: int = 10000
    max_api_calls_per_day: int = 1000
    max_users: int = 5
    max_data_sources: int = 10

# 租户上下文
class TenantContext:
    """租户上下文管理"""

    @staticmethod
    async def get_current_tenant(
        request: Request
    ) -> Tenant:
        """从请求中获取租户"""
        tenant_slug = request.headers.get('X-Tenant-ID')
        return await get_tenant_by_slug(tenant_slug)

    @staticmethod
    async def check_limit(
        tenant: Tenant,
        resource: str,
        current_usage: int
    ) -> bool:
        """检查租户限制"""
        limit = getattr(tenant.limits, f"max_{resource}")
        return current_usage < limit

# Neo4j多租户隔离
def get_tenant_label(tenant_id: UUID) -> str:
    """获取租户标签"""
    return f"Tenant_{tenant_id.hex}"

# 查询时添加租户过滤
query = f"""
MATCH (n:{get_tenant_label(tenant_id)})
WHERE n.name CONTAINS $keyword
RETURN n
"""
```

---

## 总结

这套GEO系统设计方案提供了：

### ✅ 完整的技术架构
- 微服务架构，易于扩展
- 现代化技术栈
- 完善的数据流设计

### ✅ 核心功能模块
- 多源数据采集
- 知识图谱构建
- Graph-RAG问答
- 智能内容生成
- 实时监控报告

### ✅ 生产级别特性
- 安全认证授权
- 性能监控告警
- 水平扩展能力
- 多租户支持
- 插件系统

### ✅ 自动化工作流
- n8n可视化编排
- Celery定时任务
- CI/CD流水线

### 📊 预期效果
- **内容生产效率**: 提升 300%
- **内容质量**: Citation Score > 0.7
- **系统可用性**: > 99.9%
- **响应时间**: P95 < 200ms

### 🚀 下一步
1. 根据实际需求调整架构
2. 分阶段实施开发
3. 持续优化和迭代
4. 收集用户反馈改进

---

*文档版本: 1.0*
*最后更新: 2025-10-16*

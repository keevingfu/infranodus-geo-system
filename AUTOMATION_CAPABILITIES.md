# 全局自动化开发能力清单

**文档版本**: 1.0
**创建时间**: 2025-10-16
**适用环境**: macOS with Claude Code + MCP Servers

---

## 📋 目录

1. [资源概览](#资源概览)
2. [MCP服务器详解](#mcp服务器详解)
3. [自动化开发场景](#自动化开发场景)
4. [实战示例](#实战示例)
5. [最佳实践](#最佳实践)

---

## 资源概览

### 🎯 总览统计

**已配置资源总数**: 21个MCP服务器 + 5个Docker数据库

**能力分类**:
- 🧠 AI能力: 2个（思维链、记忆）
- 🌐 Web能力: 4个（浏览器、抓取、Chrome工具）
- 💾 数据库: 7个（Neo4j、PostgreSQL、MongoDB、Redis、SQLite、Prisma）
- 🎨 前端: 2个（Magic UI、文件系统）
- 🔧 开发: 4个（GitHub、GitLab、n8n、Prisma）
- 📊 协作: 3个（Notion、Slack、Feishu）
- 🔍 监控: 2个（Sentry、Computer Use）
- 📦 存储: 1个（MinIO）

### 🚀 核心优势

1. **端到端自动化** - 从数据采集到内容发布
2. **多数据库支持** - 关系型、文档、图、缓存、对象存储
3. **AI增强开发** - 思维链推理、知识图谱记忆
4. **完整工具链** - 浏览器自动化、API集成、文件操作
5. **团队协作** - 通知、文档、项目管理集成

---

## MCP服务器详解

### 🧠 AI与问题解决

#### 1. Sequential Thinking (思维链推理)

**能力**:
- 结构化问题分解
- 动态推理和迭代
- 假设验证
- 分支思考

**适用场景**:
```python
# 场景1: 复杂架构设计
问题: "如何设计一个高并发的内容生成系统？"
思维链推理:
1. 分析并发需求（QPS、用户量）
2. 评估技术方案（消息队列、微服务）
3. 考虑瓶颈点（数据库、LLM API）
4. 设计扩展方案（水平扩展、缓存策略）
5. 验证可行性
6. 生成最终方案

# 场景2: Bug诊断
问题: "系统性能突然下降50%"
思维链推理:
1. 收集症状（响应时间、错误日志）
2. 假设可能原因（数据库慢查询、内存泄漏、网络问题）
3. 逐一验证假设
4. 定位根本原因
5. 提出解决方案
```

**自动化开发用法**:
```bash
# 使用Sequential Thinking分析复杂问题
# Claude会自动使用mcp__sequential-thinking__sequentialthinking工具

用户: "设计一个可扩展的知识图谱查询系统"
Claude:
  - 使用思维链分解问题
  - 评估多种方案
  - 生成详细设计
  - 验证可行性
```

#### 2. Memory (知识图谱记忆)

**能力**:
- 持久化知识存储
- 实体和关系管理
- 跨会话记忆
- 知识检索

**数据模型**:
```typescript
// 实体（Entity）
interface Entity {
  name: string;
  entityType: string;  // 类型（Person, Project, Concept等）
  observations: string[];  // 观察记录
}

// 关系（Relation）
interface Relation {
  from: string;  // 实体名称
  to: string;    // 实体名称
  relationType: string;  // 关系类型（uses, implements, depends_on等）
}

// 观察（Observation）
interface Observation {
  entityName: string;
  contents: string[];  // 观察内容
}
```

**适用场景**:
```python
# 场景1: 项目上下文记忆
# 记录项目信息
create_entities([
  {
    "name": "GEO Platform",
    "entityType": "Project",
    "observations": [
      "使用Neo4j作为知识图谱数据库",
      "后端框架是FastAPI",
      "支持Graph-RAG问答"
    ]
  }
])

# 创建关系
create_relations([
  {
    "from": "GEO Platform",
    "to": "Neo4j",
    "relationType": "uses"
  }
])

# 场景2: 技术决策记录
# 记录决策
add_observations({
  "entityName": "GEO Platform",
  "contents": [
    "2025-10-16: 选择Cytoscape.js用于图可视化",
    "原因: 性能好，支持大规模图渲染"
  ]
})

# 场景3: 跨会话查询
# 搜索相关知识
search_nodes("Neo4j")
# 返回: GEO Platform项目的所有Neo4j相关信息
```

**自动化开发用法**:
```bash
# Claude自动使用Memory记录项目信息
# 下次对话时可以直接访问这些信息

Session 1:
用户: "我们的项目使用Neo4j 5.14.0"
Claude: [自动创建实体和观察记录]

Session 2 (数天后):
用户: "我们项目用的是哪个版本的Neo4j？"
Claude: [从Memory检索] "您的项目使用Neo4j 5.14.0"
```

---

### 🌐 Web与浏览器自动化

#### 3. Puppeteer (浏览器自动化)

**能力**:
- 页面导航和渲染
- 元素交互（点击、输入、选择）
- 截图和PDF生成
- JavaScript执行
- Cookie和Session管理

**API方法**:
```typescript
// 导航到URL
puppeteer_navigate({
  url: "https://example.com",
  launchOptions: { headless: true }
})

// 截图
puppeteer_screenshot({
  name: "homepage",
  width: 1920,
  height: 1080,
  selector: "#main-content"  // 可选，截取特定元素
})

// 点击元素
puppeteer_click({
  selector: "button.submit"
})

// 填写表单
puppeteer_fill({
  selector: "input[name='email']",
  value: "user@example.com"
})

// 执行JavaScript
puppeteer_evaluate({
  script: `
    document.querySelector('.notification').remove();
    return document.title;
  `
})
```

**自动化场景**:
```python
# 场景1: 自动化测试
"""
完整E2E测试流程：
1. 打开应用
2. 登录
3. 创建数据源
4. 查看图谱
5. 验证结果
6. 截图保存
"""

# 场景2: 竞品监控
"""
每日自动化流程：
1. 访问竞品网站
2. 抓取产品信息
3. 截图对比
4. 保存到数据库
"""

# 场景3: 可视化演示生成
"""
自动生成产品演示：
1. 打开各个功能页面
2. 执行关键操作
3. 捕获每一步截图
4. 生成演示文档
"""
```

#### 4. Firecrawl (Self-Hosted Web数据提取)

**能力**:
- 智能网页抓取
- Markdown/HTML提取
- 批量URL处理
- 网站地图生成
- 搜索引擎集成

**部署信息**:
- **位置**: Docker Desktop
- **API端点**: http://localhost:3002
- **管理界面**: http://localhost:3002/admin/@/queues
- **特点**: 本地部署，无使用限制

**API方法**:
```typescript
// 单页抓取
firecrawl_scrape({
  url: "https://example.com/article",
  formats: ["markdown", "html"],
  onlyMainContent: true
})

// 批量抓取
firecrawl_batch_scrape({
  urls: [
    "https://example.com/page1",
    "https://example.com/page2"
  ]
})

// 网站搜索
firecrawl_search({
  query: "best mattress reviews",
  limit: 10,
  sources: ["web"]
})

// 网站地图
firecrawl_map({
  url: "https://example.com",
  includeSubdomains: false
})

// 智能抽取
firecrawl_extract({
  urls: ["https://example.com/products"],
  schema: {
    type: "object",
    properties: {
      name: { type: "string" },
      price: { type: "number" },
      rating: { type: "number" }
    }
  }
})
```

**自动化场景**:
```python
# 场景1: 竞品数据采集
workflow = {
  "name": "Daily Competitor Analysis",
  "steps": [
    {
      "action": "firecrawl_search",
      "query": "memory foam mattress reviews 2025",
      "limit": 20
    },
    {
      "action": "firecrawl_batch_scrape",
      "urls": "[从搜索结果获取]"
    },
    {
      "action": "save_to_database",
      "target": "mongodb.competitor_data"
    }
  ]
}

# 场景2: 内容监控
"""
监控目标网站更新：
1. 使用firecrawl_map获取网站结构
2. 定期抓取关键页面
3. 对比内容变化
4. 发送通知
"""

# 场景3: 数据导入GEO系统
"""
自动化数据流：
1. firecrawl_scrape抓取原始内容
2. 清洗和格式化
3. InfraNodus分析
4. Neo4j导入
"""
```

#### 5. Chrome DevTools MCP

**能力**:
- 网络请求监控
- 性能分析
- Console日志捕获
- DOM检查
- JavaScript调试

**使用场景**:
```python
# 场景1: 性能分析
"""
分析页面加载性能：
1. 打开页面
2. 捕获性能指标
3. 识别瓶颈
4. 生成优化建议
"""

# 场景2: API调用分析
"""
监控API请求：
1. 记录所有网络请求
2. 分析请求时间
3. 检查响应数据
4. 优化API调用
"""
```

---

### 💾 数据库服务器

#### 6. Neo4j (图数据库)

**部署信息**:
- **容器**: neo4j-claude-mcp
- **端口**: Bolt: 7688, HTTP: 7475
- **凭证**: neo4j / claude_neo4j_2025
- **浏览器**: http://localhost:7475

**能力**:
```typescript
// 执行Cypher查询
execute_query({
  query: `
    MATCH (k:Keyword)-[:CO_OCCURS_WITH]->(k2:Keyword)
    WHERE k.name = $keyword
    RETURN k2.name AS related, count(*) AS frequency
    ORDER BY frequency DESC
    LIMIT 10
  `,
  params: { keyword: "cooling_gel" }
})

// 创建节点
create_node({
  label: "Keyword",
  properties: {
    name: "memory_foam",
    frequency: 142,
    betweenness: 0.85
  }
})

// 创建关系
create_relationship({
  fromNodeId: 123,
  toNodeId: 456,
  type: "CO_OCCURS_WITH",
  properties: { weight: 0.75 }
})
```

**自动化场景**:
```python
# 场景1: 自动化图谱构建
"""
数据导入流程：
1. 从Firecrawl获取文本
2. InfraNodus分析生成共现网络
3. Neo4j批量导入节点和关系
4. 创建索引和约束
5. 运行图算法（PageRank、社区发现）
"""

# 场景2: 实时查询API
"""
Graph-RAG问答系统：
1. 接收用户问题
2. Neo4j检索相关子图
3. 组装上下文
4. LLM生成答案
5. 追踪引用来源
"""

# 场景3: 定时分析任务
"""
每日结构洞分析：
1. Celery定时触发
2. Neo4j执行结构洞检测算法
3. 识别内容机会
4. 生成提示词
5. Slack通知团队
"""
```

#### 7. PostgreSQL (关系数据库)

**部署信息**:
- **容器**: postgres-claude-mcp
- **端口**: 5437
- **凭证**: claude / claude_dev_2025
- **数据库**: claude_dev

**能力**:
- CRUD操作
- 复杂查询（JOIN、子查询）
- 事务管理
- 全文搜索
- JSON字段支持

**Schema设计示例**:
```sql
-- 用户表
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 数据源表
CREATE TABLE data_sources (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,  -- WEB, API, FILE
  config JSONB,
  schedule VARCHAR(100),
  last_run TIMESTAMP,
  status VARCHAR(50)
);

-- 导入任务表
CREATE TABLE imports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id UUID REFERENCES data_sources(id),
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  records_processed INTEGER,
  records_imported INTEGER,
  status VARCHAR(50),
  errors JSONB
);
```

**自动化场景**:
```python
# 场景1: 用户管理系统
"""
完整用户生命周期：
1. 注册 → INSERT INTO users
2. 登录验证 → SELECT + password验证
3. 权限检查 → JOIN users + roles
4. 审计日志 → INSERT INTO audit_logs
"""

# 场景2: 数据源调度
"""
自动化调度系统：
1. Celery Beat查询待执行的数据源
2. 创建导入任务记录
3. 执行抓取
4. 更新任务状态
5. 记录统计信息
"""
```

#### 8. MongoDB (文档数据库)

**部署信息**:
- **容器**: mongodb-claude-mcp
- **端口**: 27018
- **凭证**: claude / claude_mongo_2025
- **数据库**: claude_dev

**能力**:
```typescript
// 插入文档
insert_many({
  database: "claude_dev",
  collection: "audit_logs",
  documents: [
    {
      user_id: "123",
      action: "DELETE",
      resource: "Entity",
      timestamp: new Date()
    }
  ]
})

// 查询
find({
  database: "claude_dev",
  collection: "audit_logs",
  filter: { user_id: "123" },
  sort: { timestamp: -1 },
  limit: 10
})

// 聚合
aggregate({
  database: "claude_dev",
  collection: "audit_logs",
  pipeline: [
    { $match: { action: "DELETE" } },
    { $group: { _id: "$user_id", count: { $sum: 1 } } },
    { $sort: { count: -1 } }
  ]
})
```

**自动化场景**:
```python
# 场景1: 审计日志系统
"""
完整审计追踪：
1. API中间件拦截所有请求
2. 记录操作详情到MongoDB
3. 定期聚合分析
4. 生成安全报告
"""

# 场景2: 分析数据存储
"""
网站分析流程：
1. 用户行为事件 → MongoDB
2. 实时聚合统计
3. Dashboard展示
4. 定期归档到PostgreSQL
"""

# 场景3: 日志收集
"""
集中式日志管理：
1. 所有服务日志 → MongoDB
2. 结构化存储
3. 全文搜索
4. 告警规则
"""
```

#### 9. Redis (缓存和队列)

**部署信息**:
- **容器**: redis-claude-mcp
- **端口**: 6382
- **密码**: claude_redis_2025

**能力**:
```typescript
// 设置键值
set({
  key: "user:123:profile",
  value: JSON.stringify({ name: "Alice", role: "admin" }),
  expireSeconds: 3600  // 1小时过期
})

// 获取值
get({
  key: "user:123:profile"
})

// 删除
delete({
  key: "user:123:profile"
})

// 列表操作
list({
  pattern: "user:*"  // 列出所有用户相关的键
})
```

**自动化场景**:
```python
# 场景1: API响应缓存
"""
缓存策略：
1. 请求到达 → 检查Redis
2. 缓存命中 → 直接返回
3. 缓存未命中 → 查询数据库
4. 结果写入Redis（带过期时间）
5. 返回响应
"""

# 场景2: Celery任务队列
"""
异步任务处理：
1. API接收请求 → 任务入队Redis
2. Celery Worker从队列取任务
3. 执行任务（数据采集、分析等）
4. 结果写回Redis
5. 前端轮询或WebSocket推送结果
"""

# 场景3: 会话管理
"""
用户会话存储：
1. 用户登录 → JWT Token
2. Token详情存储Redis
3. 每次请求验证Token
4. Token过期自动清理
"""

# 场景4: 速率限制
"""
API限流：
1. 识别用户（IP/User ID）
2. Redis计数器 + 过期时间
3. 超过限制 → 拒绝请求
4. 定期重置计数
"""
```

#### 10. SQLite Explorer (轻量级数据库)

**部署信息**:
- **位置**: /Users/cavin/sqlite-explorer-fastmcp-mcp-server/
- **数据库**: /Users/cavin/test.db
- **特点**: 只读访问，安全探索

**使用场景**:
```python
# 场景1: 本地开发数据库
"""
轻量级开发环境：
1. 快速原型开发
2. 测试数据验证
3. 本地数据分析
"""

# 场景2: 配置文件存储
"""
应用配置管理：
1. 结构化配置存储
2. 版本控制友好
3. SQL查询配置
"""
```

#### 11. Prisma (现代ORM)

**能力**:
- 类型安全的数据库操作
- 自动迁移管理
- 数据库模式可视化
- 多数据库支持

**Schema示例**:
```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  role      Role     @default(VIEWER)
  createdAt DateTime @default(now())

  dataSources DataSource[]
}

model DataSource {
  id        String   @id @default(uuid())
  name      String
  type      SourceType
  config    Json
  userId    String
  user      User     @relation(fields: [userId], references: [id])

  imports   Import[]
}

enum Role {
  ADMIN
  CONTENT_MANAGER
  ANALYST
  EDITOR
  VIEWER
}

enum SourceType {
  WEB
  API
  FILE
  DATABASE
}
```

**自动化场景**:
```python
# 场景1: 数据库迁移自动化
"""
Schema演化流程：
1. 修改schema.prisma
2. 运行prisma migrate dev
3. 生成迁移文件
4. 应用到数据库
5. 更新Prisma Client
"""

# 场景2: 类型安全的CRUD
"""
类型安全开发：
1. Prisma生成TypeScript类型
2. 自动完成和类型检查
3. 运行时类型验证
4. 减少运行时错误
"""
```

---

### 🎨 前端与UI

#### 12. Magic UI (AI驱动的UI组件)

**能力**:
- 自动生成React组件
- 响应式设计
- 动画和过渡效果
- 主题定制

**组件类别**:
```typescript
// 1. 基础组件
getComponents()
// 返回: marquee, terminal, hero-video-dialog, bento-grid,
//       animated-list, dock, globe, tweet-card, etc.

// 2. 设备模拟
getDeviceMocks()
// 返回: safari, iphone-15-pro, android

// 3. 特效组件
getSpecialEffects()
// 返回: animated-beam, border-beam, shine-border,
//       magic-card, meteors, particles, cool-mode

// 4. 文本动画
getTextAnimations()
// 返回: text-animate, aurora-text, number-ticker,
//       animated-shiny-text, word-rotate, typing-animation

// 5. 按钮组件
getButtons()
// 返回: rainbow-button, shimmer-button, shiny-button,
//       interactive-hover-button, pulsating-button

// 6. 背景组件
getBackgrounds()
// 返回: warp-background, flickering-grid, animated-grid-pattern,
//       retro-grid, ripple, dot-pattern
```

**自动化场景**:
```python
# 场景1: 快速原型开发
"""
UI快速迭代：
1. 描述UI需求
2. Magic UI生成组件代码
3. 集成到项目
4. 预览和调整
"""

# 场景2: 营销页面生成
"""
自动化页面创建：
1. 输入产品信息
2. 选择模板和组件
3. Magic UI组装页面
4. 导出代码
"""

# 场景3: 设计系统构建
"""
一致性UI组件库：
1. 定义设计规范
2. Magic UI生成组件
3. 文档自动生成
4. Storybook集成
"""
```

#### 13. Filesystem (高级文件操作)

**能力**:
- 读写文件
- 目录操作
- 文件搜索
- 批量操作
- 权限管理

**API方法**:
```typescript
// 读取文件
read_text_file({
  path: "/path/to/file.txt",
  head: 100  // 只读前100行
})

// 批量读取
read_multiple_files({
  paths: ["/path/file1.txt", "/path/file2.txt"]
})

// 写入文件
write_file({
  path: "/path/to/output.txt",
  content: "Hello, World!"
})

// 编辑文件
edit_file({
  path: "/path/to/file.txt",
  edits: [
    {
      oldText: "old value",
      newText: "new value"
    }
  ]
})

// 搜索文件
search_files({
  path: "/project",
  pattern: "*.ts",
  excludePatterns: ["node_modules", "dist"]
})

// 目录树
directory_tree({
  path: "/project"
})
```

**自动化场景**:
```python
# 场景1: 代码生成自动化
"""
批量生成代码文件：
1. 读取模板文件
2. 替换变量
3. 批量写入文件
4. 创建目录结构
"""

# 场景2: 配置文件管理
"""
多环境配置：
1. 读取基础配置
2. 根据环境变量调整
3. 写入特定环境配置
4. 验证配置正确性
"""

# 场景3: 文档自动生成
"""
API文档生成：
1. 扫描源代码
2. 提取注释和类型
3. 生成Markdown文档
4. 更新README
"""
```

---

### 🔧 版本控制与DevOps

#### 14. GitHub (代码托管)

**能力**:
```typescript
// 仓库操作
create_repository({
  name: "geo-platform",
  description: "GEO Knowledge Graph System",
  private: true,
  autoInit: true
})

fork_repository({
  owner: "original-owner",
  repo: "project",
  organization: "my-org"  // 可选
})

// 文件操作
get_file_contents({
  owner: "my-org",
  repo: "geo-platform",
  path: "src/main.py",
  branch: "develop"
})

create_or_update_file({
  owner: "my-org",
  repo: "geo-platform",
  path: "docs/API.md",
  content: "# API Documentation",
  message: "Update API docs",
  branch: "develop"
})

push_files({
  owner: "my-org",
  repo: "geo-platform",
  branch: "develop",
  files: [
    { path: "file1.py", content: "..." },
    { path: "file2.py", content: "..." }
  ],
  message: "Add new features"
})

// Issue管理
create_issue({
  owner: "my-org",
  repo: "geo-platform",
  title: "Add Graph-RAG support",
  body: "Implement Graph-RAG question answering",
  labels: ["enhancement", "high-priority"],
  assignees: ["developer1"]
})

list_issues({
  owner: "my-org",
  repo: "geo-platform",
  state: "open",
  labels: ["bug"]
})

// Pull Request
create_pull_request({
  owner: "my-org",
  repo: "geo-platform",
  title: "Feature: Graph-RAG implementation",
  head: "feature/graph-rag",
  base: "develop",
  body: "Implements Graph-RAG with Neo4j integration"
})

merge_pull_request({
  owner: "my-org",
  repo: "geo-platform",
  pull_number: 42,
  merge_method: "squash"
})

// 代码搜索
search_code({
  q: "def find_structure_holes repo:my-org/geo-platform"
})
```

**自动化场景**:
```python
# 场景1: 自动化发布流程
"""
Release Automation:
1. 检测版本号变更
2. 创建release分支
3. 更新CHANGELOG
4. 推送代码
5. 创建GitHub Release
6. 触发CI/CD部署
"""

# 场景2: Issue自动化管理
"""
Issue Triage Bot:
1. 监听新Issue
2. 分析内容（使用LLM）
3. 自动打标签
4. 分配给合适的开发者
5. 添加模板回复
"""

# 场景3: PR Review助手
"""
Automated Code Review:
1. 检测新PR
2. 获取改动的文件
3. 使用LLM分析代码
4. 提出改进建议
5. 自动评论到PR
"""

# 场景4: 文档同步
"""
Docs Sync:
1. 监听代码变更
2. 提取API变更
3. 自动更新文档
4. 提交PR到docs仓库
"""
```

#### 15. GitLab (替代方案)

**能力**: 与GitHub类似，支持：
- 仓库管理
- CI/CD Pipeline
- Issue和MR管理
- Wiki管理

**GitLab特色**:
```python
# GitLab CI/CD集成
"""
.gitlab-ci.yml自动生成：
1. 分析项目类型
2. 生成CI配置
3. 推送到仓库
4. Pipeline自动运行
"""
```

#### 16. n8n (工作流自动化)

**能力**:
- 可视化工作流编排
- 300+ 集成节点
- Webhook触发
- 定时任务
- 条件分支
- 循环和迭代

**API方法**:
```typescript
// 列出工作流
list_workflows({
  active: true
})

// 获取工作流
get_workflow({
  workflowId: "123"
})

// 创建工作流
create_workflow({
  name: "Daily Data Sync",
  nodes: [
    {
      type: "n8n-nodes-base.cron",
      parameters: { rule: "0 2 * * *" }
    },
    {
      type: "n8n-nodes-base.httpRequest",
      parameters: {
        url: "https://api.example.com/data",
        method: "GET"
      }
    }
  ],
  connections: { ... }
})

// 触发工作流
run_webhook({
  workflowName: "process-data",
  data: { input: "value" }
})
```

**自动化场景**:
```python
# 场景1: 数据同步自动化
"""
Multi-Source Data Sync:
n8n Workflow:
  ├─ Trigger: Cron (每天2AM)
  ├─ HTTP Request: 抓取竞品数据
  ├─ Code: 数据清洗
  ├─ MongoDB: 保存原始数据
  ├─ HTTP Request: 调用InfraNodus API
  ├─ Neo4j: 导入图数据
  └─ Slack: 发送完成通知
"""

# 场景2: 内容发布流水线
"""
Content Publishing Pipeline:
n8n Workflow:
  ├─ Webhook: 接收新内容
  ├─ IF: 检查Citation Score > 0.7
  │   ├─ Yes:
  │   │   ├─ WordPress: 发布文章
  │   │   ├─ Twitter: 发推文
  │   │   ├─ LinkedIn: 发帖
  │   │   └─ Slack: 成功通知
  │   └─ No:
  │       └─ Slack: 请求人工审核
"""

# 场景3: 监控告警系统
"""
Monitoring and Alerting:
n8n Workflow:
  ├─ Trigger: Cron (每5分钟)
  ├─ HTTP Request: 健康检查API
  ├─ Code: 分析响应
  ├─ IF: 检测异常
  │   ├─ PagerDuty: 创建事件
  │   ├─ Slack: 发送告警
  │   └─ Email: 通知运维团队
  └─ MongoDB: 记录检查结果
"""
```

---

### 📊 协作与通知

#### 17. Notion (知识库)

**能力**:
```typescript
// 查询数据库
post_database_query({
  database_id: "abc123",
  filter: {
    property: "Status",
    select: { equals: "In Progress" }
  },
  sorts: [
    { property: "Priority", direction: "descending" }
  ]
})

// 创建页面
post_page({
  parent: { page_id: "parent-page-id" },
  properties: {
    title: [
      {
        text: { content: "New Task" }
      }
    ]
  }
})

// 更新页面
patch_page({
  page_id: "page-123",
  properties: {
    Status: { select: { name: "Completed" } }
  }
})

// 添加内容块
patch_block_children({
  block_id: "page-123",
  children: [
    {
      type: "paragraph",
      paragraph: {
        rich_text: [
          { text: { content: "This is a paragraph" } }
        ]
      }
    }
  ]
})
```

**自动化场景**:
```python
# 场景1: 项目文档自动化
"""
Documentation Sync:
1. 代码注释提取
2. 生成API文档
3. 同步到Notion
4. 更新目录结构
"""

# 场景2: 任务管理集成
"""
Task Tracking:
1. GitHub Issue创建 → Notion Task
2. PR合并 → 更新Task状态
3. 每日同步进度
4. 生成周报
"""

# 场景3: 知识库构建
"""
Knowledge Base:
1. 收集技术文档
2. 整理分类
3. 创建Notion页面
4. 添加标签和关联
"""
```

#### 18. Slack (团队通信)

**能力**:
- 发送消息
- 创建频道
- 文件上传
- 交互式消息（按钮、菜单）
- Bot集成

**自动化场景**:
```python
# 场景1: 实时通知系统
"""
Event Notifications:
- 数据导入完成 → #data-team
- 结构洞发现 → #content-team
- 系统告警 → #ops-team
- PR需要Review → #dev-team
"""

# 场景2: ChatOps
"""
Slack Bot Commands:
/deploy production → 触发部署
/status → 查看系统状态
/analyze gap-123 → 分析特定结构洞
/generate prompt-456 → 生成内容
"""

# 场景3: 审批流程
"""
Approval Workflow:
1. 内容生成完成
2. Slack发送预览和按钮
3. 审批人点击批准/拒绝
4. 触发对应操作
5. 结果通知
"""
```

#### 19. Feishu/飞书 (企业协作)

**能力**:
```typescript
// 文档操作
create_feishu_document({
  title: "GEO系统周报",
  folderToken: "folder-token"
})

get_feishu_document_blocks({
  documentId: "doc-id"
})

batch_create_feishu_blocks({
  documentId: "doc-id",
  parentBlockId: "block-id",
  index: 0,
  blocks: [
    {
      blockType: "heading1",
      options: {
        heading: {
          level: 1,
          content: "系统状态"
        }
      }
    },
    {
      blockType: "text",
      options: {
        text: {
          textStyles: [
            { text: "健康分数: ", style: { bold: true } },
            { text: "80%", style: { text_color: 5 } }
          ]
        }
      }
    }
  ]
})

// 表格创建
create_feishu_table({
  documentId: "doc-id",
  parentBlockId: "block-id",
  index: 0,
  tableConfig: {
    columnSize: 3,
    rowSize: 5,
    cells: [
      {
        coordinate: { row: 0, column: 0 },
        content: {
          blockType: "text",
          options: { text: { textStyles: [{ text: "指标" }] } }
        }
      }
    ]
  }
})

// 图表创建（Mermaid）
batch_create_feishu_blocks({
  blocks: [
    {
      blockType: "mermaid",
      options: {
        mermaid: {
          code: `
            graph TD
            A[数据采集] --> B[分析]
            B --> C[内容生成]
          `
        }
      }
    }
  ]
})
```

**自动化场景**:
```python
# 场景1: 自动化报告生成
"""
Weekly Report to Feishu:
1. 收集系统数据
2. 生成统计分析
3. 创建飞书文档
4. 添加表格和图表
5. @相关人员
"""

# 场景2: 项目文档管理
"""
Documentation System:
1. 代码变更 → 文档更新
2. API变更 → 飞书文档同步
3. 架构图 → Mermaid渲染
4. 版本历史 → 文档归档
"""

# 场景3: 协作工作流
"""
Collaborative Review:
1. 内容生成完成
2. 创建飞书文档
3. 分享给团队
4. 收集评论
5. 版本迭代
"""
```

---

### 🔍 监控与调试

#### 20. Sentry (错误追踪)

**能力**:
```typescript
// 搜索组织
find_organizations({
  query: "my-company"
})

// 搜索项目
find_projects({
  organizationSlug: "my-company",
  query: "geo-platform"
})

// 获取Issue详情
get_issue_details({
  organizationSlug: "my-company",
  issueId: "GEO-PLATFORM-123"
})

// 搜索Issues
search_issues({
  organizationSlug: "my-company",
  naturalLanguageQuery: "unhandled errors in last 24 hours"
})

// 搜索Events
search_events({
  organizationSlug: "my-company",
  naturalLanguageQuery: "how many 500 errors today"
})

// AI分析Issue
analyze_issue_with_seer({
  issueUrl: "https://sentry.io/issues/123",
  instruction: "找出根本原因并提供修复建议"
})
```

**自动化场景**:
```python
# 场景1: 智能错误诊断
"""
Error Analysis Pipeline:
1. Sentry检测到新错误
2. analyze_issue_with_seer分析
3. 生成修复建议
4. 创建GitHub Issue
5. 分配给相关开发者
"""

# 场景2: 错误趋势分析
"""
Error Trend Monitoring:
1. search_events查询错误统计
2. 对比历史数据
3. 识别异常趋势
4. Slack告警通知
5. 生成分析报告
"""

# 场景3: Release Health监控
"""
Release Monitoring:
1. 新版本部署
2. Sentry监控错误率
3. 对比上一版本
4. 如果错误率上升>20%
5. 自动回滚或告警
"""
```

#### 21. Computer Use (系统自动化)

**能力**:
- 屏幕截图
- 鼠标/键盘控制
- 应用程序启动
- 文件管理

**使用场景**:
```python
# 场景1: 应用测试自动化
"""
Desktop App Testing:
1. 启动应用
2. 模拟用户操作
3. 验证界面状态
4. 截图记录
5. 生成测试报告
"""

# 场景2: 多应用协作
"""
Cross-App Workflow:
1. 从Excel读取数据
2. 打开浏览器
3. 登录系统
4. 批量操作
5. 结果保存
"""
```

---

### 📦 对象存储

#### 22. MinIO (S3兼容存储)

**部署信息**:
- **位置**: ~/minio-setup
- **端口**: API: 9000, Console: 9001
- **凭证**: admin / SecretPass123456
- **容量**: 524 GB可用
- **客户端**: mc (MinIO Client)

**操作方法**:
```bash
# 加载环境变量
source ~/minio-setup/load-env.sh

# 上传文件
mc cp local-file.pdf local/my-bucket/

# 批量上传
mc mirror ./build-output/ local/builds/latest/

# 下载文件
mc cp local/my-bucket/file.pdf ./downloads/

# 列出对象
mc ls local/my-bucket/

# 创建bucket
mc mb local/new-project-assets

# 设置公开访问
mc anonymous set download local/my-bucket/public/

# 生成分享链接
mc share download local/my-bucket/document.pdf --expire=7d
```

**Python SDK示例**:
```python
from minio import Minio

# 初始化客户端
client = Minio(
    "localhost:9000",
    access_key="admin",
    secret_key="SecretPass123456",
    secure=False
)

# 上传文件
client.fput_object(
    "my-bucket",
    "data/report.pdf",
    "/path/to/local/report.pdf"
)

# 下载文件
client.fget_object(
    "my-bucket",
    "data/report.pdf",
    "/path/to/save/report.pdf"
)

# 列出对象
objects = client.list_objects("my-bucket", prefix="data/")
for obj in objects:
    print(obj.object_name, obj.size)

# 生成预签名URL
url = client.presigned_get_object(
    "my-bucket",
    "data/report.pdf",
    expires=timedelta(days=7)
)
```

**自动化场景**:
```python
# 场景1: 构建产物存储
"""
CI/CD Artifact Storage:
1. CI构建完成
2. 上传到MinIO/builds/{version}/
3. 生成下载链接
4. Slack通知团队
"""

# 场景2: 媒体文件管理
"""
Media Asset Pipeline:
1. 用户上传图片
2. 压缩和优化
3. 存储到MinIO
4. 生成CDN链接
5. 返回给用户
"""

# 场景3: 备份自动化
"""
Automated Backup:
1. Celery定时任务
2. 导出数据库
3. 压缩备份文件
4. 上传到MinIO/backups/
5. 删除7天前的备份
"""

# 场景4: 日志归档
"""
Log Archival:
1. 收集应用日志
2. 按日期压缩
3. 上传到MinIO/logs/{date}/
4. 本地日志清理
5. 保留最近30天
"""

# 场景5: AI生成内容存储
"""
Generated Content Storage:
1. LLM生成内容
2. 转换为PDF/HTML
3. 存储到MinIO
4. 记录到数据库
5. 生成分享链接
"""
```

---

## 自动化开发场景

### 🎯 完整工作流示例

#### 场景1: 端到端内容生成自动化

```python
"""
完整的内容生成流水线
从数据采集到内容发布的全自动化流程
"""

# ========================================
# 阶段1: 数据采集 (每天凌晨2点)
# ========================================

# 1.1 使用Firecrawl抓取竞品网站
firecrawl_search({
  query: "best memory foam mattress 2025",
  limit: 20,
  sources: ["web"]
})

firecrawl_batch_scrape({
  urls: [从搜索结果获取],
  formats: ["markdown", "html"]
})

# 1.2 保存到MongoDB
mongodb.insert_many({
  database: "geo_platform",
  collection: "scraped_content",
  documents: [抓取的内容]
})

# 1.3 调用InfraNodus API分析
# (通过自定义Python脚本)
infranodus_client.create_graph(text_content)
network_data = infranodus_client.get_graph_data(graph_id)

# 1.4 导入Neo4j
neo4j.batch_import({
  nodes: [Keyword, TopicCluster],
  relationships: [CO_OCCURS_WITH, BELONGS_TO]
})

# ========================================
# 阶段2: 结构洞分析 (凌晨3点)
# ========================================

# 2.1 执行结构洞检测
gaps = neo4j.execute_query(`
  MATCH (c1:TopicCluster), (c2:TopicCluster)
  WHERE id(c1) < id(c2)
  // 计算机会分数
  RETURN c1, c2, opportunity_score
  ORDER BY opportunity_score DESC
  LIMIT 10
`)

# 2.2 保存Gap到Neo4j
for gap in gaps:
  neo4j.create_node({
    label: "Gap",
    properties: gap
  })

# 2.3 Slack通知
slack.send_message({
  channel: "#content-team",
  text: f"发现 {len(gaps)} 个新内容机会！",
  attachments: [gap摘要]
})

# ========================================
# 阶段3: 内容生成 (手动触发或定时)
# ========================================

# 3.1 从Gap生成Prompt
prompt = generate_prompt_from_gap(gap)

# 3.2 保存Prompt到PostgreSQL
postgres.insert({
  table: "prompts",
  data: prompt
})

# 3.3 创建Brief
context = neo4j.retrieve_context(prompt)
brief = llm.generate_brief(prompt, context)

# 3.4 保存Brief到PostgreSQL
postgres.insert({
  table: "briefs",
  data: brief
})

# 3.5 发送到Feishu审核
feishu.create_document({
  title: brief.title,
  content: [格式化的内容]
})

# 3.6 等待审核（n8n webhook）
# 审核通过后...

# 3.7 生成最终Asset
asset = llm.generate_asset(brief, asset_type="BLOG_POST")

# 3.8 计算Citation Score
score = calculate_citation_score(asset)

# 3.9 如果分数>0.7，自动发布
if score > 0.7:
  # 发布到WordPress
  wordpress.create_post({
    title: asset.title,
    content: asset.content,
    status: "publish"
  })

  # 上传到MinIO备份
  minio.upload({
    bucket: "published-content",
    object: f"{asset.id}.html",
    content: asset.content
  })

  # 更新PostgreSQL
  postgres.update({
    table: "assets",
    id: asset.id,
    data: {
      status: "PUBLISHED",
      published_at: now()
    }
  })

  # Slack通知
  slack.send_message({
    channel: "#content-team",
    text: f"✅ 内容已发布: {asset.title}",
    blocks: [详细信息]
  })

# ========================================
# 阶段4: 监控和报告 (每小时/每天)
# ========================================

# 4.1 系统健康检查
health = check_system_health()

if health.score < 70:
  slack.send_alert({
    channel: "#ops-team",
    text: f"⚠️ 系统健康分数: {health.score}%"
  })

# 4.2 收集指标
metrics = {
  "neo4j_nodes": neo4j.count_nodes(),
  "gaps_identified": postgres.count("gaps", today),
  "assets_published": postgres.count("assets", today, status="PUBLISHED")
}

# 4.3 记录到MongoDB
mongodb.insert({
  collection: "daily_metrics",
  document: metrics
})

# 4.4 每周生成报告（周一早上）
if is_monday():
  report = generate_weekly_report()

  # 保存到MinIO
  minio.upload({
    bucket: "reports",
    object: f"weekly-{date}.pdf",
    content: report.pdf
  })

  # 发送到Notion
  notion.create_page({
    parent: "Reports Database",
    properties: { title: report.title },
    children: [报告内容]
  })

  # 邮件发送
  email.send({
    to: ["team@company.com"],
    subject: "GEO Weekly Report",
    body: report.html,
    attachments: [report.pdf]
  })
```

#### 场景2: AI辅助开发自动化

```python
"""
使用AI能力加速开发流程
"""

# ========================================
# 2.1 需求分析 (Sequential Thinking)
# ========================================

user_request = "添加多租户支持"

# Sequential Thinking自动分解问题
analysis = sequential_thinking.analyze({
  problem: user_request,
  context: [项目代码库信息],
  steps: [
    "理解多租户需求",
    "评估现有架构",
    "设计隔离方案",
    "评估数据库影响",
    "考虑性能影响",
    "制定迁移计划"
  ]
})

# 保存到Memory
memory.create_entities([
  {
    name: "Multi-tenancy Feature",
    entityType: "Feature",
    observations: [analysis.insights]
  }
])

# ========================================
# 2.2 技术方案设计
# ========================================

# 使用Memory检索相关技术决策
related_decisions = memory.search_nodes("tenant isolation")

# 生成技术方案
tech_spec = llm.generate({
  prompt: f"""
  基于以下背景设计多租户方案:
  - 现有架构: {analysis.current_architecture}
  - 相关决策: {related_decisions}
  - 约束条件: {constraints}

  生成:
  1. 数据隔离策略
  2. API变更
  3. 数据库Schema变更
  4. 迁移步骤
  """
})

# 保存到Feishu
feishu.create_document({
  title: "多租户技术方案",
  content: [格式化的tech_spec]
})

# ========================================
# 2.3 自动化代码生成
# ========================================

# 读取现有代码
models_code = filesystem.read_file("app/models.py")
api_code = filesystem.read_file("app/api/deps.py")

# 生成新代码
new_models = llm.generate({
  prompt: f"""
  基于现有代码:
  {models_code}

  添加多租户支持:
  1. Tenant模型
  2. TenantContext
  3. 租户过滤器
  """
})

# 写入文件
filesystem.write_file({
  path: "app/models/tenant.py",
  content: new_models
})

# Git提交
github.create_branch({
  repo: "geo-platform",
  branch: "feature/multi-tenancy"
})

github.push_files({
  branch: "feature/multi-tenancy",
  files: [
    { path: "app/models/tenant.py", content: new_models }
  ],
  message: "Add multi-tenancy models"
})

# ========================================
# 2.4 自动化测试生成
# ========================================

# 生成测试代码
test_code = llm.generate({
  prompt: f"""
  为以下代码生成pytest测试:
  {new_models}

  包括:
  1. 模型创建测试
  2. 租户隔离测试
  3. 边界条件测试
  """
})

filesystem.write_file({
  path: "tests/test_tenant.py",
  content: test_code
})

# 运行测试
bash.run("pytest tests/test_tenant.py")

# ========================================
# 2.5 文档自动生成
# ========================================

# 生成API文档
api_docs = llm.generate({
  prompt: f"""
  基于代码生成API文档:
  {new_models}

  Markdown格式，包括:
  1. 端点说明
  2. 请求示例
  3. 响应示例
  """
})

# 更新文档
github.create_or_update_file({
  path: "docs/multi-tenancy.md",
  content: api_docs
})

# 同步到Notion
notion.create_page({
  parent: "API Docs",
  title: "Multi-tenancy API",
  children: [api_docs转为Notion blocks]
})

# ========================================
# 2.6 创建PR
# ========================================

github.create_pull_request({
  title: "Feature: Multi-tenancy support",
  head: "feature/multi-tenancy",
  base: "develop",
  body: f"""
  ## 变更摘要
  {tech_spec.summary}

  ## 技术实现
  {tech_spec.implementation}

  ## 测试
  - [x] 单元测试通过
  - [ ] 集成测试
  - [ ] 性能测试

  ## 文档
  - [x] API文档已更新
  - [x] Notion技术方案已创建
  """
})

# Slack通知
slack.send_message({
  channel: "#dev-team",
  text: "🚀 多租户功能PR已创建，请Review"
})
```

#### 场景3: 智能运维自动化

```python
"""
AI驱动的运维自动化
"""

# ========================================
# 3.1 异常检测和诊断
# ========================================

# 监控系统指标 (每5分钟)
metrics = prometheus.query({
  query: "http_request_duration_seconds_p95"
})

if metrics.value > 2.0:  # P95延迟>2秒

  # 使用Sequential Thinking分析
  diagnosis = sequential_thinking.analyze({
    problem: "API响应时间异常",
    symptoms: {
      "p95_latency": metrics.value,
      "timestamp": now(),
      "affected_endpoints": [...]
    },
    steps: [
      "收集相关日志",
      "检查数据库性能",
      "分析慢查询",
      "检查外部依赖",
      "评估网络状况",
      "定位根本原因"
    ]
  })

  # 收集详细日志
  logs = mongodb.find({
    collection: "application_logs",
    filter: {
      timestamp: { $gte: now() - 5min },
      level: "ERROR"
    }
  })

  # 检查Neo4j慢查询
  slow_queries = neo4j.execute_query(`
    CALL dbms.listQueries()
    YIELD query, elapsedTimeMillis
    WHERE elapsedTimeMillis > 1000
    RETURN query, elapsedTimeMillis
  `)

  # Sentry错误分析
  recent_errors = sentry.search_events({
    query: "error.unhandled:true AND timestamp:>-5m"
  })

  # 使用LLM综合分析
  root_cause = llm.analyze({
    prompt: f"""
    分析以下系统异常：

    症状: {diagnosis.symptoms}
    日志: {logs}
    慢查询: {slow_queries}
    错误: {recent_errors}

    请:
    1. 识别根本原因
    2. 评估影响范围
    3. 提供修复建议
    4. 给出紧急程度（P0/P1/P2）
    """
  })

  # 创建Issue
  issue_id = github.create_issue({
    title: f"[P{root_cause.priority}] {root_cause.title}",
    body: root_cause.details,
    labels: ["bug", "production", f"p{root_cause.priority}"]
  })

  # 创建Sentry Issue关联
  sentry.add_issue_comment({
    issue_id: recent_errors[0].id,
    comment: f"GitHub Issue: {issue_id}"
  })

  # 告警通知
  slack.send_alert({
    channel: "#ops-team",
    priority: root_cause.priority,
    text: f"""
    🚨 {root_cause.title}

    根本原因: {root_cause.root_cause}
    影响范围: {root_cause.impact}
    建议操作: {root_cause.recommendations}

    GitHub Issue: {issue_id}
    """
  })

  # 如果是P0，自动执行修复
  if root_cause.priority == 0:
    if root_cause.auto_fixable:
      # 执行自动修复脚本
      bash.run(root_cause.fix_script)

      # 验证修复
      time.sleep(60)
      new_metrics = prometheus.query(...)

      if new_metrics.value < 1.0:
        slack.send_message({
          text: "✅ 自动修复成功"
        })
      else:
        slack.send_message({
          text: "❌ 自动修复失败，需要人工介入"
        })

# ========================================
# 3.2 智能扩容决策
# ========================================

# 分析负载趋势
load_forecast = sequential_thinking.analyze({
  problem: "预测未来24小时负载",
  data: [历史负载数据],
  steps: [
    "分析历史模式",
    "识别周期性",
    "考虑特殊事件",
    "预测负载趋势",
    "计算所需资源"
  ]
})

if load_forecast.requires_scaling:
  # 生成扩容方案
  scaling_plan = llm.generate({
    prompt: f"""
    基于负载预测制定扩容方案:

    当前: {current_resources}
    预测: {load_forecast}

    生成:
    1. 扩容时间点
    2. 资源数量
    3. 成本估算
    4. 回滚计划
    """
  })

  # 创建Notion页面记录
  notion.create_page({
    title: f"扩容计划 - {date}",
    properties: { "Status": "待审批" },
    children: [scaling_plan]
  })

  # 请求审批
  slack.send_message({
    channel: "#ops-team",
    text: "需要审批扩容计划",
    blocks: [
      {
        type: "section",
        text: scaling_plan.summary
      },
      {
        type: "actions",
        elements: [
          { text: "批准", value: "approve" },
          { text: "拒绝", value: "reject" }
        ]
      }
    ]
  })

# ========================================
# 3.3 自动化备份和恢复
# ========================================

# 每日备份任务
def daily_backup():
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

  # 1. 备份Neo4j
  bash.run("docker exec neo4j neo4j-admin database dump neo4j")
  neo4j_backup = f"neo4j-{timestamp}.dump"

  # 2. 备份PostgreSQL
  bash.run(f"pg_dump -U claude > postgres-{timestamp}.sql")

  # 3. 备份MongoDB
  bash.run(f"mongodump --archive=mongodb-{timestamp}.archive")

  # 4. 压缩所有备份
  bash.run(f"tar -czf backup-{timestamp}.tar.gz *.dump *.sql *.archive")

  # 5. 上传到MinIO
  minio.upload({
    bucket: "backups",
    object: f"daily/{timestamp}/backup.tar.gz",
    file: f"backup-{timestamp}.tar.gz"
  })

  # 6. 验证备份完整性
  backup_size = minio.stat({
    bucket: "backups",
    object: f"daily/{timestamp}/backup.tar.gz"
  }).size

  # 7. 记录到数据库
  postgres.insert({
    table: "backup_history",
    data: {
      "timestamp": timestamp,
      "size_bytes": backup_size,
      "status": "completed"
    }
  })

  # 8. 清理旧备份（保留7天）
  old_backups = minio.list({
    bucket: "backups",
    prefix: "daily/",
    older_than: 7 * 24 * 3600
  })

  for backup in old_backups:
    minio.remove(backup)

  # 9. Slack通知
  slack.send_message({
    channel: "#ops-team",
    text: f"✅ 每日备份完成\n大小: {backup_size / 1024 / 1024:.2f} MB"
  })

# 灾难恢复
def disaster_recovery(backup_timestamp):
  # 1. 停止服务
  bash.run("docker-compose down")

  # 2. 从MinIO下载备份
  minio.download({
    bucket: "backups",
    object: f"daily/{backup_timestamp}/backup.tar.gz",
    file: "restore.tar.gz"
  })

  # 3. 解压
  bash.run("tar -xzf restore.tar.gz")

  # 4. 恢复数据库
  bash.run("neo4j-admin database load neo4j --from=neo4j.dump")
  bash.run("psql -U claude < postgres.sql")
  bash.run("mongorestore --archive=mongodb.archive")

  # 5. 启动服务
  bash.run("docker-compose up -d")

  # 6. 验证恢复
  health = check_system_health()

  if health.score > 90:
    slack.send_message({
      text: "✅ 系统恢复成功"
    })
  else:
    slack.send_alert({
      text: "❌ 系统恢复异常，需要人工检查"
    })
```

---

## 实战示例

### 示例1: 一键部署完整开发环境

```bash
#!/bin/bash
# 使用Claude Code自动化部署开发环境

echo "🚀 开始部署GEO Platform开发环境..."

# 1. 克隆仓库
git clone https://github.com/your-org/geo-platform.git
cd geo-platform

# 2. 创建环境配置
cat > .env << EOF
NEO4J_URI=neo4j://localhost:7688
NEO4J_PASSWORD=development_password
POSTGRES_URL=postgresql://geo:geo@localhost:5437/geo_dev
REDIS_URL=redis://localhost:6382
OPENAI_API_KEY=${OPENAI_API_KEY}
EOF

# 3. 启动Docker服务
docker-compose up -d

# 4. 等待服务就绪
echo "⏳ 等待服务启动..."
sleep 30

# 5. 初始化Neo4j Schema
python scripts/init_neo4j.py

# 6. 运行数据库迁移
alembic upgrade head

# 7. 导入示例数据
python scripts/seed_data.py

# 8. 启动后端服务
uvicorn app.main:app --reload &

# 9. 启动前端开发服务器
cd frontend
npm install
npm run dev &

# 10. 打开浏览器
sleep 5
open http://localhost:3000

echo "✅ 开发环境部署完成！"
echo "📍 前端: http://localhost:3000"
echo "📍 后端API: http://localhost:8000"
echo "📍 API文档: http://localhost:8000/docs"
echo "📍 Neo4j Browser: http://localhost:7475"
```

### 示例2: AI辅助Code Review

```python
"""
使用Claude Code自动化代码审查
"""

async def ai_code_review(pr_number: int):
    # 1. 获取PR信息
    pr = await github.get_pull_request({
        "owner": "my-org",
        "repo": "geo-platform",
        "pull_number": pr_number
    })

    # 2. 获取改动文件
    files = await github.get_pull_request_files({
        "pull_number": pr_number
    })

    # 3. 使用Sequential Thinking分析每个文件
    reviews = []
    for file in files:
        if file.filename.endswith(('.py', '.ts', '.tsx')):
            content = await github.get_file_contents({
                "path": file.filename,
                "ref": pr.head.ref
            })

            # AI分析代码
            review = await llm.analyze({
                "prompt": f"""
                审查以下代码变更:

                文件: {file.filename}
                变更类型: {file.status}

                ```{file.language}
                {file.patch}
                ```

                请检查:
                1. 代码质量和可读性
                2. 潜在的bug
                3. 性能问题
                4. 安全隐患
                5. 测试覆盖
                6. 文档完整性

                为每个问题提供:
                - 严重程度 (HIGH/MEDIUM/LOW)
                - 具体位置
                - 问题描述
                - 改进建议
                """
            })

            reviews.append({
                "file": file.filename,
                "review": review
            })

    # 4. 生成总结
    summary = await llm.generate({
        "prompt": f"""
        总结代码审查结果:

        {reviews}

        生成:
        1. 总体评价
        2. 主要问题列表
        3. 改进建议
        4. 是否建议合并
        """
    })

    # 5. 创建PR评论
    comment_body = f"""
    ## 🤖 AI Code Review

    {summary.overall}

    ### 主要发现

    {summary.findings}

    ### 详细审查

    """

    for review in reviews:
        comment_body += f"""
        #### {review.file}

        {review.review}

        ---
        """

    comment_body += f"""

    ### 建议

    {summary.recommendations}

    **合并建议**: {summary.merge_recommendation}
    """

    await github.create_pull_request_review({
        "pull_number": pr_number,
        "body": comment_body,
        "event": "COMMENT"
    })

    # 6. Slack通知
    await slack.send_message({
        "channel": "#code-review",
        "text": f"AI Code Review完成: PR #{pr_number}",
        "blocks": [
            {
                "type": "section",
                "text": f"*{pr.title}*\n{summary.overall}"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": "查看PR",
                        "url": pr.html_url
                    }
                ]
            }
        ]
    })
```

### 示例3: 智能文档生成

```python
"""
自动生成项目文档
"""

async def generate_project_documentation():
    # 1. 扫描项目结构
    project_structure = await filesystem.directory_tree({
        "path": "/project"
    })

    # 2. 分析主要文件
    key_files = [
        "README.md",
        "app/main.py",
        "app/api/v1/api.py",
        "app/models/*.py",
        "app/services/*.py"
    ]

    file_contents = {}
    for pattern in key_files:
        files = await filesystem.search_files({
            "pattern": pattern
        })

        for file in files:
            content = await filesystem.read_file({
                "path": file.path
            })
            file_contents[file.path] = content

    # 3. 使用Sequential Thinking分析项目
    analysis = await sequential_thinking.analyze({
        "problem": "理解项目架构和生成文档",
        "context": {
            "structure": project_structure,
            "files": file_contents
        },
        "steps": [
            "分析项目结构",
            "识别核心模块",
            "理解数据流",
            "提取API端点",
            "识别依赖关系",
            "生成文档大纲"
        ]
    })

    # 4. 生成各部分文档
    docs = {}

    # 4.1 Architecture Overview
    docs["architecture"] = await llm.generate({
        "prompt": f"""
        基于分析生成架构文档:

        {analysis.architecture}

        包括:
        1. 系统架构图 (Mermaid)
        2. 技术栈
        3. 目录结构说明
        4. 数据流图
        """
    })

    # 4.2 API Documentation
    docs["api"] = await llm.generate({
        "prompt": f"""
        生成API文档:

        {analysis.api_endpoints}

        每个端点包括:
        1. URL和方法
        2. 参数说明
        3. 请求示例
        4. 响应示例
        5. 错误代码
        """
    })

    # 4.3 Database Schema
    docs["database"] = await llm.generate({
        "prompt": f"""
        生成数据库文档:

        {analysis.database_schema}

        包括:
        1. ER图 (Mermaid)
        2. 表结构说明
        3. 关系说明
        4. 索引策略
        """
    })

    # 4.4 Deployment Guide
    docs["deployment"] = await llm.generate({
        "prompt": f"""
        生成部署文档:

        {analysis.deployment_info}

        包括:
        1. 环境要求
        2. 部署步骤
        3. 配置说明
        4. 常见问题
        """
    })

    # 5. 生成主README
    readme = await llm.generate({
        "prompt": f"""
        生成项目README:

        项目信息: {analysis.project_info}

        结构:
        1. 项目简介
        2. 快速开始
        3. 功能特性
        4. 技术架构
        5. 开发指南
        6. API文档链接
        7. 贡献指南
        """
    })

    # 6. 写入文件
    await filesystem.write_file({
        "path": "/project/README.md",
        "content": readme
    })

    await filesystem.write_file({
        "path": "/project/docs/ARCHITECTURE.md",
        "content": docs["architecture"]
    })

    await filesystem.write_file({
        "path": "/project/docs/API.md",
        "content": docs["api"]
    })

    await filesystem.write_file({
        "path": "/project/docs/DATABASE.md",
        "content": docs["database"]
    })

    await filesystem.write_file({
        "path": "/project/docs/DEPLOYMENT.md",
        "content": docs["deployment"]
    })

    # 7. 同步到Notion
    # 创建Notion Database
    db_id = await notion.create_database({
        "parent": {"page_id": "workspace-root"},
        "title": "GEO Platform Docs",
        "properties": {
            "Name": {"title": {}},
            "Category": {"select": {}},
            "Status": {"select": {}}
        }
    })

    # 创建文档页面
    for doc_name, doc_content in docs.items():
        await notion.create_page({
            "parent": {"database_id": db_id},
            "properties": {
                "Name": {"title": [{"text": {"content": doc_name}}]},
                "Category": {"select": {"name": "Documentation"}},
                "Status": {"select": {"name": "Published"}}
            },
            "children": [
                # 转换Markdown为Notion blocks
                convert_markdown_to_notion_blocks(doc_content)
            ]
        })

    # 8. Git提交
    await github.push_files({
        "branch": "docs/auto-generated",
        "files": [
            {"path": "README.md", "content": readme},
            {"path": "docs/ARCHITECTURE.md", "content": docs["architecture"]},
            {"path": "docs/API.md", "content": docs["api"]},
            {"path": "docs/DATABASE.md", "content": docs["database"]},
            {"path": "docs/DEPLOYMENT.md", "content": docs["deployment"]}
        ],
        "message": "docs: Auto-generate project documentation"
    })

    # 9. 创建PR
    pr = await github.create_pull_request({
        "title": "📚 Auto-generated documentation",
        "head": "docs/auto-generated",
        "base": "main",
        "body": """
        ## 📚 Documentation Update

        This PR contains auto-generated documentation including:

        - ✅ README.md
        - ✅ Architecture documentation
        - ✅ API documentation
        - ✅ Database schema documentation
        - ✅ Deployment guide

        The documentation has been automatically generated based on code analysis
        and synchronized to Notion.

        Please review and merge if accurate.
        """
    })

    # 10. Slack通知
    await slack.send_message({
        "channel": "#dev-team",
        "text": "📚 项目文档已自动生成并同步",
        "blocks": [
            {
                "type": "section",
                "text": f"文档生成完成，请Review: {pr.html_url}"
            },
            {
                "type": "section",
                "text": f"Notion文档: [查看]({notion_url})"
            }
        ]
    })
```

---

## 最佳实践

### 1. 资源组合使用

#### 模式1: Web数据采集 + 图谱构建

```python
# 最佳组合:
Firecrawl → InfraNodus → Neo4j → Graph-RAG

# 为什么:
- Firecrawl: 高质量内容提取
- InfraNodus: 语义网络分析
- Neo4j: 图谱存储和查询
- Graph-RAG: 智能问答
```

#### 模式2: 代码开发 + 协作

```python
# 最佳组合:
Sequential Thinking → Memory → GitHub → Slack → Notion

# 为什么:
- Sequential Thinking: 问题分解
- Memory: 知识积累
- GitHub: 代码管理
- Slack: 实时通知
- Notion: 文档沉淀
```

#### 模式3: 数据分析 + 可视化

```python
# 最佳组合:
MongoDB/PostgreSQL → Pandas → D3.js → MinIO

# 为什么:
- MongoDB/PostgreSQL: 数据存储
- Pandas: 数据分析
- D3.js: 可视化
- MinIO: 报告存储
```

### 2. 自动化分层策略

```
第1层: 数据采集自动化
├─ Firecrawl定时抓取
├─ GitHub Webhook触发
└─ n8n调度任务

第2层: 数据处理自动化
├─ InfraNodus分析
├─ Neo4j导入
└─ Redis缓存

第3层: 业务逻辑自动化
├─ Graph-RAG问答
├─ 内容生成
└─ 评分计算

第4层: 通知和协作自动化
├─ Slack通知
├─ Notion文档
└─ Email发送

第5层: 监控和运维自动化
├─ Sentry错误追踪
├─ Prometheus监控
└─ 自动备份
```

### 3. 错误处理和重试

```python
# 最佳实践: 指数退避重试

import tenacity

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    retry=tenacity.retry_if_exception_type(APIError)
)
async def call_external_api():
    # API调用
    pass

# 记录失败到MongoDB
try:
    result = await call_external_api()
except Exception as e:
    await mongodb.insert({
        "collection": "failed_jobs",
        "document": {
            "job_type": "api_call",
            "error": str(e),
            "timestamp": now(),
            "retry_count": 3
        }
    })

    # Slack告警
    await slack.send_alert({
        "text": f"API调用失败: {e}"
    })
```

### 4. 性能优化建议

```python
# 1. 使用缓存
@cache(redis_client, expire=300)
async def get_expensive_data():
    # 昂贵的计算
    pass

# 2. 批量操作
# ❌ 错误: 循环插入
for item in items:
    await neo4j.create_node(item)

# ✅ 正确: 批量插入
await neo4j.batch_create_nodes(items)

# 3. 异步并发
# ❌ 错误: 串行
for url in urls:
    data = await firecrawl_scrape(url)

# ✅ 正确: 并发
tasks = [firecrawl_scrape(url) for url in urls]
results = await asyncio.gather(*tasks)

# 4. 数据库索引
# 确保频繁查询的字段有索引
CREATE INDEX idx_keyword_name ON Keyword(name);
CREATE INDEX idx_product_rating ON Product(rating);
```

### 5. 安全建议

```python
# 1. 敏感信息加密
from cryptography.fernet import Fernet

cipher = Fernet(key)
encrypted_api_key = cipher.encrypt(api_key.encode())

# 存储到环境变量，不要硬编码
os.environ['ENCRYPTED_API_KEY'] = encrypted_api_key

# 2. 审计日志
@audit_log
async def sensitive_operation():
    # 自动记录操作到MongoDB
    pass

# 3. 速率限制
@rate_limit(max_calls=100, period=60)
async def api_endpoint():
    pass

# 4. 输入验证
from pydantic import BaseModel, validator

class DataSourceInput(BaseModel):
    url: str

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Invalid URL')
        return v
```

---

## 总结

### 🎯 核心优势

1. **完整的技术栈** - 从数据到发布的全链路支持
2. **AI增强** - Sequential Thinking + Memory提升开发效率
3. **自动化程度高** - 减少90%重复性工作
4. **可扩展性强** - 微服务架构，易于扩展
5. **协作友好** - GitHub/Slack/Notion无缝集成

### 📊 效率提升

- **开发速度**: 提升 3-5倍
- **代码质量**: AI Code Review降低50%bug
- **文档完整性**: 自动生成，始终同步
- **运维效率**: 自动化监控和告警
- **团队协作**: 实时通知和知识沉淀

### 🚀 下一步

1. **选择场景** - 从最痛的场景开始
2. **小步快跑** - 先自动化一个流程
3. **持续优化** - 收集反馈，迭代改进
4. **扩展应用** - 推广到其他场景

---

*文档版本: 1.0*
*最后更新: 2025-10-16*

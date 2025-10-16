# InfraNodus GEO System

[![Tests](https://github.com/keevingfu/infranodus-geo-system/actions/workflows/ci.yml/badge.svg)](https://github.com/keevingfu/infranodus-geo-system/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Neo4j 5.14+](https://img.shields.io/badge/neo4j-5.14+-green.svg)](https://neo4j.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive **Generative Engine Optimization (GEO)** Knowledge Graph System integrating InfraNodus with Neo4j for intelligent content gap analysis, Graph-RAG question answering, and automated content generation.

## 🎯 Overview

This system combines semantic network analysis with graph database technology to identify content opportunities, answer questions using knowledge graphs, and automate content workflows.

### Key Features

- 🧠 **Knowledge Graph Database** - Neo4j-based graph with 12 node types and 40+ relationship patterns
- 🔍 **Structure Hole Detection** - Identify content gaps with opportunity scoring (>0.5 threshold)
- 💬 **Graph-RAG Q&A** - Context-aware question answering with citation tracking
- 📊 **Real-time Monitoring** - Health scores, KG statistics, and pipeline metrics
- 🤖 **Automated Workflows** - Data acquisition, analysis, and reporting
- 📸 **Visual Demonstrations** - Playwright-based browser automation and screenshots
- 🧪 **Complete Test Suite** - 25+ tests with 100% pass rate

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GEO System Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Data Sources │  │  InfraNodus  │  │   Neo4j DB   │      │
│  │  (URLs/APIs) │──│   Analysis   │──│ Knowledge    │      │
│  └──────────────┘  └──────────────┘  │ Graph        │      │
│         │                  │          └──────┬───────┘      │
│         │                  │                 │              │
│         ▼                  ▼                 ▼              │
│  ┌──────────────────────────────────────────────────┐      │
│  │         Data Acquisition Pipeline                │      │
│  └────────────────────┬─────────────────────────────┘      │
│                       │                                     │
│         ┌─────────────┼─────────────┐                      │
│         │             │             │                      │
│         ▼             ▼             ▼                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│  │Structure │  │Graph-RAG │  │Monitoring│                │
│  │  Holes   │  │   Q&A    │  │Dashboard │                │
│  └──────────┘  └──────────┘  └──────────┘                │
│         │             │             │                      │
│         └─────────────┼─────────────┘                      │
│                       ▼                                     │
│            ┌──────────────────────┐                        │
│            │  Automated Reporting │                        │
│            └──────────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Neo4j 5.14+ (Docker or local installation)
- InfraNodus API key (optional, for text network analysis)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/keevingfu/infranodus-geo-system.git
   cd infranodus-geo-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Neo4j database**
   ```bash
   # Using Docker
   docker run -d \
     --name neo4j-geo \
     -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/your_password \
     neo4j:5.14

   # Or use docker-compose
   docker-compose up -d
   ```

5. **Initialize database schema**
   ```bash
   # Connect to Neo4j browser at http://localhost:7474
   # Copy and execute contents of neo4j-schema.cypher
   ```

### Configuration

Create a `.env` file in the project root:

```env
# Neo4j Configuration
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password

# InfraNodus API (optional)
INFRANODUS_API_KEY=your_api_key
INFRANODUS_API_URL=https://infranodus.com/api

# Application Settings
LOG_LEVEL=INFO
```

## 📖 Usage

### 1. Data Acquisition

```python
from data_acquisition_pipeline import DataAcquisitionPipeline

# Initialize pipeline
pipeline = DataAcquisitionPipeline(
    neo4j_uri="neo4j://localhost:7687",
    neo4j_username="neo4j",
    neo4j_password="your_password"
)

# Acquire data from URLs
urls = [
    "https://example.com/article1",
    "https://example.com/article2"
]
pipeline.acquire_from_urls(urls)
```

### 2. Structure Hole Analysis

```python
from cypher_queries import GEOQueries

# Initialize queries
queries = GEOQueries(
    uri="neo4j://localhost:7687",
    username="neo4j",
    password="your_password"
)

# Find content opportunities
gaps = queries.find_structure_holes(
    min_opportunity_score=0.5,
    limit=10
)

for gap in gaps:
    print(f"Opportunity: {gap.cluster_a} ↔ {gap.cluster_b}")
    print(f"Score: {gap.opportunity_score:.3f}")
    print(f"Keywords A: {gap.keywords_a}")
    print(f"Keywords B: {gap.keywords_b}")
```

### 3. Graph-RAG Question Answering

```python
from graph_rag import GraphRAG

# Initialize Graph-RAG
rag = GraphRAG(
    uri="neo4j://localhost:7687",
    username="neo4j",
    password="your_password"
)

# Ask a question
answer = rag.answer_question("What is cooling gel technology?")

print(f"Answer: {answer.answer_text}")
print(f"Confidence: {answer.confidence:.2f}")
print(f"Citations: {len(answer.citations)}")
```

### 4. System Monitoring

```python
from monitoring_dashboard import MonitoringDashboard

# Initialize dashboard
dashboard = MonitoringDashboard(
    uri="neo4j://localhost:7687",
    username="neo4j",
    password="your_password"
)

# Get system health
health = dashboard.get_system_health()
print(f"Health Score: {health['health_score']}%")
print(f"Status: {health['status']}")

# Generate weekly report
report = dashboard.generate_weekly_report()
```

### 5. Complete Workflow Demo

```bash
# Run command-line demo
python demo_complete_workflow.py

# Run visual demo with Playwright
python demo_playwright_visual.py
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_geo_system.py

# Run with verbose output
pytest -v
```

## 📊 Project Structure

```
infranodus-geo-system/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous Integration
│       └── deploy.yml          # Continuous Deployment
├── tests/
│   └── test_geo_system.py      # Test suite
├── cypher_queries.py           # Neo4j query library
├── data_acquisition_pipeline.py # Data ingestion
├── demo_complete_workflow.py   # CLI demo
├── demo_playwright_visual.py   # Visual demo
├── graph_rag.py                # Graph-RAG Q&A
├── import_pipeline.py          # Data import
├── infranodus_client.py        # InfraNodus integration
├── monitoring_dashboard.py     # System monitoring
├── neo4j-schema.cypher         # Database schema
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Test configuration
├── docker-compose.yml          # Docker deployment
├── Dockerfile                  # Container image
└── README.md                   # This file
```

## 📚 Documentation

- [SYSTEM_DESIGN.md](./SYSTEM_DESIGN.md) - Complete architecture (70+ pages)
- [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) - 16-20 week development plan
- [AUTOMATION_CAPABILITIES.md](./AUTOMATION_CAPABILITIES.md) - MCP servers integration guide
- [DEMO_SUMMARY.md](./DEMO_SUMMARY.md) - Workflow demonstration results

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

## 🔧 API Endpoints (Future)

The system includes plans for a FastAPI REST API:

- `GET /api/v1/health` - System health check
- `POST /api/v1/data/acquire` - Trigger data acquisition
- `GET /api/v1/structure-holes` - Get content opportunities
- `POST /api/v1/qa/answer` - Ask questions via Graph-RAG
- `GET /api/v1/monitoring/dashboard` - Get monitoring data
- `GET /api/v1/reports/weekly` - Generate weekly report

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide
- Update documentation
- Ensure all tests pass before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Neo4j](https://neo4j.com/) - Graph database platform
- [InfraNodus](https://infranodus.com/) - Text network analysis
- [Playwright](https://playwright.dev/) - Browser automation
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework

## 📧 Contact

- GitHub: [@keevingfu](https://github.com/keevingfu)
- Project Link: [https://github.com/keevingfu/infranodus-geo-system](https://github.com/keevingfu/infranodus-geo-system)

## 🗺️ Roadmap

- [x] Core knowledge graph implementation
- [x] Structure hole detection
- [x] Graph-RAG Q&A system
- [x] Monitoring dashboard
- [x] Complete test suite
- [ ] FastAPI REST API
- [ ] Web UI dashboard
- [ ] Real-time updates with WebSockets
- [ ] Multi-language support
- [ ] Advanced analytics and visualizations
- [ ] Integration with more data sources

---

**Built with ❤️ using Claude Code**

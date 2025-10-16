"""
GEO System Playwright Visual Demo
===================================

Interactive demonstration using Playwright for browser automation
and visual documentation of the complete GEO workflow.

Features:
- Browser-based visualization
- Screenshot capture at each step
- Interactive Neo4j browser
- InfraNodus graph visualization
- Automated HTML report generation

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from playwright.async_api import async_playwright, Browser, Page

# GEO System imports
from cypher_queries import GEOQueries
from graph_rag import GraphRAG
from monitoring_dashboard import MonitoringDashboard

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PlaywrightVisualDemo:
    """Visual demonstration using Playwright browser automation"""

    def __init__(self):
        """Initialize demo"""
        self.demo_dir = Path("./demo_screenshots")
        self.demo_dir.mkdir(exist_ok=True)

        # Neo4j configuration
        self.neo4j_config = {
            "uri": "neo4j://localhost:7688",
            "username": "neo4j",
            "password": "claude_neo4j_2025"
        }

        # Initialize GEO components
        self.queries = GEOQueries(**self.neo4j_config)
        self.rag = GraphRAG(**self.neo4j_config)
        self.dashboard = MonitoringDashboard(**self.neo4j_config)

        self.browser: Browser = None
        self.page: Page = None
        self.screenshots: List[Dict[str, str]] = []

        logger.info("Playwright Visual Demo initialized")

    async def setup_browser(self):
        """Setup Playwright browser"""
        logger.info("Setting up Playwright browser...")
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page(viewport={"width": 1920, "height": 1080})
        logger.info("Browser ready")

    async def take_screenshot(self, name: str, description: str):
        """Take and save screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.png"
        filepath = self.demo_dir / filename

        await self.page.screenshot(path=str(filepath), full_page=True)

        self.screenshots.append({
            "step": len(self.screenshots) + 1,
            "name": name,
            "description": description,
            "filename": filename,
            "timestamp": timestamp
        })

        logger.info(f"Screenshot saved: {filename}")
        return filepath

    async def close_browser(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()

    def close_components(self):
        """Close GEO components"""
        self.queries.close()
        self.rag.close()
        self.dashboard.close()

    # =========================================================================
    # VISUAL DEMO STEPS
    # =========================================================================

    async def step1_neo4j_browser(self):
        """Step 1: Visualize Neo4j graph database"""
        print("\n" + "=" * 80)
        print("STEP 1: NEO4J GRAPH DATABASE VISUALIZATION")
        print("=" * 80)

        print("\n🌐 Opening Neo4j Browser...")

        try:
            # Navigate to Neo4j Browser
            await self.page.goto("http://localhost:7475/browser/")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

            print("   ✅ Neo4j Browser loaded")

            # Take screenshot of initial screen
            await self.take_screenshot(
                "01_neo4j_initial",
                "Neo4j Browser - Initial Screen"
            )

            # Try to connect (if not already connected)
            try:
                # Look for connect form
                connect_button = await self.page.query_selector('button:has-text("Connect")')
                if connect_button:
                    # Fill in credentials
                    await self.page.fill('input[name="username"]', 'neo4j')
                    await self.page.fill('input[name="password"]', 'claude_neo4j_2025')
                    await connect_button.click()
                    await asyncio.sleep(2)
                    print("   ✅ Connected to Neo4j")
            except:
                print("   ℹ️  Already connected to Neo4j")

            # Execute query to show graph
            query = """
            MATCH (n)
            RETURN n
            LIMIT 50
            """

            # Type query in editor
            try:
                editor = await self.page.query_selector('.CodeMirror textarea')
                if editor:
                    await editor.type(query)
                    await asyncio.sleep(1)

                    # Click run button
                    run_button = await self.page.query_selector('button[title="Run"]')
                    if run_button:
                        await run_button.click()
                        await asyncio.sleep(3)

                        print("   ✅ Graph query executed")

                        # Take screenshot of graph visualization
                        await self.take_screenshot(
                            "02_neo4j_graph",
                            "Neo4j Browser - Graph Visualization (50 nodes)"
                        )
            except Exception as e:
                print(f"   ⚠️  Could not execute query: {e}")

            print("\n📊 Neo4j Statistics:")
            count_query = "MATCH (n) RETURN count(n) AS total"
            result = self.queries._execute_query(count_query)
            total_nodes = result[0]["total"]
            print(f"   - Total nodes in database: {total_nodes}")

        except Exception as e:
            logger.error(f"Neo4j browser step failed: {e}")
            print(f"   ❌ Error: {e}")

    async def step2_infranodus_graph(self):
        """Step 2: Visualize InfraNodus graph"""
        print("\n" + "=" * 80)
        print("STEP 2: INFRANODUS GRAPH VISUALIZATION")
        print("=" * 80)

        print("\n🌐 Opening InfraNodus...")

        try:
            # Navigate to InfraNodus
            await self.page.goto("http://localhost:3000")
            await self.page.wait_for_load_state("networkidle")
            await asyncio.sleep(2)

            print("   ✅ InfraNodus loaded")

            # Take screenshot of homepage
            await self.take_screenshot(
                "03_infranodus_home",
                "InfraNodus - Homepage"
            )

            # Try to login
            try:
                # Check if login is needed
                login_link = await self.page.query_selector('a:has-text("Login")')
                if login_link:
                    await login_link.click()
                    await asyncio.sleep(1)

                    # Fill login form
                    await self.page.fill('input[name="username"]', 'demo_user')
                    await self.page.fill('input[name="password"]', 'demo')
                    await self.page.click('button[type="submit"]')
                    await asyncio.sleep(2)

                    print("   ✅ Logged into InfraNodus")
            except:
                print("   ℹ️  Already logged in or no login required")

            # Navigate to private graphs
            try:
                await self.page.goto("http://localhost:3000/@private")
                await asyncio.sleep(2)

                # Take screenshot of graph view
                await self.take_screenshot(
                    "04_infranodus_graph",
                    "InfraNodus - Private Graph View"
                )

                print("   ✅ Graph visualization captured")
            except Exception as e:
                print(f"   ⚠️  Could not load graph: {e}")

        except Exception as e:
            logger.error(f"InfraNodus step failed: {e}")
            print(f"   ❌ Error: {e}")

    async def step3_structure_holes_viz(self):
        """Step 3: Visualize structure hole analysis results"""
        print("\n" + "=" * 80)
        print("STEP 3: STRUCTURE HOLE ANALYSIS VISUALIZATION")
        print("=" * 80)

        print("\n🔍 Analyzing structure holes...")

        # Find structure holes
        gaps = self.queries.find_structure_holes(min_opportunity_score=0.5, limit=5)

        print(f"   ✅ Found {len(gaps)} structure holes")

        # Create HTML visualization
        html_content = self._generate_structure_holes_html(gaps)

        html_file = self.demo_dir / "structure_holes_viz.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Open in browser
        await self.page.goto(f"file://{html_file.absolute()}")
        await asyncio.sleep(2)

        # Take screenshot
        await self.take_screenshot(
            "05_structure_holes",
            f"Structure Hole Analysis - {len(gaps)} Opportunities Identified"
        )

        print(f"   ✅ Visualization created: {html_file}")

        return gaps

    def _generate_structure_holes_html(self, gaps: List[Dict]) -> str:
        """Generate HTML for structure holes visualization"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Structure Hole Analysis</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }
                h1 {
                    color: #667eea;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 15px;
                    margin-bottom: 30px;
                }
                .gap-card {
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 15px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                    transition: transform 0.3s;
                }
                .gap-card:hover {
                    transform: translateY(-5px);
                    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                }
                .cluster-connection {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 20px;
                }
                .cluster {
                    background: #667eea;
                    color: white;
                    padding: 15px 25px;
                    border-radius: 30px;
                    font-weight: bold;
                    font-size: 18px;
                    flex: 1;
                    text-align: center;
                }
                .arrow {
                    font-size: 36px;
                    color: #764ba2;
                    margin: 0 20px;
                }
                .score {
                    font-size: 32px;
                    font-weight: bold;
                    color: #764ba2;
                    text-align: center;
                    margin: 15px 0;
                }
                .keywords {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                    margin-top: 15px;
                }
                .keyword {
                    background: #764ba2;
                    color: white;
                    padding: 8px 15px;
                    border-radius: 20px;
                    font-size: 14px;
                }
                .stats {
                    background: #f0f0f0;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 30px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Structure Hole Analysis Results</h1>
                <div class="stats">
                    <strong>Total Opportunities Found:</strong> """ + str(len(gaps)) + """<br>
                    <strong>Analysis Date:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
                </div>
        """

        for i, gap in enumerate(gaps, 1):
            cluster_a = gap.get('cluster_a', 'Unknown')
            cluster_b = gap.get('cluster_b', 'Unknown')
            score = gap.get('opportunity_score', 0)
            keywords_a = gap.get('keywords_a', [])
            keywords_b = gap.get('keywords_b', [])

            html += f"""
                <div class="gap-card">
                    <h2>Opportunity #{i}</h2>
                    <div class="cluster-connection">
                        <div class="cluster">{cluster_a}</div>
                        <div class="arrow">↔</div>
                        <div class="cluster">{cluster_b}</div>
                    </div>
                    <div class="score">Score: {score:.3f}</div>
                    <div>
                        <strong>Keywords from {cluster_a}:</strong>
                        <div class="keywords">
            """

            for kw in keywords_a[:5]:
                html += f'<span class="keyword">{kw}</span>'

            html += f"""
                        </div>
                    </div>
                    <div style="margin-top: 15px;">
                        <strong>Keywords from {cluster_b}:</strong>
                        <div class="keywords">
            """

            for kw in keywords_b[:5]:
                html += f'<span class="keyword">{kw}</span>'

            html += """
                        </div>
                    </div>
                </div>
            """

        html += """
            </div>
        </body>
        </html>
        """

        return html

    async def step4_graph_rag_demo(self):
        """Step 4: Demonstrate Graph-RAG question answering"""
        print("\n" + "=" * 80)
        print("STEP 4: GRAPH-RAG QUESTION ANSWERING DEMO")
        print("=" * 80)

        print("\n💬 Testing Graph-RAG system...")

        # Demo questions
        questions = [
            "What is cooling gel?",
            "How can I solve back pain?",
            "What evidence supports cooling gel effectiveness?"
        ]

        qa_results = []

        for question in questions:
            answer = self.rag.answer_question(question)
            qa_results.append({
                "question": question,
                "answer": answer.answer_text,
                "confidence": answer.confidence,
                "citations": len(answer.citations)
            })

        print(f"   ✅ Answered {len(questions)} questions")

        # Create HTML visualization
        html_content = self._generate_qa_html(qa_results)

        html_file = self.demo_dir / "graph_rag_qa.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Open in browser
        await self.page.goto(f"file://{html_file.absolute()}")
        await asyncio.sleep(2)

        # Take screenshot
        await self.take_screenshot(
            "06_graph_rag_qa",
            f"Graph-RAG Q&A Results - {len(questions)} Questions Answered"
        )

        print(f"   ✅ Visualization created: {html_file}")

        return qa_results

    def _generate_qa_html(self, qa_results: List[Dict]) -> str:
        """Generate HTML for Q&A results"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Graph-RAG Q&A Results</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }
                .container {
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }
                h1 {
                    color: #667eea;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 15px;
                    margin-bottom: 30px;
                }
                .qa-card {
                    background: #f8f9fa;
                    border-left: 5px solid #667eea;
                    border-radius: 10px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                }
                .question {
                    font-size: 20px;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 15px;
                }
                .answer {
                    font-size: 16px;
                    line-height: 1.6;
                    color: #333;
                    margin-bottom: 15px;
                }
                .metadata {
                    display: flex;
                    gap: 20px;
                    font-size: 14px;
                    color: #666;
                }
                .confidence {
                    background: #764ba2;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                }
                .sources {
                    background: #667eea;
                    color: white;
                    padding: 5px 15px;
                    border-radius: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💬 Graph-RAG Question Answering Results</h1>
        """

        for i, qa in enumerate(qa_results, 1):
            html += f"""
                <div class="qa-card">
                    <div class="question">Q{i}: {qa['question']}</div>
                    <div class="answer">A: {qa['answer']}</div>
                    <div class="metadata">
                        <span class="confidence">Confidence: {qa['confidence']:.2f}</span>
                        <span class="sources">Citations: {qa['citations']}</span>
                    </div>
                </div>
            """

        html += """
            </div>
        </body>
        </html>
        """

        return html

    async def step5_dashboard_visualization(self):
        """Step 5: Show monitoring dashboard"""
        print("\n" + "=" * 80)
        print("STEP 5: MONITORING DASHBOARD VISUALIZATION")
        print("=" * 80)

        print("\n📊 Generating monitoring dashboard...")

        # Get monitoring data
        health = self.dashboard.check_system_health()
        metrics = self.dashboard.get_graph_metrics()
        pipeline = self.dashboard.get_pipeline_metrics()

        # Create HTML dashboard
        html_content = self._generate_dashboard_html(health, metrics, pipeline)

        html_file = self.demo_dir / "monitoring_dashboard.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Open in browser
        await self.page.goto(f"file://{html_file.absolute()}")
        await asyncio.sleep(2)

        # Take screenshot
        await self.take_screenshot(
            "07_monitoring_dashboard",
            f"Monitoring Dashboard - Health Score: {health.health_score:.0f}%"
        )

        print(f"   ✅ Dashboard created: {html_file}")

    def _generate_dashboard_html(self, health, metrics, pipeline) -> str:
        """Generate HTML for monitoring dashboard"""
        health_color = "#28a745" if health.health_score >= 90 else "#ffc107" if health.health_score >= 70 else "#dc3545"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GEO System Monitoring Dashboard</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }}
                h1 {{
                    color: #667eea;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 15px;
                    margin-bottom: 30px;
                }}
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                .metric-card {{
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    border-radius: 15px;
                    padding: 25px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                .metric-title {{
                    font-size: 14px;
                    color: #666;
                    text-transform: uppercase;
                    margin-bottom: 10px;
                }}
                .metric-value {{
                    font-size: 36px;
                    font-weight: bold;
                    color: #667eea;
                }}
                .health-score {{
                    text-align: center;
                    padding: 40px;
                    background: {health_color};
                    color: white;
                    border-radius: 15px;
                    margin-bottom: 30px;
                }}
                .health-score h2 {{
                    margin: 0;
                    font-size: 48px;
                }}
                .health-score p {{
                    margin: 10px 0 0 0;
                    font-size: 18px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background: #667eea;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🏥 GEO System Monitoring Dashboard</h1>

                <div class="health-score">
                    <h2>{health.health_score:.0f}%</h2>
                    <p>System Health Score</p>
                </div>

                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Total Nodes</div>
                        <div class="metric-value">{health.total_nodes:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Total Relationships</div>
                        <div class="metric-value">{health.total_relationships:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Neo4j Status</div>
                        <div class="metric-value">{health.neo4j_status.upper()}</div>
                    </div>
                </div>

                <h2>📊 Knowledge Graph Metrics</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Entity Type</th>
                            <th>Count</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Keywords</td><td>{metrics.keywords_count}</td></tr>
                        <tr><td>Topic Clusters</td><td>{metrics.topics_count}</td></tr>
                        <tr><td>Personas</td><td>{metrics.personas_count}</td></tr>
                        <tr><td>Pain Points</td><td>{metrics.pain_points_count}</td></tr>
                        <tr><td>Features</td><td>{metrics.features_count}</td></tr>
                        <tr><td>Products</td><td>{metrics.products_count}</td></tr>
                        <tr><td>Claims</td><td>{metrics.claims_count}</td></tr>
                        <tr><td>Evidence</td><td>{metrics.evidence_count}</td></tr>
                        <tr><td>Structure Holes</td><td>{metrics.gaps_count}</td></tr>
                        <tr><td>Prompts</td><td>{metrics.prompts_count}</td></tr>
                        <tr><td>Briefs</td><td>{metrics.briefs_count}</td></tr>
                        <tr><td>Assets</td><td>{metrics.assets_count}</td></tr>
                    </tbody>
                </table>

                <h2 style="margin-top: 40px;">🚀 Content Pipeline Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-title">Total Prompts</div>
                        <div class="metric-value">{pipeline.total_prompts}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-title">Avg Citation Score</div>
                        <div class="metric-value">{pipeline.avg_citation_score:.2f}</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    async def generate_final_report(self):
        """Generate final HTML report with all screenshots"""
        print("\n" + "=" * 80)
        print("GENERATING FINAL REPORT")
        print("=" * 80)

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>GEO System Complete Workflow Demo</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 40px;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #667eea;
                    border-bottom: 3px solid #667eea;
                    padding-bottom: 15px;
                }}
                .screenshot-section {{
                    margin: 40px 0;
                    padding: 30px;
                    background: #f8f9fa;
                    border-radius: 15px;
                }}
                .screenshot-section h2 {{
                    color: #764ba2;
                    margin-bottom: 10px;
                }}
                .screenshot-section p {{
                    color: #666;
                    margin-bottom: 20px;
                }}
                .screenshot-section img {{
                    width: 100%;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                }}
                .summary {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    border-radius: 15px;
                    margin-bottom: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 GEO System Complete Workflow Demo</h1>

                <div class="summary">
                    <h2>Demonstration Summary</h2>
                    <p><strong>Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                    <p><strong>Total Steps:</strong> {len(self.screenshots)}</p>
                    <p><strong>Purpose:</strong> Complete end-to-end demonstration of the InfraNodus + Neo4j GEO knowledge graph system</p>
                </div>
        """

        for screenshot in self.screenshots:
            html += f"""
                <div class="screenshot-section">
                    <h2>Step {screenshot['step']}: {screenshot['name'].replace('_', ' ').title()}</h2>
                    <p>{screenshot['description']}</p>
                    <img src="{screenshot['filename']}" alt="{screenshot['description']}">
                </div>
            """

        html += """
            </div>
        </body>
        </html>
        """

        report_file = self.demo_dir / "complete_workflow_report.html"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n✅ Final report generated: {report_file}")
        print(f"   Total screenshots: {len(self.screenshots)}")

        return report_file

    # =========================================================================
    # COMPLETE WORKFLOW
    # =========================================================================

    async def run_complete_demo(self):
        """Run complete visual demonstration"""
        print("\n" + "=" * 80)
        print("🎬 STARTING PLAYWRIGHT VISUAL DEMO")
        print("=" * 80)
        print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Screenshot Directory: {self.demo_dir}")

        try:
            # Setup browser
            await self.setup_browser()

            # Run demonstration steps
            await self.step1_neo4j_browser()
            await asyncio.sleep(2)

            await self.step2_infranodus_graph()
            await asyncio.sleep(2)

            await self.step3_structure_holes_viz()
            await asyncio.sleep(2)

            await self.step4_graph_rag_demo()
            await asyncio.sleep(2)

            await self.step5_dashboard_visualization()
            await asyncio.sleep(2)

            # Generate final report
            report_file = await self.generate_final_report()

            # Open final report
            await self.page.goto(f"file://{report_file.absolute()}")
            await asyncio.sleep(3)

            print("\n" + "=" * 80)
            print("✅ DEMO COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"\n📁 Screenshots saved to: {self.demo_dir}")
            print(f"📄 Final report: {report_file}")
            print(f"\n🎉 Total steps demonstrated: {len(self.screenshots)}")

            # Wait 5 seconds to view final report before closing
            print("\n⏰ Browser will close in 5 seconds...")
            await asyncio.sleep(5)

        except Exception as e:
            logger.error(f"Demo failed: {e}")
            print(f"\n❌ Demo failed: {e}")
            raise

        finally:
            await self.close_browser()
            self.close_components()


async def main():
    """Run the visual demo"""
    demo = PlaywrightVisualDemo()
    await demo.run_complete_demo()


if __name__ == "__main__":
    asyncio.run(main())

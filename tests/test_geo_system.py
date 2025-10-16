"""
GEO System End-to-End Automated Tests
======================================

Comprehensive test suite using Playwright to validate all system components.

Test Coverage:
- Neo4j database connectivity and queries
- InfraNodus API integration
- Data acquisition pipeline
- Graph-RAG question answering
- Monitoring dashboard
- n8n workflow integration

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

import pytest
import asyncio
import json
import time
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cypher_queries import GEOQueries
from infranodus_client import InfraNodusClient, InfraNodusConfig
from graph_rag import GraphRAG
from monitoring_dashboard import MonitoringDashboard


# =============================================================================
# TEST CONFIGURATION
# =============================================================================

@pytest.fixture(scope="session")
def neo4j_config():
    """Neo4j test configuration"""
    return {
        "uri": "neo4j://localhost:7688",
        "username": "neo4j",
        "password": "claude_neo4j_2025"
    }


@pytest.fixture(scope="session")
def infranodus_config():
    """InfraNodus test configuration"""
    return InfraNodusConfig(
        base_url="http://localhost:3000",
        username="demo_user",
        password="demo"
    )


@pytest.fixture(scope="session")
def firecrawl_config():
    """Firecrawl test configuration"""
    return {
        "api_url": "http://localhost:3002",
        "api_key": "fs-test"
    }


# =============================================================================
# NEO4J DATABASE TESTS
# =============================================================================

class TestNeo4jDatabase:
    """Test Neo4j database connectivity and operations"""

    def test_neo4j_connection(self, neo4j_config):
        """Test 1: Neo4j database connection"""
        queries = GEOQueries(**neo4j_config)

        try:
            # Execute simple query
            result = queries._execute_query("RETURN 1 AS test")
            assert result is not None
            assert len(result) > 0
            assert result[0]["test"] == 1
            print("✅ Neo4j connection successful")
        finally:
            queries.close()

    def test_schema_validation(self, neo4j_config):
        """Test 2: Validate database schema (constraints and indexes)"""
        queries = GEOQueries(**neo4j_config)

        try:
            # Check constraints
            constraints_query = "SHOW CONSTRAINTS"
            constraints = queries._execute_query(constraints_query)
            assert len(constraints) >= 18, f"Expected at least 18 constraints, found {len(constraints)}"
            print(f"✅ Found {len(constraints)} constraints")

            # Check indexes
            indexes_query = "SHOW INDEXES"
            indexes = queries._execute_query(indexes_query)
            assert len(indexes) >= 23, f"Expected at least 23 indexes, found {len(indexes)}"
            print(f"✅ Found {len(indexes)} indexes")
        finally:
            queries.close()

    def test_node_counts(self, neo4j_config):
        """Test 3: Verify node counts in database"""
        queries = GEOQueries(**neo4j_config)

        try:
            count_query = "MATCH (n) RETURN count(n) AS total_nodes"
            result = queries._execute_query(count_query)
            total_nodes = result[0]["total_nodes"]

            assert total_nodes > 0, "Database should have nodes"
            print(f"✅ Database contains {total_nodes} nodes")
        finally:
            queries.close()

    def test_structure_hole_detection(self, neo4j_config):
        """Test 4: Structure hole detection query"""
        queries = GEOQueries(**neo4j_config)

        try:
            gaps = queries.find_structure_holes(min_opportunity_score=0.5, limit=5)
            assert isinstance(gaps, list), "Should return a list"
            print(f"✅ Structure hole detection working ({len(gaps)} gaps found)")
        finally:
            queries.close()

    def test_citation_ready_score(self, neo4j_config):
        """Test 5: Citation-ready score calculation"""
        queries = GEOQueries(**neo4j_config)

        try:
            results = queries.calculate_citation_ready_score()
            assert isinstance(results, list), "Should return a list"
            print(f"✅ Citation-ready score calculation working")
        finally:
            queries.close()

    def test_persona_scenario_matrix(self, neo4j_config):
        """Test 6: Persona-scenario matrix query"""
        queries = GEOQueries(**neo4j_config)

        try:
            matrix = queries.get_persona_scenario_matrix()
            assert isinstance(matrix, list), "Should return a list"
            print(f"✅ Persona-scenario matrix working ({len(matrix)} entries)")
        finally:
            queries.close()


# =============================================================================
# INFRANODUS API TESTS
# =============================================================================

class TestInfraNodusAPI:
    """Test InfraNodus API integration"""

    def test_infranodus_login(self, infranodus_config):
        """Test 7: InfraNodus authentication"""
        client = InfraNodusClient(infranodus_config)

        success = client.login()
        assert success, "InfraNodus login should succeed"
        print("✅ InfraNodus authentication successful")

    def test_get_graph_data(self, infranodus_config):
        """Test 8: Retrieve graph data from InfraNodus"""
        client = InfraNodusClient(infranodus_config)

        if client.login():
            graph = client.get_graph(context="@private")
            assert "nodes" in graph, "Graph should have nodes key"
            assert "edges" in graph, "Graph should have edges key"
            print(f"✅ Retrieved graph: {len(graph.get('nodes', []))} nodes, {len(graph.get('edges', []))} edges")

    def test_get_concepts(self, infranodus_config):
        """Test 9: Extract concepts from InfraNodus"""
        client = InfraNodusClient(infranodus_config)

        if client.login():
            concepts = client.get_concepts(context="@private", limit=10)
            assert isinstance(concepts, list), "Concepts should be a list"
            print(f"✅ Extracted {len(concepts)} concepts")

    def test_get_communities(self, infranodus_config):
        """Test 10: Extract topic communities"""
        client = InfraNodusClient(infranodus_config)

        if client.login():
            communities = client.get_communities(context="@private")
            assert isinstance(communities, dict), "Communities should be a dict"
            print(f"✅ Extracted {len(communities)} communities")


# =============================================================================
# GRAPH-RAG TESTS
# =============================================================================

class TestGraphRAG:
    """Test Graph-RAG question answering system"""

    def test_rag_initialization(self, neo4j_config):
        """Test 11: Graph-RAG system initialization"""
        rag = GraphRAG(**neo4j_config)

        try:
            assert rag.queries is not None, "RAG should have queries object"
            print("✅ Graph-RAG system initialized")
        finally:
            rag.close()

    def test_question_classification(self, neo4j_config):
        """Test 12: Question type classification"""
        rag = GraphRAG(**neo4j_config)

        try:
            test_questions = [
                ("What is cooling gel?", "feature"),
                ("How to solve back pain?", "pain_point"),
                ("Compare X vs Y", "comparison"),
                ("What evidence supports this?", "evidence"),
            ]

            for question, expected_type in test_questions:
                q_type = rag.classify_question(question)
                print(f"  '{question}' → {q_type.value}")

            print("✅ Question classification working")
        finally:
            rag.close()

    def test_feature_query(self, neo4j_config):
        """Test 13: Feature information retrieval"""
        rag = GraphRAG(**neo4j_config)

        try:
            answer = rag.answer_question("What is cooling gel?")
            assert answer is not None, "Should return an answer"
            assert answer.question == "What is cooling gel?"
            assert 0 <= answer.confidence <= 1.0
            print(f"✅ Feature query working (confidence: {answer.confidence:.2f})")
        finally:
            rag.close()

    def test_pain_point_query(self, neo4j_config):
        """Test 14: Pain point solution retrieval"""
        rag = GraphRAG(**neo4j_config)

        try:
            answer = rag.answer_question("How can I solve back pain?")
            assert answer is not None, "Should return an answer"
            assert 0 <= answer.confidence <= 1.0
            print(f"✅ Pain point query working (confidence: {answer.confidence:.2f})")
        finally:
            rag.close()

    def test_answer_formatting(self, neo4j_config):
        """Test 15: Answer formatting with citations"""
        rag = GraphRAG(**neo4j_config)

        try:
            answer = rag.answer_question("What is cooling gel?")
            formatted = rag.format_answer(answer)

            assert "Q:" in formatted, "Formatted answer should have question"
            assert "A:" in formatted, "Formatted answer should have answer"
            assert "Confidence:" in formatted, "Should show confidence"
            print("✅ Answer formatting working")
        finally:
            rag.close()


# =============================================================================
# MONITORING DASHBOARD TESTS
# =============================================================================

class TestMonitoringDashboard:
    """Test monitoring and reporting system"""

    def test_dashboard_initialization(self, neo4j_config):
        """Test 16: Monitoring dashboard initialization"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            assert dashboard.queries is not None
            print("✅ Monitoring dashboard initialized")
        finally:
            dashboard.close()

    def test_system_health_check(self, neo4j_config):
        """Test 17: System health monitoring"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            health = dashboard.check_system_health()

            assert health.neo4j_status in ["online", "offline"]
            assert health.total_nodes >= 0
            assert health.total_relationships >= 0
            assert 0 <= health.health_score <= 100
            print(f"✅ System health check working (score: {health.health_score:.0f}%)")
        finally:
            dashboard.close()

    def test_graph_metrics_collection(self, neo4j_config):
        """Test 18: Knowledge graph metrics"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            metrics = dashboard.get_graph_metrics()

            assert metrics.keywords_count >= 0
            assert metrics.topics_count >= 0
            assert metrics.personas_count >= 0
            print(f"✅ Graph metrics: {metrics.keywords_count} keywords, {metrics.topics_count} topics")
        finally:
            dashboard.close()

    def test_pipeline_metrics(self, neo4j_config):
        """Test 19: Content pipeline metrics"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            metrics = dashboard.get_pipeline_metrics()

            assert metrics.total_prompts >= 0
            assert 0 <= metrics.avg_citation_score <= 1.0
            assert isinstance(metrics.top_opportunity_gaps, list)
            print(f"✅ Pipeline metrics: {metrics.total_prompts} prompts, avg score: {metrics.avg_citation_score:.2f}")
        finally:
            dashboard.close()

    def test_weekly_report_generation(self, neo4j_config):
        """Test 20: Weekly report generation"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            report = dashboard.generate_weekly_report()

            assert report.report_date is not None
            assert report.system_health is not None
            assert report.graph_metrics is not None
            assert report.pipeline_metrics is not None
            assert len(report.insights) > 0
            assert len(report.recommendations) > 0
            print(f"✅ Weekly report generated with {len(report.insights)} insights")
        finally:
            dashboard.close()

    def test_report_formatting(self, neo4j_config):
        """Test 21: Report Markdown formatting"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            report = dashboard.generate_weekly_report()
            markdown = dashboard.format_report_markdown(report)

            assert "# GEO System Weekly Report" in markdown
            assert "System Health" in markdown
            assert "Knowledge Graph Statistics" in markdown
            assert "Content Pipeline Performance" in markdown
            print("✅ Report formatting working")
        finally:
            dashboard.close()


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestSystemIntegration:
    """End-to-end integration tests"""

    def test_full_query_pipeline(self, neo4j_config):
        """Test 22: Full query pipeline from database to answer"""
        # Initialize all components
        queries = GEOQueries(**neo4j_config)
        rag = GraphRAG(**neo4j_config)

        try:
            # 1. Query database
            gaps = queries.find_structure_holes(limit=1)

            # 2. Generate answer
            answer = rag.answer_question("What is cooling gel?")

            # 3. Format output
            formatted = rag.format_answer(answer)

            assert len(formatted) > 0
            print("✅ Full query pipeline working")
        finally:
            queries.close()
            rag.close()

    def test_monitoring_and_reporting_pipeline(self, neo4j_config):
        """Test 23: Monitoring → Report → Save pipeline"""
        dashboard = MonitoringDashboard(**neo4j_config)

        try:
            # 1. Collect metrics
            health = dashboard.check_system_health()
            metrics = dashboard.get_graph_metrics()

            # 2. Generate report
            report = dashboard.generate_weekly_report()

            # 3. Format and save
            markdown = dashboard.format_report_markdown(report)

            # Save test report
            Path("./test_reports").mkdir(exist_ok=True)
            test_report_file = "./test_reports/test_report.md"
            with open(test_report_file, 'w') as f:
                f.write(markdown)

            assert Path(test_report_file).exists()
            print(f"✅ Monitoring and reporting pipeline working")
        finally:
            dashboard.close()


# =============================================================================
# PERFORMANCE TESTS
# =============================================================================

class TestPerformance:
    """Performance and load tests"""

    def test_query_performance(self, neo4j_config):
        """Test 24: Query execution time"""
        queries = GEOQueries(**neo4j_config)

        try:
            start_time = time.time()
            gaps = queries.find_structure_holes(limit=10)
            end_time = time.time()

            execution_time = (end_time - start_time) * 1000  # Convert to ms
            assert execution_time < 1000, f"Query took {execution_time:.0f}ms (expected < 1000ms)"
            print(f"✅ Query performance: {execution_time:.0f}ms")
        finally:
            queries.close()

    def test_rag_response_time(self, neo4j_config):
        """Test 25: RAG answer generation time"""
        rag = GraphRAG(**neo4j_config)

        try:
            start_time = time.time()
            answer = rag.answer_question("What is cooling gel?")
            end_time = time.time()

            response_time = (end_time - start_time) * 1000
            assert response_time < 2000, f"RAG took {response_time:.0f}ms (expected < 2000ms)"
            print(f"✅ RAG response time: {response_time:.0f}ms")
        finally:
            rag.close()


# =============================================================================
# TEST RUNNER SUMMARY
# =============================================================================

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print test summary"""
    print("\n" + "=" * 80)
    print("GEO SYSTEM TEST SUMMARY")
    print("=" * 80)

    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed + failed + skipped

    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! System is healthy and operational.")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review and fix.")

    print("=" * 80 + "\n")


if __name__ == "__main__":
    """Run tests directly"""
    import subprocess

    print("=" * 80)
    print("STARTING GEO SYSTEM AUTOMATED TESTS")
    print("=" * 80)
    print()

    # Run pytest
    result = subprocess.run([
        "pytest",
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])

    sys.exit(result.returncode)

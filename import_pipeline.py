"""
InfraNodus to Neo4j Import Pipeline
====================================

Imports data from InfraNodus into Neo4j knowledge graph.
Converts co-occurrence networks, keywords, and structure holes into graph nodes and relationships.

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

import sys
from typing import List, Dict, Any
from datetime import datetime
import logging
from neo4j import GraphDatabase
from infranodus_client import InfraNodusClient, InfraNodusConfig, Concept, Gap

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Neo4jImporter:
    """
    Imports InfraNodus data into Neo4j graph database
    """

    def __init__(self, uri: str, username: str, password: str):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        logger.info(f"Connected to Neo4j at {uri}")

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
        logger.info("Neo4j connection closed")

    def _execute_query(self, query: str, parameters: Dict[str, Any] = None):
        """Execute a Cypher query"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    def import_keywords(self, concepts: List[Concept]) -> int:
        """
        Import keywords as Keyword nodes in Neo4j

        Args:
            concepts: List of Concept objects from InfraNodus

        Returns:
            Number of keywords imported
        """
        query = """
        UNWIND $concepts AS concept
        MERGE (k:Keyword {name: concept.name})
        SET k.betweenness = concept.betweenness,
            k.degree = concept.degree,
            k.community = concept.community,
            k.last_updated = datetime()
        RETURN count(k) AS imported
        """

        concepts_data = [
            {
                "name": c.name,
                "betweenness": c.betweenness,
                "degree": c.degree,
                "community": c.community or "uncategorized"
            }
            for c in concepts
        ]

        result = self._execute_query(query, {"concepts": concepts_data})
        count = result[0]["imported"] if result else 0
        logger.info(f"Imported {count} keywords")
        return count

    def import_topic_clusters(self, communities: Dict[str, List[str]]) -> int:
        """
        Import topic clusters (communities) as TopicCluster nodes

        Args:
            communities: Dict mapping community names to keyword lists

        Returns:
            Number of clusters imported
        """
        query = """
        UNWIND $clusters AS cluster
        MERGE (tc:TopicCluster {name: cluster.name})
        SET tc.size = cluster.size,
            tc.modularity = cluster.modularity,
            tc.last_updated = datetime()
        RETURN count(tc) AS imported
        """

        clusters_data = [
            {
                "name": name,
                "size": len(keywords),
                "modularity": 0.0  # Will be calculated later
            }
            for name, keywords in communities.items()
        ]

        result = self._execute_query(query, {"clusters": clusters_data})
        count = result[0]["imported"] if result else 0
        logger.info(f"Imported {count} topic clusters")
        return count

    def link_keywords_to_clusters(self, concepts: List[Concept]) -> int:
        """
        Create BELONGS_TO relationships between Keywords and TopicClusters

        Args:
            concepts: List of Concept objects

        Returns:
            Number of relationships created
        """
        query = """
        UNWIND $concepts AS concept
        MATCH (k:Keyword {name: concept.name})
        MATCH (tc:TopicCluster {name: concept.community})
        MERGE (k)-[:BELONGS_TO]->(tc)
        RETURN count(*) AS linked
        """

        concepts_data = [
            {
                "name": c.name,
                "community": c.community or "uncategorized"
            }
            for c in concepts if c.community
        ]

        result = self._execute_query(query, {"concepts": concepts_data})
        count = result[0]["linked"] if result else 0
        logger.info(f"Created {count} BELONGS_TO relationships")
        return count

    def import_cooccurrences(self, graph_data: Dict[str, Any]) -> int:
        """
        Import co-occurrence relationships between keywords

        Args:
            graph_data: Graph data from InfraNodus (nodes and edges)

        Returns:
            Number of relationships imported
        """
        edges = graph_data.get("edges", [])

        query = """
        UNWIND $edges AS edge
        MATCH (k1:Keyword {name: edge.source})
        MATCH (k2:Keyword {name: edge.target})
        MERGE (k1)-[r:CO_OCCURS_WITH]->(k2)
        SET r.weight = edge.weight,
            r.last_updated = datetime()
        RETURN count(r) AS imported
        """

        edges_data = [
            {
                "source": edge.get("source"),
                "target": edge.get("target"),
                "weight": float(edge.get("weight", 1.0))
            }
            for edge in edges
        ]

        result = self._execute_query(query, {"edges": edges_data})
        count = result[0]["imported"] if result else 0
        logger.info(f"Imported {count} co-occurrence relationships")
        return count

    def import_gaps(self, gaps: List[Gap]) -> int:
        """
        Import structure holes (gaps) as Gap nodes

        Args:
            gaps: List of Gap objects from InfraNodus

        Returns:
            Number of gaps imported
        """
        query = """
        UNWIND $gaps AS gap
        MERGE (g:Gap {
            topic_a: gap.topic_a,
            topic_b: gap.topic_b
        })
        SET g.opportunity_score = gap.opportunity_score,
            g.discovered_at = datetime(),
            g.bridging_keywords = gap.bridging_keywords
        RETURN count(g) AS imported
        """

        gaps_data = [
            {
                "topic_a": g.topic_a,
                "topic_b": g.topic_b,
                "opportunity_score": g.opportunity_score,
                "bridging_keywords": g.bridging_keywords
            }
            for g in gaps
        ]

        result = self._execute_query(query, {"gaps": gaps_data})
        count = result[0]["imported"] if result else 0
        logger.info(f"Imported {count} structure holes")
        return count

    def generate_prompts_from_gaps(self, gaps: List[Gap]) -> int:
        """
        Generate Prompt nodes from structure holes

        Args:
            gaps: List of Gap objects

        Returns:
            Number of prompts generated
        """
        query = """
        UNWIND $prompts AS prompt
        MERGE (p:Prompt {text: prompt.text})
        SET p.type = prompt.type,
            p.priority = prompt.priority,
            p.gap_score = prompt.gap_score,
            p.generated_at = datetime()
        WITH p, prompt
        MATCH (g:Gap {topic_a: prompt.topic_a, topic_b: prompt.topic_b})
        MERGE (g)-[:SUGGESTS]->(p)
        RETURN count(p) AS generated
        """

        prompts_data = []
        for i, gap in enumerate(gaps):
            # Generate question-style prompt
            prompt_text = f"How are {gap.topic_a} and {gap.topic_b} related?"
            prompts_data.append({
                "text": prompt_text,
                "type": "exploratory",
                "priority": min(i + 1, 10),
                "gap_score": gap.opportunity_score,
                "topic_a": gap.topic_a,
                "topic_b": gap.topic_b
            })

        result = self._execute_query(query, {"prompts": prompts_data})
        count = result[0]["generated"] if result else 0
        logger.info(f"Generated {count} prompts from gaps")
        return count

    def import_full_dataset(self, context: str = "@private") -> Dict[str, int]:
        """
        Import complete dataset from InfraNodus to Neo4j

        Args:
            context: InfraNodus context to import

        Returns:
            Dict with import statistics
        """
        logger.info(f"Starting full import for context: {context}")
        stats = {}

        # Initialize InfraNodus client
        infranodus = InfraNodusClient()
        if not infranodus.login():
            logger.error("Failed to authenticate with InfraNodus")
            return stats

        try:
            # Step 1: Import concepts (keywords)
            logger.info("Step 1: Importing keywords...")
            concepts = infranodus.get_concepts(context, limit=200)
            stats["keywords"] = self.import_keywords(concepts)

            # Step 2: Import topic clusters
            logger.info("Step 2: Importing topic clusters...")
            communities = infranodus.get_communities(context)
            stats["clusters"] = self.import_topic_clusters(communities)

            # Step 3: Link keywords to clusters
            logger.info("Step 3: Linking keywords to clusters...")
            stats["cluster_links"] = self.link_keywords_to_clusters(concepts)

            # Step 4: Import co-occurrences
            logger.info("Step 4: Importing co-occurrence network...")
            graph_data = infranodus.get_graph(context)
            stats["cooccurrences"] = self.import_cooccurrences(graph_data)

            # Step 5: Import structure holes
            logger.info("Step 5: Importing structure holes (gaps)...")
            gaps = infranodus.get_gaps(context)
            stats["gaps"] = self.import_gaps(gaps)

            # Step 6: Generate prompts from gaps
            logger.info("Step 6: Generating prompts from gaps...")
            stats["prompts"] = self.generate_prompts_from_gaps(gaps)

            logger.info("Import completed successfully!")
            logger.info(f"Statistics: {stats}")

            return stats

        except Exception as e:
            logger.error(f"Import failed: {str(e)}")
            raise


def main():
    """Main execution function"""
    # Neo4j connection details
    NEO4J_URI = "neo4j://localhost:7688"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "claude_neo4j_2025"

    # InfraNodus context to import
    CONTEXT = "@private"

    try:
        # Initialize importer
        importer = Neo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

        # Run full import
        stats = importer.import_full_dataset(CONTEXT)

        # Print summary
        print("\n" + "=" * 60)
        print("IMPORT SUMMARY")
        print("=" * 60)
        print(f"Keywords imported:        {stats.get('keywords', 0)}")
        print(f"Topic clusters created:   {stats.get('clusters', 0)}")
        print(f"Cluster links created:    {stats.get('cluster_links', 0)}")
        print(f"Co-occurrences imported:  {stats.get('cooccurrences', 0)}")
        print(f"Structure holes imported: {stats.get('gaps', 0)}")
        print(f"Prompts generated:        {stats.get('prompts', 0)}")
        print("=" * 60)

        # Close connection
        importer.close()

    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

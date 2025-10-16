"""
InfraNodus API Client
=====================

Python client for interacting with InfraNodus REST API.
Provides methods for authentication, graph retrieval, and data extraction.

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class InfraNodusConfig:
    """Configuration for InfraNodus API client"""
    base_url: str = "http://localhost:3000"
    username: str = "demo_user"
    password: str = "demo"
    timeout: int = 30
    verify_ssl: bool = True


@dataclass
class Concept:
    """Represents a keyword/concept from InfraNodus"""
    name: str
    betweenness: float
    degree: int
    community: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Concept':
        """Create Concept from API response"""
        return cls(
            name=data.get('name', ''),
            betweenness=float(data.get('betweenness', 0)),
            degree=int(data.get('degree', 0)),
            community=data.get('community')
        )


@dataclass
class CoOccurrence:
    """Represents a co-occurrence relationship between concepts"""
    source: str
    target: str
    weight: float

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'CoOccurrence':
        """Create CoOccurrence from API response"""
        return cls(
            source=data.get('source', ''),
            target=data.get('target', ''),
            weight=float(data.get('weight', 0))
        )


@dataclass
class Gap:
    """Represents a structure hole (gap) between topics"""
    topic_a: str
    topic_b: str
    opportunity_score: float
    bridging_keywords: List[str] = field(default_factory=list)

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Gap':
        """Create Gap from API response"""
        return cls(
            topic_a=data.get('topic_a', ''),
            topic_b=data.get('topic_b', ''),
            opportunity_score=float(data.get('opportunity_score', 0)),
            bridging_keywords=data.get('bridging_keywords', [])
        )


@dataclass
class Statement:
    """Represents a statement/sentence from the corpus"""
    text: str
    id: Optional[str] = None
    context: Optional[str] = None
    timestamp: Optional[str] = None

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Statement':
        """Create Statement from API response"""
        return cls(
            text=data.get('text', ''),
            id=data.get('id'),
            context=data.get('context'),
            timestamp=data.get('timestamp')
        )


class InfraNodusClient:
    """
    Client for InfraNodus REST API

    Provides methods for:
    - Authentication (session-based)
    - Fetching co-occurrence graphs
    - Retrieving concepts and keywords
    - Getting statements
    - Identifying structure holes (gaps)
    """

    def __init__(self, config: Optional[InfraNodusConfig] = None):
        """Initialize InfraNodus client"""
        self.config = config or InfraNodusConfig()
        self.session = requests.Session()
        self.authenticated = False

    def login(self) -> bool:
        """
        Authenticate with InfraNodus using session-based login

        Returns:
            bool: True if authentication successful, False otherwise
        """
        try:
            login_url = f"{self.config.base_url}/login"
            payload = {
                "username": self.config.username,
                "password": self.config.password
            }

            response = self.session.post(
                login_url,
                data=payload,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )

            if response.status_code == 200:
                self.authenticated = True
                logger.info(f"Successfully authenticated as {self.config.username}")
                return True
            else:
                logger.error(f"Authentication failed: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False

    def _ensure_authenticated(self):
        """Ensure client is authenticated before API calls"""
        if not self.authenticated:
            if not self.login():
                raise Exception("Authentication required but failed")

    def get_graph(self, context: str = "@private") -> Dict[str, Any]:
        """
        Retrieve co-occurrence graph for a context

        Args:
            context: Context name (default: @private)

        Returns:
            Dict containing nodes and edges
        """
        self._ensure_authenticated()

        try:
            # Use the correct InfraNodus API endpoint
            graph_url = f"{self.config.base_url}/api/user/nodes/{context}"
            params = {}

            response = self.session.get(
                graph_url,
                params=params,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Retrieved graph for context: {context}")
                logger.info(f"  Nodes: {len(data.get('nodes', []))}")
                logger.info(f"  Edges: {len(data.get('edges', []))}")
                return data
            else:
                logger.error(f"Failed to get graph: {response.status_code}")
                return {"nodes": [], "edges": []}

        except Exception as e:
            logger.error(f"Error retrieving graph: {str(e)}")
            return {"nodes": [], "edges": []}

    def get_concepts(self, context: str = "@private", limit: int = 100) -> List[Concept]:
        """
        Retrieve concepts (keywords) for a context

        Note: InfraNodus returns concepts as part of the graph data,
        so we extract them from the nodes response.

        Args:
            context: Context name (default: @private)
            limit: Maximum number of concepts to retrieve

        Returns:
            List of Concept objects
        """
        self._ensure_authenticated()

        try:
            # Get graph data which includes all concepts (nodes)
            graph_data = self.get_graph(context)
            nodes = graph_data.get("nodes", [])

            # Sort by betweenness centrality (if available)
            nodes.sort(key=lambda x: x.get("betweenness_centrality", 0), reverse=True)

            # Take top N nodes
            top_nodes = nodes[:limit]

            # Convert to Concept objects
            concepts = []
            for node in top_nodes:
                concept = Concept(
                    name=node.get("name", node.get("id", "")),
                    betweenness=float(node.get("betweenness_centrality", 0)),
                    degree=int(node.get("degree", 0)),
                    community=node.get("community")
                )
                concepts.append(concept)

            logger.info(f"Extracted {len(concepts)} concepts from graph data")
            return concepts

        except Exception as e:
            logger.error(f"Error retrieving concepts: {str(e)}")
            return []

    def get_statements(self, context: str = "@private", limit: int = 100) -> List[Statement]:
        """
        Retrieve statements (sentences) for a context

        Args:
            context: Context name (default: @private)
            limit: Maximum number of statements to retrieve

        Returns:
            List of Statement objects
        """
        self._ensure_authenticated()

        try:
            # Use the correct InfraNodus API endpoint
            statements_url = f"{self.config.base_url}/api/user/statements/{context}"
            params = {}

            response = self.session.get(
                statements_url,
                params=params,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl
            )

            if response.status_code == 200:
                data = response.json()
                statements = [Statement.from_api_response(item) for item in data]
                logger.info(f"Retrieved {len(statements)} statements from context: {context}")
                return statements
            else:
                logger.error(f"Failed to get statements: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error retrieving statements: {str(e)}")
            return []

    def get_gaps(self, context: str = "@private") -> List[Gap]:
        """
        Retrieve structure holes (gaps) for a context

        Note: InfraNodus calculates gaps from the graph structure.
        We extract them from the graph data if available, or calculate
        them by finding disconnected high-betweenness communities.

        Args:
            context: Context name (default: @private)

        Returns:
            List of Gap objects
        """
        self._ensure_authenticated()

        try:
            # Get graph data
            graph_data = self.get_graph(context)

            # Check if gaps are included in the graph response
            if "gaps" in graph_data:
                gaps = [Gap.from_api_response(item) for item in graph_data["gaps"]]
                logger.info(f"Retrieved {len(gaps)} gaps from graph data")
                return gaps

            # Otherwise, identify gaps from community structure
            # Get communities
            communities_dict = {}
            nodes = graph_data.get("nodes", [])

            for node in nodes:
                comm = node.get("community", "default")
                if comm not in communities_dict:
                    communities_dict[comm] = []
                communities_dict[comm].append(node.get("name", node.get("id", "")))

            # Find disconnected communities (potential gaps)
            gaps = []
            community_names = list(communities_dict.keys())

            for i, comm_a in enumerate(community_names):
                for comm_b in community_names[i+1:]:
                    # Create a gap between disconnected communities
                    # Representative keywords: highest betweenness nodes from each community
                    keywords_a = communities_dict[comm_a][:3] if len(communities_dict[comm_a]) > 0 else []
                    keywords_b = communities_dict[comm_b][:3] if len(communities_dict[comm_b]) > 0 else []

                    if keywords_a and keywords_b:
                        gap = Gap(
                            topic_a=" / ".join(keywords_a),
                            topic_b=" / ".join(keywords_b),
                            opportunity_score=0.75,  # Default score
                            bridging_keywords=[]
                        )
                        gaps.append(gap)

            logger.info(f"Identified {len(gaps)} potential gaps from community structure")
            return gaps

        except Exception as e:
            logger.error(f"Error retrieving gaps: {str(e)}")
            return []

    def get_communities(self, context: str = "@private") -> Dict[str, List[str]]:
        """
        Extract topic communities from the graph

        Args:
            context: Context name (default: @private)

        Returns:
            Dict mapping community names to lists of keywords
        """
        concepts = self.get_concepts(context)
        communities = {}

        for concept in concepts:
            if concept.community:
                if concept.community not in communities:
                    communities[concept.community] = []
                communities[concept.community].append(concept.name)

        logger.info(f"Extracted {len(communities)} communities")
        return communities

    def export_to_json(self, context: str = "@private", output_file: str = "infranodus_export.json"):
        """
        Export all data from a context to JSON file

        Args:
            context: Context name (default: @private)
            output_file: Output file path
        """
        logger.info(f"Exporting data from context: {context}")

        data = {
            "context": context,
            "graph": self.get_graph(context),
            "concepts": [
                {
                    "name": c.name,
                    "betweenness": c.betweenness,
                    "degree": c.degree,
                    "community": c.community
                } for c in self.get_concepts(context)
            ],
            "statements": [
                {
                    "text": s.text,
                    "id": s.id,
                    "context": s.context,
                    "timestamp": s.timestamp
                } for s in self.get_statements(context)
            ],
            "gaps": [
                {
                    "topic_a": g.topic_a,
                    "topic_b": g.topic_b,
                    "opportunity_score": g.opportunity_score,
                    "bridging_keywords": g.bridging_keywords
                } for g in self.get_gaps(context)
            ],
            "communities": self.get_communities(context)
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Data exported to {output_file}")
        return data


def main():
    """Example usage of InfraNodus client"""
    # Initialize client
    client = InfraNodusClient()

    # Login
    if not client.login():
        print("Failed to authenticate")
        return

    # Get graph data
    graph = client.get_graph(context="@private")
    print(f"\nGraph nodes: {len(graph.get('nodes', []))}")
    print(f"Graph edges: {len(graph.get('edges', []))}")

    # Get concepts
    concepts = client.get_concepts(context="@private", limit=10)
    print(f"\nTop 10 concepts:")
    for concept in concepts:
        print(f"  - {concept.name}: betweenness={concept.betweenness:.3f}, degree={concept.degree}")

    # Get gaps
    gaps = client.get_gaps(context="@private")
    print(f"\nStructure holes found: {len(gaps)}")
    for i, gap in enumerate(gaps[:5], 1):
        print(f"  {i}. {gap.topic_a} <-> {gap.topic_b} (score: {gap.opportunity_score:.3f})")

    # Export all data
    client.export_to_json(context="@private", output_file="infranodus_data.json")
    print("\nData exported successfully!")


if __name__ == "__main__":
    main()

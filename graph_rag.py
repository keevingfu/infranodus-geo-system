"""
Graph-RAG Question Answering System
====================================

Retrieval-Augmented Generation using Neo4j knowledge graph.
Answers user questions with citations to evidence and sources.

Features:
- Natural language question understanding
- Graph-based retrieval
- Evidence-backed answer generation
- Citation tracking and provenance

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from cypher_queries import GEOQueries

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionType(Enum):
    """Types of questions the system can answer"""
    FEATURE = "feature"  # "What is cooling gel?"
    PAIN_POINT = "pain_point"  # "How to solve back pain?"
    PRODUCT = "product"  # "Which mattress is best for..."
    COMPARISON = "comparison"  # "Compare X vs Y"
    EVIDENCE = "evidence"  # "What evidence supports..."
    HOW_TO = "how_to"  # "How does X work?"
    RECOMMENDATION = "recommendation"  # "What do you recommend for..."


@dataclass
class Citation:
    """Source citation for answer"""
    source: str
    url: Optional[str]
    credibility_score: float
    quote: Optional[str] = None


@dataclass
class Answer:
    """RAG answer with sources"""
    question: str
    answer_text: str
    citations: List[Citation]
    confidence: float
    graph_path: List[str]  # Path through graph used to answer


class GraphRAG:
    """
    Graph-based Retrieval-Augmented Generation system.

    Answers questions by:
    1. Classifying question type
    2. Querying knowledge graph
    3. Retrieving evidence
    4. Generating natural language answer with citations
    """

    def __init__(self, uri: str, username: str, password: str):
        """Initialize Graph-RAG system"""
        self.queries = GEOQueries(uri, username, password)
        logger.info("Graph-RAG system initialized")

    def close(self):
        """Close connections"""
        self.queries.close()

    # =========================================================================
    # QUESTION CLASSIFICATION
    # =========================================================================

    def classify_question(self, question: str) -> QuestionType:
        """
        Classify question type based on keywords and patterns.

        Args:
            question: User question text

        Returns:
            QuestionType enum
        """
        q_lower = question.lower()

        # Feature questions
        if any(word in q_lower for word in ["what is", "explain", "describe"]):
            return QuestionType.FEATURE

        # Pain point questions
        if any(word in q_lower for word in ["solve", "fix", "relieve", "help with", "pain"]):
            return QuestionType.PAIN_POINT

        # Comparison questions
        if any(word in q_lower for word in ["compare", "vs", "versus", "difference between"]):
            return QuestionType.COMPARISON

        # Evidence questions
        if any(word in q_lower for word in ["evidence", "prove", "support", "research", "study"]):
            return QuestionType.EVIDENCE

        # How-to questions
        if any(word in q_lower for word in ["how does", "how to", "how can"]):
            return QuestionType.HOW_TO

        # Recommendation questions
        if any(word in q_lower for word in ["recommend", "best", "which", "should i", "suggest"]):
            return QuestionType.RECOMMENDATION

        # Product questions (default)
        return QuestionType.PRODUCT

    # =========================================================================
    # GRAPH RETRIEVAL
    # =========================================================================

    def retrieve_feature_info(self, question: str) -> Dict[str, Any]:
        """Retrieve information about a feature from the graph"""
        query = """
        MATCH (f:Feature)
        WHERE toLower(f.name) CONTAINS toLower($keyword)
           OR toLower(f.description) CONTAINS toLower($keyword)

        // Get pain points this relieves
        OPTIONAL MATCH (f)-[:RELIEVED_BY]-(pp:PainPoint)

        // Get products implementing this
        OPTIONAL MATCH (f)-[:IMPLEMENTED_IN]->(product:Product)

        // Get claims and evidence
        OPTIONAL MATCH (claim:Claim)-[:ABOUT]->(f)
                       -[:SUPPORTED_BY]->(evidence:Evidence)

        RETURN f.name AS feature,
               f.description AS description,
               collect(DISTINCT pp.name) AS relieves,
               collect(DISTINCT product.name) AS products,
               collect(DISTINCT {
                   claim: claim.text,
                   source: evidence.source,
                   url: evidence.url,
                   credibility: evidence.credibility_score,
                   quote: evidence.quote
               }) AS evidence
        LIMIT 1
        """

        # Extract key terms from question
        keywords = [word for word in question.split() if len(word) > 3]
        for keyword in keywords:
            results = self.queries._execute_query(query, {"keyword": keyword})
            if results:
                return results[0]

        return {}

    def retrieve_pain_point_solution(self, question: str) -> Dict[str, Any]:
        """Retrieve solutions for a pain point"""
        query = """
        MATCH (pp:PainPoint)
        WHERE toLower(pp.name) CONTAINS toLower($keyword)
           OR toLower(pp.description) CONTAINS toLower($keyword)

        // Get features that relieve this
        OPTIONAL MATCH (pp)-[:RELIEVED_BY]->(feature:Feature)
                           -[:IMPLEMENTED_IN]->(product:Product)

        // Get claims and evidence
        OPTIONAL MATCH (claim:Claim)-[:ABOUT]->(pp)
                       -[:SUPPORTED_BY]->(evidence:Evidence)

        RETURN pp.name AS pain_point,
               pp.description AS description,
               pp.severity AS severity,
               pp.evidence_count AS reported_cases,
               collect(DISTINCT {
                   feature: feature.name,
                   product: product.name
               }) AS solutions,
               collect(DISTINCT {
                   claim: claim.text,
                   source: evidence.source,
                   url: evidence.url,
                   credibility: evidence.credibility_score
               }) AS evidence
        LIMIT 1
        """

        keywords = [word for word in question.split() if len(word) > 3]
        for keyword in keywords:
            results = self.queries._execute_query(query, {"keyword": keyword})
            if results:
                return results[0]

        return {}

    def retrieve_product_comparison(self, product1: str, product2: str) -> Dict[str, Any]:
        """Compare two products"""
        return self.queries.compare_product_features(product1, product2)

    def retrieve_evidence_for_claim(self, claim_keyword: str) -> Dict[str, Any]:
        """Retrieve evidence supporting a claim"""
        results = self.queries.verify_claim_with_evidence(claim_keyword)
        return results[0] if results else {}

    # =========================================================================
    # ANSWER GENERATION
    # =========================================================================

    def generate_feature_answer(self, data: Dict[str, Any]) -> Answer:
        """Generate answer for feature question"""
        if not data:
            return Answer(
                question="",
                answer_text="I don't have information about that feature in the knowledge graph.",
                citations=[],
                confidence=0.0,
                graph_path=[]
            )

        # Build answer text
        answer_parts = []
        answer_parts.append(f"{data['feature']} is a feature that {data.get('description', 'provides comfort and support')}.")

        if data.get('relieves'):
            relieves_list = ", ".join(data['relieves'][:3])
            answer_parts.append(f"It helps relieve {relieves_list}.")

        if data.get('products'):
            products_list = ", ".join(data['products'][:3])
            answer_parts.append(f"You can find this feature in {products_list}.")

        # Extract citations
        citations = []
        if data.get('evidence'):
            for ev in data['evidence']:
                if ev.get('source'):
                    citations.append(Citation(
                        source=ev['source'],
                        url=ev.get('url'),
                        credibility_score=ev.get('credibility', 0.5),
                        quote=ev.get('quote')
                    ))

        # Build graph path
        path = ["Feature"]
        if data.get('relieves'):
            path.append("PainPoint")
        if data.get('products'):
            path.append("Product")
        if citations:
            path.extend(["Claim", "Evidence"])

        return Answer(
            question="",
            answer_text=" ".join(answer_parts),
            citations=citations[:3],  # Top 3 citations
            confidence=min(1.0, len(citations) * 0.3 + 0.4),
            graph_path=path
        )

    def generate_pain_point_answer(self, data: Dict[str, Any]) -> Answer:
        """Generate answer for pain point question"""
        if not data:
            return Answer(
                question="",
                answer_text="I don't have specific solutions for that issue in the knowledge graph.",
                citations=[],
                confidence=0.0,
                graph_path=[]
            )

        # Build answer
        answer_parts = []
        severity = data.get('severity', 0)
        severity_text = "significant" if severity >= 7 else "moderate"
        answer_parts.append(f"{data['pain_point']} is a {severity_text} issue (severity: {severity}/10).")

        if data.get('reported_cases', 0) > 0:
            answer_parts.append(f"It has been reported {data['reported_cases']} times.")

        if data.get('solutions'):
            solutions = [s['feature'] for s in data['solutions'] if s.get('feature')][:3]
            if solutions:
                solutions_text = ", ".join(solutions)
                answer_parts.append(f"Solutions include: {solutions_text}.")

                # Add product recommendations
                products = [s['product'] for s in data['solutions'] if s.get('product')][:2]
                if products:
                    products_text = " or ".join(products)
                    answer_parts.append(f"You can find these features in {products_text}.")

        # Extract citations
        citations = []
        if data.get('evidence'):
            for ev in data['evidence']:
                if ev.get('source'):
                    citations.append(Citation(
                        source=ev['source'],
                        url=ev.get('url'),
                        credibility_score=ev.get('credibility', 0.5),
                        quote=None
                    ))

        return Answer(
            question="",
            answer_text=" ".join(answer_parts),
            citations=citations[:3],
            confidence=min(1.0, (len(data.get('solutions', [])) * 0.3 + len(citations) * 0.2 + 0.2)),
            graph_path=["PainPoint", "Feature", "Product", "Evidence"]
        )

    def generate_comparison_answer(self, data: Dict[str, Any]) -> Answer:
        """Generate answer for comparison question"""
        if not data or not data.get('unique_to_us'):
            return Answer(
                question="",
                answer_text="I don't have enough information to compare those products.",
                citations=[],
                confidence=0.3,
                graph_path=[]
            )

        answer_parts = []

        # Unique features
        if data.get('unique_to_us'):
            unique_list = ", ".join(data['unique_to_us'][:3])
            answer_parts.append(f"Unique features: {unique_list}.")

        if data.get('unique_to_competitor'):
            comp_list = ", ".join(data['unique_to_competitor'][:3])
            answer_parts.append(f"Competitor has: {comp_list}.")

        if data.get('shared_features'):
            shared_count = len(data['shared_features'])
            answer_parts.append(f"They share {shared_count} common features.")

        # Calculate advantage
        our_count = data.get('our_advantage_count', 0)
        their_count = data.get('their_advantage_count', 0)

        if our_count > their_count:
            answer_parts.append(f"Our product has {our_count} unique advantages vs {their_count} for the competitor.")
        elif their_count > our_count:
            answer_parts.append(f"The competitor has {their_count} unique features vs {our_count} for us.")
        else:
            answer_parts.append("Both products have similar feature counts.")

        return Answer(
            question="",
            answer_text=" ".join(answer_parts),
            citations=[],
            confidence=0.7,
            graph_path=["Product", "Feature"]
        )

    # =========================================================================
    # MAIN RAG PIPELINE
    # =========================================================================

    def answer_question(self, question: str) -> Answer:
        """
        Main RAG pipeline: classify → retrieve → generate answer.

        Args:
            question: User's natural language question

        Returns:
            Answer object with citations
        """
        logger.info(f"Answering question: {question}")

        # Step 1: Classify question
        q_type = self.classify_question(question)
        logger.info(f"Question type: {q_type.value}")

        # Step 2: Retrieve from graph
        if q_type == QuestionType.FEATURE or q_type == QuestionType.HOW_TO:
            data = self.retrieve_feature_info(question)
            answer = self.generate_feature_answer(data)

        elif q_type == QuestionType.PAIN_POINT:
            data = self.retrieve_pain_point_solution(question)
            answer = self.generate_pain_point_answer(data)

        elif q_type == QuestionType.COMPARISON:
            # Extract product names from question
            # Simplified: assume format "compare X vs Y" or "X or Y"
            products = [p.strip() for p in question.lower().replace(" vs ", " or ").split(" or ") if len(p.strip()) > 2]
            if len(products) >= 2:
                data = self.retrieve_product_comparison(products[0], products[1])
                answer = self.generate_comparison_answer(data)
            else:
                answer = Answer(
                    question=question,
                    answer_text="Please specify two products to compare.",
                    citations=[],
                    confidence=0.0,
                    graph_path=[]
                )

        elif q_type == QuestionType.EVIDENCE:
            # Extract claim keyword
            keywords = [w for w in question.split() if len(w) > 4]
            data = self.retrieve_evidence_for_claim(keywords[0] if keywords else "")
            answer = self.generate_feature_answer(data)

        elif q_type == QuestionType.RECOMMENDATION or q_type == QuestionType.PRODUCT:
            # Treat as pain point solution
            data = self.retrieve_pain_point_solution(question)
            answer = self.generate_pain_point_answer(data)

        else:
            answer = Answer(
                question=question,
                answer_text="I'm not sure how to answer that type of question yet.",
                citations=[],
                confidence=0.2,
                graph_path=[]
            )

        # Step 3: Add question to answer
        answer.question = question

        logger.info(f"Answer generated with confidence: {answer.confidence:.2f}")
        return answer

    def format_answer(self, answer: Answer) -> str:
        """
        Format answer with citations for display.

        Args:
            answer: Answer object

        Returns:
            Formatted text with citations
        """
        output = []
        output.append(f"Q: {answer.question}")
        output.append(f"\nA: {answer.answer_text}")

        if answer.citations:
            output.append("\n\n📚 Sources:")
            for i, citation in enumerate(answer.citations, 1):
                output.append(f"\n[{i}] {citation.source}")
                if citation.url:
                    output.append(f"    {citation.url}")
                if citation.credibility_score:
                    output.append(f"    Credibility: {citation.credibility_score:.2f}")
                if citation.quote:
                    output.append(f"    Quote: \"{citation.quote}\"")

        output.append(f"\n\n🔍 Graph path: {' → '.join(answer.graph_path)}")
        output.append(f"✅ Confidence: {answer.confidence:.0%}")

        return "".join(output)


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def main():
    """Demo Graph-RAG question answering"""

    # Initialize
    rag = GraphRAG(
        uri="neo4j://localhost:7688",
        username="neo4j",
        password="claude_neo4j_2025"
    )

    try:
        print("=" * 80)
        print("GRAPH-RAG QUESTION ANSWERING DEMO")
        print("=" * 80)

        # Example questions
        questions = [
            "What is cooling gel and how does it work?",
            "How can I solve back pain while sleeping?",
            "What evidence supports cooling gel effectiveness?",
            "Which mattress is best for hot sleepers?",
            "Compare SweetNight Breeze vs Purple Mattress"
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n{'=' * 80}")
            print(f"EXAMPLE {i}")
            print('=' * 80)

            answer = rag.answer_question(question)
            formatted = rag.format_answer(answer)
            print(formatted)
            print()

    finally:
        rag.close()


if __name__ == "__main__":
    main()

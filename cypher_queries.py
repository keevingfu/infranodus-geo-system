"""
Core Cypher Query Templates
============================

Essential queries for InfraNodus + Neo4j GEO system.
Implements 10 empowerment capabilities with optimized Cypher patterns.

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

from typing import Dict, List, Any, Optional
from neo4j import GraphDatabase
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GEOQueries:
    """
    Core query library for GEO Knowledge Graph operations.

    Capabilities:
    1. Structure hole identification (Gap Detection)
    2. Prompt prioritization
    3. Persona-Scenario-PainPoint matrix
    4. Evidence-based validation
    5. Citation-Ready scoring
    6. Content coverage analysis
    7. Competitive differentiation
    8. Topic evolution tracking
    9. Graph-RAG question answering
    10. Keyword bridging
    """

    def __init__(self, uri: str, username: str, password: str):
        """Initialize Neo4j connection"""
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        logger.info(f"GEOQueries initialized with Neo4j at {uri}")

    def close(self):
        """Close Neo4j connection"""
        self.driver.close()

    def _execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute Cypher query and return results"""
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return result.data()

    # =========================================================================
    # 1. STRUCTURE HOLE IDENTIFICATION (Gap Detection)
    # =========================================================================

    def find_structure_holes(self, min_opportunity_score: float = 0.7, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Identify structure holes between disconnected topic clusters.

        A structure hole exists when two topic clusters with high betweenness
        keywords have no or few direct connections.

        Args:
            min_opportunity_score: Minimum opportunity score threshold
            limit: Maximum number of gaps to return

        Returns:
            List of gaps with opportunity scores and bridging keywords
        """
        query = """
        // Find pairs of topic clusters
        MATCH (tc1:TopicCluster), (tc2:TopicCluster)
        WHERE id(tc1) < id(tc2)  // Avoid duplicates

        // Get representative keywords from each cluster (top by betweenness)
        OPTIONAL MATCH (k1:Keyword)-[:BELONGS_TO]->(tc1)
        WITH tc1, tc2, k1
        ORDER BY k1.betweenness DESC
        LIMIT 5
        WITH tc1, tc2, collect(k1) AS cluster1_keywords

        OPTIONAL MATCH (k2:Keyword)-[:BELONGS_TO]->(tc2)
        WITH tc1, tc2, cluster1_keywords, k2
        ORDER BY k2.betweenness DESC
        LIMIT 5
        WITH tc1, tc2, cluster1_keywords, collect(k2) AS cluster2_keywords

        // Check if there's a bridge between clusters
        OPTIONAL MATCH bridge = (tc1)-[:BRIDGES]-(tc2)

        // Calculate opportunity score based on:
        // - Lack of direct bridge (higher score)
        // - High modularity of both clusters (higher score)
        // - Size difference (balanced sizes = higher score)
        WITH tc1, tc2, bridge,
             cluster1_keywords, cluster2_keywords,
             tc1.modularity AS mod1,
             tc2.modularity AS mod2,
             tc1.size AS size1,
             tc2.size AS size2,
             CASE WHEN bridge IS NULL THEN 1.0 ELSE 0.3 END AS bridge_penalty

        WITH tc1, tc2, cluster1_keywords, cluster2_keywords,
             bridge_penalty * ((mod1 + mod2) / 2.0) *
             (1.0 - abs(size1 - size2) / (size1 + size2 + 1.0)) AS opportunity_score

        WHERE opportunity_score >= $min_score

        // Extract top keywords from each cluster for representation
        WITH tc1.name AS cluster_a,
             tc2.name AS cluster_b,
             opportunity_score,
             [k IN cluster1_keywords | k.name][0..3] AS keywords_a,
             [k IN cluster2_keywords | k.name][0..3] AS keywords_b

        RETURN cluster_a,
               cluster_b,
               keywords_a,
               keywords_b,
               opportunity_score
        ORDER BY opportunity_score DESC
        LIMIT $limit
        """

        results = self._execute_query(query, {
            "min_score": min_opportunity_score,
            "limit": limit
        })

        logger.info(f"Found {len(results)} structure holes")
        return results

    def find_keyword_gaps(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Find keyword pairs with high co-occurrence potential but low actual connection.

        Identifies keywords that:
        - Have high individual betweenness (important in network)
        - Belong to different communities
        - Have no or weak direct co-occurrence

        Returns:
            List of keyword gaps with opportunity scores
        """
        query = """
        // Find high-betweenness keywords from different communities
        MATCH (k1:Keyword), (k2:Keyword)
        WHERE id(k1) < id(k2)
          AND k1.community <> k2.community
          AND k1.betweenness > 0.5
          AND k2.betweenness > 0.5

        // Check existing co-occurrence strength
        OPTIONAL MATCH (k1)-[co:CO_OCCURS_WITH]-(k2)

        // Calculate gap score: high when keywords are important but not connected
        WITH k1, k2, co,
             (k1.betweenness + k2.betweenness) / 2.0 AS avg_importance,
             COALESCE(co.weight, 0.0) AS connection_strength

        WITH k1.name AS keyword_a,
             k2.name AS keyword_b,
             k1.community AS community_a,
             k2.community AS community_b,
             avg_importance * (1.0 - connection_strength) AS opportunity_score

        WHERE opportunity_score > 0.4

        RETURN keyword_a,
               keyword_b,
               community_a,
               community_b,
               opportunity_score
        ORDER BY opportunity_score DESC
        LIMIT $limit
        """

        results = self._execute_query(query, {"limit": limit})
        logger.info(f"Found {len(results)} keyword gaps")
        return results

    # =========================================================================
    # 2. PROMPT PRIORITIZATION
    # =========================================================================

    def rank_prompts_by_priority(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Rank prompts by综合 priority score considering:
        - Gap opportunity score
        - Pain point severity
        - Evidence availability
        - Current content coverage

        Returns:
            Prioritized list of prompts with scores
        """
        query = """
        MATCH (prompt:Prompt)

        // Get associated gap score
        OPTIONAL MATCH (gap:Gap)-[:SUGGESTS]->(prompt)
        WITH prompt, gap, gap.opportunity_score AS gap_score

        // Get associated pain point severity
        OPTIONAL MATCH (prompt)-[:ADDRESSES]->(pp:PainPoint)
        WITH prompt, gap_score, pp, pp.severity AS pain_severity

        // Count existing assets addressing this prompt
        OPTIONAL MATCH (asset:Asset)-[:DERIVES_FROM]->(:Brief)-[:GENERATED_FROM]->(prompt)
        WITH prompt, gap_score, pain_severity,
             count(DISTINCT asset) AS existing_assets

        // Calculate综合 priority score
        WITH prompt,
             COALESCE(gap_score, 0.5) AS gap_component,
             COALESCE(pain_severity, 5.0) / 10.0 AS pain_component,
             1.0 / (existing_assets + 1.0) AS novelty_component,
             prompt.priority AS base_priority

        WITH prompt.text AS prompt_text,
             prompt.type AS prompt_type,
             gap_component * 0.4 +
             pain_component * 0.3 +
             novelty_component * 0.2 +
             (base_priority / 10.0) * 0.1 AS final_score

        RETURN prompt_text,
               prompt_type,
               final_score
        ORDER BY final_score DESC
        LIMIT $limit
        """

        results = self._execute_query(query, {"limit": limit})
        logger.info(f"Ranked {len(results)} prompts")
        return results

    def generate_prompts_for_gaps(self, gap_ids: List[str] = None) -> List[Dict[str, Any]]:
        """
        Generate question prompts from structure holes.

        Args:
            gap_ids: Optional list of specific Gap IDs to process

        Returns:
            Generated prompts with metadata
        """
        query = """
        MATCH (gap:Gap)
        WHERE $gap_ids IS NULL OR gap.topic_a + ' <-> ' + gap.topic_b IN $gap_ids

        // Generate exploratory question
        WITH gap,
             'How are ' + gap.topic_a + ' and ' + gap.topic_b + ' connected?' AS question_prompt,
             'What solutions bridge ' + gap.topic_a + ' and ' + gap.topic_b + '?' AS solution_prompt

        RETURN gap.topic_a AS topic_a,
               gap.topic_b AS topic_b,
               gap.opportunity_score AS opportunity_score,
               question_prompt,
               solution_prompt
        ORDER BY gap.opportunity_score DESC
        """

        results = self._execute_query(query, {"gap_ids": gap_ids})
        logger.info(f"Generated {len(results)} prompts from gaps")
        return results

    # =========================================================================
    # 3. PERSONA-SCENARIO-PAINPOINT MATRIX
    # =========================================================================

    def get_persona_scenario_matrix(self) -> List[Dict[str, Any]]:
        """
        Build comprehensive Persona × Scenario × PainPoint matrix.

        Shows which personas experience which pain points in which scenarios,
        and what features address those pain points.

        Returns:
            Matrix data with personas, scenarios, pain points, and solutions
        """
        query = """
        MATCH (persona:Persona)-[:OCCURS_IN]->(scenario:Scenario)
              -[:SUFFERS]->(painpoint:PainPoint)

        // Find features that relieve this pain point
        OPTIONAL MATCH (painpoint)-[:RELIEVED_BY]->(feature:Feature)

        // Find products implementing those features
        OPTIONAL MATCH (feature)-[:IMPLEMENTED_IN]->(product:Product)

        // Count evidence supporting this pain point
        OPTIONAL MATCH (:Claim)-[:ABOUT]->(painpoint)
                       <-[:SUPPORTED_BY]-(evidence:Evidence)

        WITH persona, scenario, painpoint, feature, product,
             count(DISTINCT evidence) AS evidence_count

        RETURN persona.name AS persona,
               persona.priority AS persona_priority,
               scenario.name AS scenario,
               scenario.frequency AS frequency,
               painpoint.name AS pain_point,
               painpoint.severity AS severity,
               painpoint.evidence_count AS reported_count,
               evidence_count AS validated_evidence,
               collect(DISTINCT feature.name) AS relieving_features,
               collect(DISTINCT product.name) AS recommended_products
        ORDER BY persona_priority, severity DESC, frequency
        """

        results = self._execute_query(query)
        logger.info(f"Generated matrix with {len(results)} entries")
        return results

    def find_underserved_personas(self, min_severity: int = 7) -> List[Dict[str, Any]]:
        """
        Identify personas with high-severity pain points but limited solutions.

        Args:
            min_severity: Minimum pain point severity threshold

        Returns:
            Underserved persona-pain point combinations
        """
        query = """
        MATCH (persona:Persona)-[:OCCURS_IN]->(:Scenario)
              -[:SUFFERS]->(pp:PainPoint)
        WHERE pp.severity >= $min_severity

        // Count solutions available
        OPTIONAL MATCH (pp)-[:RELIEVED_BY]->(feature:Feature)
                           -[:IMPLEMENTED_IN]->(product:Product)

        WITH persona, pp,
             count(DISTINCT feature) AS feature_count,
             count(DISTINCT product) AS product_count

        WHERE feature_count < 2  // Less than 2 features addressing pain

        RETURN persona.name AS persona,
               persona.description AS description,
               pp.name AS pain_point,
               pp.severity AS severity,
               pp.evidence_count AS evidence_count,
               feature_count,
               product_count,
               'Underserved - needs more solutions' AS status
        ORDER BY severity DESC, evidence_count DESC
        """

        results = self._execute_query(query, {"min_severity": min_severity})
        logger.info(f"Found {len(results)} underserved personas")
        return results

    # =========================================================================
    # 4. EVIDENCE-BASED VALIDATION
    # =========================================================================

    def verify_claim_with_evidence(self, claim_text: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve claims and their supporting evidence.

        Args:
            claim_text: Optional filter for specific claim text

        Returns:
            Claims with evidence details and credibility scores
        """
        query = """
        MATCH (claim:Claim)
        WHERE $claim_text IS NULL OR claim.text CONTAINS $claim_text

        // Get supporting evidence
        MATCH (claim)-[:SUPPORTED_BY]->(evidence:Evidence)

        // Get what the claim is about
        OPTIONAL MATCH (claim)-[:ABOUT]->(subject)

        WITH claim, subject, evidence
        ORDER BY evidence.credibility_score DESC

        RETURN claim.text AS claim,
               claim.confidence AS confidence,
               claim.verification_status AS status,
               labels(subject)[0] AS subject_type,
               COALESCE(subject.name, 'N/A') AS subject_name,
               collect({
                   source: evidence.source,
                   url: evidence.url,
                   date: evidence.date,
                   credibility: evidence.credibility_score,
                   quote: evidence.quote
               }) AS supporting_evidence,
               avg(evidence.credibility_score) AS avg_credibility
        ORDER BY confidence DESC, avg_credibility DESC
        """

        results = self._execute_query(query, {"claim_text": claim_text})
        logger.info(f"Retrieved {len(results)} verified claims")
        return results

    def find_unsupported_claims(self, min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """
        Identify claims with high confidence but insufficient evidence.

        Args:
            min_confidence: Minimum confidence threshold

        Returns:
            Claims needing more evidence
        """
        query = """
        MATCH (claim:Claim)
        WHERE claim.confidence >= $min_confidence

        // Count supporting evidence
        OPTIONAL MATCH (claim)-[:SUPPORTED_BY]->(evidence:Evidence)

        WITH claim, count(evidence) AS evidence_count,
             avg(evidence.credibility_score) AS avg_credibility

        WHERE evidence_count < 2  // Less than 2 pieces of evidence

        // Get what the claim is about
        OPTIONAL MATCH (claim)-[:ABOUT]->(subject)

        RETURN claim.text AS claim,
               claim.confidence AS confidence,
               labels(subject)[0] AS subject_type,
               COALESCE(subject.name, 'Unknown') AS subject_name,
               evidence_count,
               COALESCE(avg_credibility, 0.0) AS avg_credibility,
               'Needs more evidence' AS recommendation
        ORDER BY confidence DESC, evidence_count ASC
        """

        results = self._execute_query(query, {"min_confidence": min_confidence})
        logger.info(f"Found {len(results)} claims needing more evidence")
        return results

    # =========================================================================
    # 5. CITATION-READY SCORE CALCULATION
    # =========================================================================

    def calculate_citation_ready_score(self, asset_id: str = None) -> List[Dict[str, Any]]:
        """
        Calculate Citation-Ready Score for assets.

        Formula: 0.6 × connectivity + 0.4 × evidence_strength

        Args:
            asset_id: Optional specific asset ID to score

        Returns:
            Assets with citation-ready scores and breakdown
        """
        query = """
        MATCH (asset:Asset)
        WHERE $asset_id IS NULL OR asset.id = $asset_id

        // Count connected entities (mentions)
        OPTIONAL MATCH (asset)-[:MENTIONS]->(mentioned)
        WITH asset, count(DISTINCT mentioned) AS mention_count

        // Trace back to claims and evidence
        OPTIONAL MATCH (asset)-[:DERIVES_FROM]->(:Brief)
                       -[:GENERATED_FROM]->(:Prompt)
                       -[:ADDRESSES]->(:PainPoint)
                       <-[:ABOUT]-(claim:Claim)
                       -[:SUPPORTED_BY]->(evidence:Evidence)

        WITH asset, mention_count,
             count(DISTINCT claim) AS claim_count,
             count(DISTINCT evidence) AS evidence_count,
             avg(evidence.credibility_score) AS avg_evidence_credibility

        // Calculate components
        WITH asset,
             mention_count / 10.0 AS connectivity_score,  // Normalize to 0-1
             (evidence_count / 5.0) * COALESCE(avg_evidence_credibility, 0.5) AS evidence_score,
             mention_count,
             claim_count,
             evidence_count

        // Final citation-ready score
        WITH asset,
             0.6 * connectivity_score + 0.4 * evidence_score AS citation_ready_score,
             connectivity_score,
             evidence_score,
             mention_count,
             claim_count,
             evidence_count

        // Update asset node with score
        SET asset.citation_ready_score = citation_ready_score

        RETURN asset.id AS asset_id,
               asset.type AS type,
               asset.url AS url,
               citation_ready_score,
               connectivity_score,
               evidence_score,
               mention_count,
               claim_count,
               evidence_count,
               CASE
                   WHEN citation_ready_score >= 0.8 THEN 'Excellent'
                   WHEN citation_ready_score >= 0.6 THEN 'Good'
                   WHEN citation_ready_score >= 0.4 THEN 'Fair'
                   ELSE 'Needs Improvement'
               END AS quality_rating
        ORDER BY citation_ready_score DESC
        """

        results = self._execute_query(query, {"asset_id": asset_id})
        logger.info(f"Calculated citation-ready scores for {len(results)} assets")
        return results

    def get_low_quality_assets(self, max_score: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find assets with low citation-ready scores needing improvement.

        Args:
            max_score: Maximum score threshold

        Returns:
            Low-quality assets with improvement recommendations
        """
        query = """
        MATCH (asset:Asset)
        WHERE asset.citation_ready_score < $max_score
           OR asset.citation_ready_score IS NULL

        // Diagnose issues
        OPTIONAL MATCH (asset)-[:MENTIONS]->(mentioned)
        WITH asset, count(mentioned) AS mentions

        OPTIONAL MATCH (asset)-[:DERIVES_FROM]->(:Brief)
                       -[:GENERATED_FROM]->(:Prompt)
                       -[:ADDRESSES]->(:PainPoint)
                       <-[:ABOUT]-(claim:Claim)
        WITH asset, mentions, count(claim) AS claims

        WITH asset, mentions, claims,
             CASE
                 WHEN mentions < 3 THEN 'Add more product/feature mentions'
                 WHEN claims < 2 THEN 'Add more claims with evidence'
                 ELSE 'Improve evidence quality'
             END AS recommendation

        RETURN asset.id AS asset_id,
               asset.type AS type,
               asset.url AS url,
               COALESCE(asset.citation_ready_score, 0.0) AS current_score,
               mentions,
               claims,
               recommendation
        ORDER BY current_score ASC
        """

        results = self._execute_query(query, {"max_score": max_score})
        logger.info(f"Found {len(results)} low-quality assets")
        return results

    # =========================================================================
    # 6. CONTENT COVERAGE ANALYSIS
    # =========================================================================

    def analyze_prompt_coverage(self) -> Dict[str, Any]:
        """
        Analyze which prompts have been addressed by content.

        Returns:
            Coverage statistics and gaps
        """
        query = """
        // Total prompts
        MATCH (prompt:Prompt)
        WITH count(prompt) AS total_prompts

        // Prompts with briefs
        MATCH (prompt:Prompt)<-[:GENERATED_FROM]-(brief:Brief)
        WITH total_prompts, count(DISTINCT prompt) AS prompts_with_briefs

        // Prompts with published assets
        MATCH (prompt:Prompt)<-[:GENERATED_FROM]-(:Brief)
              <-[:DERIVES_FROM]-(asset:Asset)
        WITH total_prompts, prompts_with_briefs,
             count(DISTINCT prompt) AS prompts_with_assets

        RETURN total_prompts,
               prompts_with_briefs,
               prompts_with_assets,
               total_prompts - prompts_with_assets AS uncovered_prompts,
               toFloat(prompts_with_assets) / total_prompts AS coverage_rate
        """

        results = self._execute_query(query)
        if results:
            logger.info(f"Coverage rate: {results[0]['coverage_rate']:.1%}")
        return results[0] if results else {}

    def find_uncovered_high_priority_prompts(self, min_priority: int = 7) -> List[Dict[str, Any]]:
        """
        Find high-priority prompts without content coverage.

        Args:
            min_priority: Minimum priority threshold

        Returns:
            Uncovered high-priority prompts
        """
        query = """
        MATCH (prompt:Prompt)
        WHERE prompt.priority >= $min_priority

        // Check if prompt has any assets
        OPTIONAL MATCH (prompt)<-[:GENERATED_FROM]-(:Brief)
                       <-[:DERIVES_FROM]-(asset:Asset)

        WITH prompt, count(asset) AS asset_count
        WHERE asset_count = 0

        // Get associated pain points
        OPTIONAL MATCH (prompt)-[:ADDRESSES]->(pp:PainPoint)

        // Get associated personas
        OPTIONAL MATCH (prompt)-[:TARGETS]->(persona:Persona)

        RETURN prompt.text AS prompt_text,
               prompt.type AS type,
               prompt.priority AS priority,
               prompt.gap_score AS gap_score,
               collect(DISTINCT pp.name) AS pain_points,
               collect(DISTINCT persona.name) AS target_personas,
               'High priority - needs content' AS status
        ORDER BY priority DESC, gap_score DESC
        """

        results = self._execute_query(query, {"min_priority": min_priority})
        logger.info(f"Found {len(results)} uncovered high-priority prompts")
        return results

    # =========================================================================
    # 7. COMPETITIVE DIFFERENTIATION
    # =========================================================================

    def compare_product_features(self, our_product: str, competitor_product: str) -> Dict[str, Any]:
        """
        Compare features between our product and competitor.

        Args:
            our_product: Our product name
            competitor_product: Competitor product name

        Returns:
            Feature comparison with unique and shared features
        """
        query = """
        // Get our product features
        MATCH (our:Product {name: $our_product})
              <-[:IMPLEMENTED_IN]-(our_features:Feature)
        WITH collect(our_features.name) AS our_feature_list,
             collect(our_features) AS our_features_full

        // Get competitor features
        MATCH (comp:Product {name: $competitor_product})
              <-[:IMPLEMENTED_IN]-(comp_features:Feature)
        WITH our_feature_list, our_features_full,
             collect(comp_features.name) AS comp_feature_list,
             collect(comp_features) AS comp_features_full

        // Find unique and shared features
        WITH our_feature_list, comp_feature_list,
             [f IN our_feature_list WHERE NOT f IN comp_feature_list] AS unique_to_us,
             [f IN comp_feature_list WHERE NOT f IN our_feature_list] AS unique_to_competitor,
             [f IN our_feature_list WHERE f IN comp_feature_list] AS shared_features

        RETURN unique_to_us,
               unique_to_competitor,
               shared_features,
               size(unique_to_us) AS our_advantage_count,
               size(unique_to_competitor) AS their_advantage_count,
               size(shared_features) AS parity_count
        """

        results = self._execute_query(query, {
            "our_product": our_product,
            "competitor_product": competitor_product
        })

        if results:
            logger.info(f"Comparison: {results[0]['our_advantage_count']} unique features vs {results[0]['their_advantage_count']} competitor unique")
        return results[0] if results else {}

    def find_differentiation_opportunities(self, our_brand: str = "SweetNight") -> List[Dict[str, Any]]:
        """
        Find pain points where our brand has unique solutions.

        Args:
            our_brand: Our brand name

        Returns:
            Differentiation opportunities
        """
        query = """
        // Find pain points we address
        MATCH (:Product {brand: $our_brand})
              <-[:IMPLEMENTED_IN]-(feature:Feature)
              -[:RELIEVED_BY]->(pp:PainPoint)
        WITH pp, collect(DISTINCT feature.name) AS our_solutions

        // Find if competitors also address this pain point
        MATCH (comp_product:Product)
        WHERE comp_product.brand <> $our_brand
        OPTIONAL MATCH (comp_product)<-[:IMPLEMENTED_IN]-(comp_feature:Feature)
                       -[:RELIEVED_BY]->(pp)

        WITH pp, our_solutions,
             collect(DISTINCT comp_feature.name) AS competitor_solutions,
             count(DISTINCT comp_product) AS competitor_count

        WHERE competitor_count < 2  // Few competitors address this

        RETURN pp.name AS pain_point,
               pp.severity AS severity,
               pp.evidence_count AS evidence_count,
               our_solutions,
               competitor_solutions,
               competitor_count,
               'Differentiation opportunity' AS status
        ORDER BY severity DESC, evidence_count DESC
        """

        results = self._execute_query(query, {"our_brand": our_brand})
        logger.info(f"Found {len(results)} differentiation opportunities")
        return results

    # =========================================================================
    # 8. TOPIC EVOLUTION TRACKING
    # =========================================================================

    def track_keyword_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Track keyword importance evolution over time.

        Note: Requires timestamp data on keyword updates.

        Args:
            days: Number of days to look back

        Returns:
            Keyword trends with growth indicators
        """
        query = """
        // This query assumes keywords have a `last_updated` timestamp
        // and historical betweenness values stored

        MATCH (k:Keyword)
        WHERE k.last_updated >= datetime() - duration({days: $days})

        WITH k,
             k.betweenness AS current_betweenness,
             k.degree AS current_degree

        // Note: In production, you'd compare with historical snapshots
        // For now, we show current high-importance keywords
        WHERE current_betweenness > 0.5

        RETURN k.name AS keyword,
               k.community AS community,
               current_betweenness AS betweenness,
               current_degree AS degree,
               k.last_updated AS last_updated,
               'High importance' AS status
        ORDER BY current_betweenness DESC
        LIMIT 20
        """

        results = self._execute_query(query, {"days": days})
        logger.info(f"Tracked {len(results)} trending keywords")
        return results

    def detect_emerging_topics(self, min_growth: float = 0.2) -> List[Dict[str, Any]]:
        """
        Detect emerging topic clusters with growing keyword counts.

        Args:
            min_growth: Minimum growth rate threshold

        Returns:
            Emerging topics
        """
        query = """
        MATCH (tc:TopicCluster)<-[:BELONGS_TO]-(k:Keyword)

        WITH tc,
             count(k) AS keyword_count,
             avg(k.betweenness) AS avg_importance,
             sum(k.degree) AS total_connections

        WHERE keyword_count >= 3
          AND avg_importance > 0.4

        RETURN tc.name AS topic,
               keyword_count,
               avg_importance,
               total_connections,
               tc.modularity AS modularity,
               'Emerging topic' AS status
        ORDER BY avg_importance DESC, keyword_count DESC
        """

        results = self._execute_query(query, {"min_growth": min_growth})
        logger.info(f"Detected {len(results)} emerging topics")
        return results

    # =========================================================================
    # 9. GRAPH-RAG QUESTION ANSWERING
    # =========================================================================

    def answer_question_with_graph(self, question: str, question_type: str = "feature") -> Dict[str, Any]:
        """
        Answer questions using graph structure and evidence.

        Args:
            question: User question
            question_type: Type of question (feature, pain, comparison, etc.)

        Returns:
            Answer with supporting evidence and sources
        """
        # Different query patterns for different question types

        if question_type == "feature":
            query = """
            // For feature-related questions
            CALL db.index.fulltext.queryNodes('feature_search', $question)
            YIELD node AS feature, score
            LIMIT 3

            // Get products implementing this feature
            MATCH (feature)-[:IMPLEMENTED_IN]->(product:Product)

            // Get pain points this relieves
            OPTIONAL MATCH (feature)-[:RELIEVED_BY]-(pp:PainPoint)

            // Get supporting claims and evidence
            OPTIONAL MATCH (claim:Claim)-[:ABOUT]->(feature)
                           -[:SUPPORTED_BY]->(evidence:Evidence)

            RETURN feature.name AS feature_name,
                   feature.description AS description,
                   collect(DISTINCT product.name) AS products,
                   collect(DISTINCT pp.name) AS relieves,
                   collect(DISTINCT {
                       claim: claim.text,
                       evidence_source: evidence.source,
                       credibility: evidence.credibility_score
                   }) AS supporting_evidence,
                   score AS relevance_score
            ORDER BY relevance_score DESC
            LIMIT 1
            """

        elif question_type == "pain":
            query = """
            // For pain point questions
            MATCH (pp:PainPoint)
            WHERE toLower(pp.name) CONTAINS toLower($question)
               OR toLower(pp.description) CONTAINS toLower($question)

            // Get features that relieve this pain
            MATCH (pp)-[:RELIEVED_BY]->(feature:Feature)
                      -[:IMPLEMENTED_IN]->(product:Product)

            // Get evidence
            OPTIONAL MATCH (claim:Claim)-[:ABOUT]->(pp)
                           -[:SUPPORTED_BY]->(evidence:Evidence)

            RETURN pp.name AS pain_point,
                   pp.description AS description,
                   pp.severity AS severity,
                   collect(DISTINCT {
                       feature: feature.name,
                       product: product.name
                   }) AS solutions,
                   collect(DISTINCT {
                       claim: claim.text,
                       source: evidence.source
                   }) AS evidence
            LIMIT 1
            """

        else:  # General keyword search
            query = """
            MATCH (k:Keyword)
            WHERE toLower(k.name) CONTAINS toLower($question)

            // Get co-occurring keywords
            MATCH (k)-[co:CO_OCCURS_WITH]-(related:Keyword)

            RETURN k.name AS keyword,
                   k.betweenness AS importance,
                   k.community AS topic,
                   collect(DISTINCT related.name) AS related_keywords
            ORDER BY k.betweenness DESC
            LIMIT 1
            """

        results = self._execute_query(query, {"question": question})

        if results:
            logger.info(f"Answered question with graph data")
            return results[0]
        else:
            return {"answer": "No relevant information found in knowledge graph"}

    def get_context_for_prompt(self, prompt_text: str) -> Dict[str, Any]:
        """
        Get comprehensive context for a content prompt.

        Useful for RAG-based content generation.

        Args:
            prompt_text: Prompt to get context for

        Returns:
            Context including personas, pain points, evidence, and examples
        """
        query = """
        MATCH (prompt:Prompt {text: $prompt_text})

        // Get target personas
        OPTIONAL MATCH (prompt)-[:TARGETS]->(persona:Persona)

        // Get addressed pain points
        OPTIONAL MATCH (prompt)-[:ADDRESSES]->(pp:PainPoint)

        // Get relevant features
        OPTIONAL MATCH (pp)-[:RELIEVED_BY]->(feature:Feature)

        // Get claims and evidence
        OPTIONAL MATCH (claim:Claim)-[:ABOUT]->(pp)
                       -[:SUPPORTED_BY]->(evidence:Evidence)

        // Get existing assets on this topic
        OPTIONAL MATCH (prompt)<-[:GENERATED_FROM]-(brief:Brief)
                       <-[:DERIVES_FROM]-(asset:Asset)

        RETURN prompt.text AS prompt,
               collect(DISTINCT persona.name) AS target_personas,
               collect(DISTINCT pp.name) AS pain_points,
               collect(DISTINCT feature.name) AS relevant_features,
               collect(DISTINCT {
                   claim: claim.text,
                   evidence: evidence.source,
                   credibility: evidence.credibility_score
               }) AS supporting_evidence,
               collect(DISTINCT asset.url) AS existing_content
        """

        results = self._execute_query(query, {"prompt_text": prompt_text})

        if results:
            logger.info(f"Retrieved context for prompt")
            return results[0]
        else:
            return {}

    # =========================================================================
    # 10. KEYWORD BRIDGING
    # =========================================================================

    def find_bridging_keywords(self, cluster_a: str, cluster_b: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find keywords that bridge two topic clusters.

        Bridging keywords connect different communities and can inspire
        cross-topic content ideas.

        Args:
            cluster_a: First topic cluster name
            cluster_b: Second topic cluster name
            limit: Maximum bridging keywords to return

        Returns:
            Bridging keywords with connection scores
        """
        query = """
        // Find keywords from cluster A
        MATCH (tc1:TopicCluster {name: $cluster_a})<-[:BELONGS_TO]-(k1:Keyword)

        // Find keywords from cluster B
        MATCH (tc2:TopicCluster {name: $cluster_b})<-[:BELONGS_TO]-(k2:Keyword)

        // Find keywords that co-occur with both
        MATCH (k1)-[co1:CO_OCCURS_WITH]-(bridge:Keyword)
              -[co2:CO_OCCURS_WITH]-(k2)

        // Calculate bridge strength
        WITH bridge,
             count(DISTINCT k1) AS connections_to_a,
             count(DISTINCT k2) AS connections_to_b,
             sum(co1.weight) + sum(co2.weight) AS total_weight

        WITH bridge,
             connections_to_a + connections_to_b AS total_connections,
             total_weight,
             bridge.betweenness AS betweenness

        WITH bridge.name AS bridging_keyword,
             bridge.community AS community,
             total_connections,
             betweenness,
             total_connections * betweenness AS bridge_score

        RETURN bridging_keyword,
               community,
               total_connections,
               betweenness,
               bridge_score
        ORDER BY bridge_score DESC
        LIMIT $limit
        """

        results = self._execute_query(query, {
            "cluster_a": cluster_a,
            "cluster_b": cluster_b,
            "limit": limit
        })

        logger.info(f"Found {len(results)} bridging keywords")
        return results


# =============================================================================
# USAGE EXAMPLE
# =============================================================================

def main():
    """Example usage of GEO query library"""

    # Initialize
    queries = GEOQueries(
        uri="neo4j://localhost:7688",
        username="neo4j",
        password="claude_neo4j_2025"
    )

    try:
        print("=" * 80)
        print("GEO KNOWLEDGE GRAPH QUERY EXAMPLES")
        print("=" * 80)

        # 1. Find structure holes
        print("\n1. STRUCTURE HOLES (Top 5):")
        print("-" * 80)
        gaps = queries.find_structure_holes(limit=5)
        for gap in gaps:
            print(f"Gap: {gap['cluster_a']} <-> {gap['cluster_b']}")
            print(f"  Score: {gap['opportunity_score']:.3f}")
            print(f"  Keywords A: {', '.join(gap['keywords_a'])}")
            print(f"  Keywords B: {', '.join(gap['keywords_b'])}")
            print()

        # 2. Prioritized prompts
        print("\n2. PRIORITIZED PROMPTS (Top 5):")
        print("-" * 80)
        prompts = queries.rank_prompts_by_priority(limit=5)
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt['prompt_text']}")
            print(f"   Type: {prompt['prompt_type']}, Score: {prompt['final_score']:.3f}")
            print()

        # 3. Persona-Scenario matrix
        print("\n3. PERSONA-SCENARIO-PAINPOINT MATRIX:")
        print("-" * 80)
        matrix = queries.get_persona_scenario_matrix()
        for entry in matrix[:3]:
            print(f"Persona: {entry['persona']} | Scenario: {entry['scenario']}")
            print(f"  Pain: {entry['pain_point']} (Severity: {entry['severity']})")
            print(f"  Solutions: {', '.join(entry['relieving_features'][:3])}")
            print()

        # 4. Citation-ready scores
        print("\n4. CITATION-READY SCORES:")
        print("-" * 80)
        scores = queries.calculate_citation_ready_score()
        for asset in scores:
            print(f"Asset: {asset['type']} - {asset['quality_rating']}")
            print(f"  Score: {asset['citation_ready_score']:.3f}")
            print(f"  Mentions: {asset['mention_count']}, Evidence: {asset['evidence_count']}")
            print()

        # 5. Content coverage
        print("\n5. CONTENT COVERAGE ANALYSIS:")
        print("-" * 80)
        coverage = queries.analyze_prompt_coverage()
        if coverage:
            print(f"Total Prompts: {coverage['total_prompts']}")
            print(f"Covered: {coverage['prompts_with_assets']}")
            print(f"Coverage Rate: {coverage['coverage_rate']:.1%}")
            print(f"Uncovered: {coverage['uncovered_prompts']}")

        print("\n" + "=" * 80)
        print("Query examples completed successfully!")
        print("=" * 80)

    finally:
        queries.close()


if __name__ == "__main__":
    main()

// ===========================================================================
// InfraNodus + Neo4j GEO Knowledge Graph Schema
// Created: 2025-10-15
// Purpose: Initialize graph database schema for GEO system
// ===========================================================================

// ---------------------------------------------------------------------------
// SECTION 1: DROP EXISTING CONSTRAINTS AND INDEXES (Clean Slate)
// ---------------------------------------------------------------------------

// Note: Run this section only if you need to reset the database
// Uncomment the following lines if needed:
// DROP CONSTRAINT keyword_name_unique IF EXISTS;
// DROP CONSTRAINT persona_name_unique IF EXISTS;
// DROP INDEX keyword_name_index IF EXISTS;

// ---------------------------------------------------------------------------
// SECTION 2: CREATE CONSTRAINTS (Data Integrity)
// ---------------------------------------------------------------------------

// Keyword constraints
CREATE CONSTRAINT keyword_name_unique IF NOT EXISTS
FOR (k:Keyword) REQUIRE k.name IS UNIQUE;

// TopicCluster constraints
CREATE CONSTRAINT topic_cluster_name_unique IF NOT EXISTS
FOR (tc:TopicCluster) REQUIRE tc.name IS UNIQUE;

// Persona constraints
CREATE CONSTRAINT persona_name_unique IF NOT EXISTS
FOR (p:Persona) REQUIRE p.name IS UNIQUE;

// Scenario constraints
CREATE CONSTRAINT scenario_name_unique IF NOT EXISTS
FOR (s:Scenario) REQUIRE s.name IS UNIQUE;

// PainPoint constraints
CREATE CONSTRAINT painpoint_name_unique IF NOT EXISTS
FOR (pp:PainPoint) REQUIRE pp.name IS UNIQUE;

// Feature constraints
CREATE CONSTRAINT feature_name_unique IF NOT EXISTS
FOR (f:Feature) REQUIRE f.name IS UNIQUE;

// Product constraints
CREATE CONSTRAINT product_name_unique IF NOT EXISTS
FOR (prod:Product) REQUIRE prod.name IS UNIQUE;

// Prompt constraints
CREATE CONSTRAINT prompt_text_unique IF NOT EXISTS
FOR (pr:Prompt) REQUIRE pr.text IS UNIQUE;

// Brief constraints
CREATE CONSTRAINT brief_title_unique IF NOT EXISTS
FOR (b:Brief) REQUIRE b.title IS UNIQUE;

// Claim constraints (use ID instead of text for uniqueness)
CREATE CONSTRAINT claim_id_unique IF NOT EXISTS
FOR (c:Claim) REQUIRE c.id IS UNIQUE;

// Evidence constraints (use ID for uniqueness)
CREATE CONSTRAINT evidence_id_unique IF NOT EXISTS
FOR (e:Evidence) REQUIRE e.id IS UNIQUE;

// Asset constraints (use ID for uniqueness)
CREATE CONSTRAINT asset_id_unique IF NOT EXISTS
FOR (a:Asset) REQUIRE a.id IS UNIQUE;

// ---------------------------------------------------------------------------
// SECTION 3: CREATE INDEXES (Query Performance)
// ---------------------------------------------------------------------------

// Keyword indexes
CREATE INDEX keyword_betweenness_index IF NOT EXISTS
FOR (k:Keyword) ON (k.betweenness);

CREATE INDEX keyword_degree_index IF NOT EXISTS
FOR (k:Keyword) ON (k.degree);

CREATE INDEX keyword_community_index IF NOT EXISTS
FOR (k:Keyword) ON (k.community);

// PainPoint indexes
CREATE INDEX painpoint_severity_index IF NOT EXISTS
FOR (pp:PainPoint) ON (pp.severity);

CREATE INDEX painpoint_evidence_count_index IF NOT EXISTS
FOR (pp:PainPoint) ON (pp.evidence_count);

// Claim indexes
CREATE INDEX claim_confidence_index IF NOT EXISTS
FOR (c:Claim) ON (c.confidence);

CREATE INDEX claim_verification_status_index IF NOT EXISTS
FOR (c:Claim) ON (c.verification_status);

// Evidence indexes
CREATE INDEX evidence_credibility_score_index IF NOT EXISTS
FOR (e:Evidence) ON (e.credibility_score);

CREATE INDEX evidence_date_index IF NOT EXISTS
FOR (e:Evidence) ON (e.date);

// Asset indexes
CREATE INDEX asset_type_index IF NOT EXISTS
FOR (a:Asset) ON (a.type);

CREATE INDEX asset_channel_index IF NOT EXISTS
FOR (a:Asset) ON (a.channel);

CREATE INDEX asset_citation_ready_score_index IF NOT EXISTS
FOR (a:Asset) ON (a.citation_ready_score);

CREATE INDEX asset_published_at_index IF NOT EXISTS
FOR (a:Asset) ON (a.published_at);

// Prompt indexes
CREATE INDEX prompt_priority_index IF NOT EXISTS
FOR (pr:Prompt) ON (pr.priority);

CREATE INDEX prompt_gap_score_index IF NOT EXISTS
FOR (pr:Prompt) ON (pr.gap_score);

// Gap indexes
CREATE INDEX gap_opportunity_score_index IF NOT EXISTS
FOR (g:Gap) ON (g.opportunity_score);

CREATE INDEX gap_discovered_at_index IF NOT EXISTS
FOR (g:Gap) ON (g.discovered_at);

// ---------------------------------------------------------------------------
// SECTION 4: VERIFICATION QUERIES
// ---------------------------------------------------------------------------

// List all constraints
SHOW CONSTRAINTS;

// List all indexes
SHOW INDEXES;

// ---------------------------------------------------------------------------
// SECTION 5: SAMPLE DATA CREATION (For Testing and Validation)
// ---------------------------------------------------------------------------

// Create sample Keywords and TopicClusters
MERGE (k1:Keyword {
  name: "cooling_gel",
  betweenness: 0.85,
  degree: 12,
  community: "comfort_tech"
})
MERGE (k2:Keyword {
  name: "memory_foam",
  betweenness: 0.75,
  degree: 10,
  community: "comfort_tech"
})
MERGE (k3:Keyword {
  name: "back_pain",
  betweenness: 0.90,
  degree: 15,
  community: "health_issues"
})
MERGE (k4:Keyword {
  name: "hot_sleeper",
  betweenness: 0.70,
  degree: 8,
  community: "sleep_problems"
})

MERGE (tc1:TopicCluster {
  name: "comfort_tech",
  modularity: 0.82,
  size: 25
})
MERGE (tc2:TopicCluster {
  name: "health_issues",
  modularity: 0.78,
  size: 30
})
MERGE (tc3:TopicCluster {
  name: "sleep_problems",
  modularity: 0.75,
  size: 20
});

// Create sample Personas
MERGE (persona1:Persona {
  name: "Side Sleeper with Back Pain",
  description: "30-45 years old, suffers from chronic lower back pain, sleeps on side",
  priority: 1
})
MERGE (persona2:Persona {
  name: "Hot Sleeper",
  description: "25-40 years old, experiences night sweats, prefers cool sleeping environment",
  priority: 2
})
MERGE (persona3:Persona {
  name: "Couple Sharing Bed",
  description: "Different sleep preferences, need motion isolation and edge support",
  priority: 3
});

// Create sample Scenarios
MERGE (scenario1:Scenario {
  name: "Nighttime Overheating",
  description: "Waking up in the middle of the night due to excessive heat",
  frequency: "high"
})
MERGE (scenario2:Scenario {
  name: "Morning Back Stiffness",
  description: "Waking up with stiff or painful back requiring stretching",
  frequency: "high"
})
MERGE (scenario3:Scenario {
  name: "Partner Disturbance",
  description: "Being woken by partner's movements during sleep",
  frequency: "medium"
});

// Create sample PainPoints
MERGE (pain1:PainPoint {
  name: "Mattress Too Hot",
  description: "Excessive heat retention causing sleep disruption",
  severity: 8,
  evidence_count: 45
})
MERGE (pain2:PainPoint {
  name: "Inadequate Support",
  description: "Insufficient lumbar support leading to back pain",
  severity: 9,
  evidence_count: 62
})
MERGE (pain3:PainPoint {
  name: "Motion Transfer",
  description: "Partner's movements disturbing sleep",
  severity: 6,
  evidence_count: 28
});

// Create sample Features
MERGE (feature1:Feature {
  name: "Cooling Gel Layer",
  description: "Gel-infused foam that dissipates heat",
  category: "temperature_regulation"
})
MERGE (feature2:Feature {
  name: "Zoned Support System",
  description: "Different firmness zones for targeted support",
  category: "support"
})
MERGE (feature3:Feature {
  name: "Motion Isolation",
  description: "Foam layers that absorb movement",
  category: "comfort"
});

// Create sample Products
MERGE (product1:Product {
  name: "SweetNight Twilight",
  brand: "SweetNight",
  price_range: "mid",
  rating: 4.5
})
MERGE (product2:Product {
  name: "SweetNight Breeze",
  brand: "SweetNight",
  price_range: "premium",
  rating: 4.7
})
MERGE (product3:Product {
  name: "Purple Mattress",
  brand: "Purple",
  price_range: "premium",
  rating: 4.6
});

// Create sample Prompts
MERGE (prompt1:Prompt {
  text: "How does cooling gel technology prevent night sweats?",
  type: "educational",
  priority: 1,
  gap_score: 0.85
})
MERGE (prompt2:Prompt {
  text: "Best mattress for side sleepers with back pain",
  type: "buyer_guide",
  priority: 2,
  gap_score: 0.78
});

// Create sample Gaps
MERGE (gap1:Gap {
  topic_a: "cooling_gel",
  topic_b: "back_pain",
  opportunity_score: 0.82,
  discovered_at: datetime()
});

// Create sample Claims
MERGE (claim1:Claim {
  id: "claim_001",
  text: "Cooling gel reduces sleep surface temperature by 3-5 degrees",
  confidence: 0.85,
  verification_status: "verified"
})
MERGE (claim2:Claim {
  id: "claim_002",
  text: "Zoned support reduces back pain for 78% of side sleepers",
  confidence: 0.80,
  verification_status: "verified"
});

// Create sample Evidence
MERGE (evidence1:Evidence {
  id: "evidence_001",
  source: "Sleep Foundation Study 2024",
  url: "https://www.sleepfoundation.org/cooling-gel-study",
  date: date("2024-03-15"),
  quote: "Gel-infused memory foam demonstrated average temperature reduction of 3.8°F",
  credibility_score: 0.90
})
MERGE (evidence2:Evidence {
  id: "evidence_002",
  source: "Reddit r/Mattress Survey",
  url: "https://reddit.com/r/Mattress/comments/xyz",
  date: date("2024-09-20"),
  quote: "148 out of 190 side sleepers reported reduced back pain with zoned support",
  credibility_score: 0.75
});

// Create sample Briefs
MERGE (brief1:Brief {
  title: "Ultimate Guide: Best Cooling Mattresses for Hot Sleepers 2025",
  outline: "1. Why you overheat at night\n2. Technology comparison\n3. Top recommendations\n4. User testimonials",
  target_persona: "Hot Sleeper",
  target_scenario: "Nighttime Overheating"
});

// Create sample Assets
MERGE (asset1:Asset {
  id: "asset_001",
  type: "blog_post",
  channel: "website",
  url: "https://sweetnight.com/blog/cooling-mattress-guide",
  published_at: datetime("2024-10-01T10:00:00Z"),
  citation_ready_score: 0.88
});

// ---------------------------------------------------------------------------
// SECTION 6: CREATE RELATIONSHIPS (Network Structure)
// ---------------------------------------------------------------------------

// Keyword Co-occurrence Relationships
MATCH (k1:Keyword {name: "cooling_gel"}), (k2:Keyword {name: "hot_sleeper"})
MERGE (k1)-[:CO_OCCURS_WITH {weight: 0.75}]->(k2);

MATCH (k1:Keyword {name: "memory_foam"}), (k2:Keyword {name: "back_pain"})
MERGE (k1)-[:CO_OCCURS_WITH {weight: 0.68}]->(k2);

// Keyword to TopicCluster
MATCH (k:Keyword {name: "cooling_gel"}), (tc:TopicCluster {name: "comfort_tech"})
MERGE (k)-[:BELONGS_TO]->(tc);

MATCH (k:Keyword {name: "memory_foam"}), (tc:TopicCluster {name: "comfort_tech"})
MERGE (k)-[:BELONGS_TO]->(tc);

MATCH (k:Keyword {name: "back_pain"}), (tc:TopicCluster {name: "health_issues"})
MERGE (k)-[:BELONGS_TO]->(tc);

MATCH (k:Keyword {name: "hot_sleeper"}), (tc:TopicCluster {name: "sleep_problems"})
MERGE (k)-[:BELONGS_TO]->(tc);

// TopicCluster Bridges
MATCH (tc1:TopicCluster {name: "comfort_tech"}), (tc2:TopicCluster {name: "health_issues"})
MERGE (tc1)-[:BRIDGES {strength: 0.65}]->(tc2);

// Persona to Scenario
MATCH (p:Persona {name: "Hot Sleeper"}), (s:Scenario {name: "Nighttime Overheating"})
MERGE (p)-[:OCCURS_IN]->(s);

MATCH (p:Persona {name: "Side Sleeper with Back Pain"}), (s:Scenario {name: "Morning Back Stiffness"})
MERGE (p)-[:OCCURS_IN]->(s);

// Scenario to PainPoint
MATCH (s:Scenario {name: "Nighttime Overheating"}), (pp:PainPoint {name: "Mattress Too Hot"})
MERGE (s)-[:SUFFERS]->(pp);

MATCH (s:Scenario {name: "Morning Back Stiffness"}), (pp:PainPoint {name: "Inadequate Support"})
MERGE (s)-[:SUFFERS]->(pp);

// PainPoint to Feature
MATCH (pp:PainPoint {name: "Mattress Too Hot"}), (f:Feature {name: "Cooling Gel Layer"})
MERGE (pp)-[:RELIEVED_BY]->(f);

MATCH (pp:PainPoint {name: "Inadequate Support"}), (f:Feature {name: "Zoned Support System"})
MERGE (pp)-[:RELIEVED_BY]->(f);

// Feature to Product
MATCH (f:Feature {name: "Cooling Gel Layer"}), (prod:Product {name: "SweetNight Breeze"})
MERGE (f)-[:IMPLEMENTED_IN]->(prod);

MATCH (f:Feature {name: "Zoned Support System"}), (prod:Product {name: "SweetNight Twilight"})
MERGE (f)-[:IMPLEMENTED_IN]->(prod);

// Prompt to PainPoint
MATCH (pr:Prompt {text: "How does cooling gel technology prevent night sweats?"}),
      (pp:PainPoint {name: "Mattress Too Hot"})
MERGE (pr)-[:ADDRESSES]->(pp);

// Prompt to Persona
MATCH (pr:Prompt {text: "How does cooling gel technology prevent night sweats?"}),
      (p:Persona {name: "Hot Sleeper"})
MERGE (pr)-[:TARGETS]->(p);

// Gap to Prompt
MATCH (g:Gap {topic_a: "cooling_gel", topic_b: "back_pain"}),
      (pr:Prompt {text: "Best mattress for side sleepers with back pain"})
MERGE (g)-[:SUGGESTS]->(pr);

// Brief to TopicCluster
MATCH (b:Brief {title: "Ultimate Guide: Best Cooling Mattresses for Hot Sleepers 2025"}),
      (tc:TopicCluster {name: "comfort_tech"})
MERGE (b)-[:COVERS]->(tc);

// Brief to Prompt
MATCH (b:Brief {title: "Ultimate Guide: Best Cooling Mattresses for Hot Sleepers 2025"}),
      (pr:Prompt {text: "How does cooling gel technology prevent night sweats?"})
MERGE (b)-[:GENERATED_FROM]->(pr);

// Claim to Feature
MATCH (c:Claim {id: "claim_001"}), (f:Feature {name: "Cooling Gel Layer"})
MERGE (c)-[:ABOUT]->(f);

MATCH (c:Claim {id: "claim_002"}), (f:Feature {name: "Zoned Support System"})
MERGE (c)-[:ABOUT]->(f);

// Claim to Evidence
MATCH (c:Claim {id: "claim_001"}), (e:Evidence {id: "evidence_001"})
MERGE (c)-[:SUPPORTED_BY]->(e);

MATCH (c:Claim {id: "claim_002"}), (e:Evidence {id: "evidence_002"})
MERGE (c)-[:SUPPORTED_BY]->(e);

// Asset to Brief
MATCH (a:Asset {id: "asset_001"}),
      (b:Brief {title: "Ultimate Guide: Best Cooling Mattresses for Hot Sleepers 2025"})
MERGE (a)-[:DERIVES_FROM]->(b);

// Asset to Product
MATCH (a:Asset {id: "asset_001"}), (prod:Product {name: "SweetNight Breeze"})
MERGE (a)-[:MENTIONS]->(prod);

// Asset to PainPoint
MATCH (a:Asset {id: "asset_001"}), (pp:PainPoint {name: "Mattress Too Hot"})
MERGE (a)-[:MENTIONS]->(pp);

// ---------------------------------------------------------------------------
// SECTION 7: VALIDATION QUERIES
// ---------------------------------------------------------------------------

// Count all nodes by label
MATCH (n)
RETURN labels(n)[0] AS NodeType, count(n) AS Count
ORDER BY Count DESC;

// Count all relationships by type
MATCH ()-[r]->()
RETURN type(r) AS RelationshipType, count(r) AS Count
ORDER BY Count DESC;

// Show sample of connected graph structure
MATCH path = (p:Persona)-[:OCCURS_IN]->(s:Scenario)-[:SUFFERS]->(pp:PainPoint)-[:RELIEVED_BY]->(f:Feature)
RETURN path
LIMIT 5;

// Show Claims with Evidence
MATCH (c:Claim)-[:SUPPORTED_BY]->(e:Evidence)
RETURN c.text AS Claim, e.source AS EvidenceSource, e.credibility_score AS Credibility
LIMIT 5;

// Show Assets with Citation-Ready Score
MATCH (a:Asset)
RETURN a.type AS Type, a.channel AS Channel, a.citation_ready_score AS Score
ORDER BY a.citation_ready_score DESC
LIMIT 5;

// ===========================================================================
// END OF SCHEMA INITIALIZATION
// ===========================================================================

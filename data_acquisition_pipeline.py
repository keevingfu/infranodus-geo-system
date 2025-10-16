"""
Data Acquisition Pipeline
=========================

End-to-end pipeline for acquiring, processing, and importing data into the GEO system.

Flow:
1. Firecrawl → Web scraping and content extraction
2. Text Cleaning → Remove noise, normalize format
3. InfraNodus → Import and generate co-occurrence network
4. Neo4j → Import enriched knowledge graph

Author: Claude (InfraNodus GEO System)
Date: 2025-10-15
"""

import requests
import json
import re
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import logging
from pathlib import Path

from infranodus_client import InfraNodusClient, InfraNodusConfig
from import_pipeline import Neo4jImporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class AcquisitionConfig:
    """Configuration for data acquisition pipeline"""
    firecrawl_api_url: str = "http://localhost:3002"
    firecrawl_api_key: str = "fs-test"
    infranodus_base_url: str = "http://localhost:3000"
    infranodus_username: str = "demo_user"
    infranodus_password: str = "demo"
    neo4j_uri: str = "neo4j://localhost:7688"
    neo4j_username: str = "neo4j"
    neo4j_password: str = "claude_neo4j_2025"
    output_dir: str = "./data_output"
    max_retries: int = 3
    retry_delay: int = 5


@dataclass
class ScrapedContent:
    """Scraped content from a URL"""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    scraped_at: Optional[str] = None


class FirecrawlClient:
    """Client for Firecrawl API (self-hosted)"""

    def __init__(self, api_url: str, api_key: str):
        """Initialize Firecrawl client"""
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def scrape_url(self, url: str, formats: List[str] = None) -> Optional[ScrapedContent]:
        """
        Scrape a single URL using Firecrawl

        Args:
            url: URL to scrape
            formats: Output formats (default: ["markdown"])

        Returns:
            ScrapedContent object or None if failed
        """
        if formats is None:
            formats = ["markdown"]

        try:
            endpoint = f"{self.api_url}/v1/scrape"
            payload = {
                "url": url,
                "formats": formats
            }

            logger.info(f"Scraping URL: {url}")
            response = requests.post(
                endpoint,
                headers=self.headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()

                # Extract content
                content_data = data.get('data', {})
                markdown_content = content_data.get('markdown', '')

                scraped = ScrapedContent(
                    url=url,
                    title=content_data.get('metadata', {}).get('title', ''),
                    content=markdown_content,
                    metadata=content_data.get('metadata', {}),
                    scraped_at=content_data.get('metadata', {}).get('sourceURL', '')
                )

                logger.info(f"Successfully scraped {url} ({len(markdown_content)} chars)")
                return scraped
            else:
                logger.error(f"Firecrawl scrape failed: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            return None

    def scrape_multiple(self, urls: List[str]) -> List[ScrapedContent]:
        """Scrape multiple URLs"""
        results = []
        for url in urls:
            content = self.scrape_url(url)
            if content:
                results.append(content)
            time.sleep(1)  # Rate limiting
        return results


class TextProcessor:
    """Text cleaning and preprocessing"""

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text

        - Remove excessive whitespace
        - Remove special characters
        - Normalize line breaks
        """
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove special characters (keep alphanumeric and basic punctuation)
        text = re.sub(r'[^\w\s.,!?;:()\-\']', '', text)

        # Normalize line breaks
        text = text.replace('\n', ' ')

        return text.strip()

    @staticmethod
    def extract_sentences(text: str, min_length: int = 10) -> List[str]:
        """
        Extract sentences from text

        Args:
            text: Input text
            min_length: Minimum sentence length

        Returns:
            List of sentences
        """
        # Simple sentence splitting (can be improved with nltk/spacy)
        sentences = re.split(r'[.!?]+', text)

        # Filter by length and clean
        return [s.strip() for s in sentences if len(s.strip()) > min_length]

    @staticmethod
    def prepare_for_infranodus(scraped_contents: List[ScrapedContent]) -> str:
        """
        Prepare text for InfraNodus import

        Combines all scraped content into a single text suitable for network analysis.
        """
        all_text = []

        for content in scraped_contents:
            # Clean content
            cleaned = TextProcessor.clean_text(content.content)

            # Add title as a sentence (for emphasis)
            if content.title:
                all_text.append(content.title + ".")

            # Add content
            all_text.append(cleaned)

        combined = ' '.join(all_text)
        logger.info(f"Prepared {len(combined)} characters for InfraNodus")

        return combined


class DataAcquisitionPipeline:
    """
    End-to-end data acquisition pipeline

    Orchestrates: Firecrawl → InfraNodus → Neo4j
    """

    def __init__(self, config: Optional[AcquisitionConfig] = None):
        """Initialize pipeline with configuration"""
        self.config = config or AcquisitionConfig()

        # Initialize clients
        self.firecrawl = FirecrawlClient(
            api_url=self.config.firecrawl_api_url,
            api_key=self.config.firecrawl_api_key
        )

        self.infranodus = InfraNodusClient(InfraNodusConfig(
            base_url=self.config.infranodus_base_url,
            username=self.config.infranodus_username,
            password=self.config.infranodus_password
        ))

        self.neo4j_importer = Neo4jImporter(
            uri=self.config.neo4j_uri,
            username=self.config.neo4j_username,
            password=self.config.neo4j_password
        )

        # Create output directory
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)

        logger.info("Data Acquisition Pipeline initialized")

    def run_pipeline(self, urls: List[str], context: str = "geo_acquisition") -> Dict[str, Any]:
        """
        Run complete acquisition pipeline

        Args:
            urls: List of URLs to scrape
            context: InfraNodus context name

        Returns:
            Dictionary with pipeline statistics
        """
        logger.info("=" * 80)
        logger.info("STARTING DATA ACQUISITION PIPELINE")
        logger.info("=" * 80)

        stats = {
            "urls_scraped": 0,
            "content_size": 0,
            "infranodus_context": context,
            "keywords_imported": 0,
            "clusters_imported": 0,
            "relationships_imported": 0,
            "errors": []
        }

        try:
            # Step 1: Scrape content with Firecrawl
            logger.info("\n[Step 1/4] Scraping web content with Firecrawl...")
            scraped_contents = self.firecrawl.scrape_multiple(urls)
            stats["urls_scraped"] = len(scraped_contents)

            if not scraped_contents:
                logger.warning("No content scraped. Pipeline aborted.")
                return stats

            # Save raw scraped data
            self._save_scraped_data(scraped_contents)

            # Step 2: Process and clean text
            logger.info("\n[Step 2/4] Processing and cleaning text...")
            prepared_text = TextProcessor.prepare_for_infranodus(scraped_contents)
            stats["content_size"] = len(prepared_text)

            # Save processed text
            processed_file = f"{self.config.output_dir}/processed_text.txt"
            with open(processed_file, 'w', encoding='utf-8') as f:
                f.write(prepared_text)
            logger.info(f"Processed text saved to {processed_file}")

            # Step 3: Import to InfraNodus
            logger.info(f"\n[Step 3/4] Importing to InfraNodus context '{context}'...")
            infranodus_success = self._import_to_infranodus(prepared_text, context)

            if not infranodus_success:
                logger.warning("InfraNodus import failed. Skipping Neo4j import.")
                return stats

            # Wait for InfraNodus to process
            logger.info("Waiting for InfraNodus to process text...")
            time.sleep(5)

            # Step 4: Import to Neo4j
            logger.info("\n[Step 4/4] Importing to Neo4j knowledge graph...")
            neo4j_stats = self.neo4j_importer.import_full_dataset(context)

            stats.update({
                "keywords_imported": neo4j_stats.get("keywords", 0),
                "clusters_imported": neo4j_stats.get("clusters", 0),
                "relationships_imported": neo4j_stats.get("cooccurrences", 0) + neo4j_stats.get("cluster_links", 0),
                "gaps_identified": neo4j_stats.get("gaps", 0),
                "prompts_generated": neo4j_stats.get("prompts", 0)
            })

            logger.info("\n" + "=" * 80)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            self._print_stats(stats)

        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}")
            stats["errors"].append(str(e))

        finally:
            self.neo4j_importer.close()

        return stats

    def _save_scraped_data(self, contents: List[ScrapedContent]):
        """Save raw scraped data to JSON"""
        output_file = f"{self.config.output_dir}/scraped_data.json"

        data = [
            {
                "url": c.url,
                "title": c.title,
                "content": c.content,
                "metadata": c.metadata,
                "scraped_at": c.scraped_at
            }
            for c in contents
        ]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Scraped data saved to {output_file}")

    def _import_to_infranodus(self, text: str, context: str) -> bool:
        """
        Import text to InfraNodus

        Note: This is a simplified implementation. In a real system,
        you would use InfraNodus API endpoints for importing text.
        For now, we'll authenticate and verify the context exists.
        """
        try:
            # Authenticate
            if not self.infranodus.login():
                logger.error("InfraNodus authentication failed")
                return False

            # For demo purposes, we'll assume text is imported manually
            # In production, use InfraNodus import API
            logger.info(f"✓ InfraNodus authenticated. Context: {context}")
            logger.info(f"  [Manual step required: Import processed_text.txt to InfraNodus context '{context}']")

            return True

        except Exception as e:
            logger.error(f"InfraNodus import error: {str(e)}")
            return False

    def _print_stats(self, stats: Dict[str, Any]):
        """Pretty print pipeline statistics"""
        print("\n📊 Pipeline Statistics:")
        print(f"  URLs scraped: {stats['urls_scraped']}")
        print(f"  Content size: {stats['content_size']:,} characters")
        print(f"  Keywords imported: {stats['keywords_imported']}")
        print(f"  Topic clusters: {stats['clusters_imported']}")
        print(f"  Relationships: {stats['relationships_imported']}")
        print(f"  Structure holes: {stats.get('gaps_identified', 0)}")
        print(f"  Prompts generated: {stats.get('prompts_generated', 0)}")
        if stats['errors']:
            print(f"\n⚠️ Errors: {len(stats['errors'])}")


# =============================================================================
# USAGE EXAMPLES
# =============================================================================

def example_reddit_voc():
    """Example: Scrape Reddit VOC data"""

    pipeline = DataAcquisitionPipeline()

    # Sample Reddit threads about mattresses
    urls = [
        "https://www.reddit.com/r/Mattress/comments/15iqt2j/best_mattress_for_side_sleepers/",
        "https://www.reddit.com/r/Mattress/comments/16jkl3m/cooling_mattress_recommendations/",
        "https://www.reddit.com/r/Mattress/comments/17abc4n/back_pain_relief_mattress/",
    ]

    stats = pipeline.run_pipeline(urls, context="reddit_voc")
    return stats


def example_amazon_reviews():
    """Example: Scrape Amazon product reviews"""

    pipeline = DataAcquisitionPipeline()

    # Sample Amazon product pages
    urls = [
        "https://www.amazon.com/dp/B08JLKQX1Y",  # SweetNight Breeze
        "https://www.amazon.com/dp/B07FMK6ZVZ",  # SweetNight Twilight
    ]

    stats = pipeline.run_pipeline(urls, context="amazon_reviews")
    return stats


def example_competitor_analysis():
    """Example: Analyze competitor websites"""

    pipeline = DataAcquisitionPipeline()

    # Competitor product pages
    urls = [
        "https://purple.com/mattresses/purple-mattress",
        "https://www.casper.com/mattresses/casper-original/"
    ]

    stats = pipeline.run_pipeline(urls, context="competitor_analysis")
    return stats


def main():
    """Demo data acquisition pipeline"""

    print("=" * 80)
    print("DATA ACQUISITION PIPELINE DEMO")
    print("=" * 80)
    print("\nAvailable examples:")
    print("1. Reddit VOC (Voice of Customer)")
    print("2. Amazon Reviews")
    print("3. Competitor Analysis")
    print("\nRunning example 1: Reddit VOC...")
    print()

    # Run Reddit VOC example
    stats = example_reddit_voc()

    print("\n✅ Demo completed!")
    print("Next steps:")
    print("1. Manually import processed_text.txt to InfraNodus")
    print("2. Run import_pipeline.py to sync to Neo4j")
    print("3. Use graph_rag.py to query the knowledge graph")


if __name__ == "__main__":
    main()

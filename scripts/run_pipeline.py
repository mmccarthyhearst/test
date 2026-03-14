#!/usr/bin/env python3
"""CLI entry point for running the SDR pipeline directly (without API/worker).

Usage:
    python scripts/run_pipeline.py --icp '{"target_industries": ["SaaS"]}'
"""

import argparse
import json

from ai_sdr.agents.crew import create_sdr_crew


def main():
    parser = argparse.ArgumentParser(description="Run the AI SDR pipeline")
    parser.add_argument(
        "--icp",
        type=str,
        default='{"target_industries": ["Technology", "SaaS"], "target_titles": ["VP of Sales", "CRO"]}',
        help="ICP criteria as JSON string",
    )
    parser.add_argument("--max-leads", type=int, default=5, help="Max leads to source")
    parser.add_argument("--routing-rules", type=str, default="[]", help="Routing rules as JSON")
    args = parser.parse_args()

    print(f"Starting SDR pipeline with ICP: {args.icp}")
    print(f"Max leads: {args.max_leads}")

    crew = create_sdr_crew(
        icp_criteria=args.icp,
        routing_rules=args.routing_rules,
        max_leads=args.max_leads,
    )

    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("PIPELINE RESULT:")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()

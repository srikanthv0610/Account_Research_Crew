#!/usr/bin/env python
import sys
import warnings
import re
from pathlib import Path

from datetime import datetime

from account_research_crew.crew import ResearchCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    today = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().year
    # ── Get company name from CLI argument or interactive prompt ──────────────
    if len(sys.argv) > 1:
        # Usage: python main.py
        company = " ".join(sys.argv[1:])
    else:
        # Interactive fallback
        company = input("Query: Enter the company name for the briefing: ").strip()

    if not company:
        print("No company name provided. Exiting.")
        sys.exit(1)

    print(f"\nPreparing briefing for: {company}\n")
    print("=" * 50)

    # ── Kick off the crew ─────────────────────────────────────────────────────
    result = ResearchCrew().crew().kickoff(inputs={
        "company": company, 
        "today": today, 
        "current_year": current_year})

    # ── Print final output ────────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print(f"Briefing for {company} complete!")
    print(f"Full briefing saved to: briefing.md")
    print("\n" + str(result))
    
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    safe_company = company.strip().replace(" ", "_")
    output_file = output_dir / f"{safe_company}_executive_briefing.md"

    final_text = getattr(result, "raw", str(result))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"Saved final briefing to: {output_file}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        ResearchCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResearchCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
       ResearchCrew().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = ResearchCrew().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")


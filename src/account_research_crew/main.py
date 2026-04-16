#!/usr/bin/env python
import sys
import re
from pathlib import Path
from datetime import datetime

from account_research_crew.crew import ResearchCrew

# Utility helpers for running the crew and saving output.

def safe_filename(value: str) -> str:
    """Normalize a string into a safe filename component."""
    value = value.strip().replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9_-]", "", value)


def build_inputs(company: str) -> dict:
    """Create the input payload passed into the crew execution."""
    return {
        "company": company,
        "today": datetime.now().strftime("%B %d, %Y"),
        "current_year": str(datetime.now().year),
    }


def save_result(company: str, result) -> Path:
    """Save the final briefing result to a markdown file."""
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_company = safe_filename(company)
    output_file = output_dir / f"{safe_company}_executive_briefing.md"

    # The crew result may expose a raw string payload or a custom wrapper object.
    final_text = getattr(result, "raw", str(result))

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"# Executive Briefing: {company}\n\n")
        f.write(f"_Generated on {datetime.now().strftime('%B %d, %Y')}_\n\n")
        f.write(final_text)

    return output_file


def get_company_from_args_or_prompt(arg_index: int = 1) -> str:
    """Retrieve the target company from CLI arguments or prompt the user."""
    if len(sys.argv) > arg_index:
        return " ".join(sys.argv[arg_index:]).strip()
    return input("Query: Enter the company name for the briefing: ").strip()


def run():
    """
    Run the crew locally for a given company and save the final briefing.

    This is the main entrypoint used to demonstrate how the
    ResearchCrew is executed end-to-end from user input to output file.
    """
    company = get_company_from_args_or_prompt()

    if not company:
        print("No company name provided. Exiting.")
        sys.exit(1)

    # Present the flow: user selects a company, crew runs, output is saved.
    print(f"\nPreparing briefing for: {company}\n")
    print("=" * 50)

    try:
        # Build inputs and launch the crew pipeline.
        result = ResearchCrew().crew().kickoff(inputs=build_inputs(company))

        print("\n" + "=" * 50)
        print(f"Briefing for {company} complete!\n")

        # Persist the result as a Markdown executive briefing.
        output_file = save_result(company, result)
        print(f"\nSaved final briefing to: {output_file}")

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()

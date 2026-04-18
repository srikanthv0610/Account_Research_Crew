# Account Research Crew

A CrewAI multi-agent system that prepares a short pre-meeting briefing for an account executive.  
It researches a target company, turns the findings into business insight, and produces a concise executive briefing.

## What it does

This crew runs three agents in sequence:

- **Company Research Agent** — gathers current company facts and recent developments.
- **Account Insight Agent** — turns the research into business relevance and meeting insight.
- **Executive Briefing Agent** — writes the final concise briefing for the account executive.

The research agent uses `SerperDevTool` for live web search. The final output is saved as a Markdown file in the `output/` folder.

## Requirements

- Python 3.10 to 3.13
- `uv`
- CrewAI
- A valid 'OpenAI API KEY' for LLM calls - `OPENAI_API_KEY`
- A valid ['SERPER API KEY'](https://serper.dev/?utm_term=google%20search%20api&gad_source=1&gad_campaignid=18303173259&gbraid=0AAAAAo4ZGoFivm7unUvosOFcl7RI4rUd0&gclid=CjwKCAjw14zPBhAuEiwAP3-Eb_Tq1djTFTDleSaQmsShEzSJ1u_X_W4-NxLyD5egh99rak1WJjiFwRoCOykQAvD_BwE) for web search 

## Clone the repository

```bash
git clone https://github.com/srikanthv0610/Account_Research_Crew.git
cd Account_Research_Crew
```

## Customizing

**Create a `.env` file in the project root and add your `OPENAI_API_KEY` and `SERPER_API_KEY`**

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

## Install dependencies

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [uv](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Install crewai globally using uv

```bash
uv tool install crewai
```

Next, install the project dependencies from `pyproject.toml`:

```bash
crewai install
```

## Running the Application

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the account_research_crew Crew, assembling the agents and assigning them tasks as defined in the configuration. 

When the application starts, you will be prompted to enter the target company:

```text
Hello! Please enter the company name you would like a briefing for:
```
You simple need to type the company name as press ENTER as in the Example below. 

Example:

```text
Hello! Please enter the company name you would like a briefing for: Accenture
```

This starts the crew, runs the three agents sequentially, and saves the final briefing in the `output/` folder.


## Example run

Example:

```bash
crewai run

Hello! Please enter the company name you would like a briefing for: NVIDIA
```

## Output

The final executive briefing is saved as a Markdown file in the `output/` folder.

Example:

```text
output/NVIDIA_executive_briefing.md
```

## Project structure

```text
Account_Research_Crew/
├── .env
├── README.md
├── pyproject.toml
├── uv.lock
├── knowledge/
├── output/
└── src/
    └── account_research_crew/
        ├── crew.py
        ├── main.py
        ├── config/
        │   ├── agents.yaml
        │   └── tasks.yaml
        └── tools/
```

## Support

- CrewAI docs: https://docs.crewai.com
- CrewAI GitHub: https://github.com/crewAIInc/crewai
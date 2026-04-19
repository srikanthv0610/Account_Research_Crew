# Account Research Crew

A CrewAI based multi-agent system that prepares a short pre-meeting briefing for an account executive.  
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
- `CrewAI`
- A valid `OPENAI_API_KEY` for LLM calls
- A valid `SERPER_API_KEY` for web search - [Get one at serper.dev](https://serper.dev/?utm_term=google%20search%20api&gad_source=1&gad_campaignid=18303173259&gbraid=0AAAAAo4ZGoFivm7unUvosOFcl7RI4rUd0&gclid=CjwKCAjw14zPBhAuEiwAP3-Eb_Tq1djTFTDleSaQmsShEzSJ1u_X_W4-NxLyD5egh99rak1WJjiFwRoCOykQAvD_BwE)

## Clone the repository

```bash
git clone https://github.com/srikanthv0610/Account_Research_Crew.git
cd Account_Research_Crew
```

## Adding environment variables

Create a `.env` file in the project root. You can use the provided `.env.example` as a starting point:

```bash
cp .env.example .env
```

Then fill in your credentials:

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```

## Install dependencies

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [uv](https://docs.astral.sh/uv/) for dependency management and package handling. All dependencies are declared
in `pyproject.toml` and pinned in `uv.lock` for reproducible installs.

**Step 1:** First, if you haven't already, install uv:

```bash
pip install uv
```

**Step 2:** Next, install crewai globally using uv

```bash
uv tool install crewai
```

**Step 3:** Install all project dependencies from `pyproject.toml` using the pinned versions in `uv.lock`:

```bash
crewai install
```
This resolves and installs all dependencies exactly as declared in `pyproject.toml`, using `uv.lock`
to guarantee consistent versions across all environments.

## Running the Application

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the account research crew, assembling the agents and assigning them tasks as defined in the configuration. 

When the application starts, you will see:

```text
Hello! Please enter the company name you would like a briefing for:
```
Type the company name and press Enter:


```text
Hello! Please enter the company name you would like a briefing for: NVIDIA
```

The crew will run the three agents sequentially and save the final briefing in the `output/` folder.

## Output

The final executive briefing is saved as a Markdown file in the `output/` folder.

Example:

```text
output/NVIDIA_executive_briefing.md
```

See a sample output here:
[output/NVIDIA_executive_briefing.md](https://github.com/srikanthv0610/Account_Research_Crew/blob/main/output/NVIDIA_executive_briefing.md)

## Project structure

```text
Account_Research_Crew/
├── .env
├── README.md
├── pyproject.toml
├── uv.lock
├── LICENSE
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

## License

This project is licensed under the [MIT License](https://github.com/srikanthv0610/Account_Research_Crew/blob/main/LICENSE).
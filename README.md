# Account Research Crew

A CrewAI multi-agent system that prepares a short pre-meeting briefing for an account executive.  
It researches a target company, turns the findings into business insight, and produces a concise executive briefing.

## What it does

This crew runs three agents in sequence:

- **Company Research Agent** — gathers current company facts and recent developments.
- **Account Insight Agent** — turns the research into business relevance and meeting insight.
- **Executive Briefing Agent** — writes the final concise briefing for the account executive.

The research agent uses `SerperDevTool` for live web search. The final output is saved as a Markdown file in the `output/` folder.


## Clone the repository

```bash
git clone https://github.com/srikanthv0610/Account_Research_Crew.git
cd Account_Research_Crew
```

## Customizing

**Create a `.env` file in the project root and add your `OPENAI_API_KEY` and `SERPER_API_KEY`**


### Option 1: Use OpenAI

```env
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
```
### Option 2: Use Azure APIM

```env
AZURE_APIM_SUBSCRIPTION_KEY=your_azure_apim_subscription_key
SERPER_API_KEY=your_serper_api_key
```

## Install dependencies

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, install the project dependencies from `pyproject.toml`:

```bash
crewai install
```


## Running the Application

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the account_research_crew Crew, assembling the agents and assigning them tasks as defined in the configuration. 

When the application starts, you will be prompted to enter the target company:

```text
Query: Enter the company name for the briefing:
```

Example:

```text
Query: Enter the company name for the briefing: SAP
```

This starts the crew, runs the three agents sequentially, and saves the final briefing in the `output/` folder.

## Example runs

Run interactively and enter the company name when prompted:

```bash
crewai run
```

Run a different target company by typing it at the prompt:

```text
NVIDIA
```

Example:

```bash
crewai run
# Query: Enter the company name for the briefing: ROCHE
```

## Output

The final executive briefing is saved as a Markdown file in the `output/` folder.

Example:

```text
output/NVIDIA_executive_briefing.md
```


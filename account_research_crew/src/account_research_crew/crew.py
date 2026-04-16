import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# Load environment variables from .env file, including API keys for LLM and search tool.
load_dotenv()

# ── LLM configuration ──────────────────────────────────────────────────────
# Build the language model client used by all agents in this crew.

def build_llm() -> LLM:
    azure_apim_key = os.getenv("AZURE_APIM_SUBSCRIPTION_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    # Azure APIM when configured, otherwise fallback to OpenAI key.
    if azure_apim_key:
        return LLM(
            model="openai/gpt-4o",
            base_url=(
                "https://az-apim-svc-westeurope.azure-api.net/openai/deployments/gpt-4o"
            ),
            api_key=azure_apim_key,
            extra_headers={
                "Ocp-Apim-Subscription-Key": azure_apim_key
            },
            temperature=0.5,
        )

    if openai_key:
        return LLM(
            model="gpt-4o",
            api_key=openai_key,
            temperature=0.5,
        )

    # If no credentials are available, fail fast with a clear message.
    raise ValueError(
        "No LLM credentials found. Set either AZURE_APIM_SUBSCRIPTION_KEY or OPENAI_API_KEY in .env"
    )

llm = build_llm()

# Search tool instance used by the research agent.
search_tool = SerperDevTool()

@CrewBase
class ResearchCrew:
    """
    ResearchCrew - defines the high-level agent/task pipeline for account research and prepares 
    a pre-meeting briefing for an account executive.

    This crew is responsible for creating a pre-meeting briefing by gathering
    company intelligence, analyzing it, and delivering informative summaries.

    Workflow (sequential):
        1. Company Research Agent  → gathers raw company intelligence using web search.
    """

    # YAML configuration files that define the agent and task behavior.
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ── Agents ────────────────────────────────────────────────────────────────

    @agent
    def company_research_agent(self) -> Agent:
        """
        Create and configure the company research agent.

        This agent performs web search using SerperDevTool and returns raw
        company intelligence for later task processing.
        """
        return Agent(
            config=self.agents_config["company_research_agent"],
            llm=llm,
            tools=[search_tool],
            verbose=True,
        )
    
    @agent
    def account_insight_agent(self) -> Agent:
        """
        Create the account insight agent.

        This agent analyzes the company research output to identify 
        business insights, pain points, strategic opportunities, and 
        concise talking points.
        """
        return Agent(
            config=self.agents_config["account_insight_agent"],
            llm=llm,
            verbose=True,
        )

    # ── Tasks ─────────────────────────────────────────────────────────────────

    @task
    def company_research_task(self) -> Task:
        """
        Define the company research task that the crew will execute.

        The task binds the research agent to the task config and declares the
        work that must be completed before subsequent steps can run.
        """
        return Task(
            config=self.tasks_config["company_research_task"],
            agent=self.company_research_agent(),
        ) # type: ignore
        
    @task
    def account_insight_task(self) -> Task:
        """
        Define the account insight task that follows initial research.

        This task takes the output of the research task as input and uses the
        account insight agent to produce sales-ready insights and narrative.
        """
        return Task(
            config=self.tasks_config["account_insight_task"],
            agent=self.account_insight_agent(),
            context=[self.company_research_task()],
        )


    # ── Crew ──────────────────────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """
        Assembles the crew with sequential processing:
        ResearchAgent → AnalystAgent → SummaryAgent

        This method declares the ordering of agents and tasks, using a
        sequential process to enforce step-by-step execution.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )

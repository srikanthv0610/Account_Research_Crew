import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

load_dotenv()

# ── LLM pointed at your APIM endpoint ───────────────────────────────────────

def build_llm() -> LLM:
    azure_apim_key = os.getenv("AZURE_APIM_SUBSCRIPTION_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

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

    raise ValueError(
        "No LLM credentials found. Set either AZURE_APIM_SUBSCRIPTION_KEY or OPENAI_API_KEY in .env"
    )

llm = build_llm()



@CrewBase
class ResearchCrew:
    """
    Research Crew — prepares a pre-meeting briefing for an account executive.
    Workflow (sequential):
        1. Company Research Agent  → gathers raw company intelligence using web search.
    """

    agents_config = "config/agents.yaml"
    tasks_config  = "config/tasks.yaml"

    # ── Agents ────────────────────────────────────────────────────────────────

    @agent
    def company_research_agent(self) -> Agent:
        """
        Searches the web and compiles raw information about the target company.
        Given access to SerperDevTool for live web search.
        """
        return Agent(
            config=self.agents_config["company_research_agent"],
            llm=llm,
            #tools=[search_tool],
            verbose=True,
        )

    # ── Tasks ─────────────────────────────────────────────────────────────────

    @task
    def company_research_task(self) -> Task:
        """
        Task 1: Research the target company using web search.
        Output feeds directly into the analysis task.
        """
        return Task(
            config=self.tasks_config["company_research_task"],
            agent=self.company_research_agent(),
        ) # type: ignore

    # ── Crew ──────────────────────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """
        Assembles the crew with sequential processing:
        ResearchAgent → AnalystAgent → SummaryAgent

        Process.sequential ensures each agent waits for the previous
        agent's output before starting — critical for context passing.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )
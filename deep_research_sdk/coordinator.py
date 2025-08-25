from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from ddgs import DDGS
import time

from deep_agents import *
from deep_research_sdk.deep_agents import query_agent

console = Console()

class ResearchCoordinator:
    def __init__(self, model: str, query: str):
        self.model = model
        self.query = query
        self.search_results = []
        self.iterations = 1
    
    async def research(self) -> str:
        query_response = await self.generate_queries()

        return "dummy report"
    
    async def generate_queries(self) -> QueryResponse:
        with console.status("[bold cyan]Generating queries...[/bold cyan]") as status:
            # Run the agent to generate queries
            query_agent = QueryAgent(self.model, self.query)
            result = await query_agent.build_queries()

            # Display the results
            console.print(Panel(f"[bold cyan]Query Analysis[/bold cyan]"))
            console.print(f"[yellow]Thoughts:[/yellow] {result.thoughts}")
            console.print("\n[yellow]Generated Queries:[/yellow]")
            for i, query in enumerate(result.queries, 1):
                console.print(f"  {i}. {query}")
        return result.final_output
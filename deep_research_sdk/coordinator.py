from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from ddgs import DDGS
import time

from .deep_agents.search_agent import SearchAgent, SearchResult
from .deep_agents.query_agent import QueryAgent, QueryResponse

console = Console()

class ResearchCoordinator:
    def __init__(self, model: str, query: str):
        self.model = model
        self.query = query
        self.search_results = []
        self.iterations = 1
    
    async def research(self) -> str:
        query_response = await self.generate_queries()

        await self.perform_research_for_queries(queries=query_response.queries)

        return "dummy"
    
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
        return result
    
    def duckduckgo_search(self, query: str) -> list[dict[str, Any]]:
        try:
            results = DDGS().text(query, region='en-us', safesearch='off', timelimit="y", max_results=1)
            return results
        except Exception as ex:
            console.log(f"[bold red]Search error:[/bold red] {str(ex)}")
            return []
    
    async def perform_research_for_queries(self, queries: list[str]) -> None:
        all_search_results = {}
        for query in queries:
            search_results = self.duckduckgo_search(query)
            all_search_results[query] = search_results

        search_agent = SearchAgent(model=self.model)

        for query in queries:
            console.print(f"[bold cyan]Searching for:[/bold cyan] {query}")

            for result in all_search_results[query]:
                console.print(f"  [green]Result:[/green] {result['title']}")
                console.print(f"  [dim]URL:[/dim] {result['href']}")
                console.print(f"  [cyan]Analyzing content...[/cyan]")

                start_analysis_time = time.time()
                search_input = f"Title: {result['title']}\nURL: {result['href']}"
                agent_result = await search_agent.search(search_input)
                analysis_time = time.time() - start_analysis_time

                search_result = SearchResult(
                    title=result["title"],
                    url=result["href"],
                    summary=agent_result
                )

                self.search_results.append(search_result)

                summary_preview = agent_result.final_output[:100] + ("..." if len(agent_result.final_output) > 100 else "")

                console.print(f"  [green]Summary:[/green] {summary_preview}")
                console.print(f"  [dim]Analysis completed in {analysis_time:.2f}s[/dim]\n")

        console.print(f"\n[bold green]✓ Research round complete![/bold green] Found {len(all_search_results)} sources across {len(queries)} queries.")
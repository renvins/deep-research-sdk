from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from ddgs import DDGS
import time

from .deep_agents.follow_up_agent import FollowUpAgent, FollowUpResponse
from .deep_agents.synthesis_agent import SynthesisAgent
from .deep_agents.search_agent import SearchAgent, SearchResult
from .deep_agents.query_agent import QueryAgent, QueryResponse

console = Console()

class ResearchCoordinator:
    def __init__(self, model: str, query: str, max_iterations: int | None = 3):
        self.model = model
        self.query = query
        self.search_results = []
        self.iteration = 0
        self.max_iterations = max_iterations
    
    async def research(self) -> str:
        query_response = await self.generate_queries()

        await self.perform_research_for_queries(queries=query_response.queries)

        self.iteration += 1
        while self.iteration < self.max_iterations:
            decision_response = await self.generate_followup()

            if not decision_response.should_follow_up:
                console.print("[cyan]No more research needed.[/cyan]")
                break

            self.iteration += 1
            console.print(f"[cyan]Conducting follow-up research (iteration {self.iteration})...[/cyan]")

            await self.perform_research_for_queries(queries=decision_response.queries)

        report = await self.synthetize_response()

        console.print("[bold green]Research completed![/bold green]")
        console.print(Markdown(report))

        return report
    
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

                summary_preview = agent_result[:100] + ("..." if len(agent_result) > 100 else "")

                console.print(f"  [green]Summary:[/green] {summary_preview}")
                console.print(f"  [dim]Analysis completed in {analysis_time:.2f}s[/dim]\n")

        console.print(f"\n[bold green]✓ Research round complete![/bold green] Found {len(all_search_results)} sources across {len(queries)} queries.")

    async def generate_followup(self) -> FollowUpResponse:
        with console.status("[bold cyan]Evaluating if we need to follow up...[/bold cyan]") as status:
            findings_text = f"Original Query: {self.query}\n\nCurrent Findings:\n"
            for i, result in enumerate(self.search_results, 1):
                findings_text += f"\n{i}. Title: {result.title}\n   URL: {result.url}\n   Summary: {result.summary}\n"

            follow_up_agent = FollowUpAgent(self.model, findings_text)
            result = await follow_up_agent.follow_up()

            console.print(Panel(f"[bold cyan]Follow-up Decision[/bold cyan]"))
            console.print(f"[yellow]Decision:[/yellow] {'More research needed' if result.should_follow_up else 'Research complete'}")
            console.print(f"[yellow]Reasoning:[/yellow] {result.reasoning}")

            if result.should_follow_up:
                console.print("\n[yellow]Follow-up Queries:[/yellow]")
                for i, query in enumerate(result.queries, 1):
                    console.print(f"  {i}. {query}")

            return result

    async def synthetize_response(self) -> str:
        with console.status("[bold cyan]Synthetizying response...[/bold cyan]") as status:
            findings = f"Query: {self.query}\n\nSearch results:\n"
            for i, result in enumerate(self.search_results, 1):
                findings += f"\n{i}.  Title: {result.title}\n    URL: {result.url}\n    Summary: {result.summary}\n"
            synthesis_agent = SynthesisAgent(self.model, findings)
            result = await synthesis_agent.synthetize()

            return result
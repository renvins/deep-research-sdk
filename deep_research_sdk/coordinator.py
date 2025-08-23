from agents import trace, Runner
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from ddgs import DDGS
import time

from deep_agents import *
from models import SearchResult

console = Console()

class ResearchCoordinator:
    def __init__(self, query: str):
        self.query = query
        self.search_results = []
        self.iterations = 1
    
    async def research(self) -> str:
        with trace("Deep Research Process"):
            query_response = await self.generate_queries()

            await self.perform_research_for_queries(queries=query_response.queries)

            while self.iterations < 3:
                follow_up_response = await self.follow_up()
                if not follow_up_response.should_follow_up:
                    break
                self.iterations += 1
                await self.perform_research_for_queries(queries=follow_up_response.queries)

            final_report = await self.synthesis_report()
            console.print(Markdown(final_report))

            return final_report
    
    async def generate_queries(self) -> QueryResponse:
        with console.status("[bold cyan]Generating queries...[/bold cyan]") as status:
            # Run the agent to generate queries
            result = await Runner.run(query_agent, input=self.query)

            # Display the results
            console.print(Panel(f"[bold cyan]Query Analysis[/bold cyan]"))
            console.print(f"[yellow]Thoughts:[/yellow] {result.final_output.thoughts}")
            console.print("\n[yellow]Generated Queries:[/yellow]")
            for i, query in enumerate(result.final_output.queries, 1):
                console.print(f"  {i}. {query}")
        return result.final_output

    def duckduckgo_search(self, query: str):
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

        for query in queries:
            console.print(f"[bold cyan]Searching for:[/bold cyan] {query}")

            for result in all_search_results[query]:
                console.print(f"  [green]Result:[/green] {result['title']}")
                console.print(f"  [dim]URL:[/dim] {result['href']}")
                console.print(f"  [cyan]Analyzing content...[/cyan]")

                start_analysis_time = time.time()
                search_input = f"Title: {result['title']}\nURL: {result['href']}"
                agent_result = await Runner.run(search_agent, input=search_input)
                analysis_time = time.time() - start_analysis_time

                search_result = SearchResult(
                    title=result["title"],
                    url=result["href"],
                    summary=agent_result.final_output
                )

                self.search_results.append(search_result)

                summary_preview = agent_result.final_output[:100] + ("..." if len(agent_result.final_output) > 100 else "")

                console.print(f"  [green]Summary:[/green] {summary_preview}")
                console.print(f"  [dim]Analysis completed in {analysis_time:.2f}s[/dim]\n")

        console.print(f"\n[bold green]✓ Research round complete![/bold green] Found {len(all_search_results)} sources across {len(queries)} queries.")

    async def follow_up(self) -> FollowUpResponse:
        findings_text = f"Original Query: {self.query}\n\nCurrent Findings:\n"
        for i, result in enumerate(self.search_results, 1):
            findings_text += f"\n{i}. Title: {result.title}\n   URL: {result.url}\n   Summary: {result.summary}\n"
    
        with console.status("Analyzing if following up is needed...") as status:
            follow_up_response = await Runner.run(follow_up_agent, input=findings_text)

            console.print(Panel(f"[bold cyan]Follow Up Response[/bold cyan]"))
            console.print(f"[yellow]Decision:[/yellow] {'More research needed' if follow_up_response.final_output.should_follow_up else 'Research complete'}")
            console.print(f"[yellow]Reasoning:[/yellow] {follow_up_response.final_output.reasoning}")

            return follow_up_response.final_output
        
    async def synthesis_report(self) -> str:
         with console.status("[bold cyan]Synthesizing research findings...[/bold cyan]") as status:
            findings_text = f"Query: {self.query}\n\nSearch Results:\n"
            for i, result in enumerate(self.search_results, 1):
                findings_text += f"\n{i}. Title: {result.title}\n   URL: {result.url}\n   Summary: {result.summary}\n"

            result = await Runner.run(synthesis_agent, input=findings_text)

            return result.final_output
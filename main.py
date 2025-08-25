import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from litellm import get_supported_openai_params

from deep_research_sdk.coordinator import ResearchCoordinator

load_dotenv()

console = Console()

async def main() -> None:
    console.print("[bold cyan]Deep Agents SDK[/bold cyan] - Based on openai-agents-sdk")
    console.print("This tool performs deep researches on any topic using OpenAI models.")

    query = Prompt.ask("\n[bold]Tell me what you would like to have deep dive into[/bold]")

    if not query.strip():
        console.print("[bold red]Error:[/bold red] Please provide a valid query.")
        return

    research_coordinator = ResearchCoordinator(model="gpt-4o-mini", query=query)
    report = await research_coordinator.research()

if __name__ == "__main__":
    asyncio.run(main())
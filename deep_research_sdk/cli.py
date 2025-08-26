import argparse
import asyncio
from rich.console import Console
from rich.prompt import Prompt
from deep_research_sdk import __version__
from deep_research_sdk import ResearchCoordinator

console = Console()

async def starting_research() -> str:
    console.print("[bold cyan]Deep Research SDK[/bold cyan] - Based on LiteLLM agents.")
    console.print("This tool performs deep researches on any topic.")

    query = Prompt.ask("\n[bold]Tell me what you would like to have deep dive into[/bold]")

    if not query.strip():
        console.print("[bold red]Error:[/bold red] Please provide a valid query.")
        return

    research_coordinator = ResearchCoordinator(model="gpt-4o-mini", query=query)
    response = await research_coordinator.research()

    return response

async def main():
    """Entry point for the CLI"""
    parser = argparse.ArgumentParser(
        prog="deep-research-sdk",
        description="Deep Research SDK - Perform deep researches with any model"
    )

    parser.add_argument(
        "--version", "-v", action="version", version=f"deep-research-sdk {__version__}", help="Show version information"
    )

    parser.add_argument("command", nargs="?", choices=["research"], help="Start research of a topic")

    args = parser.parse_args()

    if args.command != "research":
        parser.print_help()
        return
    await starting_research()

def run():
    asyncio.run(main())

if __name__ == "__main__":
    run()
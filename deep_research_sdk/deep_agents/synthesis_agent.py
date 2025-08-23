from agents import Agent

synthesis_agent = Agent(
    name="Synthesis Agent",
    instructions=SYNTHESIS_AGENT_PROMPT,
    model="gpt-4o-mini",
)
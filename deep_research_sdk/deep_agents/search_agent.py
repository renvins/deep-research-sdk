import requests
import json

from pydantic import BaseModel
from litellm import acompletion
from litellm.utils import function_to_dict
from bs4 import BeautifulSoup

from .base import BaseAgent
from .prompts.templates import SEARCH_AGENT_PROMPT
from .prompts.converter import convert_to_llm_message

def url_scrape(url: str) -> str:
    """Scrape the text from a website

        Parameters
        ----------
        url: str
          The URL of the website to scrape

        Returns
        -------
        str
            the full scraped text of the website
        """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for script in soup(["script", "style"]):
                script.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000] if len(text) > 5000 else text
        except ImportError:
            return response.text[:5000]
    except Exception as e:
        return f"Failed to scrape content from {url}: {str(e)}"

class SearchResult(BaseModel):
    title: str
    url: str
    summary: str

class SearchAgent(BaseAgent):
    def __init__(self, 
      model: str,
      system_prompt: str | None = SEARCH_AGENT_PROMPT
    ):
      super().__init__(model, system_prompt)

      if not model:
        # raise error here
        pass
    
    async def search(self, input: str):
      if not input:
        pass
      messages = convert_to_llm_message(self.system_prompt, input)
      tools = [{
        "type": "function",
        "function": function_to_dict(url_scrape)
      }]

      first_response = await acompletion(
        model=self.model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
      )
      tool_calls = first_response.choices[0].message.tool_calls

      if not tool_calls:
        raise Exception("Error during tool choosing")
        pass

      # Append for context
      messages.append(first_response.choices[0].message)
      tool_call = tool_calls[0]
      function_name = tool_call.function.name
      function_args = json.loads(tool_call.function.arguments)
      
      tool_response = url_scrape(url=function_args.get("url"))
      # Extend conversation with function response
      messages.append(
          {
              "tool_call_id": tool_call.id,
              "role": "tool",
              "name": function_name,
              "content": tool_response,
          }
      )

      second_response = await acompletion(
        model=self.model,
        messages=messages,
      )

      return second_response.choices[0].message.content

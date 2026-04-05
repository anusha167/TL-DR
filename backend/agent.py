import asyncio
import os
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

def process_single_url(url):
    """Uses Browser Use to visit a URL and extract its content"""
    
    async def run():
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        agent = Agent(
            task=f"""Go to this URL: {url}
            Extract the full text content of the page.
            Return a JSON with two fields:
            - title: the title of the article or page
            - content: the full text content""",
            llm=llm
        )
        
        result = await agent.run()
        return result
    
    try:
        result = asyncio.run(run())
        
        # Try to extract title and content from result
        result_str = str(result)
        
        # Simple extraction — return full result as content
        title = url.split("/")[-1][:50] or "Untitled"
        content = result_str
        
        return content, title
    
    except Exception as e:
        print(f"Agent failed on {url}: {e}")
        return None, None
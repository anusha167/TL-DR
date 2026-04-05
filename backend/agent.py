import asyncio
import os
import requests
from bs4 import BeautifulSoup
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

async def run_agent(url):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    agent = Agent(
        task=f"Go to {url} and extract the full article title and text content. Return the title and content.",
        llm=llm
    )

    result = await agent.run()
    return str(result)

def process_single_url(url):
    """Uses Browser Use to visit a URL and extract content, falls back to scraper"""

    # Try Browser Use first
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_agent(url))
        loop.close()

        title = url.split("/")[-1][:60] or "Untitled"
        print(f"Browser Use succeeded for {url}")
        return result, title

    except Exception as e:
        print(f"Browser Use failed ({e}), falling back to scraper")

    # Fallback: plain scraper
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(['script', 'style', 'nav', 'footer']):
            tag.decompose()
        title = soup.title.string.strip() if soup.title else url.split("/")[-1]
        content = soup.get_text(separator=' ', strip=True)
        print(f"Scraper fetched {len(content)} chars")
        return content, title

    except Exception as e:
        print(f"Scraper also failed: {e}")
        return "", url
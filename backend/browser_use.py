import asyncio
import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

class Agent:
    def __init__(self, task, llm=None):
        self.task = task
        self.llm = llm

    async def run(self):
        return await asyncio.to_thread(self._run_sync)

    def _run_sync(self):
        url = self._extract_url(self.task)
        if not url:
            raise ValueError("No URL found in task")

        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; TLDRBot/1.0; +https://example.com)"
        }, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        title = self._extract_title(soup, url)
        content = self._extract_text(soup)

        return {
            "title": title,
            "content": content,
        }

    def _extract_url(self, task):
        match = re.search(r"https?://[\w\-._~:/?#[\]@!$&'()*+,;=%]+", task)
        if not match:
            return None
        return match.group(0).rstrip('.,')

    def _extract_title(self, soup, url):
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        parsed = urlparse(url)
        return parsed.netloc

    def _extract_text(self, soup):
        for element in soup(["script", "style", "noscript", "header", "footer", "svg", "iframe"]):
            element.decompose()
        return "\n\n".join(
            paragraph.strip()
            for paragraph in soup.stripped_strings
            if paragraph.strip()
        )

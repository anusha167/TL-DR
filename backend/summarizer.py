import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize(content):
    """Takes raw content and returns a clean summary using Gemini"""

    prompt = f"""You are a concise summarizer. 
    Summarize the following content in 3-5 sentences.
    Make it clear, informative, and easy to understand.
    Do not use bullet points — write in flowing prose.
    
    Content:
    {content[:8000]}
    
    Summary:"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Summarization failed: {e}")
        return "Summary could not be generated."
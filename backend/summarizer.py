import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize(content):
    """Takes raw content and returns a clean summary using Gemini"""
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""You are a concise summarizer. 
    Summarize the following content in 3-5 sentences.
    Make it clear, informative, and easy to understand.
    Do not use bullet points — write in flowing prose.
    
    Content:
    {content[:8000]}
    
    Summary:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Summarization failed: {e}")
        return "Summary could not be generated."
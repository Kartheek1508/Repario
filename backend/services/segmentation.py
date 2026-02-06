import os
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



def segment_text(text:str):
    prompt =f"""
You extract atomic idea units.

Rules:
- Do NOT rewrite.
- Do NOT summarize.
- Preserve original wording.
- Return STRICT JSON:
[
  {{"text": "idea 1"}},
  {{"text": "idea 2"}}
]

Text:
{text}
"""
    response = client.models.generate_content(
        model = "gemini-3-flash-preview",
        contents = prompt
    )

    raw_output = response.text.strip()

    raw_output = response.text.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.replace("```json", "")
        raw_output = raw_output.replace("```", "")
        raw_output = raw_output.strip()


    try:
        parsed = json.loads(raw_output)

    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned:\n{raw_output}")
    
    return [
    {"id": i, "text": item["text"]}
    for i, item in enumerate(parsed)
]

import json
import google.generativeai as genai
import os
from dotenv import load_dotenv


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

load_dotenv()

def segment_text(text:str):
    prompt =f"""
You extract atomic idea units.

Rules:
- Do NOT rewrite.
- Do NOT summarize.
- Preserve original wording.
- Each segment must be a complete standalone statement. If splitting compound ideas, repeat necessary words.
- Return STRICT JSON:
[
  {{"text": "idea 1"}},
  {{"text": "idea 2"}}
]

Text:
{text}
"""
    response = genai.models.generate_content(
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

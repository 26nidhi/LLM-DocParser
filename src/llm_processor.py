import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_key_values(full_text):

    prompt = f"""
You are an AI system that converts unstructured PDF text into structured key:value pairs.

RULES:
- You MUST return ONLY VALID JSON.
- Keys must NOT be predefined.
- You MUST infer human-meaningful keys from the text.
- Every piece of information from the PDF MUST be captured.
- If something does not fit a key:value structure, place it inside "Comments".
- Preserve EXACT original wording in values.
- DO NOT summarize. DO NOT drop ANY information.
- Multi-line text must be preserved.
- Return a LIST of objects.

OUTPUT FORMAT (ESCAPED – DO NOT CHANGE):

[
  {{
    "key": "Some Key",
    "value": "Original text exactly from PDF",
    "comments": "More extracted context if needed"
  }},
  {{
    "key": "Another Key",
    "value": "Exact value",
    "comments": ""
  }}
]

NOW PROCESS THIS TEXT:

\"\"\"{full_text}\"\"\"

Return ONLY the JSON. Nothing else.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except:
        # fallback for ANY model failure → ALL TEXT is captured
        return [{
            "key": "UNSTRUCTURED_BLOCK",
            "value": full_text,
            "comments": "LLM JSON parse failed"
        }]

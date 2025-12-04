import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_key_values(full_text):

    # IMPORTANT — ESCAPED ALL BRACES {{ }}
    prompt = f"""
You are an AI system that converts unstructured PDF text into structured key:value pairs.

OUTPUT FORMAT (MUST FOLLOW EXACTLY):

[
  {{
    "key": "Some Key",
    "value": "Exact text from PDF",
    "comments": "Context taken exactly from PDF"
  }},
  {{
    "key": "Another Key",
    "value": "Exact value",
    "comments": ""
  }}
]

RULES:
- DO NOT predefine keys. Infer keys logically (e.g., First Name, Birth City, Age, Current Salary, Degree, CGPA).
- Use human-like clean key names.
- DO NOT drop or summarize information.
- Use context sentences as comments.
- Multi-line values allowed.
- Maintain original wording.
- Capture 100% of the PDF text either as a value or in comments.
- NO explanation outside JSON.
- NO extra text outside JSON.
- Return ONLY valid JSON.
- For ambiguous text, place in 'comments' field.

PDF TEXT TO PROCESS:
\"\"\"{full_text}\"\"\"

Now return ONLY the JSON list.
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
        return [{
            "key": "UNSTRUCTURED_BLOCK",
            "value": full_text,
            "comments": "LLM JSON parse failed"
        }]

import requests
import json
from django.conf import settings

def generate_advice(prompt):
    api_url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    system_instruction = """You are a financial advisor. Provide recommendations that:
        1. Directly reference provided transaction categories
        2. Include specific percentage/dollar savings
        3. Avoid generic advice without data support
        Format as a numbered list with no special formatting or markdown."""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 600
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        advice = response.json()['choices'][0]['message']['content']
        return [line.strip() for line in advice.split('\n') if line.strip()]
    except Exception as e:
        print(f"API Error: {str(e)}")
        return ["Error Advice could not be generated"]
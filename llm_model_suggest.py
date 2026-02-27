
import os
import re
import requests
from data_to_be_prompt import clothes_data
from prompt import build_prompt, image_prompt

# Ollama API endpoint and model (from .env or defaults)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# Send prompt to Ollama LLM (local)
def get_result(prompt: str):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns {"response": "..."}
        return data.get("response", "")
    except Exception as e:
        raise RuntimeError(f"Ollama API error: {e}")

# Parse LLM result into explanations and image prompts
def save_explaination(result):
    # Split the result by image prompts (should separate each outfit block)
    blocks = result.strip().split("**Image Prompt:**")

    explanations = []
    for block in blocks[:3]:
        block = block.strip()

        # Step 1: Find the start of the outfit explanation
        start_index = block.find("Outfit")
        if start_index == -1:
            explanations.append("No outfit explanation found.")
            continue

        # Step 2: Cut off before "Image Generation Prompt:"
        end_index = block.find("Image Generation Prompt:")
        if end_index == -1:
            end_index = len(block)

        explanation = block[start_index:end_index].strip()

        # Step 3: Remove all * characters
        explanation = explanation.replace("*", "")

        # Step 4: Add \n before key headers
        explanation = re.sub(r'(Materials, Types, and Colors:)', r'\n\1', explanation)
        explanation = re.sub(r'(Why it fits:)', r'\n\1', explanation)

        # Step 5: Remove double spaces and strip
        explanation = re.sub(r'\s+', ' ', explanation).strip()

        # Optional: Fix newline formatting for visual clarity
        explanation = explanation.replace('\n ', '\n')  # fix space after newline

        explanations.append(explanation)

    while len(explanations) < 3:
        explanations.append("No outfit suggestion available.")

    return explanations

def main(user, weather_data, clothes_data, user_input):
    # Build prompt for LLM
    prompt = build_prompt(weather_data, clothes_data, user_input)
    # Call Ollama LLM
    result = get_result(prompt)
    # Parse explanations
    explanations = save_explaination(result)
    # Parse image prompts (for SD WebUI)
    imageprompts = image_prompt(result)

    suggestions = []
    for i in range(3):
        suggestions.append({
            "image_prompt": imageprompts[i] if i < len(imageprompts) else "fashion outfit suitable for the current weather and location",
            "explanation": explanations[i] if i < len(explanations) else ""
        })

    return suggestions
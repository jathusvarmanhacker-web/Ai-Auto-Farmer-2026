import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def chat_with_ai(user_message: str, history: list, user_name: str,
                 user_location: str, user_acres: float, crops: list) -> str:
    crop_info = (
        ", ".join(f"{c['type']} ({c['stage']}, {c['area']} acres)" for c in crops)
        if crops else "none added yet"
    )
    system_prompt = (
        f"You are AgroShield AI, a smart farming assistant for {user_name}, "
        f"a farmer in {user_location} with {user_acres} acres. "
        f"Their current crops: {crop_info}. "
        "Respond in the SAME LANGUAGE as the user message (English, Tamil, or Sinhala). "
        "You are an expert on vegetables, fruits, nuts, and Sri Lankan farming. "
        "Give short, practical, friendly advice under 120 words. Always end with one emoji."
    )

    messages = []
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=system_prompt,
        messages=messages,
    )
    return response.content[0].text

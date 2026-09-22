import os

def ask_claude(messages, project_context=""):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return (
            "Claude API is not connected yet. Add ANTHROPIC_API_KEY to your "
            "Streamlit secrets/environment variables. I can still help with "
            "the deterministic calculators and BOQ workflow."
        )

    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        system = f"""
You are Civil BOQ AI, a civil-estimation assistant.
Be concise, structured and transparent.
Never invent a market rate. If a rate is unavailable, say so.
Use the project's saved rate snapshot when provided.
Separate deterministic calculations from assumptions.
For structural/construction decisions, recommend engineer verification.

Project context:
{project_context}
"""
        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514"),
            max_tokens=1200,
            system=system,
            messages=messages,
        )
        return "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
    except Exception as exc:
        return f"AI service error: {exc}"

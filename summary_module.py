from gemini_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
You are EduGenie.

Summarize the following educational
content for a student.

Requirements:

- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Keep important definitions.
- Keep important facts.
- Use bullet points where useful.
- Make it suitable for quick revision.
- Do not add information that is not present
  in the original text.

Educational Text:

{text}

Summary:
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=1400
    )
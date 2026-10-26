from gemini_client import generate_text


SYSTEM_PROMPT = """
You are EduGenie, a friendly educational assistant.

Your job is to help students understand academic
and general educational questions.

Rules:

1. Give accurate answers.
2. Use simple language.
3. Explain difficult terms.
4. Keep answers concise but useful.
5. Use examples when helpful.
6. If the question is ambiguous, clearly mention it.
7. Do not invent facts.
"""


def answer_question(
    question: str
) -> str:

    prompt = f"""
{SYSTEM_PROMPT}

Student Question:

{question}


Provide a clear educational answer.

Use:

- Short paragraphs
- Bullet points
- Examples when useful


Answer:
"""


    return generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1200
    )
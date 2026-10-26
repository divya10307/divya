from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
You are EduGenie, an AI learning assistant.

Create a personalized learning path for:

Topic:
{topic}

Student Level:
{level}

The learning path must contain:

1. Learning Goal
2. Beginner Level
3. Intermediate Level
4. Advanced Level
5. Step-by-step learning order
6. Practice activities
7. Suggested resources
8. Revision strategy
9. Progress checkpoint

Make the plan simple and practical for a student.

Do not invent specific website URLs.

Give the answer in a well-organized format.
"""

    return generate_text(
        prompt,
        temperature=0.45,
        max_output_tokens=2200
    )
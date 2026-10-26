import json
import re

from typing import Any

from gemini_client import generate_text


def clean_json_block(
    text: str
) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def validate_quiz(
    data: Any
) -> list:

    if isinstance(data, dict):

        data = data.get(
            "questions",
            []
        )


    if not isinstance(data, list):

        raise ValueError(
            "Quiz must be a list."
        )


    if len(data) != 3:

        raise ValueError(
            "Quiz must contain exactly 3 questions."
        )


    questions = []


    for index, item in enumerate(
        data,
        start=1
    ):

        if not isinstance(
            item,
            dict
        ):

            raise ValueError(
                f"Question {index} is invalid."
            )


        question = str(
            item.get(
                "question",
                ""
            )
        ).strip()


        options = item.get(
            "options",
            []
        )


        answer = str(
            item.get(
                "answer",
                ""
            )
        ).strip()


        if not question:

            raise ValueError(
                f"Question {index} has no question."
            )


        if not isinstance(
            options,
            list
        ):

            raise ValueError(
                f"Question {index} options are invalid."
            )


        if len(options) != 4:

            raise ValueError(
                f"Question {index} must have 4 options."
            )


        options = [
            str(option).strip()
            for option in options
        ]


        if answer not in options:

            if answer in [
                "A",
                "B",
                "C",
                "D"
            ]:

                position = ord(answer) - ord("A")

                answer = options[position]

            else:

                raise ValueError(
                    f"Question {index} has an invalid answer."
                )


        questions.append({

            "question": question,

            "options": options,

            "answer": answer

        })


    return questions


def generate_quiz(
    passage: str
) -> list:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly 3 multiple-choice questions
from the passage below.

Each question must have exactly 4 options.

Return ONLY valid JSON.

Do NOT use Markdown.

Use this exact structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option"
        }}
    ]
}}

The answer must exactly match
one of the four options.

Make the questions educational
and relevant to the passage.

Passage:

{passage}
"""


    response = generate_text(

        prompt,

        temperature=0.5,

        max_output_tokens=1800
    )


    cleaned = clean_json_block(
        response
    )


    try:

        data = json.loads(
            cleaned
        )

        return validate_quiz(
            data
        )


    except Exception as first_error:

        repair_prompt = f"""
Convert the following quiz into valid JSON.

Return exactly 3 questions.

Each question must contain:

question
options
answer

Each question must have
exactly 4 options.

The answer must exactly match
one option.

Return ONLY JSON.

Quiz:

{response}
"""


        repaired = generate_text(

            repair_prompt,

            temperature=0.1,

            max_output_tokens=1800
        )


        try:

            repaired_json = json.loads(
                clean_json_block(
                    repaired
                )
            )

            return validate_quiz(
                repaired_json
            )


        except Exception as second_error:

            raise RuntimeError(
                "Quiz generation failed. "
                f"First error: {first_error}. "
                f"Second error: {second_error}"
            )
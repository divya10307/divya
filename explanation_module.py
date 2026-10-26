from config import USE_LOCAL_EXPLANATION

from gemini_client import generate_text


_local_pipeline = None


def _local_explain(
    text: str
) -> str:

    global _local_pipeline


    if _local_pipeline is None:

        from transformers import pipeline

        _local_pipeline = pipeline(

            "text2text-generation",

            model="MBZUAI/LaMini-Flan-T5-783M"
        )


    prompt = f"""
Explain the following concept
in very simple language.

Use an example if possible.

Concept:

{text}
"""


    result = _local_pipeline(

        prompt,

        max_new_tokens=300,

        do_sample=False
    )


    return result[0][
        "generated_text"
    ].strip()


def explain_concept(
    text: str
) -> str:

    # Use local LaMini model if enabled

    if USE_LOCAL_EXPLANATION:

        try:

            return _local_explain(text)

        except Exception:

            # Fallback to Gemini

            return generate_text(

                f"""
Explain this educational concept
in simple beginner-friendly language.

Concept:

{text}
""",

                temperature=0.35,

                max_output_tokens=1200
            )


    # Default Gemini explanation

    return generate_text(

        f"""
Explain the following concept
for a beginner.

Use simple language.

Give an example if useful.

Concept:

{text}
""",

        temperature=0.35,

        max_output_tokens=1200
    )
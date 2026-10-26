from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="AI-powered educational learning assistant"
)


# --------------------------------------------------
# Static Files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class TextRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class TopicRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# --------------------------------------------------
# Question Answering
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: QuestionRequest):

    try:

        answer = answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Concept Explanation
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    try:

        answer = explain_concept(
            payload.text
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Quiz Generation
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: TextRequest):

    try:

        quiz = generate_quiz(
            payload.text
        )

        return {
            "quiz": quiz
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Text Summarization
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    try:

        summary = summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# --------------------------------------------------
# Learning Recommendations
# --------------------------------------------------

@app.post("/learn/recommendations")
async def recommendations(
    payload: TopicRequest
):

    try:

        recommendations = get_learning_recommendations(
            payload.topic,
            payload.level
        )

        return {
            "recommendations": recommendations
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )
# app/services/generation.py
from openai import OpenAI
from app.config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

def generate_answer(question: str, chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source: {c['title']}]\n{c['chunk_text']}" for c in chunks
    )

    prompt = f"""You are an assistant answering questions about Ayurveda IP and regulatory guidance.
Use ONLY the information in the sources below. If the sources don't contain enough information, say so clearly.
Always be precise — this is a legal/regulatory context.

Sources:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model=settings.GENERATION_MODEL_NAME,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    print("RAW RESPONSE:", response)  # temporary debug line

    return response.choices[0].message.content

def generate_synthesis(question: str, per_regime_answers: list[dict]) -> str:
    combined = "\n\n".join(
        f"[{r['regime']}]\n{r['answer']}" for r in per_regime_answers
    )

    prompt = f"""You are comparing regulatory guidance across jurisdictions for Ayurveda-related IP and regulatory questions.
Below are answers already generated for each jurisdiction, based strictly on their own regulatory sources.

Question: {question}

Per-jurisdiction answers:
{combined}

Write a brief, precise synthesis (3-5 sentences) highlighting where these jurisdictions agree or differ. Do not introduce new claims — only compare what's stated above."""

    response = client.chat.completions.create(
        model=settings.GENERATION_MODEL_NAME,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content
    if not content:
        content = "Synthesis unavailable — please review the per-jurisdiction answers above."

    return content
# app/routers/query.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.schemas.query import QueryRequest, QueryResponse
from app.services.retrieval import retrieve_chunks
from app.services.generation import generate_answer

router = APIRouter(prefix="/api/v1/query", tags=["query"])

@router.post("", response_model=QueryResponse)
def query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
):
    chunks = retrieve_chunks(
        query=request.question,
        regime=request.regime,
        top_k=request.top_k,
    )
    print("RETRIEVED CHUNKS:", chunks)

    answer = generate_answer(request.question, chunks)

    return QueryResponse(
        answer=answer,
        regime=request.regime,
        citations=chunks,
    )
from app.services.cache import query_cache, make_cache_key

@router.post("", response_model=QueryResponse)
def query(request: QueryRequest, current_user: User = Depends(get_current_user)):
    cache_key = make_cache_key(request.question, request.regime, request.top_k)
    cached = query_cache.get(cache_key)
    if cached:
        return cached

    chunks = retrieve_chunks(query=request.question, regime=request.regime, top_k=request.top_k)
    answer = generate_answer(request.question, chunks)

    result = QueryResponse(answer=answer, regime=request.regime, citations=chunks)
    query_cache[cache_key] = result
    return result

from app.models.schemas.query import CompareQueryRequest, CompareQueryResponse, RegimeAnswer
from app.services.generation import generate_synthesis

@router.post("/compare", response_model=CompareQueryResponse)
def compare_query(
    request: CompareQueryRequest,
    current_user: User = Depends(get_current_user),
):
    per_regime_answers = []

    for regime in request.regimes:
        chunks = retrieve_chunks(
            query=request.question,
            regime=regime,
            top_k=request.top_k,
        )
        answer = generate_answer(request.question, chunks)
        per_regime_answers.append({
            "regime": regime,
            "answer": answer,
            "citations": chunks,
        })

    synthesis = generate_synthesis(request.question, per_regime_answers)

    return CompareQueryResponse(
        per_regime_answers=per_regime_answers,
        synthesis=synthesis,
    )

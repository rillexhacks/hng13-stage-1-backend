# app/main.py
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
from src.db.main import init_db, get_session

from src import schemas
from src import models, crud, utils

# from . import database, models, schemas, crud, utils


string_router = APIRouter()


@string_router.get("/strings/filter-by-natural-language", response_model=dict)
async def filter_by_natural_language(
    query: str = Query(..., description="Natural language filter query"),
    session: AsyncSession = Depends(get_session),
):
    try:
        parsed_filters = utils.parse_natural_language_query(query)
        data = await crud.get_filtered_strings(
            session=session,
            is_palindrome=parsed_filters.get("is_palindrome"),
            min_length=parsed_filters.get("min_length"),
            max_length=parsed_filters.get("max_length"),
            word_count=parsed_filters.get("word_count"),
            contains_character=parsed_filters.get("contains_character"),
        )

        # Convert SQLModel objects to dicts to ensure proper JSON serialization
        response_data = []
        for item in data:
            response_data.append(
                {
                    "id": item.id,
                    "value": item.value,
                    "properties": item.properties,
                    "created_at": item.created_at,
                }
            )

        return {
            "data": response_data,
            "count": len(response_data),
            "interpreted_query": {"original": query, "parsed_filters": parsed_filters},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@string_router.post("/strings", response_model=schemas.StringResponse, status_code=201)
async def analyze_string_endpoint(
    payload: schemas.StringCreate, session: AsyncSession = Depends(get_session)
):
    value = payload.value.strip()
    if not value:
        raise HTTPException(status_code=400, detail="Missing or empty 'value' field")

    sha, properties = utils.analyze_string(value)

    # Check for existing string by value first
    existing = await crud.get_by_value(session, value)
    if existing:
        raise HTTPException(status_code=409, detail="String already exists")

    record = models.AnalyzedString(id=sha, value=value, properties=properties)

    try:
        created = await crud.create_string(session, record)
        return created
    except Exception as e:
        # If we get a unique constraint violation or any other error
        raise HTTPException(status_code=500, detail=str(e))


@string_router.get("/strings/{string_value}", response_model=schemas.StringResponse)
async def get_string_by_value(
    string_value: str, session: AsyncSession = Depends(get_session)
):
    record = await crud.get_by_value(session, string_value)
    if not record:
        raise HTTPException(status_code=404, detail="String not found")
    return record


@string_router.get("/all_strings", response_model=list[schemas.StringResponse])
async def get_all_strings(session: AsyncSession = Depends(get_session)):
    return await crud.get_all(session)


@string_router.get("/strings", response_model=dict)
async def get_all_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None),
    max_length: Optional[int] = Query(None),
    word_count: Optional[int] = Query(None),
    contains_character: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
):
    try:
        records = await crud.get_filtered_strings(
            session,
            is_palindrome=is_palindrome,
            min_length=min_length,
            max_length=max_length,
            word_count=word_count,
            contains_character=contains_character,
        )
        data = [schemas.StringResponse.from_orm(r) for r in records]

        return {
            "data": data,
            "count": len(data),
            "filters_applied": {
                "is_palindrome": is_palindrome,
                "min_length": min_length,
                "max_length": max_length,
                "word_count": word_count,
                "contains_character": contains_character,
            },
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@string_router.delete("/strings/{string_value}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_string(
    string_value: str, session: AsyncSession = Depends(get_session)
):
    deleted = await crud.delete_by_value(session, string_value)
    if not deleted:
        raise HTTPException(
            status_code=404, detail="String does not exist in the system"
        )
    return None  # 204 No Content

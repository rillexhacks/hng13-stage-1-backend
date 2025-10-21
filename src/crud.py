# app/crud.py
from typing import List, Optional
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import AnalyzedString
from sqlalchemy import func
from src import models


async def get_by_value(session: AsyncSession, value: str):
    result = await session.exec(
        select(AnalyzedString).where(AnalyzedString.value == value)
    )
    return result.scalar_one_or_none()


async def create_string(session: AsyncSession, record: AnalyzedString):
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def get_all(session: AsyncSession):
    result = await session.exec(select(AnalyzedString))
    return result.scalars().all()


async def get_filtered_strings(
    session: AsyncSession,
    is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    word_count: Optional[int] = None,
    contains_character: Optional[str] = None,
) -> List[AnalyzedString]:
    query = select(AnalyzedString)

    # properties is a JSON column containing info like length, word_count, etc.
    if is_palindrome is not None:
        query = query.where(
            AnalyzedString.properties["is_palindrome"].as_boolean() == is_palindrome
        )
    if min_length is not None:
        query = query.where(
            AnalyzedString.properties["length"].as_integer() >= min_length
        )
    if max_length is not None:
        query = query.where(
            AnalyzedString.properties["length"].as_integer() <= max_length
        )
    if word_count is not None:
        query = query.where(
            AnalyzedString.properties["word_count"].as_integer() == word_count
        )
    if contains_character is not None:
        query = query.where(
            func.lower(AnalyzedString.value).contains(contains_character.lower())
        )

    result = await session.exec(query)
    return result.scalars().all()


async def delete_by_value(session: AsyncSession, value: str):
    # compute hash to find exact record
    import hashlib

    sha = hashlib.sha256(value.strip().encode()).hexdigest()

    result = await session.exec(select(AnalyzedString).where(AnalyzedString.id == sha))
    record = result.scalar_one_or_none()

    if not record:
        return None

    await session.delete(record)
    await session.commit()
    return True

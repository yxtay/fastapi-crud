from typing import Annotated

from databases import Database
from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.api import crud
from app.api.models import NoteDB, NoteSchema
from app.db import database, engine, metadata

metadata.create_all(engine)

router = APIRouter()


async def get_db():
    try:
        await database.connect()
        yield database
    finally:
        await database.disconnect()


@router.post("/", response_model=NoteDB, status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteSchema, db: Annotated[Database, Depends(get_db)]):
    note_id = await crud.post(db, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(
    id: Annotated[int, Path(..., gt=0)], db: Annotated[Database, Depends(get_db)]
):
    note = await crud.get(db, id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


@router.get("/", response_model=list[NoteDB])
async def read_all_notes(db: Annotated[Database, Depends(get_db)]):
    return await crud.get_all(db)


@router.put("/{id}/", response_model=NoteDB)
async def update_note(
    payload: NoteSchema,
    id: Annotated[int, Path(..., gt=0)],
    db: Annotated[Database, Depends(get_db)],
):
    note = await crud.get(db, id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    note_id = await crud.put(db, id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(
    id: Annotated[int, Path(..., gt=0)], db: Annotated[Database, Depends(get_db)]
):
    note = await crud.get(db, id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    await crud.delete(db, id)

    return note

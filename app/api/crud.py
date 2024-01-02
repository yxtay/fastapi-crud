from databases import Database

from app.api.models import NoteSchema
from app.db import notes


async def post(db: Database, payload: NoteSchema):
    query = notes.insert().values(title=payload.title, description=payload.description)
    return await db.execute(query=query)


async def get(db: Database, id: int):
    query = notes.select().where(id == notes.c.id)
    return await db.fetch_one(query=query)


async def get_all(
    db: Database,
):
    query = notes.select()
    return await db.fetch_all(query=query)


async def put(db: Database, id: int, payload: NoteSchema):
    query = (
        notes.update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await db.execute(query=query)


async def delete(db: Database, id: int):
    query = notes.delete().where(id == notes.c.id)
    return await db.execute(query=query)

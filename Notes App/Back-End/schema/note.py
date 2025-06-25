def NoteEntity(item) -> dict:
    return {
        "Note": str(item["Note"]),
        "id": str(item["_id"]),
        "date": str(item["date"])
    }

def NoteEntityList(items) -> list:

    return [NoteEntity(item) for item in items]
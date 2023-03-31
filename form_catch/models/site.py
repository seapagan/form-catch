import ormar

from form_catch.database.db import database, metadata


class Site(ormar.Model):
    class Meta:
        tablename = "sites"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    slug: str = ormar.String(max_length=20)

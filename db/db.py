import databases
import sqlalchemy
import ormar
from utils.config import settings

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata

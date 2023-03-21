import databases
import ormar
import sqlalchemy
from utils.config import settings

database = databases.Database(settings.DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata

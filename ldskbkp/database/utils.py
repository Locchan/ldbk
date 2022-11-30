from ldskbkp.conf.config import DB_CONFIG_KEYS
from ldskbkp.database.connection import get_transaction
from ldskbkp.database.models import Config
from __main__ import database_version


def validate_db():
    session, session_transaction = get_transaction()
    with session_transaction:
        version = session.query(Config).filter_by(key=DB_CONFIG_KEYS["version"]).first()
        if version is None:
            return False
        else:
            return version


def initialize_new_db():
    session, session_transaction = get_transaction()
    with session_transaction:
        session.add(Config(key=DB_CONFIG_KEYS["version"], value=database_version))


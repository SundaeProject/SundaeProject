from logging import getLogger
from sqlalchemy.orm import sessionmaker


class Plugin:
    info = {
        "name": "Plugin",
        "description": "Plugin description",
        "version": "0.0.1-alpha",
    }

    def __init__(self, base):
        self.logger = getLogger(self.info.get("name", self.__class__.__name__))
        self.base = base
        self.database_session = sessionmaker(bind=self.base.database_engine)()
        self.logger.info(f"Plugin {self.info['name']} loaded")

    def __repr__(self) -> str:
        return f"<Plugin: {self.info.get('name', self.__class__.__name__)}>"

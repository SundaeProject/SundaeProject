import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models import Base as ModelBase, Settings
import os
import importlib


class Base:
    def __init__(self):
        # Sets up logging
        self.setup_logging()
        self.logger = logging.getLogger("Base")

        # Loads config
        self.config = json.load(open("config.json", "r"))
        self.logger.info("Loaded config from `config.json`")

        # Sets up database
        self.database_session = None
        self.database_engine = None
        self.setup_database()

        # Load Models
        self.setup_models()

        # Load settings from database
        self.setup_settings()

        # Load plugins
        self.plugins = {}
        self.load_plugins()

    def setup_logging(self) -> None:
        return logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s: %(name)s: %(levelname)s:\t %(message)s",
        )

    def setup_database(self) -> None:
        self.database_engine = create_engine(
            self.config["database"]["url"], echo=self.config["database"]["echo"]
        )
        self.database_session = sessionmaker(bind=self.database_engine)()

    def setup_models(self) -> None:
        ModelBase.metadata.create_all(bind=self.database_engine)

    def setup_settings(self) -> None:
        # Try loading settings from database, if not present create a new row.
        settings = (
                self.database_session.query(Settings.Settings)
                .filter(Settings.Settings.identifier == "base_settings")
                .first()
        )
        if not settings:
            settings = Settings.Settings(identifier="base_settings")
            self.database_session.add(settings)
            self.database_session.commit()
            self.logger.info("Created new settings row in database")
        self.logger.info("Settings setup complete")

    def load_plugins(self) -> None:
        for plugin in os.listdir("Plugins"):
            # Import the plugin
            p = importlib.import_module(f"Plugins.{plugin}")
            self.plugins[plugin] = p.__getattribute__(plugin)(self)
        self.logger.info(f"Loaded {len(self.plugins)} plugins")

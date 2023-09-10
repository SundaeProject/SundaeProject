from classes.Plugin import Plugin
from .Models import Base as ModelBase
from .Models import TestModel


class TestPlugin(Plugin):
    info = {
        "name": "TestPlugin",
        "description": "Test plugin",
        "version": "0.0.1-alpha",
    }

    def __init__(self, base):
        super().__init__(base)
        # Setting up database
        ModelBase.metadata.create_all(bind=self.base.database_engine)
        self.logger.info("TestPlugin database setup complete")
        self.run_something()

    def __repr__(self) -> str:
        return f"<Plugin: {self.info.get('name', self.__class__.__name__)}>"

    def run_something(self):
        test = TestModel.TestModel(name="Test", description="Test description")
        self.database_session.add(test)
        self.database_session.commit()
        self.logger.info("Added test model to database")

import os, sys
currentdir = os.getcwd()
sys.path.append(os.path.join(currentdir, 'app'))
from os.path import exists
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.model import CycleMeta, CycleTimeSeries, Model
from app.archive_constants import TEST_DB_URL, FORMAT
from app.controllers import cell_controller as cc 
from datetime import date

@pytest.fixture(scope="session")
def db_engine():
    engine_ = create_engine(TEST_DB_URL, echo=True)
    Model.metadata.create_all(engine_)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    session_ = db_session_factory()

    yield session_

    session_.rollback()
    session_.close()

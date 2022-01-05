import os
from os.path import exists
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sys
currentdir = os.getcwd()
sys.path.append(os.path.join(currentdir, 'app'))
from app.model import Model
from app.archive_constants import TEST_DB_URL
from app.controllers import cell_controller as cc 

rawTestDataPath = "/bas/tests/test_data/01_raw/"

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

@pytest.mark.skip(reason="test takes a long time to run")
def test_export_cycle_cells_to_csv_full(db_session):
    cell_lists_path = "/bas/data/01_raw/default_user/data_set_samples/cycle/"
    assert cc.import_cells_xls_to_db(cell_lists_path)
    cell_id = "HC_VC"
    out = rawTestDataPath + "tmp/out/cycle/"
    cc.export_cycle_ts_data_csv(cell_id,out)

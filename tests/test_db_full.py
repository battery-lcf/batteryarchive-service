import os
from os.path import exists
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.app.model import CycleMeta, CycleTimeSeries, Model
from src.app.archive_constants import DB_URL, FORMAT
from src.api.controllers.cell_controller import (
    export_cycle_ts_data_csv, import_cells_xls_to_db,
    export_cycle_cells_to_fmt, export_cycle_meta_data_with_id_to_fmt,
    update_cycle_cells)

rawTestDataPath = "/bas/tests/test_data/01_raw/"

@pytest.fixture(scope="session")
def db_engine():
    engine_ = create_engine(DB_URL, echo=True)
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


def test_export_cycle_cells_to_csv_full(db_session):
    cell_lists_path = "/bas/data/01_raw/default_user/data_set_samples/cycle/"
    assert import_cells_xls_to_db(cell_lists_path)
    cell_id = "HC_VC"
    out = rawTestDataPath + "tmp/out/cycle/"
    export_cycle_ts_data_csv(cell_id,out)

import pandas as pd
import os
from os.path import exists
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from model import ArchiveOperator, CycleMeta, CycleTimeSeries, Model
from archive_constants import TEST_DB_URL

tmpBasePath = "/bas/tests/test-data/tmp/"
os.makedirs(tmpBasePath, exist_ok=True)


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


def test_generate_cycle_data(db_session):
    output_file = tmpBasePath + "cell_id_cycle_data.csv"
    cell_id = "cell_id"
    new_CycleData = CycleMeta(cell_id=cell_id,
                              temperature=1,
                              v_max=1,
                              v_min=1.0,
                              soc_max=1.0,
                              soc_min=1.0,
                              crate_c=1.0,
                              crate_d=1.0)
    db_session.add(new_CycleData)
    db_session.commit()
    ao = ArchiveOperator(TEST_DB_URL)
    ao.generate_cycle_data(cell_id, tmpBasePath)
    assert exists(output_file)
    db_session.delete(new_CycleData)
    os.remove(output_file)
    assert ~exists(output_file)


def test_generate_timeseries_data(db_session):
    output_file = tmpBasePath + "cell_id_timeseries_data.csv"
    cell_id = "cell_id"
    new_Timeseries = CycleTimeSeries(
        cycle_index=1,
        cell_id=cell_id,
        v=1,
        i=1,
        cycle_time=1.0,
        ah_c=1.0,
        ah_d=1.0,
        e_c=1.0,
        e_d=1.0,
        temp_1=1.0,
        temp_2=1.0,
        date_time=1.0,
        test_time=1.0,
    )
    db_session.add(new_Timeseries)
    db_session.commit()
    ao = ArchiveOperator(TEST_DB_URL)
    ao.generate_timeseries_data(cell_id, tmpBasePath)
    assert exists(output_file)
    db_session.delete(new_Timeseries)
    os.remove(output_file)
    assert ~exists(output_file)


def test_add_abuse_cells_to_database(db_session):
    cell_lists_path = "/bas/tests/test-data/abuse/"
    Model.metadata.drop_all(db_session.bind)
    ao = ArchiveOperator(TEST_DB_URL)
    assert ao.add_cells_to_database(cell_lists_path)


def test_add_cycle_cells_to_database(db_session):
    cell_lists_path = "/bas/tests/test-data/cycle/"
    result_path = (
        "/bas/tests/test-data/cycle/MACCOR_example/MACCOR_example.txt_df"
    )
    Model.metadata.drop_all(db_session.bind)
    ao = ArchiveOperator(TEST_DB_URL)
    assert ao.add_cells_to_database(cell_lists_path)
    os.remove(result_path)


@pytest.mark.skip(reason="not yet implemented. requires sqlalchemy")
def test_export_cells(db_session):
    pass


@pytest.mark.skip(reason="not yet implemented. requires sqlalchemy")
def test_update_cells():
    pass

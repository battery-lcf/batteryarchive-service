import os, sys
currentdir = os.getcwd()
sys.path.append(os.path.join(currentdir))
sys.path.append(os.path.join(currentdir, 'app'))
from os.path import exists
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.model import CycleMeta, CycleTimeSeries, Model
from app.archive_constants import TEST_DB_URL, FORMAT
from app.controllers import cell_controller as cc 
from datetime import date

testDataBasePath = os.path.join(currentdir, 'tests', 'test_data')
tmpBasePath = os.path.join(testDataBasePath, "tmp",'')
os.makedirs(tmpBasePath, exist_ok=True)
os.environ['DATABASE_CONNECTION'] = TEST_DB_URL


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
    output_file = os.path.join(
        tmpBasePath, "cell_id_cycle_data.csv")
    cell_id = "cell_id"
    print("CYCLE DATA TEST START")
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
    cc.export_cycle_meta_data_with_id_to_fmt(cell_id, tmpBasePath,
                                          FORMAT.CSV.value)
    assert exists(output_file)
    db_session.delete(new_CycleData)
    db_session.commit()
    os.remove(output_file)
    assert ~exists(output_file)


def test_generate_timeseries_data(db_session):
    output_file = os.path.join(
        tmpBasePath, "cell_id_timeseries_data.csv")
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
        env_temperature=1.0,
        cell_temperature=1.0,
        date_time=date.today(),
        test_time=1.0,
    )
    db_session.add(new_Timeseries)
    db_session.commit()
    cc.export_cycle_ts_data_csv(cell_id, tmpBasePath)
    assert exists(output_file)
    db_session.delete(new_Timeseries)
    db_session.commit()
    os.remove(output_file)
    assert ~exists(output_file)


def test_add_abuse_cells_to_database(db_session):
    cell_lists_path = os.path.join(
        testDataBasePath, "abuse", '')

    Model.metadata.drop_all(db_session.bind)
    assert cc.import_cells_xls_to_db(cell_lists_path)


def test_add_cycle_cells_to_database(db_session):
    cell_lists_path = os.path.join(
        testDataBasePath, "cycle", '')
    temp_file_path = os.path.join(
        testDataBasePath, "cycle", 'MACCOR_example', 'MACCOR_example.txt_df')
    Model.metadata.drop_all(db_session.bind)
    assert cc.import_cells_xls_to_db(cell_lists_path)
    os.remove(temp_file_path)


@pytest.mark.skip(reason="takes long time to run")
def test_add_cycle_cells_to_database_full(db_session):
    cell_lists_path = os.path.join(
        testDataBasePath, "feather", 'in', 'cycle', '')
    Model.metadata.drop_all(db_session.bind)
    assert cc.import_cells_xls_to_db(cell_lists_path)


def test_export_cells_to_feather():
    cell_id = "HC_VC"
    out = os.path.join(
        testDataBasePath, "tmp",'')
    cc.export_cycle_meta_data_with_id_to_fmt(cell_id, out, FORMAT.FEATHER.value)
    assert True


def test_export_db_to_csv(db_session):
    cell_lists_path = os.path.join(
        testDataBasePath, "cycle",'')
    temp_file_path = os.path.join(
        testDataBasePath, "cycle",'MACCOR_example', 'MACCOR_example.txt_df')
    Model.metadata.drop_all(db_session.bind)
    cc.import_cells_xls_to_db(cell_lists_path)
    cc.export_cycle_cells_to_fmt(cell_lists_path, tmpBasePath)
    assert exists(temp_file_path)
    os.remove(temp_file_path)
    assert ~exists(temp_file_path)

def test_export_db_to_feather(db_session):
    cell_lists_path = os.path.join(
        testDataBasePath, "cycle",'')
    temp_file_path = os.path.join(
        testDataBasePath, "cycle",'MACCOR_example', 'MACCOR_example.txt_df')
    Model.metadata.drop_all(db_session.bind)
    cc.import_cells_xls_to_db(cell_lists_path)
    cell_id = "HC_VC"
    cc.export_cycle_meta_data_with_id_to_fmt(cell_id, tmpBasePath,
                                          FORMAT.FEATHER.value)
    assert exists(temp_file_path)
    os.remove(temp_file_path)
    assert ~exists(temp_file_path)


def test_update_cycle_cells():
    cell_lists_path = os.path.join(
        testDataBasePath, "cycle", '')
    cc.import_cells_xls_to_db(cell_lists_path)
    assert cc.update_cycle_cells(cell_lists_path)
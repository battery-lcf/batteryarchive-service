import os
from pandas.core.frame import DataFrame
from sqlalchemy import (
    Column,
    Index,
    Integer,
    TEXT,
    Float,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from sqlalchemy.sql.sqltypes import FLOAT, TIMESTAMP
from app.archive_constants import (LABEL, DEGREE, OUTPUT_LABELS, SLASH,
                               ARCHIVE_TABLE, CELL_LIST_FILE_NAME, DB_URL, TEST_DB_URL)
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Model = declarative_base()


class AbuseMeta(Model):
    __tablename__ = ARCHIVE_TABLE.ABUSE_META.value
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    temperature = Column(Float, nullable=True)
    thickness = Column(Float, nullable=True)
    v_init = Column(Float, nullable=True)
    indentor = Column(Float, nullable=True)
    nail_speed = Column(Float, nullable=True)
    soc = Column(Float, nullable=True, primary_key=True)
    idx_abuse_metadata_cell_id = Index("cell_id")

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "thickness": self.thickness,
            "v_init": self.v_init,
            "indentor": self.indentor,
            "nail_speed": self.nail_speed,
            "cell_id": self.cell_id,
            "soc" : self.soc
        }

class AbuseTimeSeries(Model):
    __tablename__ = ARCHIVE_TABLE.ABUSE_TS.value
    axial_d = Column(Float, nullable=True)
    axial_f = Column(FLOAT, nullable=True)
    v = Column(FLOAT, nullable=True)
    norm_d = Column(Float, nullable=True)
    strain = Column(Float, nullable=True)
    top_indent_temperature = Column(Float, nullable=True)
    top_back_temperature = Column(Float, nullable=True)
    left_bottom_temperature = Column(Float, nullable=True)
    right_bottom_temperature = Column(Float, nullable=True)
    above_punch_temperature = Column(Float, nullable=True)
    below_punch_temperature = Column(Float, nullable=True)
    test_time = Column(Float, nullable=True, primary_key=True)
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    ambient_temperature = Column(Float, nullable=True)
    load = Column(Float, nullable=True)
    idx_abuse_timeseries_cell_id = Index("cell_id")

    def to_dict(self):
        return {
            "axial_d": self.axial_d,
            "axial_f": self.axial_f,
            "v": self.v,
            "strain": self.strain,
            "top_indent_temperature": self.top_indent_temperature,
            "top_back_temperature": self.top_back_temperature,
            "left_bottom_temperature": self.left_bottom_temperature,
            "right_bottom_temperature": self.right_bottom_temperature,
            "above_punch_temperature": self.above_punch_temperature,
            "below_punch_temperature": self.below_punch_temperature,
            "test_time": self.test_time,
            "cell_id": self.cell_id,
            "ambient_temperature": self.ambient_temperature,
            "load": self.load
        }

class CellMeta(Model):
    __tablename__ = ARCHIVE_TABLE.CELL_META.value
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    anode = Column(TEXT, nullable=True)
    cathode = Column(TEXT, nullable=True)
    source = Column(TEXT, nullable=True)
    ah = Column(Integer, nullable=True)
    form_factor = Column(TEXT, nullable=True)
    test = Column(TEXT, nullable=False, primary_key=True)
    tester = Column(TEXT, nullable=True)
    status = Column(TEXT, nullable=True)
    weight = Column(TEXT, nullable=True)
    dimensions = Column(TEXT, nullable=True)
    idx_cell_metadata_cell_id = Index("cell_id")

    def to_dict(self):
        return {
            "cell_id": self.cell_id,
            "anode": self.anode,
            "cathode": self.cathode,
            "source": self.source,
            "ah": self.ah,
            "form_factor": self.form_factor,
            "test": self.test,
            "tester": self.tester,
            "status": self.status,
            "weight": self.weight,
            "dimensions": self.dimensions
            # "mapping": self.mapping
        }

    @staticmethod
    def columns():
        return [
            "cell_id", "anode", "cathode", "source", "ah", "form_factor",
            "test", "tester","status", "weight", "dimensions"#, "mapping"
        ]

class CycleMeta(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_META.value
    temperature = Column(Float, nullable=True)
    soc_max = Column(Float, nullable=True)
    soc_min = Column(Float, nullable=True)
    v_max = Column(Float, nullable=True)
    v_min = Column(Float, nullable=True)
    crate_c = Column(Float, nullable=True)
    crate_d = Column(Float, nullable=True)
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    step = Column(Integer, nullable=True, primary_key=True)
    idx_cycle_metadata_cell_id = Index("cell_id")

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "soc_max": self.soc_max,
            "soc_min": self.soc_min,
            "v_max": self.v_max,
            "v_min": self.v_min,
            "crate_c": self.crate_c,
            "crate_d": self.crate_d,
            "cell_id": self.cell_id,
            "step": self.step
        }

class CycleStats(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_STATS.value
    v_max = Column(Float, nullable=True)
    v_min = Column(Float, nullable=True)
    ah_c = Column(Float, nullable=True)
    ah_d = Column(Float, nullable=True)
    e_c = Column(Float, nullable=True)
    e_d = Column(Float, nullable=True)
    i_max = Column(Float, nullable=True)
    i_min = Column(Float, nullable=True)
    v_c_mean = Column(Float, nullable=True)
    v_d_mean = Column(Float, nullable=True)
    e_eff = Column(Float, nullable=True)
    ah_eff = Column(Float, nullable=True)
    cycle_index = Column(Integer, nullable=True, primary_key=True)
    test_time = Column(Float, nullable=False, primary_key=True)
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    idx_cycle_stats_cell_id_cycle_index = Index("cell_id", "cycle_index")
    idx_cycle_stats_cell_id = Index("cell_id")

    def to_dict(self):
        return {
            "v_max": self.v_max,
            "v_min": self.v_min,
            "ah_c": self.ah_c,
            "ah_d": self.ah_d,
            "e_c": self.e_c,
            "e_d": self.e_d,
            "i_max": self.i_max,
            "i_min": self.i_min,
            "v_c_mean": self.v_c_mean,
            "v_d_mean": self.v_d_mean,
            "e_eff": self.e_eff,
            "ah_eff": self.ah_eff,
            "cycle_index": self.cycle_index,
            "test_time": self.test_time,
            "cell_id": self.cell_id
        }

class CycleTimeSeries(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_TS.value
    i = Column(Float, nullable=True)
    v = Column(Float, nullable=True)
    ah_c = Column(Float, nullable=True)
    ah_d = Column(Float, nullable=True)
    e_c = Column(Float, nullable=True)
    e_d = Column(Float, nullable=True)
    env_temperature = Column(Float, nullable=True)
    cell_temperature = Column(Float, nullable=True)
    cycle_time = Column(Float, nullable=True)
    date_time = Column(TIMESTAMP, nullable=True)
    cycle_index = Column(Integer, nullable=False, primary_key=True)
    test_time = Column(Float, nullable=True)
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    idx_cycle_timeseries_cell_id_cycle_index = Index("cell_id", "cycle_index")
    idx_cycle_timeseries_cell_id = Index("cell_id")


    def to_dict(self):
        return {
            "i": self.i,
            "v": self.v,
            "ah_c": self.ah_c,
            "ah_d": self.ah_d,
            "env_temperature": self.env_temperature,
            "cell_temperature": self.cell_temperature,
            "e_c": self.e_c,
            "e_d": self.e_d,
            "cycle_time": self.cycle_time,
            "date_time": self.date_time,
            "cycle_index": self.cycle_index,
            "test_time": self.test_time,
            "cell_id": self.cell_id
        }

class CycleTimeSeriesBuffer(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_TS_BUF.value
    i = Column(Float, nullable=True)
    v = Column(Float, nullable=True)
    ah_c = Column(Float, nullable=True)
    ah_d = Column(Float, nullable=True)
    e_c = Column(Float, nullable=True)
    e_d = Column(Float, nullable=True)
    env_temperature = Column(Float, nullable=True)
    cell_temperature = Column(Float, nullable=True)
    cycle_time = Column(Float, nullable=True)
    date_time = Column(TIMESTAMP, nullable=True)
    cycle_index = Column(Integer, nullable=False, primary_key=True)
    test_time = Column(Float, nullable=True)
    cell_id = Column(TEXT, nullable=False, primary_key=True)
    sheetname = Column(TEXT, nullable=True)
    idx_cycle_timeseries_buffer_cell_id_cycle_index = Index("cell_id", "cycle_index")
    idx_cycle_timeseries_buffer_cell_id = Index("cell_id")


    def to_dict(self):
        return {
            "i": self.i,
            "v": self.v,
            "ah_c": self.ah_c,
            "ah_d": self.ah_d,
            "env_temperature": self.env_temperature,
            "cell_temperature": self.cell_temperature,
            "e_c": self.e_c,
            "e_d": self.e_d,
            "cycle_time": self.cycle_time,
            "date_time": self.date_time,
            "cycle_index": self.cycle_index,
            "test_time": self.test_time,
            "cell_id": self.cell_id,
            "sheetname" : self.sheetname
        }

"""
Archive Operator
- Manages objects in Archive
- Supports Create/Read/Update/Delete of ArchiveCells
- For example, methods accept ArchiveCell(s) as input and provides ArchiveCell(s) as output 
- Performs all necessary SQL functions related to Archive db
"""


class ArchiveOperator:
    def __init__(self, config={}):
        url = os.getenv('DATABASE_CONNECTION', DB_URL)

        engine = create_engine(url, **config)
        Model.metadata.create_all(engine)
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine))


    def add_meta_to_db(self, cell):
        df_cell_md = cell.cellmeta
        df_test_meta_md = cell.testmeta
        df_stats, _ = cell.stat
        df_cell_md.to_sql(cell.cell_meta_table,
                          con=self.session.bind,
                          if_exists="append",
                          chunksize=1000,
                          index=False)
        df_test_meta_md.to_sql(cell.test_meta_table,
                               con=self.session.bind,
                               if_exists='append',
                               chunksize=1000,
                               index=False)
        if cell.test_stats_table:
            df_stats.to_sql(ARCHIVE_TABLE.CYCLE_STATS.value,
                            con=self.session.bind,
                            if_exists='append',
                            chunksize=1000,
                            index=False)

    def add_ts_to_db(self, cell): 
        _, df_timeseries = cell.stat
        df_timeseries.to_sql(cell.test_ts_table,
                             con=self.session.bind,
                             if_exists='append',
                             chunksize=1000,
                             index=False)

    def add_cell_to_db(self, cell):
        df_cell_md = cell.cellmeta
        df_test_meta_md = cell.testmeta
        df_stats, df_timeseries = cell.stat
        df_cell_md.to_sql(cell.cell_meta_table,
                          con=self.session.bind,
                          if_exists="append",
                          chunksize=1000,
                          index=False)
        df_test_meta_md.to_sql(cell.test_meta_table,
                               con=self.session.bind,
                               if_exists='append',
                               chunksize=1000,
                               index=False)
        if cell.test_stats_table:
            df_stats.to_sql(ARCHIVE_TABLE.CYCLE_STATS.value,
                            con=self.session.bind,
                            if_exists='append',
                            chunksize=1000,
                            index=False)
        df_timeseries.to_sql(cell.test_ts_table,
                             con=self.session.bind,
                             if_exists='append',
                             chunksize=1000,
                             index=False)
    def add_cells_to_db(self, cell_list):
        for cell in cell_list:
            self.add_cell_to_db(cell)
        return True

    def remove_cell_from_table(self, table, cell_id):
        self.session.query(table).filter(table.cell_id == cell_id).delete()
        self.session.commit()

    def remove_cell_from_archive(self, cell_id):
        self.remove_cell_from_table(CellMeta, cell_id)
        self.remove_cell_from_table(CycleMeta, cell_id)
        self.remove_cell_from_table(CycleStats, cell_id)
        self.remove_cell_from_table(CycleTimeSeries, cell_id)
        self.remove_cell_from_table(AbuseMeta, cell_id)
        self.remove_cell_from_table(AbuseTimeSeries, cell_id)

    """
    getters
    """

    def get_df_cycle_ts_with_cell_id(self, cell_id):
        sql = self.session.query(
            CycleTimeSeries.date_time.label(OUTPUT_LABELS.DATE_TIME.value),
            CycleTimeSeries.test_time.label(OUTPUT_LABELS.TEST_TIME.value),
            CycleTimeSeries.cycle_index.label(OUTPUT_LABELS.CYCLE_INDEX.value),
            CycleTimeSeries.i.label(OUTPUT_LABELS.CURRENT.value),
            CycleTimeSeries.v.label(OUTPUT_LABELS.VOLTAGE.value),
            CycleTimeSeries.ah_c.label(OUTPUT_LABELS.CHARGE_CAPACITY.value),
            CycleTimeSeries.ah_d.label(OUTPUT_LABELS.DISCHARGE_CAPACITY.value),
            CycleTimeSeries.e_c.label(OUTPUT_LABELS.CHARGE_ENERGY.value),
            CycleTimeSeries.e_d.label(OUTPUT_LABELS.DISCHARGE_ENERGY.value),
            CycleTimeSeries.env_temperature.label(OUTPUT_LABELS.ENV_TEMPERATURE.value),
            CycleTimeSeries.cell_temperature.label(
                OUTPUT_LABELS.CELL_TEMPERATURE.value)).filter(
                    CycleTimeSeries.cell_id == cell_id).statement
        return pd.read_sql(sql, self.session.bind).round(DEGREE)

    # CELL

    def get_df_cell_meta_with_id(self, cell_id):
        return self.get_df_with_id(CellMeta, cell_id)

    def get_all_cell_meta(self):
        return self.get_all_data_from_table(CellMeta)

    def get_all_cell_meta_with_id(self, cell_id):
        return self.get_all_data_from_table_with_id(CellMeta, cell_id)

    # ABUSE

    def get_df_abuse_meta_with_id(self, cell_id):
        return self.get_df_with_id(AbuseMeta, cell_id)

    def get_all_abuse_meta(self):
        return self.get_all_data_from_table(AbuseMeta)

    def get_all_abuse_meta_with_id(self, cell_id):
        return self.get_all_data_from_table_with_id(AbuseMeta, cell_id)

    def get_all_abuse_ts(self):
        return self.get_all_data_from_table(AbuseTimeSeries)

    def get_all_abuse_ts_with_id(self, cell_id):
        return self.get_all_data_from_table_with_id(AbuseTimeSeries, cell_id)

    # CYCLE

    def get_df_cycle_meta_with_id(self, cell_id):
        return self.get_df_with_id(CycleMeta, cell_id)

    def get_all_cycle_meta(self):
        return self.get_all_data_from_table(CycleMeta)

    def get_all_cycle_meta_with_id(self, cell_id):
        return self.get_all_data_from_table_with_id(CycleMeta, cell_id)

    def get_df_cycle_stats_with_id(self, cell_id):
        return self.get_df_with_id(CycleStats, cell_id)

    def get_all_cycle_stats(self):
        return self.get_all_data_from_table(CycleStats)

    def get_all_cycle_stats_with_id(self, cell_id):
        return self.get_all_data_from_table_with_id(CycleStats, cell_id)

    def get_all_cycle_ts(self):
        return self.get_all_data_from_table(CycleTimeSeries)

    def get_all_cycle_ts_with_id(self, cell_id):
        return self.get_all_data_from_table_with_id(CycleTimeSeries, cell_id)

    # GENERAL SQL

    def get_df_with_id(self, table: Model, cell_id: str):
        return pd.read_sql(
            self.select_table_with_id(table, cell_id).statement,
            self.session.bind).round(DEGREE)

    # GENERAL ORM

    def get_all_data_from_table(self, table):
        return self.select_table(table).all()

    def get_all_data_from_table_with_id(self, table, cell_id):
        return self.select_table_with_id(table, cell_id).all()

    # BASIC

    def select_table(self, table):
        return self.session.query(table)

    def select_table_with_id(self, table, cell_id):
        return self.session.query(table).filter(table.cell_id == cell_id)

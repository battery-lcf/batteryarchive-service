from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    TEXT,
    Float,
    select,
)
from sqlalchemy.ext.declarative import declarative_base
import logging
import pandas as pd
from sqlalchemy.sql.sqltypes import FLOAT
from converter import (split_metadata, sort_timeseries, calc_cycle_stats,
                       calc_stats)

from aio import (read_ornlabuse, read_snlabuse, read_maccor, read_arbin)

from archive_constants import (LABEL, DEGREE, TEST_TYPE, TESTER, OUTPUT_LABELS,
                               SLASH, ARCHIVE_TABLE, CELL_LIST_FILE_NAME)
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from server import app

Model = declarative_base()


class AbuseMeta(Model):
    __tablename__ = ARCHIVE_TABLE.ABUSE_META.value
    id = Column(Integer, primary_key=True)
    cell_id = Column(TEXT, nullable=False)
    temperature = Column(Float, nullable=False)
    thickness = Column(Float, nullable=False)
    v_init = Column(Float, nullable=False)
    indentor = Column(Float, nullable=False)
    nail_speed = Column(Float, nullable=False)


class AbuseTimeSeries(Model):
    __tablename__ = ARCHIVE_TABLE.ABUSE_TS.value
    id = Column(Integer, primary_key=True)
    axial_d = Column(Float, nullable=False)
    axial_f = Column(FLOAT, nullable=False)
    v = Column(FLOAT, nullable=False)
    norm_d = Column(Float, nullable=True)
    strain = Column(Float, nullable=True)
    temp_1 = Column(Float, nullable=True)
    temp_2 = Column(Float, nullable=True)
    temp_3 = Column(Float, nullable=True)
    temp_4 = Column(Float, nullable=True)
    temp_5 = Column(Float, nullable=True)
    temp_6 = Column(Float, nullable=True)
    test_time = Column(Float, nullable=True)
    cell_id = Column(TEXT, nullable=True)


class CellMeta(Model):
    __tablename__ = ARCHIVE_TABLE.CELL_META.value
    id = Column(Integer, primary_key=True)
    cell_id = Column(TEXT, nullable=False)
    anode = Column(TEXT, nullable=False)
    cathode = Column(TEXT, nullable=False)
    source = Column(TEXT, nullable=False)
    ah = Column(BigInteger, nullable=False)
    form_factor = Column(TEXT, nullable=False)
    test = Column(TEXT, nullable=False)
    tester = Column(TEXT, nullable=False)


class CycleMeta(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_META.value
    id = Column(Integer, primary_key=True)
    temperature = Column(Float, nullable=False)
    soc_max = Column(Float, nullable=False)
    soc_min = Column(Float, nullable=False)
    v_max = Column(Float, nullable=True)
    v_min = Column(Float, nullable=True)
    crate_c = Column(Float, nullable=False)
    crate_d = Column(Float, nullable=False)
    cell_id = Column(TEXT, nullable=False)


class CycleStats(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_STATS.value
    id = Column(Integer, primary_key=True)
    v_max = Column(Float, nullable=False)
    v_min = Column(Float, nullable=False)
    ah_c = Column(Float, nullable=False)
    ah_d = Column(Float, nullable=False)
    e_c = Column(Float, nullable=False)
    e_d = Column(Float, nullable=False)
    i_max = Column(Float, nullable=False)
    i_min = Column(Float, nullable=False)
    v_c_mean = Column(Float, nullable=True)
    v_d_mean = Column(Float, nullable=True)
    e_eff = Column(Float, nullable=True)
    ah_eff = Column(Float, nullable=True)
    cycle_index = Column(Integer, nullable=False)
    test_time = Column(Float, nullable=False)
    cell_id = Column(TEXT, nullable=False)


class CycleTimeSeries(Model):
    __tablename__ = ARCHIVE_TABLE.CYCLE_TS.value
    id = Column(Integer, primary_key=True)
    i = Column(Float, nullable=False)
    v = Column(Float, nullable=False)
    ah_c = Column(Float, nullable=False)
    ah_d = Column(Float, nullable=False)
    e_c = Column(Float, nullable=False)
    e_d = Column(Float, nullable=False)
    temp_1 = Column(Float, nullable=False)
    temp_2 = Column(Float, nullable=False)
    cycle_time = Column(Float, nullable=False)
    date_time = Column(Float, nullable=False)
    cycle_index = Column(Integer, nullable=False)
    test_time = Column(Float, nullable=False)
    cell_id = Column(TEXT, nullable=False)


class ArchiveOperator:
    def __init__(self,
                 url=app.config['DATABASE_URI'],
                 config=app.config['DATABASE_CONNECT_OPTIONS']):
        engine = create_engine(url, **config)
        Model.metadata.create_all(engine)
        self.session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine))

    """
    export_to_csv exports dataframe to csv

    :param df: Dataframe of data to be exported 
    :param cell_id: Cell ID that will be written to file
    :param path: Path to the output directory
    :return: Path to output csv file 
    """

    def export_to_csv(self, df, cell_id, path, suffix):
        cell_id_to_file = cell_id.replace(r"/", "-")
        csv_file = path + cell_id_to_file + "_" + suffix + ".csv"
        df.to_csv(csv_file, encoding="utf-8", index=False)
        return csv_file

    """
    generate_cycle_data queries data from the database and exports to csv

    :param session: Database session that 
    :param cell_id: Absolute Path to the cell_list directory
    :param path: Path to the cell_list directory
    :return: Boolean True if method succeeds False if method fails
    """

    def generate_cycle_data(self, cell_id, path):
        query = select([
            CycleMeta.cell_id.label(OUTPUT_LABELS.CELL_ID.value),
            CycleMeta.v_max.label(OUTPUT_LABELS.MAX_VOLTAGE.value),
            CycleMeta.v_min.label(OUTPUT_LABELS.MIN_VOLTAGE.value)
        ])
        df = pd.read_sql(query, self.session.bind)
        df = df[df[OUTPUT_LABELS.CELL_ID.value] == cell_id]
        df = df.round(DEGREE)
        return self.export_to_csv(df, cell_id, path, "cycle_data")

    """
    generate_timeseries_data queries data from the database and exports to csv

    :param session: Database session that 
    :param cell_id: Absolute Path to the cell_list directory
    :param path: Path to the cell_list directory
    :return: Boolean True if successful False if method fails
    """

    def generate_timeseries_data(self, cell_id, path):
        query = select([
            CycleTimeSeries.date_time.label(OUTPUT_LABELS.DATE_TIME.value),
            CycleTimeSeries.test_time.label(OUTPUT_LABELS.TEST_TIME.value),
            CycleTimeSeries.cycle_index.label(OUTPUT_LABELS.CYCLE_INDEX.value),
            CycleTimeSeries.i.label(OUTPUT_LABELS.CURRENT.value),
            CycleTimeSeries.v.label(OUTPUT_LABELS.VOLTAGE.value),
            CycleTimeSeries.ah_c.label(OUTPUT_LABELS.CHARGE_CAPACITY.value),
            CycleTimeSeries.ah_d.label(OUTPUT_LABELS.DISCHARGE_CAPACITY.value),
            CycleTimeSeries.e_c.label(OUTPUT_LABELS.CHARGE_ENERGY.value),
            CycleTimeSeries.e_d.label(OUTPUT_LABELS.DISCHARGE_ENERGY.value),
            CycleTimeSeries.temp_1.label(OUTPUT_LABELS.ENV_TEMPERATURE.value),
            CycleTimeSeries.temp_2.label(OUTPUT_LABELS.CELL_TEMPERATURE.value),
        ])
        df = pd.read_sql(query, self.session.bind)
        df = df.round(DEGREE)
        return self.export_to_csv(df, cell_id, path, "timeseries_data")

    """
    output_cycle_series_to_csv adds cells defined in cell_list and add

    :param session: Database session that 
    :param cell_id: Absolute Path to the cell_list directory
    :param path: Path to the cell_list directory
    :return: Boolean True if successful False if method fails
    """

    def output_cycle_series_to_csv(self, cell_id, path):
        query = select([
            CycleMeta.v_max.label(OUTPUT_LABELS.VOLTAGE.value),
        ])
        df = pd.read_sql(self.session.query(query))
        self.export_to_csv(self.session, df, cell_id, path, "cycle_data")

    def add_cycle_cells_to_database():
        pass

    """
    read_data reads data from all supported tester types

    :param cell_id: Unique Cell Identifier
    :param file_path: Absolute Path to the file that is to be read
    :param tester: String identifier of what tester type is being read
    :return: DataFrame with data from reader
    """

    def read_data(self, cell_id, file_path, tester):
        if tester == TESTER.ARBIN.value:
            return read_arbin(cell_id, file_path)
        if tester == TESTER.MACCOR.value:
            return read_maccor(cell_id, file_path)
        if tester == TESTER.ORNL.value:
            return read_ornlabuse(cell_id, file_path)
        if tester == TESTER.SNL.value:
            return read_snlabuse(cell_id, file_path)

    """
    add_cells_to_database adds cells defined in cell_list and add

    :param session: Database session that 
    :param cell_list_path: Path to the cell_list directory
    :return: Boolean True if successful False if method fails
    """

    def add_cells_to_database(self, cell_list_path):
        df_excel = pd.read_excel(cell_list_path + CELL_LIST_FILE_NAME)
        for i in df_excel.index:
            df_tmp = df_excel.iloc[i]
            test_type = str(df_excel[LABEL.TEST.value][i])
            cell_id = df_excel[LABEL.CELL_ID.value][i]
            file_id = df_excel[LABEL.FILE_ID.value][i]
            tester = df_excel[LABEL.TESTER.value][i]
            file_path = cell_list_path + file_id + SLASH
            df_cell_md, df_test_meta_md = split_metadata(df_tmp, test_type)
            df_cell_md.to_sql(ARCHIVE_TABLE.CELL_META.value,
                              con=self.session.bind,
                              if_exists="append",
                              chunksize=1000,
                              index=False)

            df_ts = self.read_data(cell_id, file_path, tester)
            df_stats, df_timeseries = calc_stats(df_ts, df_test_meta_md,
                                                 test_type)
            if test_type == TEST_TYPE.CYCLE.value:
                df_ts = sort_timeseries(df_ts)
                df_stats.to_sql(ARCHIVE_TABLE.CYCLE_STATS.value,
                                con=self.session.bind,
                                if_exists='append',
                                chunksize=1000,
                                index=False)
                df_timeseries.to_sql(ARCHIVE_TABLE.CYCLE_TS.value,
                                     con=self.session.bind,
                                     if_exists='append',
                                     chunksize=1000,
                                     index=False)
                df_test_meta_md.to_sql(ARCHIVE_TABLE.CYCLE_META.value,
                                       con=self.session.bind,
                                       if_exists='append',
                                       chunksize=1000,
                                       index=False)
                return True
            if test_type == TEST_TYPE.ABUSE.value:
                df_timeseries.to_sql(ARCHIVE_TABLE.ABUSE_TS.value,
                                     con=self.session.bind,
                                     if_exists='append',
                                     chunksize=1000,
                                     index=False)
                df_test_meta_md.to_sql(ARCHIVE_TABLE.ABUSE_META.value,
                                       con=self.session.bind,
                                       if_exists='append',
                                       chunksize=1000,
                                       index=False)
                return True

    def export_cells(self, cell_list, path):
        df_excel = pd.read_excel(cell_list)

        for i in df_excel.index:
            cell_id = df_excel[LABEL.CELL_ID.value][i]
            query = select([
                CycleMeta.cell_id.label(OUTPUT_LABELS.CELL_ID.value),
                CycleMeta.v_max.label(OUTPUT_LABELS.MAX_VOLTAGE.value),
                CycleMeta.v_min.label(OUTPUT_LABELS.MIN_VOLTAGE.value),
            ])
            df = pd.read_sql(query, self.session.bind)
            df = df[df[OUTPUT_LABELS.CELL_ID.value] == cell_id]
            df = df.round(DEGREE)

            if not df.empty:
                self.generate_cycle_data(cell_id, path)
                self.generate_timeseries_data(cell_id, path)

    def update_cells(self, cell_list):
        df_excel = pd.read_excel(cell_list)

        for i in df_excel.index:

            cell_id = df_excel[LABEL.CELL_ID.value][i]
            query = select([
                CycleMeta.cell_id.label(OUTPUT_LABELS.CELL_ID.value),
                CycleMeta.v_max.label(OUTPUT_LABELS.MAX_VOLTAGE.value),
                CycleMeta.v_min.label(OUTPUT_LABELS.MIN_VOLTAGE.value),
            ])
            df = pd.read_sql(query, self.session.bind)

            if df.empty:
                logging.info("cell:" + cell_id + " not found")
                return

            df_tmp = df_excel.iloc[i]
            df_cell_md, df_test_md = split_metadata(df_tmp,
                                                    TEST_TYPE.CYCLE.value)

            cell_id = df_tmp[OUTPUT_LABELS.CELL_ID.value]

            query = select([
                CycleTimeSeries.date_time.label(OUTPUT_LABELS.DATE_TIME.value),
                CycleTimeSeries.test_time.label(OUTPUT_LABELS.TEST_TIME.value),
                CycleTimeSeries.cycle_index.label(
                    OUTPUT_LABELS.CYCLE_INDEX.value),
                CycleTimeSeries.i.label(OUTPUT_LABELS.CURRENT.value),
                CycleTimeSeries.v.label(OUTPUT_LABELS.VOLTAGE.value),
                CycleTimeSeries.ah_c.label(
                    OUTPUT_LABELS.CHARGE_CAPACITY.value),
                CycleTimeSeries.ah_d.label(
                    OUTPUT_LABELS.DISCHARGE_CAPACITY.value),
                CycleTimeSeries.e_c.label(OUTPUT_LABELS.CHARGE_ENERGY.value),
                CycleTimeSeries.e_d.label(
                    OUTPUT_LABELS.DISCHARGE_ENERGY.value),
                CycleTimeSeries.temp_1.label(
                    OUTPUT_LABELS.ENV_TEMPERATURE.value),
                CycleTimeSeries.temp_2.label(
                    OUTPUT_LABELS.CELL_TEMPERATURE.value),
            ])
            df_ts = pd.read_sql(query, self.session.bind)
            df_ts = df_ts[df_ts[OUTPUT_LABELS.CELL_ID.value] == cell_id]
            df_ts = df_ts.round(DEGREE)

            df_cycle_data, df_timeseries_data = calc_cycle_stats(
                df_ts, df_cell_md, df_test_md)

            df_cell_md.to_sql(ARCHIVE_TABLE.CELL_META,
                              con=self.session.bind,
                              if_exists='append',
                              chunksize=1000,
                              index=False)
            df_test_md.to_sql(ARCHIVE_TABLE.CYCLE_META,
                              con=self.session.bind,
                              if_exists='append',
                              chunksize=1000,
                              index=False)
            df_cycle_data.to_sql(ARCHIVE_TABLE.CYCLE_STATS,
                                 con=self.session.bind,
                                 if_exists='append',
                                 chunksize=1000,
                                 index=False)
            df_timeseries_data.to_sql(ARCHIVE_TABLE.CYCLE_TS,
                                      con=self.session.bind,
                                      if_exists='append',
                                      chunksize=1000,
                                      index=False)
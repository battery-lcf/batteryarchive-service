from src.app.model import ArchiveOperator, CellMeta
from src.app.aio import ArchiveExporter
from src.app.archive_cell import ArchiveCell
import pandas as pd
from src.app.archive_constants import (LABEL, DEGREE, SLASH,
                                       CELL_LIST_FILE_NAME, TEST_TYPE, FORMAT)

# Routes


def root():
    return "Hello World", 200


def liveness():
    return "Alive", 200


def readiness():
    return "Ready", 200


def get_cells():
    """get_cell
    Gets all cells
    :rtype: list of Cell
    """
    ao = ArchiveOperator()
    archive_cells = ao.get_all_cell_meta()
    result = [cell.to_dict() for cell in archive_cells]
    return result, 200


def get_cell_with_id(cell_id):

    ao = ArchiveOperator()
    archive_cells = ao.get_all_cell_meta_with_id(cell_id)
    result = [cell.to_dict() for cell in archive_cells]
    return result, 200


def get_test(test_name):
    """
    """
    ao = ArchiveOperator()
    if test_name == TEST_TYPE.CYCLE.value:
        archive_cells = ao.get_all_cycle_meta()
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200
    if test_name == TEST_TYPE.ABUSE.value:
        archive_cells = ao.get_all_abuse_meta()
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200


def get_ts(test_name):
    if test_name == TEST_TYPE.CYCLE.value:
        archive_cells = ArchiveOperator().get_all_cycle_ts()
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200
    if test_name == TEST_TYPE.ABUSE.value:
        archive_cells = ArchiveOperator().get_all_abuse_ts()
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200


def get_test_ts_with_id(cell_id, test_name):
    if test_name == TEST_TYPE.CYCLE.value:
        archive_cells = ArchiveOperator().get_all_cycle_ts_with_id(cell_id)
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200
    if test_name == TEST_TYPE.ABUSE.value:
        archive_cells = ArchiveOperator().get_all_abuse_ts_with_id()
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200


def get_meta_with_id(cell_id, test_name):
    if test_name == TEST_TYPE.CYCLE.value:
        archive_cells = ArchiveOperator().get_all_cycle_meta_with_id(cell_id)
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200
    if test_name == TEST_TYPE.ABUSE.value:
        archive_cells = ArchiveOperator().get_all_abuse_meta_with_id()
        result = [cell.to_dict() for cell in archive_cells]
        return result, 200


# EXPORTERS


def export_cycle_cells_to_csv(session, cell_list_path, path):
    df_excel = pd.read_excel(cell_list_path + CELL_LIST_FILE_NAME)
    for i in df_excel.index:
        cell_id = df_excel[LABEL.CELL_ID.value][i]
        query = session.query(CellMeta).filter(CellMeta.cell_id == cell_id)
        df = pd.read_sql(query.statement, session.bind)
        df = df[df[LABEL.CELL_ID.value] == cell_id]
        df = df.round(DEGREE)
        if not df.empty:
            export_cycle_meta_data_with_id_to_csv(cell_id, path)
            export_cycle_ts_data_csv(cell_id, path)


def export_cycle_cells_to_format(cell_list_path, path, fmt="csv"):
    df_excel = pd.read_excel(cell_list_path + CELL_LIST_FILE_NAME)
    #TODO Refactor this to a join instead of looping slowly
    for i in df_excel.index:
        cell_id = df_excel[LABEL.CELL_ID.value][i]
        df = ArchiveOperator().lod_cell_meta_into_df_with_cell_id(cell_id)
        if not df.empty:
            if fmt == FORMAT.CSV.value:
                export_cycle_meta_data_with_id_to_csv(cell_id, path)
                export_cycle_ts_data_csv(cell_id, path)
            if fmt == FORMAT.FEATHER.value:
                export_cycle_meta_data_with_id_to_feather(cell_id, path)
                export_cycle_ts_data_feather(cell_id, path)


"""
generate_cycle_data queries data from the database and exports to csv

:param cell_id: Absolute Path to the cell_list directory
:param path: Path to the cell_list directory
:return: Boolean True if method succeeds False if method fails
"""


def export_cycle_meta_data_with_id_to_csv(cell_id: str, path: str):
    return ArchiveExporter.write_to_csv(
        ArchiveOperator().get_df_cycle_meta_with_id(cell_id), cell_id, path,
        "cycle_data")


def export_cycle_meta_data_with_id_to_feather(cell_id: str, path: str):
    return ArchiveExporter.write_to_feather(
        ArchiveOperator().get_df_cycle_meta_with_id(cell_id), cell_id, path,
        "cycle_data")


def export_cycle_meta_data_with_id_to_format(cell_id: str, path: str,
                                             fmt: str):
    if fmt == FORMAT.CSV.value:
        return export_cycle_meta_data_with_id_to_csv(cell_id, path)
    if fmt == FORMAT.FEATHER.value:
        return export_cycle_meta_data_with_id_to_feather(cell_id, path)


"""
generate_timeseries_data queries data from the database and exports to csv

:param session: Database session that 
:param cell_id: Absolute Path to the cell_list directory
:param path: Path to the cell_list directory
:return: Boolean True if successful False if method fails
"""


def export_cycle_ts_data_csv(cell_id: str, path: str):
    return ArchiveExporter.write_to_csv(
        ArchiveOperator().get_df_cycle_ts_with_cell_id(cell_id), cell_id, path,
        "timeseries_data")


def export_cycle_ts_data_feather(cell_id: str, path: str):
    return ArchiveExporter.write_to_feather(
        ArchiveOperator().get_df_cycle_ts_with_cell_id(cell_id), cell_id, path,
        "timeseries_data")


# Importers


def import_cells_xls_to_db(cell_list_path):
    ao = ArchiveOperator()
    df = pd.read_excel(cell_list_path + CELL_LIST_FILE_NAME)
    cells = []
    for i in df.index:
        cell = ArchiveCell(cell_id=df[LABEL.CELL_ID.value][i],
                           test_type=str(df[LABEL.TEST.value][i]),
                           file_id=df[LABEL.FILE_ID.value][i],
                           file_type=str(df[LABEL.FILE_TYPE.value][i]),
                           tester=df[LABEL.TESTER.value][i],
                           file_path=cell_list_path +
                           df[LABEL.FILE_ID.value][i] + SLASH,
                           metadata=df.iloc[i])
        cells.append(cell)
    return ao.add_cells_to_db(cells)


def import_cells_xls_to_db(cell_list_path):
    return add_df_to_db(pd.read_excel(cell_list_path + CELL_LIST_FILE_NAME),
                        cell_list_path)


def import_cells_feather_to_db(cell_list_path):
    return add_df_to_db(pd.read_feather(cell_list_path + CELL_LIST_FILE_NAME),
                        cell_list_path)


def add_df_to_db(df, cell_list_path):
    cells = []
    for i in df.index:
        cell = ArchiveCell(cell_id=df[LABEL.CELL_ID.value][i],
                           test_type=str(df[LABEL.TEST.value][i]),
                           file_id=df[LABEL.FILE_ID.value][i],
                           file_type=str(df[LABEL.FILE_TYPE.value][i]),
                           tester=df[LABEL.TESTER.value][i],
                           file_path=cell_list_path +
                           df[LABEL.FILE_ID.value][i] + SLASH,
                           metadata=df.iloc[i])
        cells.append(cell)
    return ArchiveOperator().add_cells_to_db(cells)


def update_cycle_cells(cell_list_path):
    df_excel = pd.read_excel(cell_list_path + CELL_LIST_FILE_NAME)
    ao = ArchiveOperator()
    for i in df_excel.index:
        cell_id = df_excel[LABEL.CELL_ID.value][i]
        df = ArchiveOperator().get_df_cell_meta_with_id(cell_id)
        if df.empty:
            print("cell:" + cell_id + " not found")
            continue
        ao.remove_cell_from_archive(cell_id)
    import_cells_xls_to_db(cell_list_path)
    return True
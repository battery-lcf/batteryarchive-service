import pandas as pd
from archive_constants import (LABEL, DEGREE, TEST_TYPE, TESTER, OUTPUT_LABELS,
                               SLASH, ARCHIVE_TABLE, CELL_LIST_FILE_NAME)
from converter import (split_cycle_metadata, split_abuse_metadata,
                       sort_timeseries, calc_cycle_stats, calc_abuse_stats)
from readers import (read_ornlabuse, read_snlabuse, read_maccor, read_arbin)


class TestTypeException(Exception):
    pass


class Cell:
    def __init__(self, cell_id, test_type, file_id, tester, file_path,
                 metadata):
        assert self.is_supported_test_type(
                test_type), test_type + ": Unrecognized Test Type"
        self.cell_id = cell_id
        self.test_type = test_type
        self.file_id = file_id
        self.tester = tester
        self.file_path = file_path
        self.metadata = metadata
        self.cellmeta, self.testmeta = self.split_metadata()
        self.cell_meta_table = ARCHIVE_TABLE.CELL_META.value
        if self.test_type == TEST_TYPE.ABUSE.value:
            self.test_ts_table = ARCHIVE_TABLE.ABUSE_TS.value
            self.test_meta_table = ARCHIVE_TABLE.ABUSE_META.value
            self.test_stats_table = None
        if self.test_type == TEST_TYPE.CYCLE.value:
            self.test_ts_table = ARCHIVE_TABLE.CYCLE_TS.value
            self.test_meta_table = ARCHIVE_TABLE.CYCLE_META.value
            self.test_stats_table = ARCHIVE_TABLE.CYCLE_STATS.value

    def is_supported_test_type(self, test_type):
        for T in TEST_TYPE:
            if test_type == T.value: return True
        return False

    def split_metadata(self):
        if self.test_type == TEST_TYPE.CYCLE.value:
            A, B = split_cycle_metadata(self.metadata)
            return A, B
        elif self.test_type == TEST_TYPE.ABUSE.value:
            A, B = split_abuse_metadata(self.metadata)
            return A, B
        else:
            raise TestTypeException

    # calculate statistics for testdata
    def calc_stats(self):
        df_t = self.read_data()
        if self.test_type == TEST_TYPE.CYCLE.value:
            return calc_cycle_stats(df_t)
        if self.test_type == TEST_TYPE.ABUSE.value:
            return None, calc_abuse_stats(df_t, self.testmeta)

    """
    read_data reads data from all supported tester types

    :param cell_id: Unique Cell Identifier
    :param file_path: Absolute Path to the file that is to be read
    :param tester: String identifier of what tester type is being read
    :return: DataFrame with data from reader
    """

    def read_data(self):
        if self.tester == TESTER.ARBIN.value:
            data = read_arbin(self.cell_id, self.file_path)
        if self.tester == TESTER.MACCOR.value:
            data = read_maccor(self.cell_id, self.file_path)
        if self.tester == TESTER.ORNL.value:
            data = read_ornlabuse(self.cell_id, self.file_path)
        if self.tester == TESTER.SNL.value:
            data = read_snlabuse(self.cell_id, self.file_path)
        if self.test_type == TEST_TYPE.CYCLE.value:
            return sort_timeseries(data)
        else:
            return data

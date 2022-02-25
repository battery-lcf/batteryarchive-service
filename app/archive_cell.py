from app.archive_constants import (LABEL, DEGREE, TEST_TYPE, TESTER, OUTPUT_LABELS,
                               SLASH, ARCHIVE_TABLE, CELL_LIST_FILE_NAME)
from app.converter import (split_cycle_metadata, split_abuse_metadata,
                       calc_cycle_stats, calc_abuse_stats)
from app.aio import CellTestReader


class TestTypeException(Exception):
    pass


class ArchiveCell:
    def __init__(self,
                 cell_id,
                 test_type=None,
                 file_id=None,
                 file_type=None,
                 tester=None,
                 file_path=None,
                 metadata=None,
                 data=None,
                 stat=None):
        assert self.is_supported_test_type(
            test_type), test_type + ": Unrecognized Test Type"
        self.cell_id = cell_id
        self.test_type = test_type
        self.tester = tester
        self.file_path = file_path
        self.file_type = file_type
        self.file_id = file_id
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
        if data is not None: self.data = data
        else: self.load_data()
        if stat: self.stat = stat
        else: self.stat = self.calc_stats()

    def load_data(self):
        ctr = CellTestReader(self.tester, self.test_type)
        self.data = ctr.read_data(self.file_path)
        self.data[LABEL.CELL_ID.value] = self.cell_id
        return self

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
        if self.test_type == TEST_TYPE.CYCLE.value:
            return calc_cycle_stats(self.data)
        if self.test_type == TEST_TYPE.ABUSE.value:
            return None, calc_abuse_stats(self.data, self.testmeta)

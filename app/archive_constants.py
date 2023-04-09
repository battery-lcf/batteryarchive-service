from enum import Enum, auto

SLASH = "/"

DEGREE = 3
CELL_LIST_FILE_NAME = "cell_list.xlsx"
TEST_DB_URL = "sqlite:///tests/test_data/db/bas-test.db"
LIVE_DB_URL = "<your-db-string>"

DB_URL = LIVE_DB_URL

class TEST_TYPE(Enum):
    ABUSE = "abuse"
    CYCLE = "cycle"


class FORMAT(Enum):
    CSV = "csv"
    FEATHER = "feather"
    XLSX = "xlsx"
    H5 = "h5"


class TESTER(Enum):
    ORNL = "ornl"
    SNL = "snl"
    ARBIN = "arbin"
    MACCOR = "maccor"
    GENERIC = "generic"


class ARCHIVE_TABLE(Enum):
    ABUSE_META = "abuse_metadata"
    ABUSE_TS = "abuse_timeseries"
    CELL_META = "cell_metadata"
    CYCLE_META = "cycle_metadata"
    CYCLE_STATS = "cycle_stats"
    CYCLE_TS = "cycle_timeseries"
    CYCLE_TS_BUF = "cycle_timeseries_buffer"


class INP_LABELS(Enum):
    TEST_TIME = "Running Time"
    AXIAL_D = "Axial Displacement"
    AXIAL_F = "Axial Force"
    V = "Analog 1"
    TC_01 = "TC 01"
    TC_02 = "TC 02"
    TC_03 = "TC 03"
    TC_04 = "TC 04"
    TC_05 = "TC 05"
    TC_06 = "TC 06"


class ARCHIVE_COLS(Enum):
    TEST_TIME = "test_time"
    AXIAL_D = "axial_d"
    AXIAL_F = "axial_f"
    I = "i"
    V = "v"

    temp_1 = "pos_terminal_temperature"
    temp_2 = "neg_terminal_temperature"

    temp_3 = "left_bottom_temperature"
    temp_4 = "right_bottom_temperature"
    temp_5 = "above_punch_temperature"
    temp_6 = "below_punch_temperature"


class OUTPUT_LABELS(Enum):
    CYCLE_INDEX = "Cycle_Index"
    CELL_ID = "Cell_ID"
    DATE_TIME = "Date_Time"
    TEST_TIME = "Test_Time (s)"
    VOLTAGE = "Voltage (V)"
    CURRENT = "Current (A)"
    MAX_VOLTAGE = "Max_Voltage (V)"
    MAX_CURRENT = "Max_Current (A)"
    MIN_VOLTAGE = "Min_Voltage (V)"
    MIN_CURRENT = "Min_Current (A)"
    CHARGE_CAPACITY = "Charge_Capacity (Ah)"
    DISCHARGE_CAPACITY = "Discharge_Capacity (Ah)"
    CHARGE_ENERGY = "Charge_Energy (Wh)"
    DISCHARGE_ENERGY = "Discharge_Energy (Wh)"
    ENV_TEMPERATURE = "Environment_Temperature (C)"
    CELL_TEMPERATURE = "Cell_Temperature (C)"


class LABEL(Enum):
    CELL_ID = "cell_id"
    MAPPING = "mapping"
    ANODE = "anode"
    CATHODE = "cathode"
    SOURCE = "source"
    AH = "ah"
    FORM_FACTOR = "form_factor"
    TEST = "test"
    TESTER = "tester"
    CRATE_C = "crate_c"
    CRATE_D = "crate_d"
    SOC_MAX = "soc_max"
    SOC_MIN = "soc_min"
    TEMP = "temperature"
    THICKNESS = "thickness"
    V_INIT = "v_init"
    INDENTOR = "indentor"
    NAIL_SPEED = "nail_speed"
    FILE_ID = "file_id"
    CYCLE_INDEX = "cycle_index"
    CYCLE_TIME = "cycle_time"
    V_MAX = "v_max"
    I_MAX = "i_max"
    V_MIN = "v_min"
    I_MIN = "i_min"
    AH_C = "ah_c"
    AH_D = "ah_d"
    E_C = "e_c"
    E_D = "e_d"
    V_C_MEAN = "v_c_mean"
    V_D_MEAN = "v_d_mean"
    DATE_TIME = "date_time"
    TEST_TIME = "test_time"
    AH_EFF = "ah_eff"
    E_EFF = "e_eff"
    I = "i"
    V = "v"
    DT = "dt"
    NORM_D = "norm_d"
    AXIAL_D = "axial_d"
    STRAIN = "strain"
    CYCLE_INDEX_FILE = "cycle_index_file"
    FILENAME = "filename"
    FILE_TYPE = "file_type"

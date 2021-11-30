from enum import Enum

SLASH = "/"

DEGREE = 3
CELL_LIST_FILE_NAME = "cell_list.xlsx"

class TEST_TYPE(Enum):
    ABUSE = "abuse"
    CYCLE = "cycle"


class TESTER(Enum):
    ORNL = "ornl"
    SNL = "snl"
    ARBIN = "arbin"
    MACCOR = "maccor"


class ARCHIVE_TABLE(Enum):
    ABUSE_META = "abuse_metadata"
    ABUSE_TS = "abuse_timeseries"
    CELL_META = "cell_metadata"
    CYCLE_META = "cycle_metadata"
    CYCLE_STATS = "cycle_stats"
    CYCLE_TS = "cycle_timeseries"


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

TEST_DB_URL = "sqlite:///tests/test-data/tmp/bas-test.db"

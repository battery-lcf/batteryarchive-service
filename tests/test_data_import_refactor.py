import pandas as pd
import os, sys
currentdir = os.getcwd()
sys.path.append(os.path.join(currentdir))
sys.path.append(os.path.join(currentdir, 'app'))



from app.aio import CellTestReader, listToString, signedCurrent
from app.converter import (calc_cycle_quantities, calc_cycle_stats,
                           calc_abuse_stats, sort_timeseries, split_abuse_metadata, split_cycle_metadata)
from app.archive_constants import TEST_TYPE, TESTER
testDataBasePath = os.path.join(currentdir, 'tests', 'test_data')


def df_print(output, result):
    for i in output:
        print("========START=========" + i)
        print(
            "Index",
            i,
            "Index Type",
            type(i),
            "\nOutput PD",
            output[i],
            "Output PD Type",
            type(output[i]),
            "\nResult PD",
            result[i],
            "Result PD Type",
            type(result[i]),
            "\nCompare",
            result[i] == output[i],
        )
        print("========END=========" + i)


def test_always_passes():
    assert True


def test_listToString():
    assert listToString(["x"]) == "x"
    assert listToString(["x", "y", "z"]) == "xyz"


def test_calc_cycle_quantities():
    cols = ["test_time", "i", "v", "ah_c", "e_c", "ah_d", "e_d", "cycle_time"]

    test_df = [{
        "test_time": 1,
        "i": 1,
        "v": 1,
        "ah_c": 3600,
        "e_c": 3600,
        "ah_d": 3600,
        "e_d": 3600,
        "cycle_time": 1,
    }]
    test_pd_df = pd.DataFrame(data=test_df, columns=cols)
    output_test_pd_df = calc_cycle_quantities(test_pd_df)
    result_df = [{
        "test_time": 1,
        "i": 1,
        "v": 1,
        "ah_c": 1.0,
        "e_c": 1.0,
        "ah_d": -1.0,
        "e_d": -1.0,
        "cycle_time": 0,
    }]
    result_pd_df = pd.DataFrame(data=result_df, columns=cols)
    df_print(output_test_pd_df, result_pd_df)

    assert output_test_pd_df.equals(result_pd_df)


def test_calc_abuse_stats():
    test_cols = ["axial_d"]
    test_df = [{"axial_d": 1}]
    test_pd_df = pd.DataFrame(data=test_df, columns=test_cols)

    df_test_md = {"thickness": 1}
    output_test_pd_df = calc_abuse_stats(test_pd_df, df_test_md)

    result_cols = ["axial_d", "norm_d", "strain"]
    result_df = [{"axial_d": 1, "norm_d": 0, "strain": 0.0}]
    result_pd_df = pd.DataFrame(data=result_df, columns=result_cols)

    df_print(output_test_pd_df, result_pd_df)

    assert output_test_pd_df.equals(result_pd_df)


def test_calc_cycle_stats():
    test_cols = ["cycle_index", "cell_id"]
    test_df = [{"cycle_index": 1, "cell_id": 1}]
    test_pd_df = pd.DataFrame(data=test_df, columns=test_cols)

    output_dfc, output_dft = calc_cycle_stats(test_pd_df)
    result_dfc_cols = [
        "cycle_index",
        "cell_id",
        "v_max",
        "i_max",
        "v_min",
        "i_min",
        "ah_c",
        "ah_d",
        "e_c",
        "e_d",
        "v_c_mean",
        "v_d_mean",
        "test_time",
        "ah_eff",
        "e_eff",
    ]
    result_dfc = [{
        "cycle_index": 1,
        "cell_id": 1,
        "v_max": 0,
        "i_max": 0,
        "v_min": 0,
        "i_min": 0,
        "ah_c": 0,
        "ah_d": 0,
        "e_c": 0,
        "e_d": 0,
        "v_c_mean": 0,
        "v_d_mean": 0,
        "test_time": 0,
        "ah_eff": 0,
        "e_eff": 0,
    }]
    result_pd_dfc = pd.DataFrame(data=result_dfc, columns=result_dfc_cols)
    print("======DFC======")
    df_print(output_dfc, result_pd_dfc)

    result_dft_cols = ["cycle_index", "cell_id", "cycle_time"]
    result_dft = [{"cycle_index": 1, "cell_id": 1, "cycle_time": 0}]
    result_pd_dft = pd.DataFrame(data=result_dft, columns=result_dft_cols)

    print("======DFT======")
    df_print(output_dft, result_pd_dft)

    assert output_dft.equals(result_pd_dft)
    assert output_dfc.equals(result_pd_dfc)


def test_prepare_maccor_file():
    maccor_file = os.path.join(
        testDataBasePath, "cycle", "MACCOR_example", "MACCOR_example.txt")
    result_path = os.path.join(
        testDataBasePath, "cycle", "MACCOR_example", "MACCOR_example.txt_df")
    print(testDataBasePath)
    print(result_path)
    cellpath_df = CellTestReader(
        TESTER.MACCOR, TEST_TYPE.CYCLE).prepare_maccor_file(maccor_file)
    assert cellpath_df == result_path
    assert os.path.exists(cellpath_df)
    os.remove(cellpath_df)
    assert ~os.path.exists(cellpath_df)


def test_signedCurrent():
    assert signedCurrent("D", 1) == -1
    assert signedCurrent("X", 1) == 1


def test_read_ornlabuse():
    cell_id = "S1Abuse"
    file_path = os.path.join(testDataBasePath,  "abuse-ornl", '')
    output_df = CellTestReader(TESTER.ORNL, TEST_TYPE.ABUSE).read_ornlabuse(file_path)
    print(output_df)

    result_df_cols = [
        "test_time",
        "axial_d",
        "v",
        "axial_f",
        "pos_terminal_temperature",
        "neg_terminal_temperature",
        "left_bottom_temperature",
        "right_bottom_temperature",
        "above_punch_temperature",
        "below_punch_temperature",
        "cell_id",
    ]
    result_df = [
        {
            "test_time": 0.000,
            "axial_d": 0,
            "v": 4.128,
            "axial_f": 0,
            "pos_terminal_temperature": 0.00,
            "neg_terminal_temperature": 0.00,
            "left_bottom_temperature": 0.00,
            "right_bottom_temperature": 0.00,
            "above_punch_temperature": 0.00,
            "below_punch_temperature": 0.00,
            "cell_id": cell_id,
        },
        {
            "test_time": 0.046,
            "axial_d": 0,
            "v": 4.137,
            "axial_f": 1,
            "pos_terminal_temperature": 0.00,
            "neg_terminal_temperature": 0.00,
            "left_bottom_temperature": 0.00,
            "right_bottom_temperature": 0.00,
            "above_punch_temperature": 0.00,
            "below_punch_temperature": 0.00,
            "cell_id": cell_id,
        },
        {
            "test_time": 0.000,
            "axial_d": 0,
            "v": 0,
            "axial_f": 0,
            "pos_terminal_temperature": 22.27,
            "neg_terminal_temperature": 22.12,
            "left_bottom_temperature": 22.44,
            "right_bottom_temperature": 22.03,
            "above_punch_temperature": 22.08,
            "below_punch_temperature": 22.58,
            "cell_id": cell_id,
        },
        {
            "test_time": 0.500,
            "axial_d": 0,
            "v": 0,
            "axial_f": 0,
            "pos_terminal_temperature": 22.23,
            "neg_terminal_temperature": 22.03,
            "left_bottom_temperature": 22.56,
            "right_bottom_temperature": 22.07,
            "above_punch_temperature": 22.12,
            "below_punch_temperature": 22.62,
            "cell_id": cell_id,
        },
    ]
    result_pd_df = pd.DataFrame(data=result_df, columns=result_df_cols)
    df_print(output_df, result_pd_df)
    assert True


def test_read_snlabuse():
    cell_id = "S2Abuse"
    file_path = os.path.join(testDataBasePath,  "abuse-snl", '')
    output_df = CellTestReader(TESTER.SNL, TEST_TYPE.ABUSE).read_snlabuse(file_path)
    result_df_cols = [
        "test_time",
        "axial_d",
        "axial_f",
        "v",
        "pos_terminal_temperature",
        "neg_terminal_temperature",
        "left_bottom_temperature",
        "right_bottom_temperature",
        "above_punch_temperature",
        "below_punch_temperature",
        "cell_id",
    ]
    result_df = [
        {
            "test_time": 1.06,
            "axial_d": -0.055,
            "axial_f": 4.9,
            "v": 4.132,
            "pos_terminal_temperature": 20.3,
            "neg_terminal_temperature": 20,
            "left_bottom_temperature": 20.2,
            "right_bottom_temperature": 20.1,
            "above_punch_temperature": 20.2,
            "below_punch_temperature": 20.1,
            "cell_id": cell_id,
        },
        {
            "test_time": 2.06,
            "axial_d": -0.085,
            "axial_f": 3.503,
            "v": 4.132,
            "pos_terminal_temperature": 20.4,
            "neg_terminal_temperature": 20,
            "left_bottom_temperature": 20.2,
            "right_bottom_temperature": 20.1,
            "above_punch_temperature": 20.2,
            "below_punch_temperature": 20.1,
            "cell_id": cell_id,
        },
    ]
    result_pd_df = pd.DataFrame(data=result_df, columns=result_df_cols)
    print(len(output_df), len(result_pd_df))
    df_print(output_df, result_pd_df)
    assert True


def test_read_maccor():
    maccor_file = os.path.join(testDataBasePath,  "cycle", "MACCOR_example", '')
    df_output = CellTestReader(
        TESTER.MACCOR, TEST_TYPE.CYCLE).read_maccor(maccor_file)
    assert len(df_output) == 499
    remove_file = os.path.join(testDataBasePath,  "cycle", "MACCOR_example", "MACCOR_example.txt_df")
    os.remove(remove_file)


def test_read_arbin():
    arbin_file = os.path.join(testDataBasePath,  "cycle-arbin", '')
    df_output = CellTestReader(
        TESTER.ARBIN, TEST_TYPE.CYCLE).read_arbin(arbin_file)
    assert len(df_output) == 119


def test_read_generic_csv():
    csv_file = os.path.join(testDataBasePath,"cycle-generic", "csv", "")
    df_output = CellTestReader(TESTER.GENERIC, TEST_TYPE.CYCLE).read_generic(csv_file, 'csv', 'date_time, test_time, cycle_index, i, v')
    assert len(df_output) == 460380


def test_read_generic_h5():
    # requires tables
    h5_file = os.path.join(testDataBasePath,"cycle-generic", "h5", "")
    df_output = CellTestReader(TESTER.GENERIC, TEST_TYPE.CYCLE).read_generic(h5_file, 'h5', 'cycle_index,skip,test_time,i,cell_temperature,skip,v')
    assert len(df_output) == 568027


def test_sort_timeseries():
    cell_id = "sort-timeseries"
    input_df_cols = [
        "date_time",
        "test_time",
        "cycle_index_file",
        "cycle_index",
        "filename",
        "cell_id",
    ]
    input_df = [
        {
            "date_time": 0,
            "test_time": 2,
            "cycle_index_file": 1,
            "cycle_index": 1,
            "filename": "name",
            "cell_id": cell_id,
        },
        {
            "date_time": 0,
            "test_time": 1,
            "cycle_index_file": 1,
            "cycle_index": 1,
            "filename": "name",
            "cell_id": cell_id,
        },
    ]
    input_pd_df = pd.DataFrame(data=input_df, columns=input_df_cols)
    output_pd_df = sort_timeseries(input_pd_df)

    result_df_cols = [
        "date_time",
        "test_time",
        "cycle_index",
        "cell_id",
    ]
    result_df = [
        {
            "date_time": 0,
            "test_time": 1,
            "cycle_index": 1,
            "cell_id": cell_id,
        },
        {
            "date_time": 0,
            "test_time": 2,
            "cycle_index": 1,
            "cell_id": cell_id,
        },
    ]
    result_pd_df = pd.DataFrame(data=result_df, columns=result_df_cols)
    df_print(output_pd_df, result_pd_df)
    assert output_pd_df.compare(result_pd_df).empty


def test_populate_abuse_metadata():
    cell_id = "sort-populate-abuse-metadata"
    input_df_cols = [
        "cell_id",
        "anode",
        "cathode",
        "source",
        "ah",
        "form_factor",
        "test",
        "mapping",
        "tester",
        "temperature",
        "thickness",
        "v_init",
        "indentor",
        "nail_speed",
    ]
    input_df = [{
        "cell_id": cell_id,
        "anode": 2,
        "cathode": 1,
        "source": 1,
        "ah": "name",
        "form_factor": "form",
        "test": "abuse",
        "mapping": "date_time, test_time, cycle_index, i, v",
        "tester": "person",
        "temperature": 123,
        "thickness": 1,
        "v_init": 0,
        "indentor": 1,
        "nail_speed": 0,
    }]
    input_pd_df = pd.DataFrame(data=input_df, columns=input_df_cols)
    output_df_cell_md, output_df_test_md = split_abuse_metadata(input_pd_df)
    assert len(output_df_cell_md) == 1 and len(output_df_cell_md.columns) == 8
    assert len(output_df_test_md) == 1 and len(output_df_test_md.columns) == 6


def test_populate_cycle_metadata():
    cell_id = "sort-populate-cycle-metadata"
    input_df_cols = [
        "cell_id",
        "anode",
        "cathode",
        "source",
        "ah",
        "form_factor",
        "test",
        "mapping",
        "tester",
        "temperature",
        "soc_max",
        "soc_min",
        "crate_c",
        "crate_d",
    ]
    input_df = [{
        "cell_id": cell_id,
        "anode": 2,
        "cathode": 1,
        "source": 1,
        "ah": "name",
        "form_factor": "form",
        "test": "abuse",
        "mapping": "date_time, test_time, cycle_index, i, v",
        "tester": "person",
        "temperature": 123,
        "soc_max": 1,
        "soc_min": 0,
        "crate_c": 1,
        "crate_d": 0,
    }]
    input_pd_df = pd.DataFrame(data=input_df, columns=input_df_cols)
    output_df_cell_md, output_df_test_md = split_cycle_metadata(input_pd_df)
    print(output_df_cell_md, output_df_test_md )
    assert len(output_df_cell_md) == 1 and len(output_df_cell_md.columns) == 8
    assert len(output_df_test_md) == 1 and len(output_df_test_md.columns) == 6




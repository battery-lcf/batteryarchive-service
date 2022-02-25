import pandas as pd
from app.archive_constants import (LABEL)
import warnings
from pandas.core.common import SettingWithCopyWarning

pd.set_option('mode.chained_assignment', None)

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


def extract_cell_metdata(df_c_md):
    """ Build cell metadata """
    df_cell_md = pd.DataFrame()
    df_cell_md[LABEL.CELL_ID.value] = [df_c_md[LABEL.CELL_ID.value]]
    df_cell_md[LABEL.ANODE.value] = [df_c_md[LABEL.ANODE.value]]
    df_cell_md[LABEL.CATHODE.value] = [df_c_md[LABEL.CATHODE.value]]
    df_cell_md[LABEL.SOURCE.value] = [df_c_md[LABEL.SOURCE.value]]
    df_cell_md[LABEL.AH.value] = [df_c_md[LABEL.AH.value]]
    df_cell_md[LABEL.FORM_FACTOR.value] = [df_c_md[LABEL.FORM_FACTOR.value]]
    df_cell_md[LABEL.TEST.value] = [df_c_md[LABEL.TEST.value]]
    # df_cell_md[LABEL.MAPPING.value] = [df_c_md[LABEL.MAPPING.value]]
    df_cell_md[LABEL.TESTER.value] = [df_c_md[LABEL.TESTER.value]]

    return df_cell_md


def split_cycle_metadata(df_c_md):

    df_cell_md = extract_cell_metdata(df_c_md)

    # Build test metadata
    df_test_md = pd.DataFrame()
    df_test_md[LABEL.CELL_ID.value] = [df_c_md[LABEL.CELL_ID.value]]
    df_test_md[LABEL.CRATE_C.value] = [df_c_md[LABEL.CRATE_C.value]]
    df_test_md[LABEL.CRATE_D.value] = [df_c_md[LABEL.CRATE_D.value]]
    df_test_md[LABEL.SOC_MAX.value] = [df_c_md[LABEL.SOC_MAX.value]]
    df_test_md[LABEL.SOC_MIN.value] = [df_c_md[LABEL.SOC_MIN.value]]
    df_test_md[LABEL.TEMP.value] = [df_c_md[LABEL.TEMP.value]]

    return df_cell_md, df_test_md


def split_abuse_metadata(df_c_md):

    df_cell_md = extract_cell_metdata(df_c_md)

    # Build test metadata
    df_test_md = pd.DataFrame()
    df_test_md[LABEL.CELL_ID.value] = [df_c_md[LABEL.CELL_ID.value]]
    df_test_md[LABEL.THICKNESS.value] = [df_c_md[LABEL.THICKNESS.value]]
    df_test_md[LABEL.V_INIT.value] = [df_c_md[LABEL.V_INIT.value]]
    df_test_md[LABEL.INDENTOR.value] = [df_c_md[LABEL.INDENTOR.value]]
    df_test_md[LABEL.NAIL_SPEED.value] = [df_c_md[LABEL.NAIL_SPEED.value]]
    df_test_md[LABEL.TEMP.value] = [df_c_md[LABEL.TEMP.value]]

    return df_cell_md, df_test_md


# sort data imported to insure cycle index and test times are correctly calculated
def sort_timeseries(df_tmerge):
    # Arrange the data by date time first, then by test time
    # Rebuild Cycle Index and test time to increment from file to file
    # This method does not depend on data from a specific testers

    if not df_tmerge.empty:

        df_t = df_tmerge.sort_values(
            by=[LABEL.DATE_TIME.value, LABEL.TEST_TIME.value])
        df_t = df_t.reset_index(drop=True)

        cycles = df_t[[
            LABEL.CYCLE_INDEX_FILE.value, LABEL.CYCLE_INDEX.value,
            LABEL.FILENAME.value, LABEL.TEST_TIME.value
        ]].to_numpy()

        max_cycle = 1
        past_index = 1
        max_time = 0
        last_file = ""
        delta_t = 0
        start = 0

        for x in cycles:

            if start == 0:
                last_file = x[2]
                start += 1

            if x[2] != last_file:
                delta_t = max_time
                x[3] += delta_t
                last_file = x[2]
            else:
                x[3] += delta_t
                max_time = x[3]
                last_file = x[2]

            if x[0] < max_cycle:

                if past_index == x[0]:
                    past_index = x[0]
                    x[1] = max_cycle
                else:
                    past_index = x[0]
                    x[1] = max_cycle + 1
                    max_cycle = x[1]

            else:
                past_index = x[0]
                max_cycle = x[0]
                x[1] = x[0]

        df_tmp = pd.DataFrame(data=cycles[:, [1]],
                              columns=[LABEL.CYCLE_INDEX.value])
        df_t[LABEL.CYCLE_INDEX.value] = df_tmp[LABEL.CYCLE_INDEX.value]

        df_tmp = pd.DataFrame(data=cycles[:, [3]],
                              columns=[LABEL.TEST_TIME.value])
        df_t[LABEL.TEST_TIME.value] = pd.to_numeric(
            df_tmp[LABEL.TEST_TIME.value])

        df_ts = df_t.sort_values(by=[LABEL.TEST_TIME.value])

        # Remove quantities only needed to tag files
        df_ts.drop(LABEL.FILENAME.value, axis=1, inplace=True)
        df_ts.drop(LABEL.CYCLE_INDEX_FILE.value, axis=1, inplace=True)

        return df_ts


# calculate statistics for abuse test
def calc_abuse_stats(df_t, df_test_md):

    for _ in df_t.index:
        df_t[LABEL.NORM_D.value] = df_t.iloc[
            0:, df_t.columns.get_loc(LABEL.AXIAL_D.value)] - df_t[
                LABEL.AXIAL_D.value][0]
        df_t[LABEL.STRAIN.value] = df_t.iloc[
            0:, df_t.columns.get_loc(LABEL.NORM_D.value)] / df_test_md[
                LABEL.THICKNESS.value]

    return df_t


def calc_cycle_stats(df_t):

    df_t[LABEL.CYCLE_TIME.value] = 0

    no_cycles = int(df_t[LABEL.CYCLE_INDEX.value].max())

    # Initialize the cycle_data time frame
    a = [0 for _ in range(no_cycles)]  # using loops

    df_c = pd.DataFrame(data=a, columns=[LABEL.CYCLE_INDEX.value])

    df_c[LABEL.CELL_ID.value] = df_t[LABEL.CELL_ID.value]
    df_c[LABEL.CYCLE_INDEX.value] = 0
    df_c[LABEL.V_MAX.value] = 0
    df_c[LABEL.I_MAX.value] = 0
    df_c[LABEL.V_MIN.value] = 0
    df_c[LABEL.I_MIN.value] = 0
    df_c[LABEL.AH_C.value] = 0
    df_c[LABEL.AH_D.value] = 0
    df_c[LABEL.E_C.value] = 0
    df_c[LABEL.E_D.value] = 0
    df_c[LABEL.V_C_MEAN.value] = 0
    df_c[LABEL.V_D_MEAN.value] = 0
    df_c[LABEL.TEST_TIME.value] = 0
    df_c[LABEL.AH_EFF.value] = 0
    df_c[LABEL.E_EFF.value] = 0

    for c_ind in df_c.index:
        x = c_ind + 1

        df_f = df_t[df_t[LABEL.CYCLE_INDEX.value] == x]

        df_f[LABEL.AH_C.value] = 0
        df_f[LABEL.E_C.value] = 0
        df_f[LABEL.AH_D.value] = 0
        df_f[LABEL.E_D.value] = 0

        if not df_f.empty:

            try:

                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.CYCLE_INDEX.value)] = x

                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.V_MAX.value)] = df_f.loc[
                              df_f[LABEL.V.value].idxmax()].v
                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.V_MIN.value)] = df_f.loc[
                              df_f[LABEL.V.value].idxmin()].v

                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.I_MAX.value)] = df_f.loc[
                              df_f[LABEL.I.value].idxmax()].i
                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.I_MIN.value)] = df_f.loc[
                              df_f[LABEL.I.value].idxmin()].i

                df_c.iloc[
                    c_ind,
                    df_c.columns.get_loc(LABEL.TEST_TIME.value)] = df_f.loc[
                        df_f[LABEL.TEST_TIME.value].idxmax()].test_time

                df_f[LABEL.DT.value] = df_f[LABEL.TEST_TIME.value].diff() / 3600.0
                df_f_c = df_f[df_f[LABEL.I.value] > 0]
                df_f_d = df_f[df_f[LABEL.I.value] < 0]

                df_f = calc_cycle_quantities(df_f)

                df_t.loc[df_t.cycle_index == x,
                         LABEL.CYCLE_TIME.value] = df_f[LABEL.CYCLE_TIME.value]
                df_t.loc[df_t.cycle_index == x,
                         LABEL.AH_C.value] = df_f[LABEL.AH_C.value]
                df_t.loc[df_t.cycle_index == x,
                         LABEL.E_C.value] = df_f[LABEL.E_C.value]
                df_t.loc[df_t.cycle_index == x,
                         LABEL.AH_D.value] = df_f[LABEL.AH_D.value]
                df_t.loc[df_t.cycle_index == x,
                         LABEL.E_D.value] = df_f[LABEL.E_D.value]

                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.AH_C.value)] = df_f[
                              LABEL.AH_C.value].max()
                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.AH_D.value)] = df_f[
                              LABEL.AH_D.value].max()
                df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.E_C.value)] = df_f[
                    LABEL.E_C.value].max()
                df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.E_D.value)] = df_f[
                    LABEL.E_D.value].max()

                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.V_C_MEAN.value)] = df_f_c[
                              LABEL.V.value].mean()
                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.V_D_MEAN.value)] = df_f_d[
                              LABEL.V.value].mean()

                if df_c.iloc[c_ind,
                             df_c.columns.get_loc(LABEL.AH_C.value)] == 0:
                    df_c.iloc[c_ind,
                              df_c.columns.get_loc(LABEL.AH_EFF.value)] = 0
                else:
                    df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.AH_EFF.value)] = df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.AH_D.value)] / \
                                                                       df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.AH_C.value)]

                if df_c.iloc[c_ind,
                             df_c.columns.get_loc(LABEL.E_C.value)] == 0:
                    df_c.iloc[c_ind,
                              df_c.columns.get_loc(LABEL.E_EFF.value)] = 0
                else:
                    df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.E_EFF.value)] = df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.E_D.value)] / \
                                                                      df_c.iloc[c_ind, df_c.columns.get_loc(LABEL.E_C.value)]

            except Exception as e:
                pass

    df_cc = df_c[df_c[LABEL.CYCLE_INDEX.value] > 0]
    df_tt = df_t[df_t[LABEL.CYCLE_INDEX.value] > 0]
    return df_cc, df_tt


# unpack the dataframe and calculate quantities used in statistics
def calc_cycle_quantities(df):

    tmp_arr = df[[
        LABEL.TEST_TIME.value, LABEL.I.value, LABEL.V.value, LABEL.AH_C.value,
        LABEL.E_C.value, LABEL.AH_D.value, LABEL.E_D.value,
        LABEL.CYCLE_TIME.value
    ]].to_numpy()

    start = 0
    last_time = 0
    last_i_c = 0
    last_v_c = 0
    last_i_d = 0
    last_v_d = 0
    last_ah_c = 0
    last_e_c = 0
    last_ah_d = 0
    last_e_d = 0
    initial_time = 0

    for x in tmp_arr:

        if start == 0:
            start += 1
            initial_time = x[0]
        else:
            if x[1] >= 0:
                x[3] = (x[0] - last_time) * (x[1] + last_i_c) * 0.5 + last_ah_c
                x[4] = (x[0] - last_time) * (x[1] + last_i_c) * 0.5 * (
                    x[2] + last_v_c) * 0.5 + last_e_c
                last_i_c = x[1]
                last_v_c = x[2]
                last_ah_c = x[3]
                last_e_c = x[4]

            if x[1] <= 0:
                x[5] = (x[0] - last_time) * (x[1] + last_i_d) * 0.5 + last_ah_d
                # if x[5] == 0:
                #     print("x5=0:" + str(x[5]) + " last_ah_d: " +
                #           str(last_ah_d))
                # if last_ah_d == 0:
                #     print("x5:" + str(x[5]) + " last_ah_d=0: " +
                #           str(last_ah_d))
                x[6] = (x[0] - last_time) * (x[1] + last_i_d) * 0.5 * (
                    x[2] + last_v_d) * 0.5 + last_e_d
                last_i_d = x[1]
                last_v_d = x[2]
                last_ah_d = x[5]
                last_e_d = x[6]

        x[7] = x[0] - initial_time
        last_time = x[0]

    df_tmp = pd.DataFrame(data=tmp_arr[:, [3]], columns=[LABEL.AH_C.value])
    df_tmp.index += df.index[0]
    df[LABEL.AH_C.value] = df_tmp[LABEL.AH_C.value] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [4]], columns=[LABEL.E_C.value])
    df_tmp.index += df.index[0]
    df[LABEL.E_C.value] = df_tmp[LABEL.E_C.value] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [5]], columns=[LABEL.AH_D.value])
    df_tmp.index += df.index[0]
    df[LABEL.AH_D.value] = -df_tmp[LABEL.AH_D.value] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [6]], columns=[LABEL.E_D.value])
    df_tmp.index += df.index[0]
    df[LABEL.E_D.value] = -df_tmp[LABEL.E_D.value] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [7]],
                          columns=[LABEL.CYCLE_TIME.value])
    df_tmp.index += df.index[0]
    df[LABEL.CYCLE_TIME.value] = df_tmp[LABEL.CYCLE_TIME.value]

    return df

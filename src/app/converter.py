import pandas as pd
from archive_constants import (LABEL, TEST_TYPE)


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
            "cycle_index_file", "cycle_index", "filename", "test_time"
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

        df_tmp = pd.DataFrame(data=cycles[:, [1]], columns=["cycle_index"])
        df_t['cycle_index'] = df_tmp['cycle_index']

        df_tmp = pd.DataFrame(data=cycles[:, [3]], columns=["test_time"])
        df_t['test_time'] = pd.to_numeric(df_tmp['test_time'])

        df_ts = df_t.sort_values(by=['test_time'])

        # Remove quantities only needed to tag files
        df_ts.drop('filename', axis=1, inplace=True)
        df_ts.drop('cycle_index_file', axis=1, inplace=True)

        return df_ts


# calculate statistics for abuse test
def calc_abuse_stats(df_t, df_test_md):

    for _ in df_t.index:
        df_t["norm_d"] = df_t.iloc[
            0:, df_t.columns.get_loc("axial_d")] - df_t['axial_d'][0]
        df_t['strain'] = df_t.iloc[
            0:, df_t.columns.get_loc("norm_d")] / df_test_md['thickness']

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
                              df_f['v'].idxmax()].v
                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.V_MIN.value)] = df_f.loc[
                              df_f['v'].idxmin()].v

                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.I_MAX.value)] = df_f.loc[
                              df_f['i'].idxmax()].i
                df_c.iloc[c_ind,
                          df_c.columns.get_loc(LABEL.I_MIN.value)] = df_f.loc[
                              df_f['i'].idxmin()].i

                df_c.iloc[c_ind, df_c.columns.get_loc('test_time')] = df_f.loc[
                    df_f['test_time'].idxmax()].test_time

                df_f['dt'] = df_f['test_time'].diff() / 3600.0
                df_f_c = df_f[df_f['i'] > 0]
                df_f_d = df_f[df_f['i'] < 0]

                df_f = calc_cycle_quantities(df_f)

                df_t.loc[df_t.cycle_index == x,
                         'cycle_time'] = df_f['cycle_time']
                df_t.loc[df_t.cycle_index == x, 'ah_c'] = df_f['ah_c']
                df_t.loc[df_t.cycle_index == x, 'e_c'] = df_f['e_c']
                df_t.loc[df_t.cycle_index == x, 'ah_d'] = df_f['ah_d']
                df_t.loc[df_t.cycle_index == x, 'e_d'] = df_f['e_d']

                df_c.iloc[c_ind,
                          df_c.columns.get_loc('ah_c')] = df_f['ah_c'].max()
                df_c.iloc[c_ind,
                          df_c.columns.get_loc('ah_d')] = df_f['ah_d'].max()
                df_c.iloc[c_ind,
                          df_c.columns.get_loc('e_c')] = df_f['e_c'].max()
                df_c.iloc[c_ind,
                          df_c.columns.get_loc('e_d')] = df_f['e_d'].max()

                df_c.iloc[
                    c_ind,
                    df_c.columns.get_loc('v_c_mean')] = df_f_c['v'].mean()
                df_c.iloc[
                    c_ind,
                    df_c.columns.get_loc('v_d_mean')] = df_f_d['v'].mean()

                if df_c.iloc[c_ind, df_c.columns.get_loc('ah_c')] == 0:
                    df_c.iloc[c_ind, df_c.columns.get_loc('ah_eff')] = 0
                else:
                    df_c.iloc[c_ind, df_c.columns.get_loc('ah_eff')] = df_c.iloc[c_ind, df_c.columns.get_loc('ah_d')] / \
                                                                       df_c.iloc[c_ind, df_c.columns.get_loc('ah_c')]

                if df_c.iloc[c_ind, df_c.columns.get_loc('e_c')] == 0:
                    df_c.iloc[c_ind, df_c.columns.get_loc('e_eff')] = 0
                else:
                    df_c.iloc[c_ind, df_c.columns.get_loc('e_eff')] = df_c.iloc[c_ind, df_c.columns.get_loc('e_d')] / \
                                                                      df_c.iloc[c_ind, df_c.columns.get_loc('e_c')]

            except Exception as e:
                pass

    df_cc = df_c[df_c[LABEL.CYCLE_INDEX.value] > 0]
    df_tt = df_t[df_t[LABEL.CYCLE_INDEX.value] > 0]
    return df_cc, df_tt


# unpack the dataframe and calculate quantities used in statistics
def calc_cycle_quantities(df):

    tmp_arr = df[[
        "test_time", "i", "v", "ah_c", 'e_c', 'ah_d', 'e_d', 'cycle_time'
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

    df_tmp = pd.DataFrame(data=tmp_arr[:, [3]], columns=["ah_c"])
    df_tmp.index += df.index[0]
    df['ah_c'] = df_tmp['ah_c'] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [4]], columns=["e_c"])
    df_tmp.index += df.index[0]
    df['e_c'] = df_tmp['e_c'] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [5]], columns=["ah_d"])
    df_tmp.index += df.index[0]
    df['ah_d'] = -df_tmp['ah_d'] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [6]], columns=["e_d"])
    df_tmp.index += df.index[0]
    df['e_d'] = -df_tmp['e_d'] / 3600.0

    df_tmp = pd.DataFrame(data=tmp_arr[:, [7]], columns=["cycle_time"])
    df_tmp.index += df.index[0]
    df['cycle_time'] = df_tmp['cycle_time']

    return df

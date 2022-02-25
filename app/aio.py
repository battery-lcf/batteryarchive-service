import glob
import logging
import pandas as pd
import os
from app.archive_constants import (GA_API_HOST, LABEL,
                                   TEST_TYPE, TESTER, INP_LABELS, ARCHIVE_COLS, FORMAT)
from app.converter import (sort_timeseries)
import pyarrow.feather as feather
import datetime
import time
import batteryclient
from pprint import pprint
from batteryclient.api import users_api
import numpy as np


class GAReader:
    def __init__(self, token):
        self.host = GA_API_HOST
        self.token = token

    def read_metadata(self, dataset_id):
        configuration = batteryclient.Configuration(
            host=self.host,
            access_token=self.token
        )
        # Enter a context with an instance of the API client
        with batteryclient.ApiClient(configuration) as api_client:
            try:
                # Create an instance of the API class
                api_instance = users_api.UsersApi(api_client)
                response = api_instance.get_dataset(dataset_id)
                cell = response.cell
                name = response.name
                columns = response.columns
                metadata = {}
                metadata[LABEL.SOURCE.value] = 'OX'
                metadata[LABEL.CELL_ID.value] = metadata[LABEL.SOURCE.value] + '-' + name
                metadata[LABEL.AH.value] = cell['nominal_capacity']
                metadata[LABEL.ANODE.value] = cell['anode_chemistry']
                metadata[LABEL.CATHODE.value] = cell['cathode_chemistry']
                metadata[LABEL.FORM_FACTOR.value] = 'test-form-factor'
                metadata[LABEL.TEST.value] = TEST_TYPE.CYCLE.value
                metadata[LABEL.TESTER.value] = TESTER.MACCOR.value
                metadata[LABEL.CRATE_C.value] = None
                metadata[LABEL.CRATE_D.value] = None
                metadata[LABEL.SOC_MAX.value] = None
                metadata[LABEL.SOC_MIN.value] = None

                metadata[LABEL.TEMP.value] = None

                return metadata, columns

            except batteryclient.ApiException as e:
                print("Exception when calling UsersApi->get_dataset: %s\n" % e)
            except Exception as e:
                print(e)

    def read_data(self, dataset_id, columns):
        configuration = batteryclient.Configuration(
            host=self.host,
            access_token=self.token
        )
        column_ids = {}
        for col in columns:
            if col['name'] == 'time/s':
                column_ids['time/s'] = col['id']
            if col['name'] == 'Ewe/V':
                column_ids['Ewe/V'] = col['id']
            if col['name'] == 'I/mA':
                column_ids['I/mA'] = col['id']

        print("READING DATA:", dataset_id)
        # Enter a context with an instance of the API client
        with batteryclient.ApiClient(configuration) as api_client:
            try:
                # Create an instance of the API class
                api_instance = users_api.UsersApi(api_client)

                data = {
                    column_name: np.frombuffer(
                        api_instance.get_column(dataset_id, column_id).read(),
                        dtype=np.float32
                    ) for column_name, column_id in column_ids.items()
                }
                data[LABEL.V.value] = data['Ewe/V']
                data[LABEL.I.value] = data['I/mA']
                data[LABEL.CYCLE_INDEX.value] = [1] * len(data['I/mA'])
                data[LABEL.TEST_TIME.value] = data['time/s']
                data[LABEL.DATE_TIME.value] = [datetime.datetime(
                    2020, 1, 1) + datetime.timedelta(seconds=d.item()) for d in data['time/s']]
                data.pop('time/s')
                data.pop('Ewe/V')
                data.pop('I/mA')

                return data

            except batteryclient.ApiException as e:
                print("Exception when calling UsersApi->get_dataset: %s\n" % e)
            except Exception as e:
                print(e)


class CellTestReader:
    def __init__(self, tester, test_type):
        self.tester = tester
        self.test_type = test_type

    """
    read_data reads data from all supported tester types

    :param cell_id: Unique Cell Identifier
    :param file_path: Absolute Path to the file that is to be read
    :param tester: String identifier of what tester type is being read
    :return: DataFrame with data from reader
    """

    def read_data(self, file_path):
        if self.tester == TESTER.ARBIN.value:
            data = self.read_arbin(file_path)
        if self.tester == TESTER.MACCOR.value:
            data = self.read_maccor(file_path)
        if self.tester == TESTER.GENERIC.value:
            data = self.read_generic(file_path)
        if self.tester == TESTER.ORNL.value:
            data = self.read_ornlabuse(file_path)
        if self.tester == TESTER.SNL.value:
            data = self.read_snlabuse(file_path)

        if self.test_type == TEST_TYPE.CYCLE.value:
            return sort_timeseries(data)
        if self.test_type == TEST_TYPE.ABUSE.value:
            return data

    # import data from a generic tester
    @staticmethod
    def read_generic(file_path, file_type='cvs', mapping='test_time, date_time, voltage, current'):

        logging.info('adding files')

        listOfFiles = glob.glob(file_path + '*.' + file_type)

        for i in range(len(listOfFiles)):
            listOfFiles[i] = listOfFiles[i].replace(file_path[:-1], '')

        logging.info('list of files to add: ' + str(listOfFiles))

        df_file = pd.DataFrame(listOfFiles, columns=['filename'])

        df_file.sort_values(by=['filename'], inplace=True)

        if df_file.empty:
            return

        # df_file['cell_id'] = cell_id

        df_tmerge = pd.DataFrame()

        # Loop through all the Excel test files
        for ind in df_file.index:

            filename = df_file['filename'][ind]
            cellpath = file_path + filename

            logging.info('processing file: ' + filename)

            if os.path.exists(cellpath):

                if file_type == 'csv':
                    df_time_series_file = pd.read_csv(cellpath, sep=',')
                elif file_type == 'h5':
                    # need to make a bit more generic. Use raw_data for now
                    df_time_series_file = pd.read_hdf(cellpath, "raw_data")

                # Find the time series sheet in the excel file
                df_ts = pd.DataFrame()
                column_list = mapping.split(",")

                file_col = 0
                for col in column_list:

                    if col == 'date_time':
                        file_col_name = df_time_series_file.columns[file_col]
                        df_ts['date_time'] = pd.to_datetime(
                            df_time_series_file[file_col_name], format='%Y-%m-%d %H:%M:%S.%f')
                    elif col != "skip":
                        file_col_name = df_time_series_file.columns[file_col]
                        df_ts[col] = df_time_series_file[file_col_name].apply(
                            pd.to_numeric)

                    file_col += 1

                # need at the least one of date_time or test_time
                # TODO: how do we fail the import?

                if "date_time" not in df_ts.columns and "test_time" in df_ts.columns:
                    df_ts['date_time'] = pd.Timestamp(
                        datetime.datetime.now()) + pd.to_timedelta(df_ts['test_time'], unit='s')

                if "date_time" in df_ts.columns and "test_time" not in df_ts.columns:
                    df_ts['test_time'] = df_ts['date_time'] - \
                        df_ts['date_time'].iloc[0]
                    df_ts['test_time'] = df_ts['test_time'].dt.total_seconds()

                df_ts['ah_c'] = 0
                df_ts['e_c'] = 0
                df_ts['ah_d'] = 0
                df_ts['e_d'] = 0
                # df_ts['cell_id'] = cell_id
                df_ts['cycle_time'] = 0

                if df_tmerge.empty:
                    df_tmerge = df_ts[df_ts['test_time'] > 0]
                else:
                    df_tmerge = df_tmerge.append(
                        df_ts[df_ts['test_time'] > 0], ignore_index=True)

        return df_tmerge

    # import data from Arbin-generated Excel files

    @staticmethod
    def read_arbin(file_path, file_type='xlsx'):

        # the importer can read Excel worksheets with the Channel number from Arbin files.
        # it assumes column names generated by the Arbin:
        # Cycle_Index -> cycle_index
        # Test_Time(s) -> test_time
        # Current(A) -> i
        # Voltage(V) -> v
        # Date_Time -> date_time

        logging.info('adding files')

        listOfFiles = glob.glob(file_path + '*.xls*')

        for i in range(len(listOfFiles)):
            listOfFiles[i] = listOfFiles[i].replace(file_path[:-1], '')

        logging.info('list of files to add: ' + str(listOfFiles))

        df_file = pd.DataFrame(listOfFiles, columns=['filename'])

        df_file.sort_values(by=['filename'], inplace=True)

        if df_file.empty:
            return

        # df_file['cell_id'] = cell_id

        df_tmerge = pd.DataFrame()

        # Loop through all the Excel test files
        for ind in df_file.index:

            filename = df_file['filename'][ind]
            cellpath = file_path + filename
            timeseries = ""

            logging.info('processing file: ' + filename)

            if os.path.exists(cellpath):
                if '~$' in cellpath:
                    continue
                df_cell = []
                if file_type == FORMAT.XLSX.value:
                    df_cell = pd.read_excel(cellpath, None)
                if file_type == FORMAT.FEATHER.value:
                    df_cell = pd.read_feather(cellpath, None)
                # Find the time series sheet in the excel file
                for k in df_cell.keys():
                    if "hannel" in k:
                        logging.info("file: " + filename + " sheet:" + str(k))
                        timeseries = k

                        df_time_series_file = df_cell[timeseries]

                        df_ts = pd.DataFrame()

                        df_ts['cycle_index_file'] = df_time_series_file[
                            'Cycle_Index']
                        df_ts['test_time'] = df_time_series_file[
                            'Test_Time(s)']
                        df_ts['i'] = df_time_series_file['Current(A)']
                        df_ts['v'] = df_time_series_file['Voltage(V)']
                        df_ts['date_time'] = df_time_series_file['Date_Time']
                        df_ts['filename'] = filename

                        # if not df_time_series_file['Temperature (C)_1'].empty:
                        #    df_time_series['temp_2'] = df_time_series_file['Temperature (C)_1']

                        df_ts['ah_c'] = 0
                        df_ts['e_c'] = 0
                        df_ts['ah_d'] = 0
                        df_ts['e_d'] = 0
                        df_ts['cycle_index'] = 0
                        df_ts['cycle_time'] = 0

                        cycles_index = df_ts[["cycle_index_file"]].to_numpy()
                        past_cycle = 0
                        start = 0

                        for x in cycles_index:
                            if start == 0:
                                past_cycle = x[0]
                                start += 1
                            else:
                                if x[0] < past_cycle:
                                    x[0] = past_cycle
                                past_cycle = x[0]

                        df_tmp = pd.DataFrame(data=cycles_index[:, [0]],
                                              columns=["cycle_index_file"])
                        df_ts['cycle_index_file'] = df_tmp['cycle_index_file']

                        if df_tmerge.empty:
                            df_tmerge = df_ts
                        else:
                            df_tmerge = df_tmerge.append(df_ts,
                                                         ignore_index=True)

        return df_tmerge

    # import data from MACCOR-generated  files
    @staticmethod
    def read_maccor(file_path):

        # the importer can read Excel worksheets with the Channel number from Arbin files.
        # it assumes column names generated by the MACCOR:
        # Cycle_Index -> cycle_index
        # Test_Time(s) -> test_time
        # Current(A) -> i
        # Voltage(V) -> v
        # Date_Time -> date_time

        logging.info('adding files')

        listOfFiles = glob.glob(file_path + '*.txt')

        for i in range(len(listOfFiles)):
            listOfFiles[i] = listOfFiles[i].replace(file_path[:-1], '')

        logging.info('list of files to add: ' + str(listOfFiles))

        df_file = pd.DataFrame(listOfFiles, columns=['filename'])

        df_file.sort_values(by=['filename'], inplace=True)

        if df_file.empty:
            return

        df_tmerge = pd.DataFrame()

        # Loop through all the Excel test files
        for ind in df_file.index:

            filename = df_file['filename'][ind]
            cellpath = file_path + filename

            logging.info('processing file: ' + filename)

            if os.path.exists(cellpath):

                cellpath_df = CellTestReader(
                    TESTER.MACCOR,
                    TEST_TYPE.CYCLE).prepare_maccor_file(cellpath)

                df_cell = pd.read_csv(cellpath_df, sep='\t')
                # Find the time series sheet in the excel file

                df_time_series_file = df_cell

                df_time_series = pd.DataFrame()

                df_time_series['cycle_index_file'] = df_time_series_file[
                    'Cycle'].apply(pd.to_numeric)
                df_time_series['test_time'] = df_time_series_file[
                    'Test Time (sec)'].str.replace(',',
                                                   '').apply(pd.to_numeric)

                df_time_series['i'] = df_time_series_file['Current'].apply(
                    pd.to_numeric)
                df_time_series['MD'] = df_time_series_file['MD']

                df_time_series['i'] = df_time_series.apply(
                    lambda x: signedCurrent(x.MD, x.i), axis=1)

                df_time_series.drop('MD', axis=1, inplace=True)

                df_time_series['v'] = df_time_series_file['Voltage'].apply(
                    pd.to_numeric)
                df_time_series['date_time'] = pd.to_datetime(
                    df_time_series_file['DPT Time'],
                    format='%m/%d/%Y %I:%M:%S %p')
                df_time_series['filename'] = filename

                df_time_series['ah_c'] = 0
                df_time_series['e_c'] = 0
                df_time_series['ah_d'] = 0
                df_time_series['e_d'] = 0
                df_time_series['cycle_index'] = 0
                df_time_series['cycle_time'] = 0

                if df_tmerge.empty:
                    df_tmerge = df_time_series
                else:
                    df_tmerge = df_tmerge.append(df_time_series,
                                                 ignore_index=True)

        return df_tmerge

    # Read the abuse excel file from ORNL
    @staticmethod
    def read_ornlabuse(file_path):

        excels = glob.glob(file_path + '*.xls*')

        df_tmerge = pd.DataFrame()
        for excel in excels:
            if '~$' in excel:
                continue
            df_ts_file = pd.read_excel(
                excel, sheet_name='data')  # dictionary of sheets

            df_ts_a = pd.DataFrame()
            df_ts_a['test_time'] = df_ts_file['Running Time']
            df_ts_a['axial_d'] = df_ts_file['Axial Displacement']
            df_ts_a['v'] = df_ts_file['Analog 1']
            df_ts_a['axial_f'] = df_ts_file['Axial Force']
            df_ts_a[ARCHIVE_COLS.temp_1.value] = 0
            df_ts_a[ARCHIVE_COLS.temp_2.value] = 0
            df_ts_a[ARCHIVE_COLS.temp_3.value] = 0
            df_ts_a[ARCHIVE_COLS.temp_4.value] = 0
            df_ts_a[ARCHIVE_COLS.temp_5.value] = 0
            df_ts_a[ARCHIVE_COLS.temp_6.value] = 0

            df_ts_b = pd.DataFrame()
            df_ts_b['test_time'] = df_ts_file['Running Time 1']
            df_ts_b[ARCHIVE_COLS.AXIAL_D.value] = 0
            df_ts_b[ARCHIVE_COLS.V.value] = 0
            df_ts_b[ARCHIVE_COLS.AXIAL_F.value] = 0
            df_ts_b[ARCHIVE_COLS.temp_1.value] = df_ts_file[
                INP_LABELS.TC_01.value]
            df_ts_b[ARCHIVE_COLS.temp_2.value] = df_ts_file[
                INP_LABELS.TC_02.value]
            df_ts_b[ARCHIVE_COLS.temp_3.value] = df_ts_file[
                INP_LABELS.TC_03.value]
            df_ts_b[ARCHIVE_COLS.temp_4.value] = df_ts_file[
                INP_LABELS.TC_04.value]
            df_ts_b[ARCHIVE_COLS.temp_5.value] = df_ts_file[
                INP_LABELS.TC_05.value]
            df_ts_b[ARCHIVE_COLS.temp_6.value] = df_ts_file[
                INP_LABELS.TC_06.value]

            if df_tmerge.empty:
                df_tmerge = df_ts_a
                df_tmerge = df_tmerge.append(df_ts_b, ignore_index=True)
            else:
                df_tmerge = df_tmerge.append(df_ts_a, ignore_index=True)
                df_tmerge = df_tmerge.append(df_ts_b, ignore_index=True)

        return df_tmerge

    # read the abuse excel files from SNL
    @staticmethod
    def read_snlabuse(file_path):

        excels = glob.glob(file_path + '*.xls*')

        df_tmerge = pd.DataFrame()

        for excel in excels:
            if '~$' in excel:
                continue
            df_ts_file = pd.read_excel(
                excel, sheet_name='data')  # dictionary of sheets

            df_ts = pd.DataFrame()
            df_ts[ARCHIVE_COLS.TEST_TIME.value] = df_ts_file[
                INP_LABELS.TEST_TIME.value]
            df_ts[ARCHIVE_COLS.AXIAL_D.value] = df_ts_file[
                INP_LABELS.AXIAL_D.value]
            df_ts[ARCHIVE_COLS.AXIAL_F.value] = df_ts_file[
                INP_LABELS.AXIAL_F.value]
            df_ts[ARCHIVE_COLS.V.value] = df_ts_file[INP_LABELS.V.value]
            df_ts[ARCHIVE_COLS.temp_1.value] = df_ts_file[
                INP_LABELS.TC_01.value]
            df_ts[ARCHIVE_COLS.temp_2.value] = df_ts_file[
                INP_LABELS.TC_02.value]
            df_ts[ARCHIVE_COLS.temp_3.value] = df_ts_file[
                INP_LABELS.TC_03.value]
            df_ts[ARCHIVE_COLS.temp_4.value] = df_ts_file[
                INP_LABELS.TC_04.value]
            df_ts[ARCHIVE_COLS.temp_5.value] = df_ts_file[
                INP_LABELS.TC_05.value]
            df_ts[ARCHIVE_COLS.temp_6.value] = df_ts_file[
                INP_LABELS.TC_06.value]

            if df_tmerge.empty:
                df_tmerge = df_ts
            else:
                df_tmerge = df_tmerge.append(df_ts, ignore_index=True)

        return df_tmerge

    # remove metadata entries from MACCOR files
    @staticmethod
    def prepare_maccor_file(cellpath):

        a_file = open(cellpath, "r", encoding='utf8', errors='ignore')
        lines = a_file.readlines()
        a_file.close()

        cellpath_df = cellpath + "_df"

        new_file = open(cellpath_df, "w")
        for line in lines:
            forget_line = line.startswith("Today") or line.startswith(
                "Filename") or line.startswith("Procedure") or line.startswith(
                    "Comment")

            if not forget_line:
                new_file.write(line)

        new_file.close()

        return cellpath_df


class ArchiveExporter:
    def __init__(self):
        pass

    """
    export_to_csv exports dataframe to csv

    :param df: Dataframe of data to be exported 
    :param cell_id: Cell ID that will be written to file
    :param path: Path to the output directory
    :return: Path to output csv file 
    """

    @staticmethod
    def write_to_csv(df, cell_id, out_path, suffix):
        cell_id_to_file = cell_id.replace(r"/", "-")
        csv_file = out_path + cell_id_to_file + "_" + suffix + ".csv"
        df.to_csv(csv_file, encoding="utf-8", index=False)
        return csv_file

    @staticmethod
    def write_to_feather(df, cell_id, out_path, suffix):
        cell_id_to_file = cell_id.replace(r"/", "-")
        feather_file = out_path + cell_id_to_file + "_" + suffix + ".feather"
        feather.write_feather(df, feather_file)
        # df.reset_index().to_feather(feather_file)
        return feather_file


# Function to convert a list to a string
def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


# identify the sign of the current for a MACCOR file
def signedCurrent(x, y):
    if x == "D":
        return -y
    else:
        return y

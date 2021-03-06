import datetime

CSData_SEPARATOR = ", "

CSData_COMMENT_PREFIX = "#"

CSData_FILE_SUFFIX = ".csd"

CSData_END_LINE = "\n"

class CSDataSaver:

    def __init__(self, cs_data):
        self._cs_data = cs_data
        self._file = None

    def _save_array(self, arr):
        for i in range(len(arr)):
            entry = arr[i]
            if i == len(arr) - 1:
                self._file.write(str(entry))
            else:
                self._file.write(str(entry) + CSData_SEPARATOR)
        self._file.write(CSData_END_LINE)

    def _save_array_of_arrays(self, arr_o_arr):
        for arr in arr_o_arr:
            self._save_array(arr)

    def _add_comment(self, string):
        self._file.write(CSData_COMMENT_PREFIX + " " + string + CSData_END_LINE)

    def _add_string(self, string):
        self._file.write(string + CSData_END_LINE)
    
    def _construct_filename(self):
        return "Results/" + self._cs_data.name + "-" + str(self._cs_data.timestamp).replace(" ", "-").replace(":", "-").split(".")[0] + CSData_FILE_SUFFIX

    def save_data(self):
        print("[CSDATA] saving started")
        with open(self._construct_filename(), "w") as f:
            self._file = f

            # HEADER
            self._add_comment("Data file of " + self._cs_data.name + " created at " + str(self._cs_data.timestamp))

            # Name
            self._add_comment("Subject name: ")
            self._add_string(self._cs_data.name)
            
            # Time stampt
            self._add_comment("Start time: ")
            self._add_string(str(self._cs_data.timestamp))

            # Step counts
            self._add_comment("Step counts:")
            self._save_array(self._cs_data.step_count)

            # Seconds
            self._add_comment("Seconds: ")
            self._save_array(self._cs_data._seconds)

            # Additional data
            self._add_comment("ms")
            self._save_array_of_arrays(self._cs_data.ms)

            self._add_comment("ms striped")
            self._save_array_of_arrays(self._cs_data.ms_stripped)

            self._add_comment("step nums striped")
            self._save_array_of_arrays(self._cs_data.step_nums_stripped)

            self._add_comment("ms interpolated")
            self._save_array_of_arrays(self._cs_data.ms_interpolated)

            self._add_comment("mean by digit")
            self._save_array_of_arrays(self._cs_data.mean_by_digit)

            self._add_comment("fft")
            self._save_array_of_arrays(self._cs_data.fft)

            self._add_comment("fft frequencies")
            self._save_array_of_arrays(self._cs_data.fft_freq)

            self._add_comment("aus")
            self._save_array(self._cs_data.aus)

            self._add_comment("mean")
            self._save_array(self._cs_data.mean)

            self._add_comment("standard deviation")
            self._save_array(self._cs_data.std_dev)

            self._add_comment("regression line")
            self._save_array(self._cs_data.regression_line)

            self._add_comment("comission error")
            self._save_array(self._cs_data.comission_errors)

            self._add_comment("omission error")
            self._save_array(self._cs_data.omission_errors)

            self._add_comment("random errors")
            self._save_array(self._cs_data.other_errors)

    def _load_int_array(self, string):
        items = string.split(CSData_SEPARATOR)
        arr = []
        for item in items:
            try:
                value = int(item)
                arr.append(value)
            except ValueError:
                print("[CSDataSaver] cannot convert string '" + item + "' to int")
        return arr

    # sorry for code repetition
    def _load_float_array(self, string):
        items = string.split(CSData_SEPARATOR)
        arr = []
        for item in items:
            try:
                value = float(item)
                arr.append(value)
            except ValueError:
                print("[CSDataSaver] cannot convert string '" + item + "' to float")
        return arr

    def _load_array_of_array(self, list_of_strings):
        arr = []
        for string in list_of_strings:
            arr.append(self._load_float_array(string))
        return arr

    def load_data(self, filename):
        print("[CSDATA] loading started")
        with open(filename, "r") as f:
            self._file = f

            lines = self._file.readlines()
            data_lines = []
            # Throw away comments
            for line in lines:
                if line[0] != CSData_COMMENT_PREFIX:
                    data_lines.append(line)
            
            # reading name
            self._cs_data.name = data_lines[0].replace(CSData_END_LINE, "")
            # reading timestamp
            # conversion based on: https://stackabuse.com/converting-strings-to-datetime-in-python/
            self._cs_data.timestamp = datetime.datetime.strptime(data_lines[1].replace(CSData_END_LINE, ""), '%Y-%m-%d %H:%M:%S.%f')
            # reading step count
            self._cs_data.step_count = self._load_int_array(data_lines[2])
            # reading seconds
            self._cs_data._seconds = self._load_float_array(data_lines[3])
            self._cs_data._multiple_press_errors = [0, 0, 0]  # todo temporary solution since its not being saved

            self._cs_data.ms = self._load_array_of_array(data_lines[4:7])
            self._cs_data.ms_stripped = self._load_array_of_array(data_lines[7:10])
            self._cs_data.step_nums_stripped = self._load_array_of_array(data_lines[10:13])
            self._cs_data.ms_interpolated = self._load_array_of_array(data_lines[13:16])
            self._cs_data.mean_by_digit = self._load_array_of_array(data_lines[16:19])
            self._cs_data.fft = self._load_array_of_array(data_lines[19:22])
            self._cs_data.fft_freq = self._load_array_of_array(data_lines[22:25])

            # statistics
            self._cs_data.aus = self._load_float_array(data_lines[25])
            self._cs_data.mean = self._load_float_array(data_lines[26])
            self._cs_data.std_dev = self._load_float_array(data_lines[27])
            self._cs_data.regression_line = self._load_float_array(data_lines[28])
            self._cs_data.comission_errors = self._load_int_array(data_lines[29])
            self._cs_data.omission_errors = self._load_int_array(data_lines[30])
            self._cs_data.other_errors = self._load_int_array(data_lines[31])

import datetime

CSData_SEPARATOR = ", "

CSData_COMMENT_PREFIX = "#"

CSData_FILE_SUFFIX = ".csd"

CSData_END_LINE = "\n"

class CSDataSaver:

    def __init__(self, cs_data):
        self.cs_data = cs_data

    def _save_array(self, arr):
        for entry in arr:
            self.file.write(str(entry)+CSData_SEPARATOR)
        self.file.write(CSData_END_LINE)

    def _save_array_of_arrays(self, arr_o_arr):
        for arr in arr_o_arr:
            self._save_array(arr)

    def _add_comment(self, string):
        self.file.write(CSData_COMMENT_PREFIX + " " + string + CSData_END_LINE)

    def _add_string(self, string):
        self.file.write(string+CSData_END_LINE)
    
    def _construct_filename(self):
        return self.cs_data._name + "-" + str(self.cs_data._timestamp).replace(" ","-").split(".")[0] + CSData_FILE_SUFFIX

    def save_data(self):
        print("[CSDATA] saving started")
        with open(self._construct_filename() , "w") as f:
            self.file = f

            # HEADER
            self._add_comment("Data file of " + self.cs_data._name + " created at " + str(self.cs_data._timestamp))

            # Name
            self._add_comment("Subject name: ")
            self._add_string(self.cs_data._name)
            
            # Time stampt
            self._add_comment("Start time: ")
            self._add_string(str(self.cs_data._timestamp))

            # Step counts
            self._add_comment("Step counts:")
            self._save_array(self.cs_data._step_count)

            # Seconds
            self._add_comment("Seconds: ")
            self._save_array(self.cs_data._seconds)

            # Additional data
            self._add_comment("ms")
            self._save_array_of_arrays(self.cs_data._ms)

            self._add_comment("ms striped")
            self._save_array_of_arrays(self.cs_data._ms_stripped)

            self._add_comment("step nums striped")
            self._save_array_of_arrays(self.cs_data._step_nums_stripped)

            self._add_comment("ms interpolated")
            self._save_array_of_arrays(self.cs_data._ms_interpolated)

            self._add_comment("mean")
            self._save_array(self.cs_data._mean)

            self._add_comment("standard deviation")
            self._save_array(self.cs_data._std_dev)

            self._add_comment("regression line")
            self._save_array(self.cs_data._regression_line)

            self._add_comment("comission error")
            self._save_array(self.cs_data._comission_errors)

            self._add_comment("omission error")
            self._save_array(self.cs_data._omission_errors)

            self._add_comment("random errors")
            self._save_array(self.cs_data._random_errors)

    def _load_int_array(self, string):
        items = string.split(CSData_SEPARATOR)
        arr = []
        for i in range(len(items)-1):
            arr.append(int(items[i]))
        return arr

    # sorry for code repetition
    def _load_float_array(self, string):
        items = string.split(CSData_SEPARATOR)
        arr = []
        for i in range(len(items)-1):
            arr.append(float(items[i]))
        return arr

    def _load_array_of_array(self, list_of_strings):
        arr = []
        for string in list_of_strings:
            arr.append(self._load_float_array(string))
        return arr

    def load_data(self, filename):
        print("[CSDATA] loading started")
        with open(filename, "r") as f:
            self.file = f

            lines = self.file.readlines()
            data_lines = []
            # Throw away comments
            for line in lines:
                if line[0] != CSData_COMMENT_PREFIX:
                    data_lines.append(line)
            
            # reading name
            self.cs_data._name = data_lines[0].replace(CSData_END_LINE,"")
            # reading timestamp
            # conversion based on: https://stackabuse.com/converting-strings-to-datetime-in-python/
            print(data_lines[1])
            self.cs_data._timestamp = datetime.datetime.strptime(data_lines[1].replace(CSData_END_LINE,""), '%Y-%m-%d %H:%M:%S.%f')
            # reading step count
            self.cs_data._step_count = self._load_int_array(data_lines[2])
            # reading seconds
            self.cs_data._seconds = self._load_float_array(data_lines[3])

            self.cs_data._ms = self._load_array_of_array(data_lines[4:7])
            self.cs_data._ms_stripped = self._load_array_of_array(data_lines[7:10])
            self.cs_data._step_nums_stripped = self._load_array_of_array(data_lines[10:13])
            self.cs_data._ms_interpolated = self._load_array_of_array(data_lines[13:16])

            # statistics
            self.cs_data._mean = self._load_float_array(data_lines[16])
            self.cs_data._std_dev = self._load_float_array(data_lines[17])
            self.cs_data._regression_line = self._load_float_array(data_lines[18])
            self.cs_data._comission_errors = self._load_float_array(data_lines[19])
            self.cs_data._omission_errors = self._load_float_array(data_lines[20])
            self.cs_data._random_errors = self._load_float_array(data_lines[21]) 

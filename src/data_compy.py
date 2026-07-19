import pandas as pd
from datacompy import PandasCompare
from config import FileGather


class df_Compare:
    def __init__(self):
        filepath = FileGather()
        self.driverconfig = filepath.driverconfig
        self.sources_file = filepath.sources_file
        self.targets_file = filepath.targets_file

    def extract_required_data(self):
        driverconfig_df = pd.read_excel(self.driverconfig)

        consider_data_df = driverconfig_df[driverconfig_df.iloc[:, 0].astype(str).str.strip().str.upper() == "Y"]

        for _, row in consider_data_df.iterrows():
            yield (
                row["testcase_name"],
                row["source_file"],
                row["target_file"],
                row["compare_key"],
            )

c1 = df_Compare()

for testcase, source_file, target_file, compare_key in c1.extract_required_data():

    print(f"Running Test Case: {testcase}")

    source_df = pd.read_excel(c1.sources_file / source_file)
    target_df = pd.read_excel(c1.targets_file / target_file)

    compare = PandasCompare(
        source_df,
        target_df,
        join_columns=[compare_key],
        df1_name="Source",
        df2_name="Target",
        ignore_case=True,
        ignore_spaces=True,
    )

    print(compare.report())
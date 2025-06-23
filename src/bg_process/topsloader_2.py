import pandas as pd
from bg_process.logloader_1 import (logsection)
import os



def top_load(file_path):
    """
    This function reads a CSV file and creates a list of all the well tops.

    Return:
        well_tops_list: list of all well tops from a CSV file.
    """
    _, _, _, _, _, _, kb = logsection(file_path)

    current_dir = os.path.dirname(__file__)
    csv_path = os.path.abspath(os.path.join(current_dir, "../../csv_files/1506tops.csv"))
    well_tops = pd.read_csv(csv_path)

    # print(well_tops.head())

    well_tops_list = []
    for _, row in well_tops.iterrows():
        tops = {}  # creating a dictionary
        for column in well_tops.columns:
            if column == 'UWI':
                continue  # skip non-depth columns

            val = row[column]  # get depth value from current row and column
            if pd.notna(val):
                # Convert depth to subsea by subtracting kb
                ss_val = kb - val
                tops[column] = ss_val  # save ss in tops dict w column name as key

        well_tops_list.append(tops)

    # print(f'well tops list: {well_tops_list}')

    return well_tops_list



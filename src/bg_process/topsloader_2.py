import pandas as pd
from bg_process.logloader_1 import (logsection)


def top_load(file_path):
    """
    This function reads an LAS file and creates a list of all the well tops.

    Return:
        well_tops_list: list of all well tops from an LAS file.
    """
    _, _, _, _, _, _, kb = logsection(file_path)

    well_tops = pd.read_csv(file_path)

    # print(well_tops.head())

    well_tops_list = []
    for _, row in well_tops.iterrows():
        tops = {}  # creating a dictionary
        for column in well_tops.columns:
            if column == 'UWI':
                continue  # skip non-depth columns

            val = row[column]  # get depth value from current row and column
            print(f'val: {val}')
            if pd.notna(val):
                # convert depth to subsea by subtracting kb
                if kb is not None:
                    print(f'kb: {kb}')
                    ss_val = kb - val
                    print(f'ss_val: {ss_val}')
                else:
                    ss_val = 824.1 - val
                tops[column] = ss_val  # save ss in tops dict w column name as key

        well_tops_list.append(tops)

    # print(f'well tops list: {well_tops_list}')

    return well_tops_list



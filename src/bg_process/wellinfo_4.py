import pandas as pd
import os


def horz_loader(horz_path):
    """
    This function reads a CSV file and pulls horizontal well information.
    """
    df_raw = pd.read_csv(os.path.abspath(horz_path))

    df = pd.DataFrame({
        'UWI': df_raw['UWI'],
        'EW': df_raw['eoff'],
        'NS': df_raw['noff'],
        'MD': df_raw['MD'],
        'TVD': df_raw['tvd'],
        'SS': df_raw['ss']
    })

    return df
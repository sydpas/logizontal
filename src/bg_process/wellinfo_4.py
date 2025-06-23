import pandas as pd
import os


def horz_loader():
    """
    This function reads a CSV file and pulls horizontal well information.
    """
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.abspath(os.path.join(current_dir, "../../csv_files/horz_1-7Surv.csv"))
    surv_1_7 = pd.read_csv(csv_path)

    df = pd.DataFrame({
        'UWI': surv_1_7['UWI'],
        'EW': surv_1_7['eoff'],
        'NS': surv_1_7['noff'],
        'MD': surv_1_7['MD'],
        'TVD': surv_1_7['tvd'],
        'SS': surv_1_7['ss']})


    return df
import pandas as pd
import os


def horz_loader(horz_path):
    """
    This function reads a CSV file and pulls horizontal well information.
    """
    with open(os.path.abspath(horz_path), 'r', encoding='ISO-8859-1') as f:
        lines = f.readlines()

    data_start = next(i for i, line in enumerate(lines) if line.strip().startswith('100/'))  # finding UWI column

    print(f'line at data_start: {lines[data_start]}')
    print(f'line after data_start: {lines[data_start + 1]}')

    kb = 824.1
    for line in lines:
        if 'KB ELEVATION' in line:
            kb = float(line.split(':')[1].strip().lstrip(',').strip())
            break

    print(f'kb: {kb}')

    df = pd.read_csv(
        horz_path, skiprows=data_start, encoding='ISO-8859-1', header=None,
        names=['UWI', 'MD', 'INC', 'AZ', 'TVD', 'NS', 'EW'], usecols=range(7))  # manually assigning names
        # usecols to get rid of the "column" after ,

    df['TVD'] = pd.to_numeric(df['TVD'], errors='coerce')
    df['EW'] = pd.to_numeric(df['EW'], errors='coerce')

    df['SS'] = kb - df['TVD']

    print(f'new df header with subsea: {df.head()}')

    return df
import lasio
import os


def logsection(file_path):
    """
    This function reads an LAS file and prints various information.

    Returns:
         columns: length of non_depth_curves list.
         non_depth_curves: list of curves without depth.
         curve_unit_list: list of all curve units excluding depth.
         df: the LAS file converted to a pandas DataFrame.
    """
    las = lasio.read(os.path.abspath(file_path))
    df = las.df()  # converting to pandas dataframe

    df['DEPTH'] = df.index  # adding depth column

    # prints stats
    # print(f'df describe: {df.describe()}')

    non_depth_curves = [
        curve_name.mnemonic for curve_name in las.curves if curve_name.mnemonic != 'DEPT'
            and curve_name.mnemonic in df.columns]
    # removing the DEPT curve

    # making list of units
    curve_unit_list = {curve.mnemonic: curve.unit for curve in las.curves if curve.mnemonic != 'DEPT'}

    columns = len(non_depth_curves)

    loc = las.well.LOC.value if 'LOC' in las.well else None
    comp = las.well.COMP.value if 'COMP' in las.well else None
    kb = las.params['EREF'].value if 'EREF' in las.params else 824.1
    print(f'kb: {kb}')

    # depth to ss
    df['SUBSEA'] = kb - df['DEPTH']
    df[['DEPTH', 'SUBSEA']].reset_index()  # turns depth into normal column

    if 'DT' in df.columns:
        df['DT'] = df['DT'].clip(upper=450)
    else:
        print('no DT!')

    if 'ILD' in df.columns:
        df['ILD'] = df['ILD'].clip(upper=30)
    else:
        print('no ILD!')

    return columns, non_depth_curves, curve_unit_list, df, loc, comp, kb

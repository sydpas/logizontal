from bg_process.logloader_1 import (logsection)

# defining aliases
curve_groups = {
    'col1': [['GR', 'Gamma Ray', None], ['SP', 'Spontaneous Potential', None]],
    'col2': [['ILD', 'Resistivity', None]],
    'col3': [['GR', 'Gamma Ray', None]],
    'col4': [['PE', None], ['RHOB', 'Density', 'Bulk Density', None]],
    'col5': [['DT', 'Delta t', 'Sonic', None], ['DTS', 'Shear Sonic', None]]
}

def organize_curves(file_path):
    """
    This function organizes curves and groups them together for plotting.

    Return:
        ax_list: list of all groups of curves.
        col_list:
    """

    # call necessary bg functions
    _, non_depth_curves, _, df, _, _, _ = logsection(file_path)

    # uppercase everything for consistent matching
    non_depth_curves = [c.upper() for c in non_depth_curves]
    df.columns = [c.upper() for c in df.columns]

    ax_list = []
    col_list = []

    for group_name_options in curve_groups.values():
        group = []

        for name_option in group_name_options:
            for name in name_option:
                if isinstance(name, str) and name.upper() in non_depth_curves:
                    group.append((name, df[name]))
                    break
        ax_list.append(group)
        col_list.append(len(group))

    # print(f'ax_list: {ax_list}')
    # print(f'col_list: {col_list}')

    return ax_list, col_list

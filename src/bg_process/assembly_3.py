from bg_process.logloader_1 import (logsection)


def organize_curves(file_path):
    """
    This function organizes curves and groups them together for plotting.

    Return:
        ax_list: list of all groups of curves.
    """

    # call necessary bg functions
    _, non_depth_curves, _, _, _, _, _ = logsection(file_path)

    # # just for knowing the index of all curves
    # for i, curve in enumerate(non_depth_curves, start=0):
    #     print(f'{i}: {curve}')

    # using the non_depth_curves list, we can group accordingly...
    ax1 = [non_depth_curves[2], non_depth_curves[6]]
    col1 = len(ax1)
    ax2 = [non_depth_curves[3]]
    col2 = len(ax2)
    ax3 = [non_depth_curves[2]]
    col3 = len(ax3)
    ax4 = [non_depth_curves[8], non_depth_curves[7]]
    col4 = len(ax4)
    ax5 = [non_depth_curves[1]]
    col5 = len(ax5)


    ax_list = [ax1, ax2, ax3, ax4, ax5]
    col_list = [col1, col2, col3, col4, col5]

    return ax_list, col_list

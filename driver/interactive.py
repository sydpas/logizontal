import sys

from bg_process.logloader_1 import (logsection)
from bg_process.topsloader_2 import (top_load)
from bg_process.assembly_3 import (organize_curves)
from bg_process.wellinfo_4 import (horz_loader)

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas
    )

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QApplication, QToolButton, QFileDialog
)


from PySide6.QtGui import QIcon, QAction, Qt


class WellLogPlotter(FigureCanvas):
    def __init__(self):
        self.fig, self.axes = plt.subplots(1, 1)
        super().__init__(self.fig)

        print('loading data...')
        self.df = None
        self.well_tops_list = None
        self.ax_list = None
        self.col_list = None

        print('calling functions...')

        # for the tops button
        self.show_tops = True  # have tops on
        self.tops_lines_list = []  # empty list to fill with tops


        # plotting horizontal well
        self.plot_horizontal_well()

    def title_box(self, file_path):
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = logsection(file_path)
        horz_df = horz_loader()

        uwi_title = horz_df['UWI'][0]
        title_text = f'Horizontal Well ({uwi_title}) on {loc} for {comp}\n+{kb:.2f} m'

        self.setText(title_text)
        self.setAlignment(Qt.AlignCenter)  # issue but it works
        self.setStyleSheet("""
            QLabel {background-color: #9ad1d4; color: black; font-weight: bold; font-size: 14px; padding: 2px;
                border: 2px solid #80ced7; border-radius: 4px;
            }""")

    def plotting_logs(self, file_path):
        """
        This function plots the logs.
        """
        print(f'plotting logs function starting...')
        global current_ax
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = logsection(file_path)
        self.df = df
        well_tops_list = top_load(file_path)
        ax_list, col_list = organize_curves(file_path)

        self.fig.clear()
        self.axes = self.fig.subplots(1, len(ax_list), sharey = True,
                                      gridspec_kw={'width_ratios': [1, 2, 1, 2, 2]})
        self.fig.subplots_adjust(bottom=0.15)  # increase margins to prevent overlap
        # subplots: gridbased, good for shared axes

        shade_list = ['#0c63e7', '#4c956c', '#f77f00']
        curve_counter = 0

        for i, (curves, ax) in enumerate(zip(ax_list, self.axes)):  # zip pairs up elements from 2 lists and brings them together
            ax = self.axes[i]
            top = well_tops_list[0]

            print(f'Plotting curve(s): {curves}...')

            for horz, depth in top.items():
                if pd.notna(depth):
                    y = float(depth)
                    line = ax.axhline(y=y, color='red', lw=1, ls='-')  # tops
                    self.tops_lines_list.append(line) # add lines to the list
                    if i == 0:
                        top_name = ax.text(x=0, y=y - 5, s=horz, color='red', fontsize=5, ha='right', va='center')
                        self.tops_lines_list.append(top_name)  # add top names to the list

            ax2 = ax.twiny()
            # unit labels
            ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True, labeltop=False,
                           labelsize=6)
            ax2.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True,
                            labelsize=6)

            # take away y just to use the horz ss well
            ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)
            ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)
            ax.set_ylabel('')
            ax2.set_ylabel('')

            for j, curve in enumerate(curves):
                unit = curve_unit_list.get(curve, '')
                print(f'Plotting curve: {curve}...')
                print(f'The unit for {curve} is {unit}')

                if curve == 'GR':
                    df.plot(
                        x=curve, y='SUBSEA', color='black', ax=ax,
                        linewidth=0.5, marker='o', markersize=0.1, alpha=0.4, label='GR')
                    ax.fill_betweenx(df['SUBSEA'], df[curve], 75, facecolor='#ffc300', alpha=0.5)
                    ax.fill_betweenx(df['SUBSEA'], df[curve], 0, facecolor='white')
                    ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)

                else:
                    shade = shade_list[curve_counter % len(shade_list)]
                    curve_counter += 1
                    # print(f'Shade for {curve}: {shade}')

                    next_ax = ax2 if j != 0 and ax2 else ax
                    df.plot(
                        x=curve, y='SUBSEA', color=shade, ax=next_ax,
                        linewidth=0.5, marker='o', markersize=0.1, alpha=0.4, label=curve)

                if j != 0:
                    ax2.set_xlabel(f'{curve} ({unit})', fontsize=5, labelpad=4, fontstyle='italic')

                else:
                    ax.set_xlabel(f'{curve} ({unit})', fontsize=5, labelpad=4, fontstyle='italic')

            # adjusting proper y limits
            ax.set_ylim(df['SUBSEA'].min(), df['SUBSEA'].max())

            # ... and x limits
            ax.set_xlim(df[curves[0]].min(), df[curves[0]].max())
            if ax2:
                ax2.set_xlim(df[curves[-1]].min(), df[curves[-1]].max())

            # combining the legends and putting bottom left
            if ax2:
                lines_1, labels_1 = ax.get_legend_handles_labels()
                lines_2, labels_2 = ax2.get_legend_handles_labels()
                ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower left', fontsize=6)
                ax2.get_legend().remove() if ax2.get_legend() else None

            ax.set_title(' and '.join(curves), fontsize=12, pad=8)

            ax.minorticks_on()
            ax.tick_params(axis='y', which='minor', labelsize=0)  # hide minor tick labels
            ax.yaxis.grid(True, which='both', linestyle='-', alpha=0.5, linewidth=0.5)
            ax.xaxis.grid(True, which='both', linestyle='-', alpha=0.5, linewidth=0.5)

        print('re-drawing logs...')
        self.draw()

    def toggle_tops(self):
        self.show_tops = not self.show_tops
        for pair in self.tops_lines_list:
            pair.set_visible(self.show_tops)
        self.draw()


    def plot_horizontal_well(self):
        """
        This function creates a horizontal well overlay on top of the previous well logs.
        """
        horz_df = horz_loader()

        # create an overlay axis, will have to fix width and height
        self.horz_well_axes = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey=self.axes)  # l b width height
        self.horz_well_axes.set_navigate(False)

        # make transparent background
        self.horz_well_axes.patch.set_alpha(0)

        # get rid of window outline
        for spine in self.horz_well_axes.spines.values():
            spine.set_alpha(0)

        # x axis
        self.horz_well_axes.set_xlabel('E-W Offset', labelpad=15)
        self.horz_well_axes.set_xticks([])

        # y axis label
        self.horz_well_axes.set_ylabel('Subsea (m)', color='darkblue', labelpad=10, size=8)
        self.horz_well_axes.yaxis.set_label_position('right')
        self.horz_well_axes.yaxis.label.set_rotation(270)

        # y axis ticks
        self.horz_well_axes.yaxis.set_ticks_position('right')
        self.horz_well_axes.tick_params(axis='y', labelsize=8, colors='darkblue', length=3)

        xmin, xmax = horz_df['EW'].min(), horz_df['EW'].max()
        self.horz_well_axes.set_xlim(xmin, xmax)

        # sea level line
        self.horz_well_axes.axhline(0, 0, 1, color='#3a506b', lw=1.5, ls='--', alpha=0.6,
                                    label='Sea Level')

        for i in range(1, len(horz_df['SS'].values)):
            if horz_df['SS'].values[i-1] - horz_df['SS'].values[i] <= 0.8:
                constant = horz_df['SS'].values[i]
                self.horz_well_axes.axhline(constant, 0, 1, color='#4A3728', lw=1.5, ls='-', alpha=0.8,
                                            label='Constant')
                # print(f'constant: {constant}')
                break

        self.horz_well_axes.plot(
                horz_df['EW'], horz_df['SS'],  # x, y
                color='#371D10', label='Horizontal Well')

        self.horz_well_axes.legend(loc='upper right', fontsize=7)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        print('creating window...')
        self.setWindowTitle("LogiZontal")
        self.setGeometry(100, 100, 800, 1100)  # width, height

        print('adding file button to menu...')
        # for the file menu
        open_file = QAction('Open LAS file', self)
        open_file.triggered.connect(self.load_las_file)
        file_menu = self.menuBar().addMenu('Files')
        file_menu.addAction(open_file)

        print('going to well log plotter...')
        self.well_plot = WellLogPlotter()

        # for the tops
        self.toggle_button = QToolButton()
        self.toggle_button.setText('Toggle Tops')
        self.toggle_button.clicked.connect(self.well_plot.toggle_tops)
        self.toggle_button.setAutoRaise(False)
        # styling the button
        self.toggle_button.setStyleSheet("""
        QToolButton {background-color: #d00000; color: white; font: bold 12px; border: 2px white; border-radius: 4px;
            padding: 4px;
        }

        QToolButton:hover {background-color: #9d0208; color: white; font: bold 12px; border: 2px white; 
            border-radius: 4px; padding: 4px;
        }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(10,10,10,10)

        # layout.addWidget(self.toggle_button)
        layout.addWidget(self.well_plot)

        # 'wrap' everything
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def load_las_file(self):
        print('loading las file...')
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setNameFilter('LAS (*.las)')
        if dialog.exec():  # if user clicks okay
            fileName = dialog.selectedFiles() # grabs file
            print(f'chose file {fileName}...')
            for file in fileName:
                self.well_plot.plotting_logs(file)
                print(f'plotting file {file}...')
                print('applying title...')
                # self.title_box = TitleBox(file)
                print('title was applied!')


def main():
    try:
        img = Image.open('C:/Users/sydne/git/rvgs/qtpractice_rvgs_test/icon/lgz.png')
        img.save('C:/Users/sydne/git/rvgs/qtpractice_rvgs_test/icon/lgz.ico', format='ICO', sizes=[
            (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
        ])
        print('png-ico conversion worked...')
    except Exception as e:
        print(f'conversion did not work! {e}')

    app = QApplication(sys.argv)
    icon_path = 'C:/Users/sydne/git/rvgs/qtpractice_rvgs_test/icon/lgz.ico'

    app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.setWindowIcon(QIcon(icon_path))  # if not working, ctrl shift esp and restart windows expl
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
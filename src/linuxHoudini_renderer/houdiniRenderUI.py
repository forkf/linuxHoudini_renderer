"""This is main script file which set ups UI for houdini rendering.
# Author: Mehul Joshi
# Project: Linux Houdini Renderer
# Description : It's an application which render your hip file without opening Houdini UI.
"""

import os
import sys

from PySide2.QtWidgets import (QApplication, QComboBox, QFileDialog, QHBoxLayout,
                               QLabel, QLineEdit, QListWidget, QMessageBox, QPushButton,
                               QVBoxLayout, QWidget)
from PySide2.QtCore import QProcess

from src.linuxHoudini_renderer import utility
from src.linuxHoudini_renderer.constants import LOGGER


class HouRender(QWidget):
    """Setup main-ui for houdini rendering."""

    def __init__(self, parent=None):
        """Initialize UI"""
        super(HouRender, self).__init__(parent)
        self.setGeometry(10, 10, 700, 400)
        self.setWindowTitle("Offline Houdini Render")

        self.out_process = QProcess(self)

        # Adding Layouts in Main UI
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Adding Layouts in UI Layout
        self.config_layout = QHBoxLayout()
        self.layout.addLayout(self.config_layout)
        self.path_layout = QHBoxLayout()
        self.layout.addLayout(self.path_layout)
        self.node_layout = QHBoxLayout()
        self.layout.addLayout(self.node_layout)

        # Adding Widgets Here
        self.config_label = QLabel('Houdini Install Dir.')
        self.config_line = QLineEdit()
        self.config_button = QPushButton('Locate')
        self.config_layout.addWidget(self.config_label)
        self.config_layout.addWidget(self.config_line)
        self.config_layout.addWidget(self.config_button)

        self.label_hip_file = QLabel('Hip File')
        self.line_hip_file = QLineEdit()
        self.line_hip_file.setPlaceholderText('Enter HIP File Path')
        self.button_browse_hip = QPushButton('Browse')
        self.path_layout.addWidget(self.label_hip_file)
        self.path_layout.addWidget(self.line_hip_file)
        self.path_layout.addWidget(self.button_browse_hip)

        self.button_analyse = QPushButton('Analyse')
        self.path_layout.addWidget(self.button_analyse)

        self.label_node = QLabel('Nodes Type')
        self.label_node.setMaximumWidth(80)
        self.combo_node = QComboBox()
        self.node_layout.addWidget(self.label_node)
        self.node_layout.addWidget(self.combo_node)

        self.list_info = QListWidget()
        self.list_info.setMinimumWidth(400)
        self.layout.addWidget(self.list_info)
        self.button_start = QPushButton('Start')
        self.layout.addWidget(self.button_start)

        # Initial Checks
        self.out_nodes = {}
        self.houdini_batch_location = None
        self.hou_location = None
        self.houdini_install_dir = None
        self.render_path = None
        self._initial_checks()

        # CONNECTION OF FUNCTION TO MAIN UI
        self.connect_hou_render()

    def connect_hou_render(self):
        """Setup button connections of UI."""
        self.config_button.clicked.connect(self.re_locate_houdini)
        self.button_browse_hip.clicked.connect(self.browse_file)
        self.button_analyse.clicked.connect(self.run_go)
        self.button_start.clicked.connect(self.run_start)

    def re_locate_houdini(self):
        """Setup application configuration by picking houdini installed directory.        """
        LOGGER.debug('Opening fileBrowser to pick houdini install dir.')
        while True:
            get_directory = utility.pick_houdini_directory()
            if get_directory:
                self.houdini_batch_location = get_directory.get("hbatch_location")
                self.hou_location = get_directory.get("hou_location")

                LOGGER.debug('hbatch found : %s', self.houdini_batch_location)
                self._enable_widgets(switch=True)
                self.houdini_install_dir = get_directory.get("houdini_installed_directory")
                self.config_line.setText(self.houdini_install_dir)
                break
            else:
                continue

    def _initial_checks(self):
        """Perform initials check of UI."""
        LOGGER.debug('Performing initial checks ...')
        checks = utility.check_configs()
        self.hou_location = checks.get("houdini_installed_directory")

        if self.hou_location:
            self.houdini_batch_location = checks.get('hbatch_location')
            self.hou_location = checks.get("hou_location")
            self.houdini_install_dir = checks.get("houdini_installed_directory")
            self._enable_widgets(switch=True)
        else:
            self.re_locate_houdini()
        self.config_line.setText(self.houdini_install_dir)

    def _enable_widgets(self, switch):
        """Enable or Disable UI widgets.

        Args:
            switch (bool): Whether widgets need to be enabled/disabled.
        """
        self.label_hip_file.setEnabled(switch)
        self.button_browse_hip.setEnabled(switch)
        self.button_analyse.setEnabled(switch)
        self.label_node.setEnabled(switch)
        self.combo_node.setEnabled(switch)
        self.list_info.setEnabled(switch)
        self.button_start.setEnabled(switch)

        self.config_line.setDisabled(switch)

    def browse_file(self):
        """Open browser and pick houdini file."""
        _dir = os.getenv('HOME')
        get_file = QFileDialog.getOpenFileNames(
            self,
            'Select .hip File',
            _dir,
            filter='Houdini File(*.hip)'
        )
        self.line_hip_file.setText(str(get_file[0][0]))
        self.line_hip_file.setReadOnly(True)
        self.list_info.clear()
        self.combo_node.clear()

    def run_go(self):
        """Read houdini hip file and fetch mantra nodes."""
        try:
            sys.path.insert(0, self.hou_location)
            import hou
            hip_path = str(self.line_hip_file.text())
            if hip_path == '':
                QMessageBox.information(
                    self,
                    'Information',
                    'Please enter hip file path.'
                )
            else:
                hou.hipFile.load(hip_path, ignore_load_warnings=True)
                node = hou.node('/')
                all_child = node.allSubChildren()
                i = 0
                for each in all_child:
                    if each.type().name() == 'ifd':
                        node_path = each.path()
                        f_start = hou.node(each.path()).parm('f1').eval()
                        f_end = hou.node(each.path()).parm('f2').eval()
                        self.out_nodes[i] = {
                            'NodePath': '',
                            'sFrame': '',
                            'eFrame': '',
                            'out_path': ''
                        }
                        eval_out_path = hou.node(each.path()).parm('vm_picture').eval()
                        self.out_nodes[i]['NodePath'] = node_path
                        self.out_nodes[i]['sFrame'] = f_start
                        self.out_nodes[i]['eFrame'] = f_end
                        self.out_nodes[i]['out_path'] = eval_out_path
                        i = i+1

                sorted(self.out_nodes)
                for each in self.out_nodes:
                    self.combo_node.addItem(self.out_nodes[each]['NodePath'])

        except IOError as msg:
            QMessageBox.critical(self, 'Critical', msg)

    def run_start(self):
        """Perform rendering of file."""
        if self.combo_node.currentText() == '':
            QMessageBox.information(self, 'Information', 'Out node selection is empty.')
        else:
            index = self.combo_node.currentIndex()
            hip_path = str(self.line_hip_file.text())
            render_node = self.out_nodes[index]['NodePath']
            self.render_path = self.out_nodes[index]['out_path']
            render_command = '{} {} -c "render -f {} {} -V {};q"'.format(
                self.houdini_batch_location,
                hip_path,
                self.out_nodes[index]['sFrame'],
                self.out_nodes[index]["eFrame"],
                render_node
            )
            self.list_info.addItem('Rendering : {}'.format(self.render_path))
            self.out_process.start(render_command)
            self.out_process.readyReadStandardOutput.connect(self.handle_std_out)
            self.out_process.readyReadStandardError.connect(self.handle_std_err)

    def handle_std_out(self):
        """Handle stand-out prints."""
        data = self.out_process.readAllStandardOutput().data()
        self.list_info.addItem(data.decode('utf-8'))
        self.list_info.scrollToBottom()

    def handle_std_err(self):
        """Handle stand-out errors."""
        data = self.out_process.readAllStandardError().data()
        self.list_info.addItem(data.decode('utf-8'))
        self.list_info.scrollToBottom()
        # self.textEdit.append(out_process)


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    WIN = HouRender()
    WIN.show()
    APP.exec_()

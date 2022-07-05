# Author: Mehul Joshi
# Project: Linux Houdini Renderer
# Description : It's an application which render your hip file without opening Houdini UI.

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except ImportError:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

import os
import sys


class HouRender(QWidget):
    def __init__(self, parent=None):
        super(HouRender, self).__init__(parent)
        self.setGeometry(10, 10, 700, 400)
        self.setWindowTitle("Offline Houdini Render")

        self.out_process = QProcess(self)
        self.out_nodes = {}

        # Adding Layouts in Main UI
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Adding Layouts in UI Layout
        self.pathLayout = QHBoxLayout()
        self.layout.addLayout(self.pathLayout)
        self.node_layout = QHBoxLayout()
        self.layout.addLayout(self.node_layout)

        # Adding Widgets Here
        self.path_text = QLabel()
        self.path_text.setText('Hip File')
        self.path_field = QLineEdit()
        self.path_field.setPlaceholderText('Enter HIP File Path')
        self.browse_button = QPushButton()
        self.browse_button.setText('Browse')
        self.pathLayout.addWidget(self.path_text)
        self.pathLayout.addWidget(self.path_field)
        self.pathLayout.addWidget(self.browse_button)

        self.go_button = QPushButton()
        self.go_button.setText('Analyse')
        self.pathLayout.addWidget(self.go_button)

        self.node_label = QLabel()
        self.node_label.setText('Nodes Type')
        self.node_label.setMaximumWidth(80)
        self.node_combo = QComboBox()
        self.node_layout.addWidget(self.node_label)
        self.node_layout.addWidget(self.node_combo)

        self.listInfo = QListWidget()
        self.listInfo.setMinimumWidth(400)
        self.layout.addWidget(self.listInfo)
        self.start_button = QPushButton()
        self.start_button.setText('Start')
        self.layout.addWidget(self.start_button)

        # CONNECTION OF FUNCTION TO MAIN UI
        self.connect_hou_render()

    def connect_hou_render(self):
        self.browse_button.clicked.connect(self.browse_file)
        self.go_button.clicked.connect(self.run_go)
        self.start_button.clicked.connect(self.run_start)

    def browse_file(self):
        _dir = os.getenv('HOME')
        get_file = QFileDialog.getOpenFileNames(self, 'Select .hip File', _dir, filter='Houdini File(*.hip)')
        self.path_field.setText(str(get_file[0][0]))
        self.path_field.setReadOnly(True)
        self.listInfo.clear()
        self.node_combo.clear()

    def run_go(self):
        try:
            sys.path.insert(0, '/opt/hfs16.0.557/houdini/python2.7libs/')
            import hou
            hip_path = str(self.path_field.text())
            if hip_path == '':
                QMessageBox.information(self, 'Information', 'Please enter hip file path.')
            else:
                hou.hipFile.load(hip_path)
                node = hou.node('/')
                all_child = node.allSubChildren()
                i = 0
                for each in all_child:
                    if each.type().name() == 'ifd':
                        node_path = each.path()
                        f_start = hou.node(each.path()).parm('f1').eval()
                        f_end = hou.node(each.path()).parm('f2').eval()
                        self.out_nodes[i] = {'NodePath': '', 'sFrame': '', 'eFrame': ''}
                        self.out_nodes[i]['NodePath'] = node_path
                        self.out_nodes[i]['sFrame'] = f_start
                        self.out_nodes[i]['eFrame'] = f_end
                        i = i+1

                sorted(self.out_nodes)
                for each in self.out_nodes:
                    self.node_combo.addItem(self.out_nodes[each]['NodePath'])

        except IOError as msg:
            QMessageBox.critical(self, 'Critical', msg)

    def run_start(self):
        if self.node_combo.currentText() == '':
            QMessageBox.information(self, 'Information', 'Out node selection is empty.')
        else:
            hbatch = '/apps/sidefx/hfs16.0.504/bin/hbatch'  # EXTRA NEED TO REMOVE
            index = self.node_combo.currentIndex()
            hip_path = str(self.path_field.text())
            render_node = self.out_nodes[index]['NodePath']
            render_command = 'hbatch {0} -c "render -f {1} {2} -V {3};q"'.format(
                hip_path,
                self.out_nodes[index]['sFrame'],
                self.out_nodes[index]['eFrame'],
                render_node
            )
            self.out_process.start(render_command)
            self.out_process.readyReadStandardOutput.connect(self.handle_std_out)
            self.out_process.readyReadStandardError.connect(self.handle_std_err)

    def handle_std_out(self):
        data = self.out_process.readAllStandardOutput().data()
        self.listInfo.addItem(data.decode('utf-8'))
        self.listInfo.scrollToBottom()

    def handle_std_err(self):
        data = self.out_process.readAllStandardError().data()
        self.listInfo.addItem(data.decode('utf-8'))
        self.listInfo.scrollToBottom()
        # self.textEdit.append(out_process)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = HouRender()
    win.show()
    app.exec_()

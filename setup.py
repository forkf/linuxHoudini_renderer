import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

build_exe_options = {
    "packages": [
        "PySide2.QtCore.QProcess",
        "PySide2.QtCore.QUrl"
        "PySide2.QtWidgets.QApplication",
        "PySide2.QtWidgets.QComboBox",
        "PySide2.QtWidgets.QFileDialog",
        "PySide2.QtWidgets.QHBoxLayout",
        "PySide2.QtWidgets.QLabel",
        "PySide2.QtWidgets.QLineEdit",
        "PySide2.QtWidgets.QListWidget",
        "PySide2.QtWidgets.QMessageBox",
        "PySide2.QtWidgets.QPushButton",
        "PySide2.QtWidgets.QVBoxLayout",
        "PySide2.QtWidgets.QWidget"
        ],
    "excludes": [],
    "include_files": []
}


setuptools.setup(
    name="linuxHoudini_renderer",
    version="1.0",
    author="Mehul Joshi",
    author_email="forkf.developer@gmail.com",
    description="Package to render hip files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)

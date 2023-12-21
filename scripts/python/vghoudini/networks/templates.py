import os
import hou
from PySide2 import QtWidgets, QtCore

templates = {}


def get_directory() -> str:
    return os.environ['HOUDINI_TEMPLATES_PATH')


def merge_file(name: str) -> None:
    file_name = templates.get(name, name)
    if not file_name:
        return
    _, ext = os.path.splitext(file_name)
    if not ext:
        file_name = file_name + '.hip'
    file_path = os.path.join(get_directory(), file_name)
    if os.path.exists(file_path):
        hou.hipFile.merge(file_path)


class TemplateBrowserWidget(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Templates')
        self.dialog_buttons = QtWidgets.QDialogButtonBox(self)
        self.dialog_buttons.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_buttons.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.dialog_buttons.accepted.connect(self.accept)
        self.dialog_buttons.rejected.connect(self.reject)
        self.template = QtWidgets.QComboBox()
        self.template.setEditable(True)
        self.fill_templates()
        self.set_layout()

    def fill_templates(self):
        dir_path = get_directory()
        if not os.path.isdir(dir_path):
            return
        templates = [os.path.splitext(i) for i in os.listdir(dir_path)]
        self.template.addItems(
            [name for name, ext in templates if ext == '.hip'])

    def set_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout(self)
        form_layout.addRow('Template', self.template)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.dialog_buttons)
        self.setLayout(main_layout)


if hou.isUIAvailable():
    def show_template_browser_dialog():
        dialog = TemplateBrowserWidget()
        result = dialog.exec_()
        if not result:
            return
        template = dialog.template.currentText()
        merge_file(template)

from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import temp_path


class TExceptionDialog(QDialog):

    def __init__(self, exception: str, offset: tuple | None = None):
        super().__init__()
        self.setGeometry(550 + offset[0], 350 + offset[1], 200, 175)
        self.setWindowIcon(QIcon(temp_path.resource_path('assets\\Exception_x.png')))
        self.setWindowTitle('Errore')
        self.setFont(QFont("Segoe UI", 11))

        label = QLabel(exception)
        label.setAlignment(Qt.AlignCenter)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.setCenterButtons(True)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

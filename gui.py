import sys
import time

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal

import TExceptionDialog
import backup
import detect_drives
import get_size
import temp_path


class TMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TrueNAS Backup")
        self.setGeometry(300, 300, 800, 300)
        self.setFixedSize(700, 450)
        self.icon = QIcon(temp_path.resource_path(r'assets/logo.jpg'))
        self.setWindowIcon(self.icon)

        self.drive_list = detect_drives.get_drives()

        self.bar = QProgressBar(self)
        self.bar.setRange(0, 100)
        self.bar.setValue(0)

        self.widget = QLabel()
        self.create_background()

        self.layout = QGridLayout()
        self.create_layout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def create_background(self):
        pixmap = QPixmap(temp_path.resource_path(r'assets/wall_1.jpg'))

        new_pix = QPixmap(pixmap.size())
        overlay_color = QColor(245, 245, 255)
        new_pix.fill(overlay_color)

        painter = QPainter(new_pix)
        painter.setOpacity(0.45)
        painter.drawPixmap(QtCore.QPoint(), pixmap)
        painter.end()

        self.widget.setPixmap(new_pix)
        self.widget.setScaledContents(True)
        self.widget.setFont(QFont('Arial', 12))

    def create_layout(self):
        font1 = QFont("Courier", 11, QFont.Bold)

        label_select_drive = QLabel(self)
        label_select_drive.setText("Scegli il disco su cui effettuare il backup")

        self.box_select_drive = QComboBox(self)
        self.box_select_drive.addItems(self.drive_list)
        self.box_select_drive.setFont(font1)

        label_select_drive.setBuddy(self.box_select_drive)

        label_select_nas = QLabel(self)
        label_select_nas.setText("Scegli l'unità corrispondente al NAS")

        self.box_select_nas = QComboBox(self)
        self.box_select_nas.addItems(self.drive_list)
        self.box_select_nas.setFont(font1)
        label_select_nas.setBuddy(self.box_select_nas)

        self.btn_create_backup = QPushButton(self)
        self.btn_create_backup.setText("Crea BackUp")
        self.btn_create_backup.setMinimumHeight(40)
        self.btn_create_backup.clicked.connect(self.create_backup)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(label_select_drive)
        vbox1.addWidget(self.box_select_drive)
        vbox1.setContentsMargins(10, 10, 10, 30)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(label_select_nas)
        vbox2.addWidget(self.box_select_nas)
        vbox2.setContentsMargins(10, 10, 10, 30)

        true_nas_label = QLabel(self)
        true_nas_pix = QPixmap(temp_path.resource_path(r'assets/wall_4.png'))
        true_nas_pix = true_nas_pix.scaledToHeight(70)
        true_nas_label.setPixmap(true_nas_pix)
        true_nas_label.setScaledContents(True)

        self.label_finished = QLabel(self)
        self.label_finished.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(QLabel(), 0, 0, 1, 4, alignment=Qt.AlignBottom)   # Blank object
        self.layout.addWidget(true_nas_label, 1, 1, 1, 2, alignment=Qt.AlignVCenter)
        self.layout.addWidget(QLabel(), 2, 0, 1, 4, alignment=Qt.AlignBottom)   # Blank object
        self.layout.addLayout(vbox1, 3, 0, 1, 4, alignment=Qt.AlignBottom)
        self.layout.addLayout(vbox2, 4, 0, 1, 4, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.btn_create_backup, 5, 1, 1, 2, alignment=Qt.AlignTop)
        self.layout.addWidget(QLabel(), 6, 0, 1, 4, alignment=Qt.AlignBottom)  # Blank object
        self.layout.addWidget(self.bar, 7, 0, 1, 4, alignment=Qt.AlignBottom)
        self.layout.addWidget(self.label_finished, 8, 1, 1, 2, alignment=Qt.AlignCenter)

    def create_backup(self):
        if self.box_select_drive.currentIndex() == 0 or self.box_select_nas.currentIndex() == 0:
            errmsg = TExceptionDialog.TExceptionDialog("Selezionare un disco valido!")
            errmsg.exec()
            return

        drive_letter = self.box_select_drive.currentText()[0]
        nas_letter = self.box_select_nas.currentText()[0]

        # Actual copying
        self.copy_thread = QThread()
        self.backup_obj = Backup(drive_letter, nas_letter)
        self.backup_obj.moveToThread(self.copy_thread)

        self.backup_obj.error.connect(self.error_dialog)
        self.copy_thread.started.connect(self.backup_obj.run)
        self.backup_obj.finished.connect(self.copy_thread.quit)
        self.backup_obj.finished.connect(self.backup_obj.deleteLater)
        self.copy_thread.finished.connect(self.copy_thread.deleteLater)

        # Progress bar update
        self.progress_thread = QThread()
        self.progress_obj = Backup(drive_letter, nas_letter)
        self.progress_obj.moveToThread(self.progress_thread)

        self.update_progress(0)

        self.progress_obj.error.connect(self.error_dialog)
        self.progress_thread.started.connect(self.progress_obj.update_progress_bar)
        self.progress_obj.finished.connect(self.progress_thread.quit)
        self.progress_obj.finished.connect(self.progress_obj.deleteLater)
        self.progress_thread.finished.connect(self.progress_thread.deleteLater)
        self.progress_obj.progress.connect(self.update_progress)

        self.copy_thread.start()
        self.progress_thread.start()
        self.btn_create_backup.setEnabled(False)

        # todo if file exist, app crash

    def update_progress(self, progress):
        self.bar.setValue(progress)
        if progress == 100:
            self.label_finished.setText("Backup terminato con successo")

    def error_dialog(self, error_msg: str):
        errmsg = TExceptionDialog.TExceptionDialog(error_msg + "\n"
                                                   "Impossibile trovare i percorsi di cui effettuare il backup, "
                                                   "assicurarsi di aver selezionato il NAS correttamente.")
        errmsg.exec()
        self.btn_create_backup.setEnabled(True)


class Backup(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, drive_letter: str, nas_letter: str) -> None:
        super().__init__()
        self.drive_letter = drive_letter
        self.nas_letter = nas_letter

    def run(self):
        try:
            backup.create_backup(self.drive_letter, self.nas_letter)
        except PermissionError as e:
            self.error.emit(repr(e))
        self.finished.emit()

    def update_progress_bar(self):
        try:
            total_data = get_size.nas_size(self.nas_letter)
        except FileNotFoundError as e:
            self.error.emit(repr(e))
            self.finished.emit()
            return
        while True:
            time.sleep(1)
            transferred_data = get_size.disk_size(self.drive_letter)
            self.progress.emit(int((transferred_data / total_data) * 100))
            if transferred_data == total_data:
                print("ended")
                break


app = QApplication(sys.argv)
window = TMainWindow()
window.show()
app.exec()

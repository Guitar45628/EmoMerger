import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTreeWidget, QTreeWidgetItem, QPushButton, QCheckBox, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QAction, QMenu, QDialog
from PyQt5.QtCore import Qt

app_name = "EmoMerger"
app_ver = "0.1 beta"
dev_name = "Guitar45628"

class CSVMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{app_name} V{app_ver}")
        self.setGeometry(100, 100, 800, 600)

        # Create and configure UI elements
        self.initUI()

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Initialize data
        self.file_paths = []

    def initUI(self):
        # Create and configure UI elements
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        drag_drop_layout = QHBoxLayout()
        main_layout.addLayout(drag_drop_layout)

        self.label = QLabel("ลากและวางไฟล์ CSV ที่นี่:")
        drag_drop_layout.addWidget(self.label)

        self.entry = QLineEdit()
        self.entry.setAcceptDrops(True)
        self.entry.setPlaceholderText("ลากไฟล์ CSV มาวางที่นี่")
        drag_drop_layout.addWidget(self.entry)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["No.", "ชื่อไฟล์"])
        self.tree.setColumnWidth(0, 50)
        main_layout.addWidget(self.tree)

        checkboxes_layout = QVBoxLayout()
        main_layout.addLayout(checkboxes_layout)

        self.checkboxes = {}
        endings = ["AK", "AX", "AY", "AZ", "B_", "BI", "BV", "EA", "EL", "EM", "GX", "GY", "GZ", "HR", "MX", "MY", "MZ", "PG", "PI", "PR", "RD", "SA", "SF", "SR", "T1", "TH", "TL"]
        current_hbox = None
        for ending in endings:
            checkbox = QCheckBox(ending)
            checkbox.stateChanged.connect(self.updateFileList)
            self.checkboxes[ending] = checkbox

            if not current_hbox or len(current_hbox) >= 10:
                current_hbox = QHBoxLayout()
                checkboxes_layout.addLayout(current_hbox)

            current_hbox.addWidget(checkbox)

        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        self.delete_button = QPushButton("ลบรายการที่เลือก")
        self.delete_button.clicked.connect(self.deleteSelectedFiles)
        buttons_layout.addWidget(self.delete_button)

        self.merge_button = QPushButton("รวมไฟล์")
        self.merge_button.clicked.connect(self.mergeFiles)
        buttons_layout.addWidget(self.merge_button)

        # Create a menu bar
        menubar = self.menuBar()

        # EmoMerger menu
        emomerger_menu = menubar.addMenu("EmoMerger")

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        emomerger_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        # Fullscreen action
        fullscreen_action = QAction("Fullscreen", self, checkable=True)
        fullscreen_action.triggered.connect(self.toggleFullscreen)
        view_menu.addAction(fullscreen_action)

        # Maximize action
        maximize_action = QAction("Maximize", self, checkable=False)
        maximize_action.triggered.connect(self.toggleMaximize)
        view_menu.addAction(maximize_action)

        # Minimize action
        minimize_action = QAction("Minimize", self, checkable=False)
        minimize_action.triggered.connect(self.toggleMinimize)
        view_menu.addAction(minimize_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAboutDialog)
        help_menu.addAction(about_action)

    def showAboutDialog(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About EmoMerger")
        about_dialog.setFixedSize(300, 150)  # Set the dialog size

        layout = QVBoxLayout()

        # Add application information
        app_label = QLabel(f"EmoMerger Version {app_ver}")
        layout.addWidget(app_label)

        # Add developer information
        developer_label = QLabel(f"Developed by {dev_name}")
        layout.addWidget(developer_label)

        about_dialog.setLayout(layout)
        about_dialog.exec_()

    def toggleFullscreen(self):
        if not self.isFullScreen():
            self.showFullScreen()
        else:
            self.showNormal()

    def toggleMaximize(self):
        if not self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()

    def toggleMinimize(self):
        if not self.isMinimized():
            self.showMinimized()
        else:
            self.showNormal()

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and all(url.isLocalFile() for url in mime_data.urls()):
            event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls() and all(url.isLocalFile() for url in mime_data.urls()):
            file_paths = [url.toLocalFile() for url in mime_data.urls()]
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                if file_name.lower().endswith(tuple("_{}.csv".format(ending.lower()) for ending, checkbox in self.checkboxes.items() if checkbox.isChecked())):
                    self.file_paths.append(file_path)
            self.updateFileList()

    def updateFileList(self):
        self.tree.clear()
        for index, file_name in enumerate(self.file_paths, start=1):
            item = QTreeWidgetItem(self.tree, [str(index), file_name])

    def deleteSelectedFiles(self):
        selected_items = self.tree.selectedItems()
        for item in selected_items:
            file_name = item.text(1)
            self.file_paths.remove(file_name)
            self.tree.invisibleRootItem().removeChild(item)

    def mergeFiles(self):
        if not self.file_paths:
            QMessageBox.warning(self, "Error", "ไม่มีไฟล์ CSV ที่เลือก")
            return

        output_file_name, _ = QFileDialog.getSaveFileName(self, "บันทึกไฟล์ผลลัพธ์", "", "CSV Files (*.csv)")
        if not output_file_name:
            return

        try:
            data_list = []
            for file_path in self.file_paths:
                df = pd.read_csv(file_path)
                selected_columns = ['LocalTimestamp'] + [col for col in df.columns if col in self.checkboxes and self.checkboxes[col].isChecked()]
                df = df[selected_columns]
                data_list.append(df)

            if data_list:
                merged_data = pd.concat(data_list, axis=0, ignore_index=True, sort=False)
                merged_data = merged_data.groupby('LocalTimestamp', as_index=False).agg('sum')
                merged_data.fillna('', inplace=True)
                merged_data.replace(0.0, '', inplace=True)


                merged_data.to_csv(output_file_name, index=False)
                QMessageBox.information(self, "Success", f"รวมข้อมูลเสร็จสิ้น ไฟล์ถูกบันทึกที่ {output_file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"เกิดข้อผิดพลาดในการรวมไฟล์: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = CSVMergerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

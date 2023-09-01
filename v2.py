import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTreeWidget, QTreeWidgetItem, QPushButton, QCheckBox, QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QWidget

class CSVMergerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag and Drop CSV Files")
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

        checkboxes_layout = QHBoxLayout()
        main_layout.addLayout(checkboxes_layout)

        self.checkboxes = {}
        endings = ["AK", "AX", "AY", "AZ", "B_", "BI", "BV", "EA", "EL", "EM", "GX", "GY", "GZ", "HR", "MX", "MY", "MZ", "PG", "PI", "PR", "RD", "SA", "SF", "SR", "T1", "TH", "TL"]
        for ending in endings:
            checkbox = QCheckBox(ending)
            checkbox.stateChanged.connect(self.updateFileList)
            self.checkboxes[ending] = checkbox
            checkboxes_layout.addWidget(checkbox)

        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        self.delete_button = QPushButton("ลบรายการที่เลือก")
        self.delete_button.clicked.connect(self.deleteSelectedFiles)
        buttons_layout.addWidget(self.delete_button)

        self.merge_button = QPushButton("รวมไฟล์")
        self.merge_button.clicked.connect(self.mergeFiles)
        buttons_layout.addWidget(self.merge_button)

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

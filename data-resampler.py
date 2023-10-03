import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QLineEdit
import datetime
import time

class DataResamplerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Resampler')
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        self.listbox = QListWidget(self)
        self.layout.addWidget(self.listbox)

        self.select_file_button = QPushButton('Select CSV File', self)
        self.select_file_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_file_button)

        self.resample_frequency = QLineEdit(self)
        self.resample_frequency.setPlaceholderText('Resample Frequency (seconds)')
        self.layout.addWidget(self.resample_frequency)

        self.resample_button = QPushButton('Resample Data', self)
        self.resample_button.clicked.connect(self.resample_data)
        self.layout.addWidget(self.resample_button)

        self.save_button = QPushButton('Save Result', self)
        self.save_button.clicked.connect(self.save_result)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.selected_file_path = None  # Store the selected file path
        self.resampled_df = None  # Store the resampled DataFrame

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("CSV Files (*.csv)")
        if file_dialog.exec_():
            self.selected_file_path = file_dialog.selectedFiles()[0]
            self.listbox.clear()  # Clear previous selections
            self.listbox.addItem(self.selected_file_path)

    def resample_data(self):
        if self.selected_file_path:
            resample_freq_sec = self.resample_frequency.text()

            try:
                resample_freq_sec = float(resample_freq_sec)
                resample_freq = f'{resample_freq_sec}S'  # Convert to string with 'S' for seconds
            except ValueError:
                print('Please enter a valid resample frequency (in seconds).')
                return

            # Load CSV file and resample data
            df = pd.read_csv(self.selected_file_path)
            df['LocalTimestamp'] = pd.to_datetime(df['LocalTimestamp'], unit='s')  # Convert timestamp to datetime
            df.set_index('LocalTimestamp', inplace=True)  # Set timestamp as index
            self.resampled_df = df.resample(resample_freq).max()
            try:
                self.resample_df['LocalTimestamp'] = time.mktime(self.resample_df['LocalTimestamp'].timetuple())
            except:
                print('failed')
                

            print("Resampled Data:")
            print(self.resampled_df.head())  # Print the first 5 rows

    def save_result(self):
        if self.resampled_df is not None:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Resampled CSV", "", "CSV Files (*.csv)")
            if save_path:
                # Save resampled data to CSV
                self.resampled_df.to_csv(save_path)
                print('Resampled data saved to:', save_path)
        else:
            print('Please select a file to resample.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataResamplerApp()
    window.show()
    sys.exit(app.exec_())

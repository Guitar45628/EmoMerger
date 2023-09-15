import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class DataProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Data Processor')
        
        self.btn_open = QPushButton('Open CSV', self)
        self.btn_open.setGeometry(50, 50, 200, 30)
        self.btn_open.clicked.connect(self.openCSV)

    def openCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if fileName:
            self.processCSV(fileName)

    def processCSV(self, filename):
        # Read CSV
        df = pd.read_csv(filename)

        # Convert 'LocalTimestamp' column to datetime
        df['LocalTimestamp'] = pd.to_datetime(df['LocalTimestamp'])

        # Set 'LocalTimestamp' as index
        df.set_index('LocalTimestamp', inplace=True)

        # Split data into 15-second intervals
        interval = '15S'
        dfs_by_interval = [group for name, group in df.groupby(pd.Grouper(freq=interval))]

        for i, df_interval in enumerate(dfs_by_interval):
            output_filename = f'output_{i}.csv'
            df_interval.to_csv(output_filename)
            print(f'Saved {output_filename}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataProcessorApp()
    window.show()
    sys.exit(app.exec_())

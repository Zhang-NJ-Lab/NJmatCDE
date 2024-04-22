# import sys
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox
# from chemdataextractor import Document
#
# class ChemFormulaExtractor(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setGeometry(100, 100, 400, 200)
#         self.setWindowTitle('Chemical Formula Extractor')
#
#         self.file_path_label = QLabel('CSV File Path:', self)
#         self.file_path_label.setGeometry(20, 20, 100, 20)
#         self.file_path_entry = QLineEdit(self)
#         self.file_path_entry.setGeometry(130, 20, 200, 20)
#         self.browse_button = QPushButton('Browse', self)
#         self.browse_button.setGeometry(340, 20, 50, 20)
#         self.browse_button.clicked.connect(self.select_file)
#
#         self.save_path_label = QLabel('Save Path:', self)
#         self.save_path_label.setGeometry(20, 50, 100, 20)
#         self.save_path_entry = QLineEdit(self)
#         self.save_path_entry.setGeometry(130, 50, 200, 20)
#         self.browse_save_button = QPushButton('Browse', self)
#         self.browse_save_button.setGeometry(340, 50, 50, 20)
#         self.browse_save_button.clicked.connect(self.select_save_path)
#
#         self.process_button = QPushButton('Process CSV', self)
#         self.process_button.setGeometry(150, 100, 100, 30)
#         self.process_button.clicked.connect(self.process_csv)
#
#     def select_file(self):
#         file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
#         self.file_path_entry.setText(file_path)
#
#     def select_save_path(self):
#         save_path = QFileDialog.getExistingDirectory(self, 'Select Save Path')
#         self.save_path_entry.setText(save_path)
#
#     def process_csv(self):
#         input_file = self.file_path_entry.text()
#         output_path = self.save_path_entry.text()
#
#         try:
#             df = pd.read_csv(input_file, encoding='utf-8')
#             df.dropna(inplace=True)  # Drop any rows with NaN values
#             df['Chemical_Formula'] = df.iloc[:, 0].apply(lambda x: self.extract_formula(str(x)))
#             df = df[df['Chemical_Formula'].astype(bool)]  # Keep rows where chemical formula is found
#             output_file = f"{output_path}/processed_data.csv"
#             df.to_csv(output_file, index=False)
#             QMessageBox.information(self, 'Success', 'CSV file processed and saved successfully!')
#         except Exception as e:
#             QMessageBox.critical(self, 'Error', f'An error occurred: {str(e)}')
#
#     def extract_formula(self, text):
#         doc = Document(text)
#         if doc.cems:
#             return '; '.join([cem.text for cem in doc.cems])
#         else:
#             return ''
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = ChemFormulaExtractor()
#     ex.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
import pandas as pd
from chemdataextractor import Document


class ChemExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_label = QLabel("Input CSV File Path:")
        self.file_edit = QLineEdit()
        self.file_button = QPushButton("Browse")
        self.file_button.clicked.connect(self.browse_file)

        self.column_label = QLabel("Name of First Column:")
        self.column_edit = QLineEdit()

        self.output_label = QLabel("Output CSV File Path:")
        self.output_edit = QLineEdit()
        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.browse_output)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_extraction)

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_edit)
        layout.addWidget(self.file_button)
        layout.addWidget(self.column_label)
        layout.addWidget(self.column_edit)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_edit)
        layout.addWidget(self.output_button)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
        self.setWindowTitle("Chemical Extractor")
        self.show()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.file_edit.setText(file_path)

    def browse_output(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)")
        if output_path:
            self.output_edit.setText(output_path)

    def is_chemical(self, entity):
        doc = Document(entity)
        chem_entities = doc.cems
        return len(chem_entities) > 0

    def run_extraction(self):
        input_file = self.file_edit.text()
        column_name = self.column_edit.text()
        output_file = self.output_edit.text()

        try:
            df = pd.read_csv(input_file, encoding='gb18030')
            #df = pd.read_csv(input_file, encoding='utf-8')
            column_data = df[column_name]
            df['Chemical'] = column_data.apply(lambda x: 1 if self.is_chemical(x) else 0)
            df = df[df.iloc[:, -1] != 0]
            df = df.drop(df.columns[-1], axis=1)
            df.to_csv(output_file, index=False)
            QMessageBox.information(self, "Extraction Complete", "Chemical extraction completed successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChemExtractorApp()
    sys.exit(app.exec_())
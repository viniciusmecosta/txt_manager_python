import os
from PyQt5.QtWidgets import QDialog, QLineEdit, QTextEdit, QVBoxLayout, QPushButton

class EditWindow(QDialog):
    def __init__(self, fileName=None):
        super().__init__()
        self.setWindowTitle("Editar Arquivo")
        self.setGeometry(100, 100, 600, 400)

        self.fileName = fileName
        self.fileNameLineEdit = QLineEdit(self.fileName if self.fileName else "")
        self.fileContentTextEdit = QTextEdit()
        self.saveButton = QPushButton("Salvar")

        self.fileNameLineEdit.setStyleSheet("QLineEdit { font-size: 20px; padding: 12px; }")
        self.fileContentTextEdit.setStyleSheet("QTextEdit { font-size: 20px; padding: 12px; }")
        self.saveButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: #d3d3d3;
                color: black;
                font-size: 20px;
                padding: 15px 30px;
            }
            QPushButton:pressed {
                background-color: #a8a8a8;
            }
        """)

        self.fileNameLineEdit.setPlaceholderText("Nome do arquivo")
        self.fileContentTextEdit.setPlaceholderText("Texto do arquivo")

        self.saveButton.clicked.connect(self.save_txt)

        layout = QVBoxLayout()
        layout.addWidget(self.fileNameLineEdit)
        layout.addWidget(self.fileContentTextEdit)
        layout.addWidget(self.saveButton)
        self.setLayout(layout)

        if self.fileName:
            self.load_txt()

    def load_txt(self):
        with open(f'./data/{self.fileName}', 'r') as f:
            self.fileContentTextEdit.setPlainText(f.read())

    def save_txt(self):
        fileName = self.fileNameLineEdit.text()
        if not fileName.endswith('.txt'):
            fileName += '.txt'
        content = self.fileContentTextEdit.toPlainText()
        with open(f'./data/{fileName}', 'w') as f:
            f.write(content)
        self.accept()

    def ensure_unique_filename(self, baseFileName):
        fileName = baseFileName
        fileNumber = 1
        while os.path.exists(f'./data/{fileName}'):
            fileName = f"{baseFileName.rstrip('.txt')}({fileNumber}).txt"
            fileNumber += 1
        return fileName

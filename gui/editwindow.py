import os
from PyQt5.QtWidgets import QDialog, QLineEdit, QTextEdit, QVBoxLayout, QPushButton, QMessageBox


class EditWindow(QDialog):
    def __init__(self, fileName=None):
        super().__init__()
        self.setWindowTitle("Editar Arquivo")
        self.setGeometry(100, 100, 600, 400)

        self.originalFileName = fileName  # Armazena o nome original do arquivo para verificação
        self.fileNameLineEdit = QLineEdit(self.originalFileName if self.originalFileName else "")
        self.fileContentTextEdit = QTextEdit()
        self.saveButton = QPushButton("Salvar")

        self.fileNameLineEdit.setStyleSheet("""
            QLineEdit {
                font-size: 20px;
                padding: 12px;
            }
        """)
        self.fileContentTextEdit.setStyleSheet("""
            QTextEdit {
                font-size: 20px;
                padding: 12px;
            }
        """)
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

        if self.originalFileName:
            self.load_txt()

    def load_txt(self):
        with open(f'./data/{self.originalFileName}', 'r') as f:
            self.fileContentTextEdit.setPlainText(f.read())

    def save_txt(self):
        newFileName = self.fileNameLineEdit.text()
        if not newFileName.endswith('.txt'):
            newFileName += '.txt'
        content = self.fileContentTextEdit.toPlainText()

        newPath = f'./data/{newFileName}'
        originalPath = f'./data/{self.originalFileName}'

        # Se o nome do arquivo foi alterado e o novo nome já existe, mostra um aviso.
        if self.originalFileName != newFileName and os.path.exists(newPath):
            QMessageBox.warning(self, "Erro de Renomeação", "Um arquivo com esse nome já existe.")
            return

        # Renomeia ou cria o arquivo com o novo conteúdo.
        if self.originalFileName and self.originalFileName != newFileName:
            os.rename(originalPath, newPath)
        with open(newPath, 'w') as f:
            f.write(content)

        self.originalFileName = newFileName  # Atualiza o nome original para o novo nome
        self.accept()

    def ensure_unique_filename(self, baseFileName):
        fileName = baseFileName
        fileNumber = 1
        while os.path.exists(f'./data/{fileName}'):
            fileName = f"{baseFileName.rstrip('.txt')}({fileNumber}).txt"
            fileNumber += 1
        return fileName

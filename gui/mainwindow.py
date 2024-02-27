import os
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QMessageBox, QAbstractItemView
from PyQt5.QtCore import pyqtSlot
from gui.editwindow import EditWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciador de Arquivos TXT")
        self.setStyleSheet("""
            QWidget { 
                background-color: #f0f0f0; 
                font-size: 20px;  # Aumento do tamanho da fonte
            }
        """)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Arquivos TXT"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setVisible(True)  # Mantém os números das linhas visíveis
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setStyleSheet("""
            QTableWidget, QHeaderView::section {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                font-size: 18px;  # Aumento do tamanho da fonte na tabela
            }
            QTableWidget::item {
                padding: 12px;
            }
            QHeaderView::section {
                background-color: transparent;  # Remoção da cor do cabeçalho
                padding: 6px;
                border: 2px solid transparent;
                border-radius: 6px;
                font-weight: bold;
            }
            QTableWidget::verticalHeader {
                background-color: transparent;
            }
            QTableWidget::verticalHeader::section {
                background-color: transparent;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #a8a8a8;
            }
        """)
        self.load_txt_files()

        self.createButton = QPushButton("Criar Arquivo de Texto")
        self.editButton = QPushButton("Editar")
        self.deleteButton = QPushButton("Deletar")

        buttonStyle = """
        QPushButton {
            border: 2px solid #8f8f91;
            border-radius: 6px;
            background-color: #d3d3d3;
            color: black;
            font-size: 20px;  # Aumento do tamanho da fonte
            padding: 20px 40px;  # Aumento do padding para botões maiores
            margin: 20px;  # Aumento do espaço entre os botões
        }
        QPushButton:pressed {
            background-color: #a8a8a8;
        }
        """

        self.createButton.setStyleSheet(buttonStyle)
        self.editButton.setStyleSheet(buttonStyle)
        self.deleteButton.setStyleSheet(buttonStyle)

        # Inicialmente desabilita os botões de editar e deletar até que um item seja selecionado
        self.editButton.setEnabled(False)
        self.deleteButton.setEnabled(False)

        self.createButton.clicked.connect(self.create_txt)
        self.editButton.clicked.connect(self.edit_txt)
        self.deleteButton.clicked.connect(self.delete_txt)

        # Conecta o sinal de item selecionado e desselecionado para habilitar/desabilitar botões
        self.tableWidget.itemSelectionChanged.connect(self.toggle_edit_delete_buttons)

        self.tableWidget.itemDoubleClicked.connect(self.edit_txt)

        buttonsLayout = QVBoxLayout()
        buttonsLayout.addWidget(self.createButton)
        buttonsLayout.addWidget(self.editButton)
        buttonsLayout.addWidget(self.deleteButton)
        buttonsLayout.addStretch()

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.tableWidget, 7)
        mainLayout.addLayout(buttonsLayout, 3)

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def load_txt_files(self):
        path = './data'
        files = [f for f in os.listdir(path) if f.endswith('.txt')]
        self.tableWidget.setRowCount(len(files))
        for i, file in enumerate(files):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(file))

    @pyqtSlot()
    def create_txt(self):
        self.editWindow = EditWindow()
        self.editWindow.accepted.connect(self.reload_files)
        self.editWindow.show()

    @pyqtSlot()
    def edit_txt(self):
        selected = self.tableWidget.currentRow()
        if selected >= 0:
            fileName = self.tableWidget.item(selected, 0).text()
            self.editWindow = EditWindow(fileName)
            self.editWindow.accepted.connect(self.reload_files)
            self.editWindow.show()

    @pyqtSlot()
    def delete_txt(self):
        selected = self.tableWidget.currentRow()
        if selected >= 0:
            fileName = self.tableWidget.item(selected, 0).text()
            confirm = QMessageBox.question(self, 'Deletar Arquivo', f'Tem certeza que deseja deletar "{fileName}"?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                os.remove(f'./data/{fileName}')
                self.reload_files()
        else:
            QMessageBox.warning(self, 'Seleção Necessária', 'Por favor, selecione um arquivo para deletar.', QMessageBox.Ok)

    def toggle_edit_delete_buttons(self):
        # Habilita ou desabilita os botões com base na seleção atual
        hasSelection = self.tableWidget.selectionModel().hasSelection()
        self.editButton.setEnabled(hasSelection)
        self.deleteButton.setEnabled(hasSelection)

    def reload_files(self):
        self.load_txt_files()

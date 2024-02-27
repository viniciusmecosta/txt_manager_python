import sys
from PyQt5.QtWidgets import QApplication
from gui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()  # Maximiza a janela principal
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

import sys
from PyQt5.QtWidgets import QApplication
from ui.login import LoginScreen

def main():
    app = QApplication(sys.argv)
    login_screen = LoginScreen()
    login_screen.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    

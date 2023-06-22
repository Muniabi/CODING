import os
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet


class PasswordManager(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Менеджер паролей"
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Оформление
        self.setStyleSheet("background: black, gray")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.label_site = QLabel("Сайт:")
        self.grid.addWidget(self.label_site, 0, 0)
        self.input_site = QLineEdit()
        self.grid.addWidget(self.input_site, 0, 1)

        self.label_username = QLabel("Имя пользователя:")
        self.grid.addWidget(self.label_username, 1, 0)
        self.input_username = QLineEdit()
        self.grid.addWidget(self.input_username, 1, 1)

        self.label_password = QLabel("Пароль:")
        self.grid.addWidget(self.label_password, 2, 0)
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        self.grid.addWidget(self.input_password, 2, 1)

        self.button_save = QPushButton("Сохранить")
        self.button_save.clicked.connect(self.save_password)
        self.grid.addWidget(self.button_save, 3, 0)

        self.button_delete = QPushButton("Удалить пароль")
        self.button_delete.clicked.connect(self.delete_password)
        self.grid.addWidget(self.button_delete, 3, 1)

        self.button_show = QPushButton("Показать пароли")
        self.button_show.clicked.connect(self.show_passwords)
        self.grid.addWidget(self.button_show, 4, 1)

        self.show()

    def save_password(self):
        site = self.input_site.text()
        username = self.input_username.text()
        password = self.input_password.text()

        if site and username and password:
            key = Fernet.generate_key()
            f = Fernet(key)
            encrypted_password = f.encrypt(password.encode())

            with open("passwords.txt", "a") as file:
                file.write(
                    f"{site},{username},{encrypted_password.decode()},{key.decode()}\n"
                )

            self.input_site.setText("")
            self.input_username.setText("")
            self.input_password.setText("")

            QMessageBox.information(self, "Успех", "Пароль сохранен")

        else:
            QMessageBox.warning(self, "Внимание", "Заполните все поля")

    def show_passwords(self):
        try:
            password_file = open("passwords.txt", "r")
            passwords = password_file.readlines()
            password_file.close()

            message = ""
            for password in passwords:
                site, username, encrypted_password, key = password.split(",")
                f = Fernet(key.encode())
                decrypted_password = f.decrypt(encrypted_password.encode())
                message += f"Сайт: {site}, Имя пользователя: {username}, Пароль: {decrypted_password.decode()}\n"

            QMessageBox.information(self, "Созраненные пароли", message)

        except FileNotFoundError:
            QMessageBox.warning(self, "Ощибка", "Файл с паролями не найден")

    def delete_password(self):
        site = self.input_site.text()
        username = self.input_username.text()

        if site and username:
            if os.path.isfile("passwords.txt"):
                with open("passwords.txt", "r") as file:
                    lines = file.readlines()
                with open("passwords.txt", "w") as file:
                    for line in lines:
                        site_, username_, _ = line.strip().split(",")
                        if site != site_ and username != username_:
                            file.write(line)
                self.input_site.setText("")
                self.input_username.setText("")
                self.input_password.setText("")

                QMessageBox.information(self, "Успешно", "Пароль удален")
            else:
                QMessageBox.warning(self, "Ошибка", "Файл не существует")
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля")

        # Проверка успешности операции записи в файл
        with open("passwords.txt") as file:
            if not any(line.strip() for line in file):
                os.remove("passwords.txt")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    password_manager = PasswordManager()
    sys.exit(app.exec_())

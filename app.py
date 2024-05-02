from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random
import string

app: Flask = Flask(__name__)
socketio: SocketIO = SocketIO(app)


class PasswordGenerator:
    """Класс для генерации случайных паролей.

    Атрибуты:
        length (int): Длина сгенерированного пароля (по умолчанию 12).
        include_lowercase (bool): Флаг, указывающий на включение строчных букв (по умолчанию True).
        include_uppercase (bool): Флаг, указывающий на включение заглавных букв (по умолчанию True).
        include_numbers (bool): Флаг, указывающий на включение цифр (по умолчанию True).
        include_special_chars (bool): Флаг, указывающий на включение специальных символов (по умолчанию True).

    Методы:
        generate_password: Генерирует случайный пароль на основе указанных критериев.
    """

    def __init__(self, length: int = 12, include_lowercase: bool = True, include_uppercase: bool = True, include_numbers: bool = True, include_special_chars: bool = True) -> None:
        self.length: int = length
        self.include_lowercase: bool = include_lowercase
        self.include_uppercase: bool = include_uppercase
        self.include_numbers: bool = include_numbers
        self.include_special_chars: bool = include_special_chars

    def generate_password(self) -> str:
        """Генерирует случайный пароль на основе указанных критериев.

        Возвращает:
            str: Сгенерированный пароль.
        """
        characters: str = ''

        if self.include_lowercase:
            characters += string.ascii_lowercase
        if self.include_uppercase:
            characters += string.ascii_uppercase
        if self.include_numbers:
            characters += string.digits
        if self.include_special_chars:
            characters += string.punctuation

        if not (self.include_numbers or self.include_uppercase or self.include_lowercase or self.include_special_chars):
            characters = string.ascii_letters + string.digits + string.punctuation

        password: str = ''.join(random.choices(characters, k=self.length))
        return password


@app.route('/')
def index() -> str:
    """Рендерит главную страницу."""
    return render_template('index.html')


@socketio.on('generate_password')
def generate_password(data: dict) -> None:
    """Генерирует пароль на основе введённых пользователем данных.

    Аргументы:
        data (dict): Словарь, содержащий данные, введённые пользователем.

    Сгенерированный пароль отправляется обратно на клиент.
    """

    length: int = int(data['length'])
    include_lowercase: bool = data.get('include_lowercase', True)
    include_uppercase: bool = data.get('include_uppercase', True)
    include_numbers: bool = data.get('include_numbers', True)
    include_special_chars: bool = data.get('include_special_chars', True)

    generator: PasswordGenerator = PasswordGenerator(
        length=length,
        include_lowercase=include_lowercase,
        include_uppercase=include_uppercase,
        include_numbers=include_numbers,
        include_special_chars=include_special_chars
    )
    password: str = generator.generate_password()
    emit('password_generated', {'password': password})


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)

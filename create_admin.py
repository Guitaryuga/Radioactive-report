from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db
from webapp.models import User

app = create_app()

"""Создание первого пользователя с правами администратора"""

with app.app_context():
    username = input('Username: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password1 = getpass('Password: ')
    password2 = getpass('Repeat the password: ')
    if not password1 == password2:
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Admin created with id {}'.format(new_user.id))

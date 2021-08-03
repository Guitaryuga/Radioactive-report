def test_admin_login_process(test_client, admin_login):
    """Тест логина аккаунта администратора.
    Должны ПРИСУТСТВОВАТЬ элементы меню, доступные только администратору:
    Create user, Control panel, приветствие Welcome, admin!
    """
    response = admin_login
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'success' in response.data
    assert b'Welcome, admin!' in response.data
    assert b'Control panel' in response.data
    assert b'Create report' in response.data
    assert b'Create user' in response.data


def test_user_login_process(test_client, user_login):
    """Тест логина аккаунта пользователя.
    Должны ОТСУТСТВОВАТЬ элементы меню, доступные администратору и дозиметристу:
    Create user, Control panel, Create report, приветствие Welcome, user!
    """
    response = user_login
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'success' in response.data
    assert b'Welcome, user!' in response.data
    assert b'Search' in response.data
    assert b'Control panel' not in response.data
    assert b'Create report' not in response.data
    assert b'Create user' not in response.data


def test_dosimetrist_login_process(test_client, dosimetrist_login):
    """Тест логина аккаунта дозиметриста.
    Должны ПРИСУТСТВОВАТЬ элементы меню, доступные дозиметристу:
    Create report, приветствие Welcome, dosimetrist!
    """
    response = dosimetrist_login
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'success' in response.data
    assert b'Welcome, dosimetrist!' in response.data
    assert b'Search' in response.data
    assert b'Administration system' not in response.data
    assert b'Create report' in response.data
    assert b'Create user' not in response.data


def test_login_invalid_login(test_client):
    """Тест процесса логина с неверным username
    Должно происходить перенаправление страницу логина с алертом - danger"""
    response = test_client.post('process-login', data=dict(username='admeeen', password='admin123'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_login_invalid_password(test_client):
    """Тест процесса логина с неверным паролем
    Должно происходить перенаправление страницу логина с алертом - danger"""
    response = test_client.post('process-login', data=dict(username='admin', password='0123456'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_admin_logout(test_client, admin_login):
    """Тест процесса логаута из аккаунта администратора
    Должно просиходить перенаправление на страницу логина с алертом - success"""
    response = test_client.get('logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'success' in response.data


def test_user_logout(test_client, user_login):
    """Тест процесса логаута из аккаунта пользователя
    Должно просиходить перенаправление на страницу логина с алертом - success"""
    response = test_client.get('logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'success' in response.data


def test_dosimetrist_logout(test_client, dosimetrist_login):
    """Тест процесса логаута из аккаунта дозиметриста
    Должно просиходить перенаправление на страницу логина с алертом - success"""
    response = test_client.get('logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'success' in response.data

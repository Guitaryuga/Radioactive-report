def test_report_generation_without_auth(test_client):
    """Тест генерации PDF отчета без авторизации.
    Должно происходить перенаправление на страницу логина, алерт - danger"""
    response = test_client.get('report_generation/2021-05-17_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_admin_report_generation(test_client, admin_login):
    """Тест генерации PDF отчета администратором.
    Проверка, транслируется ли PDF inline"""
    response = test_client.get('report_generation/2021-05-17_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'PDF' in response.data


def test_dosimetrist_report_generation(test_client, dosimetrist_login):
    """Тест генерации PDF отчета дозиметристом.
    Проверка, транслируется ли PDF inline"""
    response = test_client.get('report_generation/2021-05-17_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'PDF' in response.data


def test_user_report_generation(test_client, user_login):
    """Тест генерации PDF отчета пользователем(user).
    Проверка, транслируется ли PDF inline"""
    response = test_client.get('report_generation/2021-05-17_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'PDF' in response.data


def test_report_creation_and_generation(test_client, admin_login, report_creation_complete):
    """Тест создания и генерации PDF отчета администратором.
    Проверка, транслируется ли PDF inline"""
    response = test_client.get('report_generation/2021-07-29_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'PDF' in response.data


def test_report_creation_and_generation_image(test_client, admin_login, report_with_image):
    """Тест создания и генерации PDF отчета с изображением администратором.
    Проверка, транслируется ли PDF inline"""
    response = test_client.get('report_generation/2021-07-29_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'PDF' in response.data

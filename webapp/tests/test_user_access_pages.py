def test_user_login_page(test_client, user_login):
    """Тест доступа страницы логина из аккаунта пользователя(user)
    Должен происходить редирект на главную страницу поиска отчетов,
    так как авторизация выполнена"""
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data


def test_user_control_panel(test_client, user_login):
    """Тест доступа админки из аккаунта пользователя(user)
    Должен происходить редирект на главную страницу поиска очтетов,
    алерт - danger, эта страница недоступна для пользователя.
    """
    response = test_client.get('admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'danger' in response.data


def test_user_creation(test_client, user_login):
    """Тест доступа к созданию учетных записей из аккаунта пользователя(user)
    Должен происходить редирект на главную страницу поиска очтетов,
    алерт - danger, эта страница недоступна для пользователя.
    """
    response = test_client.get('user_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'danger' in response.data


def test_user_report_creation(test_client, user_login):
    """Тест доступа к созданию отчетов из аккаунта пользователя(user)
    Должен происходить редирект на главную страницу поиска очтетов,
    алерт - danger, эта страница недоступна для пользователя.
    """
    response = test_client.get('report_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'danger' in response.data


def test_user_reports(test_client, user_login):
    """Тест доступа к странице поиска отчетов из аккаунта пользователя(user)
    Должно отражаться название страницы - Search reports"""
    response = test_client.get('reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data


def test_user_all_reports(test_client, user_login):
    """Тест доступа к странице ВСЕХ отчетов из аккаунта пользователя(user)
    В случае доступа должно отражаться название страницы - Search reports"""
    response = test_client.get('reports/all', follow_redirects=True)
    assert response.status_code == 200
    assert b'All reports' in response.data


def test_user_report(test_client, user_login):
    """Тест доступа к странице конкретного отчета из аккаунта пользователя(user)
    Должен происходить редирект на главную страницу поиска очтетов,
    алерт - danger, эта страница недоступна для пользователя.
    """
    response = test_client.get('reports/2021-05-17_X.7_N123', follow_redirects=True)
    assert b'Search reports' in response.data
    assert b'danger' in response.data


def test_user_uploads(test_client, user_login):
    """Тест доступа к изображениям, загруженным на сервер"""
    response = test_client.get('uploads/test_one.jpg', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' not in response.data


def test_user_import(test_client, user_login):
    """Тест доступа к странице импорта excel-файлов для БД.
    Доступна только администратору, идет перенаправление на главную."""
    response = test_client.get('/import', follow_redirects=True)
    assert response.status_code == 200
    assert b'Import data' not in response.data
    assert b'Search report' in response.data


def test_user_export_reports(test_client, user_login):
    """Тест доступа к экспорту отчетов в excel-формате
    Доступ есть только у администратора, идет перенаправление на главную."""
    response = test_client.get('/export_reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search report' in response.data


def test_user_export_db(test_client, user_login):
    """Тест доступа к экспорту БД в excel-формате
    Доступ есть только у администратора, идет перенаправление на главную."""
    response = test_client.get('export_db', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search report' in response.data


def test_user_excel_tables_download(test_client, user_login):
    """Тест доступа к возможности загрузки excel-шаблона.
    Данная ссылка должна быть доступна и работать только у администратора."""
    response = test_client.get('/xlsx/db_input_blank.xlsx', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search report' in response.data
    assert b'danger' in response.data

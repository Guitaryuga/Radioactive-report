def test_login_page_without_auth(test_client):
    """Тест доступа к странице логина без авторизации.
    Страница должна быть доступна, но без элементов меню,
    доступных авторизованным пользователям"""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'Search' not in response.data
    assert b'Create report' not in response.data
    assert b'Create user' not in response.data
    assert b'Administration system' not in response.data


def test_admin_without_auth(test_client):
    """Тест доступа к админке без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Home - Admin' not in response.data
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_search_page_without_auth(test_client):
    """Тест доступа к странице поиска отчетов без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_report_page_without_auth(test_client):
    """Тест доступа к странице отчета без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('reports/2021-05-17_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_all_reports_page_without_auth(test_client):
    """Тест доступа к странице со всеми отчетами без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('reports/all', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_user_creation_without_auth(test_client):
    """Тест доступа к странице создания пользователей без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('user_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_report_creation_page_without_auth(test_client):
    """Тест доступа к странице создания отчета без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('report_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_uploads_without_auth(test_client):
    """Тест доступа к загруженному на сервер изображению без авторизации.
    Должно происходить перенаправление на страницу логина
    и алерт - danger"""
    response = test_client.get('uploads/20-456-2.jpg', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_import_without_auth(test_client):
    """Тест доступа к странице импорта excel-файлов для БД без авторизации.
    Должно происходить перенаправление на страницу логина и алерт - danger."""
    response = test_client.get('/import', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_export_reports_without_auth(test_client):
    """Тест доступа к экспорту отчетов в excel-формате без авторизации.
    Должно происходить перенаправление на страницу логина и алерт - danger."""
    response = test_client.get('/export_reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_export_db_without_auth(test_client):
    """Тест доступа к экспорту БД в excel-формате без авторизации.
    Должно происходить перенаправление на страницу логина и алерт - danger."""
    response = test_client.get('export_db', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data


def test_excel_tables_download_without_auth(test_client):
    """Тест доступа к возможности загрузки excel-шаблона без авторизации.
    Должно происходить перенаправление на страницу логина и алерт - danger."""
    response = test_client.get('/admin/xlsxadmin/db_input_blank.xlsx', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' in response.data
    assert b'danger' in response.data

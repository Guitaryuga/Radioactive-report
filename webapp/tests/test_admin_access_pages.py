def test_admin_login_page(test_client, admin_login):
    """Тест доступа к странице логина из аккаунта администратора.
    Так как администратор авторизован в системе, его должно перенаправить
    на страницу с отчетами.
    В случае доступа должно отражаться название страницы - Search reports.
    """
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data


def test_admin_control_panel(test_client, admin_login):
    """Тест доступа к админке из аккаунта администратора.
    В случае доступа должно отражаться название страницы - Home - Admin.
    """
    response = test_client.get('admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Home - Admin' in response.data


def test_admin_user_creation(test_client, admin_login):
    """Тест доступа к странице создания пользователей из аккаунта администратора.
    В случае доступа должно отражаться название страницы - User creation.
    Данная страинца доступна ТОЛЬКО администраторам.
    """
    response = test_client.get('user_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'User creation' in response.data


def test_admin_report_creation(test_client, admin_login):
    """Тест доступа к странице создания отчетов из аккаунта администратора.
    В случае доступа должно отражаться название страницы - Report creation.
    Данная страница доступна только администраторам и дозиметристам.
    """
    response = test_client.get('report_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Report creation' in response.data


def test_admin_reports(test_client, admin_login):
    """Тест доступа к странице поиска отчетов из аккаунта администратора.
    В случае доступа должно отражаться название страницы - Search reports
    """
    response = test_client.get('reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'Show all' in response.data


def test_admin_all_reports(test_client, admin_login):
    """Тест доступа к сводке со ВСЕМИ отчетами из аккаунта администратора.
    В случае доступа должно отражаться название страницы - All reports.
    Также на странице должен отражаться элемент Status, видимый только
    администраторам и дозиметристам.
    """
    response = test_client.get('reports/all', follow_redirects=True)
    assert response.status_code == 200
    assert b'All reports' in response.data
    assert b'Status' in response.data
    assert b'complete' in response.data
    assert b'incomplete' in response.data


def test_admin_report(test_client, admin_login):
    """Тест доступа к конкретному отчету(сводке) из аккаунта администратора.
    В случае доступа должно отражаться название страницы:
    Report (Дата отчета_Код источника_Серийный номер источника)
    """
    response = test_client.get('reports/2021-05-17_X.7_N123', follow_redirects=True)
    assert response.status_code == 200
    assert b'Report 2021-05-17_X.7_N123' in response.data
    assert b'Generate report' in response.data
    assert b'NET CPM' in response.data


def test_admin_uploads(test_client, admin_login):
    """Тест доступа к загруженным на сервер изображениям из аккаунта администратора
    При наличии доступа, не должно быть перенаправления на главную страницу."""
    response = test_client.get('uploads/test_one.jpg', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' not in response.data


def test_admin_import(test_client, admin_login):
    """Тест доступа к странице импорта excel-файлов для БД.
    Доступна только администратору."""
    response = test_client.get('/import', follow_redirects=True)
    assert response.status_code == 200
    assert b'Import data' in response.data


def test_admin_export_reports(test_client, admin_login):
    """Тест доступа к экспорту отчетов в excel-формате
    Доступ есть только у администратора, должно начаться скачивание файла,
    перенапраления на главную страницу нет."""
    response = test_client.get('/export_reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search report' not in response.data


def test_admin_export_db(test_client, admin_login):
    """Тест доступа к экспорту БД в excel-формате
    Доступ есть только у администратора, должно начаться скачивание файла,
    перенапраления на главную страницу нет."""
    response = test_client.get('export_db', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search report' not in response.data


def test_admin_excel_tables_download(test_client, admin_login):
    """Тест доступа к возможности загрузки excel-шаблона.
    Данная ссылка должна быть доступна и работать только у администратора."""
    response = test_client.get('/xlsx/db_input_blank.xlsx', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search report' not in response.data

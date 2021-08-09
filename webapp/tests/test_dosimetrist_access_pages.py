def test_dosimetrist_login_page(test_client, dosimetrist_login):
    """Тест доступа к странице логина из аккаунта дозиметриста.
    Так как дозиметрист авторизован в системе, его должно перенаправить
    на страницу с отчетами.
    В случае доступа должно отражаться название страницы - Search reports.
    """
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data


def test_dosimetrist_control_panel(test_client, dosimetrist_login):
    """Тест доступа к админке из аккаунта дозиметриста.
    Доступ к ней есть только у администратора, поэтому должно быть перенаправление на
    главную и алерт с предупреждением - danger.
    """
    response = test_client.get('admin', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'danger' in response.data


def test_dosimetrist_user_creation(test_client, dosimetrist_login):
    """Тест доступа к странице создания пользователей из аккаунта дозиметриста.
    Доступ к ней есть только у администратора, поэтому должно быть перенаправление на
    главную и алерт с предупреждением - danger.
    """
    response = test_client.get('user_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'danger' in response.data


def test_dosimetrist_report_creation(test_client, dosimetrist_login):
    """Тест доступа к странице создания отчетов из аккаунта дозиметриста.
    В случае доступа должно отражаться название страницы - Report creation.
    """
    response = test_client.get('report_creation', follow_redirects=True)
    assert response.status_code == 200
    assert b'Report creation' in response.data


def test_dosimetrist_reports(test_client, dosimetrist_login):
    """Тест доступа к странице поиска отчетов из аккаунта дозиметриста.
    В случае доступа должно отражаться название страницы - Search reports
    """
    response = test_client.get('reports', follow_redirects=True)
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'Show all' in response.data


def test_dosimetrist_all_reports(test_client, dosimetrist_login):
    """Тест доступа к сводке со ВСЕМИ отчетами из аккаунта дозиметриста.
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


def test_dosimetrist_report(test_client, dosimetrist_login):
    """Тест доступа к конкретному отчету(сводке) из аккаунта дозиметриста.
    В случае доступа должно отражаться название страницы:
    Report (Дата отчета_Код источника_Серийный номер источника)
    """
    response = test_client.get('reports/2021-05-17_X.7_N123', follow_redirects=True)
    assert b'Report 2021-05-17_X.7_N123' in response.data
    assert b'Generate report' in response.data
    assert b'NET CPM' in response.data


def test_dosimetrist_uploads(test_client, dosimetrist_login):
    """Тест доступа к загруженным на сервер изображениям из аккаунта дозиметриста.
    При наличии доступа, не должно быть перенаправления на главную страницу."""
    response = test_client.get('uploads/test_one.jpg', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login page' not in response.data

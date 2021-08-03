def test_create_admin_report(test_client, admin_login, report_creation_complete):
    """Тест создания полного отчета из аккаунта администратора без приложения файла.
    Должно осуществляться перенаправление на страницу отчета, алерт - success"""
    response = report_creation_complete
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Search' in response.data
    assert b'Show all' in response.data
    assert b'Report 2021-07-29_X.7_N123' in response.data
    assert b'Generate report' in response.data
    assert b'A6321' in response.data
    assert b'Source code' in response.data
    assert b'Isotope' in response.data
    assert b'Activity' in response.data
    assert b'Customer' in response.data
    assert b'NET CPM' in response.data
    assert b'test@example.com' in response.data
    assert b'No files attached' in response.data


def test_create_admin_incomplete_report(test_client, admin_login, report_creation_incomplete):
    """Тест создания неполного отчета из аккаунта администратора без приложения файла.
    Должно осуществляться перенаправление на страницу отчета, алерт - success"""
    response = report_creation_incomplete
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Search' in response.data
    assert b'Show all' in response.data
    assert b'Report 2021-07-29_X.7_N123' in response.data
    assert b'None' in response.data
    assert b'A6321' in response.data
    assert b'Source code' in response.data
    assert b'Isotope' in response.data
    assert b'Activity' in response.data
    assert b'Customer' in response.data
    assert b'NET CPM' in response.data
    assert b'test@example.com' in response.data
    assert b'No files attached' in response.data


def test_admin_report_creation_with_file(test_client, admin_login, report_with_image):
    """Тест создания отчета из аккаунта администратора c приложением файла.
    Должно осуществляться перенаправление на страницу отчета, алерт - success,
    ссылка на изображение на сервере должна быть на странице."""
    response = report_with_image
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Report 2021-07-29_X.7_N123' in response.data
    assert b'Test report with file' in response.data
    assert b'/uploads/20-321-3.jpg' in response.data
    assert b'No files attached' not in response.data


def test_admin_report_creation_with_file_too_big(test_client, admin_login, report_with_heavy_image):
    """Тест создания отчета из аккаунта администратора c приложением файла > 5МБ.
    Перенаправления нет, пользователь остаетя на странице создания отчета, алерт - danger"""
    response = report_with_heavy_image
    assert response.status_code == 200
    assert b'danger' in response.data
    assert b'Report creation' in response.data


def test_create_dosimetrist_complete_report(test_client, dosimetrist_login, report_creation_complete):
    """Тест создания полного отчета из аккаунта дозиметриста без приложения файла.
    Должно осуществляться перенаправление на страницу отчета, алерт - success"""
    response = report_creation_complete
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Search' in response.data
    assert b'Show all' in response.data
    assert b'Report 2021-07-29_X.7_N123' in response.data
    assert b'Generate report' in response.data
    assert b'A6321' in response.data
    assert b'Source code' in response.data
    assert b'Isotope' in response.data
    assert b'Activity' in response.data
    assert b'Customer' in response.data
    assert b'NET CPM' in response.data
    assert b'test@example.com' in response.data
    assert b'No files attached' in response.data


def test_create_dosimetrist_incomplete_report(test_client, dosimetrist_login, report_creation_incomplete):
    """Тест создания неполного отчета из аккаунта дозиметриста без приложения файла.
    Должно осуществляться перенаправление на страницу отчета, алерт - success"""
    response = report_creation_incomplete
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Search' in response.data
    assert b'Show all' in response.data
    assert b'Report 2021-07-29_X.7_N123' in response.data
    assert b'None' in response.data
    assert b'A6321' in response.data
    assert b'Source code' in response.data
    assert b'Isotope' in response.data
    assert b'Activity' in response.data
    assert b'Customer' in response.data
    assert b'NET CPM' in response.data
    assert b'test@example.com' in response.data
    assert b'No files attached' in response.data


def test_dosimetrist_report_creation_with_file(test_client, dosimetrist_login, report_with_image):
    """Тест создания отчета из аккаунта дозиметриста c приложением файла.
    Должно осуществляться перенаправление на страницу отчета, алерт - success,
    ссылка на изображение на сервере должна быть на странице."""
    response = report_with_image
    assert response.status_code == 200
    assert b'success' in response.data
    assert b'Report 2021-07-29_X.7_N123' in response.data
    assert b'Test report with file' in response.data
    assert b'/uploads/20-321-3.jpg' in response.data
    assert b'No files attached' not in response.data


def test_dosimetrist_report_creation_with_file_too_big(test_client, dosimetrist_login, report_with_heavy_image):
    """Тест создания отчета из аккаунта дозиметриста c приложением файла > 5МБ.
    Перенаправления нет, пользователь остаетя на странице создания отчета, алерт - danger"""
    response = report_with_heavy_image
    assert response.status_code == 200
    assert b'danger' in response.data
    assert b'Report creation' in response.data


def test_user_report_creation(test_client, user_login, report_creation_complete):
    """Тест создания отчета из аккаунта пользователя(user)
    Перенаправление на страницу поиска очтетов, алерт - danger,
    поскольку пользователю недоступен функционал создания отчетов"""
    response = report_creation_complete
    assert response.status_code == 200
    assert b'danger' in response.data
    assert b'Search reports' in response.data

def test_excel_import(test_client, admin_login, import_start_db):
    """Тест импорта данных из файла с полной стартовой БД. Доступен только администратору,
    в случае успеха происходит перенаправление на главную страницу, алерт - success."""
    response = import_start_db
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'success' in response.data


def test_excel_import_blank(test_client, admin_login, import_blank_input):
    """Тест импорта данных из файла с частичной БД или пустой. Доступен только администратору,
    в случае успеха происходит перенаправление на главную страницу, алерт - success. """
    response = import_blank_input
    assert response.status_code == 200
    assert b'Search reports' in response.data
    assert b'success' in response.data


def test_empty_file_field(test_client, admin_login, empty_file_field):
    """Тест попытки загрузки без приложенного файла. Доступно только администратору,
    возвращает на страницу импорта, появляется предупреждение, алерт - danger."""
    response = empty_file_field
    assert response.status_code == 200
    assert b'Import data' in response.data
    assert b'danger' in response.data


def test_unsupported_format(test_client, admin_login, import_unsupported_format):
    """Тест попытки загрузки файла неподдерживаемого формата.Доступно только администратору,
    возвращает на страницу импорта, появляется предупреждение, алерт - danger."""
    response = import_unsupported_format
    assert response.status_code == 200
    assert b'Import data' in response.data
    assert b'danger' in response.data

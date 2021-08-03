def test_user_search_report_number(test_client, user_login):
    """Тест поиска отчета пользователем по номеру отчета
    На странице появляется список со значениями
    Report №, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='20/321-1'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-1' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-17' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' not in response.data


def test_user_search_source_serial_number(test_client, user_login):
    """Тест поиска отчета пользователем по серийному номеру источника
    На странице появляется список со значениями
    Report №, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='N123'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-1' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-17' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' not in response.data


def test_dosimetrist_search_report_number_complete(test_client, dosimetrist_login):
    """Тест поиска полного отчета дозиметристом по номеру отчета
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='20/321-1'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-1' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-17' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'complete' in response.data


def test_dosimetrist_search_report_number_incomplete(test_client, dosimetrist_login):
    """Тест поиска неполного отчета дозиметристом по номеру отчета
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='20/321-2'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-2' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-10' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'incomplete' in response.data


def test_dosimetrist_search_source_serial_number(test_client, dosimetrist_login):
    """Тест поиска нескольких отчетов дозиметристом по одинаковому серийному номеру источника
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='N123'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-1' in response.data
    assert b'20/321-2' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-17' in response.data
    assert b'2021-05-10' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'complete' in response.data
    assert b'incomplete' in response.data


def test_admin_search_report_number_complete(test_client, admin_login):
    """Тест поиска полного отчета администратором по номеру отчета
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='20/321-1'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-1' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-17' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'complete' in response.data


def test_admin_search_report_number_incomplete(test_client, admin_login):
    """Тест поиска неполного отчета администратором по номеру отчета
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='20/321-2'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-2' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-10' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'incomplete' in response.data


def test_admin_search_source_serial_number(test_client, admin_login):
    """Тест поиска нескольких отчетов администратором по одинаковому серийному номеру источника
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='N123'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-1' in response.data
    assert b'20/321-2' in response.data
    assert b'Report date' in response.data
    assert b'2021-05-17' in response.data
    assert b'2021-05-10' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'complete' in response.data
    assert b'incomplete' in response.data


def test_admin_search_fresh_report(test_client, admin_login, report_creation_complete):
    """Тест поиска нового созданного отчета администратором по номеру отчета
    На странице появляется список со значениями
    Report №, Status, Report date, Source serial №, Source code"""
    response = test_client.post('reports', data=dict(report_field='20/321-3'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Report' in response.data
    assert b'20/321-3' in response.data
    assert b'Report date' in response.data
    assert b'2021-07-29' in response.data
    assert b'Source serial' in response.data
    assert b'N123' in response.data
    assert b'Source code' in response.data
    assert b'X.7' in response.data
    assert b'Status' in response.data
    assert b'complete' in response.data

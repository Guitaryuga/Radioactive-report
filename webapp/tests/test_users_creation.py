def test_user_creation(test_client, admin_login):
    """Тест создания учетной записи пользователя из аккаунта администратора
    Должно отображаться название страницы - Report creation, алерт при успехе - success"""
    response = test_client.post('user_creation', data=dict(username='newcomer', password='Intel', password2='Intel',
                                                           role='user'), follow_redirects=True)
    assert response.status_code == 200
    assert b'User creation' in response.data
    assert b'success' in response.data


def test_dosimetrist_creation(test_client, admin_login):
    """Тест создания учетной записи дозиметриста из аккаунта администратора
    Должно отображаться название страницы - Report creation, алерт при успехе - success"""
    response = test_client.post('user_creation', data=dict(username='newcomer', password='Intel', password2='Intel',
                                                           role='dosimetrist'), follow_redirects=True)
    assert response.status_code == 200
    assert b'User creation' in response.data
    assert b'success' in response.data

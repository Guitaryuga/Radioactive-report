import os
import pytest

from datetime import date
from werkzeug.datastructures import FileStorage
from webapp import create_app
from webapp.models import (db, User, Report, TaskAndPlace, SourceCode, Isotope, Activity, WipedObjects,
                           Devices, Customer, Documents, QuartalNumber, MicroCiLimit)
from webapp.testing_data import extracting_data


@pytest.fixture
def test_client(scope='module'):
    flask_app = create_app({'TESTING': True})

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            extracting_data()
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def new_user():
    user = User(id='2', username='demouser', password='example', role='user')
    return user


@pytest.fixture(scope='module')
def new_dosimetrist():
    dosimetrist = User(id='2', username='demodos', password='exampletoo', role='dosimetrist')
    return dosimetrist


@pytest.fixture(scope='module')
def new_report():
    report = Report(id='1', report_number='20/321-1', status='complete', report_path='2021-05-17_X.7_N123',
                    report_date='2021-05-17', customer='ООО «ТопНефтеГаз»', customer_eng='LLC «TopNefteGas»',
                    task_and_place='Анализ, Москва', task_and_place_eng='Analasys, Moscow',
                    source_code='X.7', source_code_eng='X.7', isotope='Цезий-137', isotope_eng='Cs-137',
                    activity='7,4 ГБк (0,2 Кюри)', activity_eng='7,4 GBq (0,2 Ci)', efficiency=0.95,
                    source_serial_number='N123', wiped_object='Плотномер', wiped_object_eng='Densitometer',
                    wiped_serial_number='N123', wipe_date='2021-05-18', bkg_cpm=15, gross_cpm=19,
                    net_cpm=4, removable_activity_micro_ci='1.897e-06', removable_activity_bq='7.019e-02',
                    limit_micro_ci='5.000e-03', device='Дозиметр', device_eng='Dosimeter', bill_for='CoolCompany',
                    email='test@example.com', ike_recieved='2021-05-17', results_sent='2021-05-17',
                    days_for_analasys=0, comments='Test with no image attached',
                    bill='bill', photo_link='No file attached')
    return report


@pytest.fixture(scope='module')
def new_task_and_place():
    task_and_place = TaskAndPlace(rus='Анализ, Москва', eng='Analasys, Moscow')
    return task_and_place


@pytest.fixture(scope='module')
def new_source_code():
    source_code = SourceCode(rus='X.7', eng='X.7', isotope_id='1', activity_id='1',
                             efficiency=0.95)
    return source_code


@pytest.fixture(scope='module')
def new_isotope():
    isotope = Isotope(rus='Цезий-137', eng='Cs-137')
    return isotope


@pytest.fixture(scope='module')
def new_activity():
    activity = Activity(rus='7,4 ГБк (0,2 Кюри)', eng='7,4 GBq (0,2 Ci)')
    return activity


@pytest.fixture(scope='module')
def new_wiped_objects():
    wiped_objects = WipedObjects(rus='Плотномер', eng='Densitometer')
    return wiped_objects


@pytest.fixture(scope='module')
def new_devices():
    devices = Devices(rus='Дозиметр', eng='Dosimeter')
    return devices


@pytest.fixture(scope='module')
def new_customer():
    customer = Customer(rus='ООО «ТопНефтеГаз»', eng='LLC «TopNefteGas»')
    return customer


@pytest.fixture(scope='module')
def new_documents():
    documents = Documents(rus='Лицензия №1 от 21.03.2018', eng='License #1 from 21/03/2018')
    return documents


@pytest.fixture(scope='module')
def new_quartal_number():
    quartal = QuartalNumber(quartal='20/325')
    return quartal


@pytest.fixture(scope='module')
def new_micro_ci_limit():
    micro_ci_limit = MicroCiLimit(id='1', micro_ci_limit='5.000e-03')
    return micro_ci_limit


@pytest.fixture
def admin_login(test_client):
    return test_client.post('process-login', data=dict(username='admin', password='admin123'),
                            follow_redirects=True)


@pytest.fixture
def user_login(test_client):
    return test_client.post('process-login', data=dict(username='user', password='example123'),
                            follow_redirects=True)


@pytest.fixture
def dosimetrist_login(test_client):
    return test_client.post('process-login', data=dict(username='dosimetrist', password='demodos'),
                            follow_redirects=True)


@pytest.fixture
def user_creation(test_client):
    return test_client.post('user_creation', data=dict(username='newcomer', password='Intel', password2='Intel',
                                                       role='user'))


@pytest.fixture
def report_creation_complete(test_client):
    return test_client.post('report_creation', data=dict(date=date(2021, 7, 29), customer=1, task_and_place=1,
                                                         source_code=1, source_serial_number='N123', wiped_object=1,
                                                         wiped_serial_number='A6321', wipe_date=date(2021, 7, 10),
                                                         bkg_cpm=12, gross_cpm=20, device=1, bill_for='That company',
                                                         email='test@example.com', ike_recieved=date(2021, 7, 28),
                                                         results_sent=date(2021, 7, 27),
                                                         foto=FileStorage(filename='',
                                                                          content_type='application/octet-stream'),
                                                         bill='1456-7895', comments='Test report without file'),
                            content_type="multipart/form-data", follow_redirects=True)


@pytest.fixture
def report_creation_incomplete(test_client):
    return test_client.post('report_creation', data=dict(date=date(2021, 7, 29), customer=1, task_and_place=1,
                                                         source_code=1, source_serial_number='N123', wiped_object=1,
                                                         wiped_serial_number='A6321', wipe_date=date(2021, 7, 10),
                                                         gross_cpm=20, device=1, bill_for='That company',
                                                         email='test@example.com', ike_recieved=date(2021, 7, 28),
                                                         results_sent=date(2021, 7, 27),
                                                         foto=FileStorage(filename='',
                                                                          content_type='application/octet-stream'),
                                                         bill='1456-7895', comments='Test report without file'),
                            content_type="multipart/form-data", follow_redirects=True)


@pytest.fixture
def report_with_image(test_client):
    my_file = os.path.join('webapp/tests/test_small.jpg')
    return test_client.post('report_creation', data=dict(date=date(2021, 7, 29), customer=1, task_and_place=1,
                                                         source_code=1, source_serial_number='N123', wiped_object=1,
                                                         wiped_serial_number='A6321', wipe_date=date(2021, 7, 10),
                                                         bkg_cpm=12, gross_cpm=20, device=1, bill_for='That company',
                                                         email='test@example.com', ike_recieved=date(2021, 7, 28),
                                                         results_sent=date(2021, 7, 27),
                                                         foto=FileStorage(stream=open(my_file, 'rb'),
                                                                          filename='test_small.jpg',
                                                                          content_type='application/octet-stream'),
                                                         bill='1456-7895', comments='Test report with file'),
                            content_type="multipart/form-data", follow_redirects=True)


@pytest.fixture
def report_with_heavy_image(test_client):
    my_file = os.path.join('webapp/tests/test_big.jpg')
    return test_client.post('report_creation', data=dict(date=date(2021, 7, 29), customer=1, task_and_place=1,
                                                         source_code=1, source_serial_number='N123', wiped_object=1,
                                                         wiped_serial_number='A6321', wipe_date=date(2021, 7, 10),
                                                         bkg_cpm=12, gross_cpm=20, device=1, bill_for='That company',
                                                         email='test@example.com', ike_recieved=date(2021, 7, 28),
                                                         results_sent=date(2021, 7, 27),
                                                         foto=FileStorage(stream=open(my_file, 'rb'),
                                                                          filename='test_big.jpg',
                                                                          content_type='application/octet-stream'),
                                                         bill='1456-7895', comments='Test report with file'),
                            content_type="multipart/form-data", follow_redirects=True)


@pytest.fixture
def import_start_db(test_client):
    my_file = os.path.join('webapp/xlsx/db_start_version.xlsx')
    return test_client.post('/import', data=dict(file=FileStorage(stream=open(my_file, 'rb'),
                                                                  filename='db_start_version.xlsx',
                                                                  content_type='application/octet-stream')),
                            follow_redirects=True)


@pytest.fixture
def import_blank_input(test_client):
    my_file = os.path.join('webapp/xlsx/db_input_blank.xlsx')
    return test_client.post('/import', data=dict(file=FileStorage(stream=open(my_file, 'rb'),
                                                                  filename='db_input_blank.xlsx',
                                                                  content_type='application/octet-stream')),
                            follow_redirects=True)


@pytest.fixture
def empty_file_field(test_client):
    return test_client.post('/import', data=dict(file=FileStorage(filename='',
                                                                  content_type='application/octet-stream')),
                            follow_redirects=True)


@pytest.fixture
def import_unsupported_format(test_client):
    my_file = os.path.join('webapp/tests/test_small.jpg')
    return test_client.post('/import', data=dict(file=FileStorage(stream=open(my_file, 'rb'),
                                                                  filename='test_small.jpg',
                                                                  content_type='application/octet-stream')),
                            follow_redirects=True)

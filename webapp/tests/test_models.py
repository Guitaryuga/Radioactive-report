def test_new_user(new_user):
    assert new_user.id == '2'
    assert new_user.username == 'demouser'
    assert new_user.check_password != 'example'
    assert new_user.role == 'user'


def test_new_dosimetrist(new_dosimetrist):
    assert new_dosimetrist.id == '2'
    assert new_dosimetrist.username == 'demodos'
    assert new_dosimetrist.check_password != 'exampletoo'
    assert new_dosimetrist.role == 'dosimetrist'


def test_new_report(new_report):
    assert new_report.id == '1'
    assert new_report.report_number == '20/321-1'
    assert new_report.status == 'complete'
    assert new_report.report_path == '2021-05-17_X.7_N123'
    assert new_report.report_date == '2021-05-17'
    assert new_report.customer == 'ООО «ТопНефтеГаз»'
    assert new_report.customer_eng == 'LLC «TopNefteGas»'
    assert new_report.task_and_place == 'Анализ, Москва'
    assert new_report.task_and_place_eng == 'Analasys, Moscow'
    assert new_report.source_code == 'X.7'
    assert new_report.source_code_eng == 'X.7'
    assert new_report.isotope == 'Цезий-137'
    assert new_report.isotope_eng == 'Cs-137'
    assert new_report.activity == '7,4 ГБк (0,2 Кюри)'
    assert new_report.activity_eng == '7,4 GBq (0,2 Ci)'
    assert new_report.efficiency == 0.95
    assert new_report.source_serial_number == 'N123'
    assert new_report.wiped_object == 'Плотномер'
    assert new_report.wiped_object_eng == 'Densitometer'
    assert new_report.wiped_serial_number == 'N123'
    assert new_report.wipe_date == '2021-05-18'
    assert new_report.bkg_cpm == 15
    assert new_report.gross_cpm == 19
    assert new_report.net_cpm == 4
    assert new_report.removable_activity_micro_ci == '1.897e-06'
    assert new_report.removable_activity_bq == '7.019e-02'
    assert new_report.limit_micro_ci == '5.000e-03'
    assert new_report.device == 'Дозиметр'
    assert new_report.device_eng == 'Dosimeter'
    assert new_report.bill_for == 'CoolCompany'
    assert new_report.email == 'test@example.com'
    assert new_report.ike_recieved == '2021-05-17'
    assert new_report.results_sent == '2021-05-17'
    assert new_report.days_for_analasys == 0
    assert new_report.comments == 'Test with no image attached'
    assert new_report.bill == 'bill'
    assert new_report.photo_link == 'No file attached'


def test_new_task_and_place(new_task_and_place):
    assert new_task_and_place.rus == 'Анализ, Москва'
    assert new_task_and_place.eng == 'Analasys, Moscow'


def test_new_source_code(new_source_code):
    assert new_source_code.rus == 'X.7'
    assert new_source_code.eng == 'X.7'
    assert new_source_code.isotope_id == '1'
    assert new_source_code.activity_id == '1'
    assert new_source_code.efficiency == 0.95


def test_new_isotope(new_isotope):
    assert new_isotope.rus == 'Цезий-137'
    assert new_isotope.eng == 'Cs-137'


def test_new_activity(new_activity):
    assert new_activity.rus == '7,4 ГБк (0,2 Кюри)'
    assert new_activity.eng == '7,4 GBq (0,2 Ci)'


def test_new_wiped_objects(new_wiped_objects):
    assert new_wiped_objects.rus == 'Плотномер'
    assert new_wiped_objects.eng == 'Densitometer'


def test_new_devices(new_devices):
    assert new_devices.rus == 'Дозиметр'
    assert new_devices.eng == 'Dosimeter'


def test_new_customer(new_customer):
    assert new_customer.rus == 'ООО «ТопНефтеГаз»'
    assert new_customer.eng == 'LLC «TopNefteGas»'


def test_new_documents(new_documents):
    assert new_documents.rus == 'Лицензия №1 от 21.03.2018'
    assert new_documents.eng == 'License #1 from 21/03/2018'


def test_new_qurtal_number(new_quartal_number):
    assert new_quartal_number.quartal == '20/325'


def test_new_micro_ci_limit(new_micro_ci_limit):
    assert new_micro_ci_limit.id == '1'
    assert new_micro_ci_limit.micro_ci_limit == '5.000e-03'

from datetime import date
from webapp.models import Report, db, User, TaskAndPlace, Isotope, Activity, SourceCode, WipedObjects, Devices, Customer, QuartalNumber, MicroCiLimit


users = [{'username': 'admin', 'password': 'admin123', 'role': 'admin'},
         {'username': 'user', 'password': 'example123', 'role': 'user'},
         {'username': 'dosimetrist', 'password': 'demodos', 'role': 'dosimetrist'}]


reports = [{'report_number': '20/321-1', 'status': 'complete', 'source_code': 'X.7', 'source_serial_number': 'N123',
            'report_date': date(2021, 5, 17), 'wipe_date': date(2021, 5, 17), 'report_path': '2021-05-17_X.7_N123',
            'photo_link': 'No file attached'},
           {'report_number': '20/321-2', 'status': 'incomplete', 'source_code': 'X.7', 'source_serial_number': 'N123',
            'report_date': date(2021, 5, 10), 'wipe_date': date(2021, 5, 8), 'report_path': '2021-05-10_X.7_N123',
            'photo_link': 'No file attached'}]


task_and_places = [{'rus': 'Анализ, Москва', 'eng': 'Analasys, Moscow'}]

source_codes = [{'rus': 'X.7', 'eng': 'X.7', 'isotope_id': 1, 'activity_id': 1, 'efficiency': 0.95}]

isotopes = [{'rus': 'Цезий-137', 'eng': 'Cs-137'}]

activities = [{'rus': '7,4 ГБк (0,2 Кюри)', 'eng': '7,4 GBq (0,2 Ci)'}]

wiped_objects = [{'rus': 'Плотномер', 'eng': 'Densitometer'}]

devices = [{'rus': 'Дозиметр', 'eng': 'Densitometer'}]

customers = [{'rus': 'ООО «ТопНефтеГаз»', 'eng': 'LLC «TopNefteGas»'}]

quartal_number = [{'quartal': '20/321'}]

micro_ci_limit = [{'micro_ci_limit': '5.000e-03'}]


def save_users(username, password, role):
    """Функция записи информации из словаря users в БД """
    new_user = User(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()


def save_reports(report_number, source_code, source_serial_number, report_date, wipe_date, report_path, status, photo_link):
    new_report = Report(report_number=report_number, source_code=source_code, source_serial_number=source_serial_number,
                        report_date=report_date, wipe_date=wipe_date, report_path=report_path, status=status,
                        photo_link=photo_link)
    new_report.math_probe_freq(15, 20)
    d1 = date(2021, 5, 17)
    d2 = date(2021, 5, 19)
    new_report.days_for_analasys_func(d1, d2)
    new_report.removable_activity_ci_func(None, 0.95)
    new_report.removable_activity_bq_func(None)
    db.session.add(new_report)
    db.session.commit()


def save_task_and_places(rus, eng):
    new_task_and_place = TaskAndPlace(rus=rus, eng=eng)
    db.session.add(new_task_and_place)
    db.session.commit()


def save_isotopes(rus, eng):
    new_isotope = Isotope(rus=rus, eng=eng)
    db.session.add(new_isotope)
    db.session.commit()


def save_activities(rus, eng):
    new_activity = Activity(rus=rus, eng=eng)
    db.session.add(new_activity)
    db.session.commit()


def save_source_codes(rus, eng, isotope_id, activity_id, efficiency):
    new_source_code = SourceCode(rus=rus, eng=eng, isotope_id=isotope_id, activity_id=activity_id,
                                 efficiency=efficiency)
    db.session.add(new_source_code)
    db.session.commit()


def save_wiped_objects(rus, eng):
    new_wiped_object = WipedObjects(rus=rus, eng=eng)
    db.session.add(new_wiped_object)
    db.session.commit()


def save_devices(rus, eng):
    new_device = Devices(rus=rus, eng=eng)
    db.session.add(new_device)
    db.session.commit()


def save_customers(rus, eng):
    new_customer = Customer(rus=rus, eng=eng)
    db.session.add(new_customer)
    db.session.commit()


def save_quartal_number(quartal):
    new_quartal = QuartalNumber(quartal=quartal)
    db.session.add(new_quartal)
    db.session.commit()


def save_micro_ci_limit(micro_ci_limit):
    new_micro_ci_limit = MicroCiLimit(micro_ci_limit=micro_ci_limit)
    db.session.add(new_micro_ci_limit)
    db.session.commit()


def extracting_data():
    for check_report in reports:
        save_reports(**check_report)

    for check_user in users:
        save_users(**check_user)

    for check_task in task_and_places:
        save_task_and_places(**check_task)

    for check_isotope in isotopes:
        save_isotopes(**check_isotope)

    for check_activities in activities:
        save_activities(**check_activities)

    for check_source_codes in source_codes:
        save_source_codes(**check_source_codes)

    for check_wiped_objects in wiped_objects:
        save_wiped_objects(**check_wiped_objects)

    for check_devices in devices:
        save_devices(**check_devices)

    for check_customers in customers:
        save_customers(**check_customers)

    for check_quartal_number in quartal_number:
        save_quartal_number(**check_quartal_number)

    for check_micro_ci_limit in micro_ci_limit:
        save_micro_ci_limit(**check_micro_ci_limit)

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Модель пользователя в БД.
    Возможные роли: admin(полный доступ ко всем аспектам приложения),
    dosimetrist(доступ к базе данных отчетов и возможность создавать и генерировать pdf отчеты),
    user(доступ к базе данных отчетов и возможность генерировать pdf отчеты)
    """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_dosimetrist(self):
        return self.role == 'dosimetrist'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Report(db.Model):
    """Модель данных отчета"""
    __tablename__ = 'Report'
    id = db.Column(db.Integer, primary_key=True)
    report_number = db.Column(db.String(32))
    status = db.Column(db.String(32))
    report_path = db.Column(db.String)
    report_date = db.Column(db.Date, nullable=False)
    customer = db.Column(db.String(128))
    customer_eng = db.Column(db.String(128))
    task_and_place = db.Column(db.Text)
    task_and_place_eng = db.Column(db.Text)
    source_code = db.Column(db.String)
    source_code_eng = db.Column(db.String)
    isotope = db.Column(db.String(32))
    isotope_eng = db.Column(db.String(32))
    activity = db.Column(db.String(32))
    activity_eng = db.Column(db.String(32))
    efficiency = db.Column(db.Float)
    source_serial_number = db.Column(db.String(32))
    wiped_object = db.Column(db.String(128))
    wiped_object_eng = db.Column(db.String(128))
    wiped_serial_number = db.Column(db.String(32))
    wipe_date = db.Column(db.Date, nullable=False)
    bkg_cpm = db.Column(db.Integer)
    gross_cpm = db.Column(db.Integer)
    net_cpm = db.Column(db.Integer)
    removable_activity_micro_ci = db.Column(db.String)
    removable_activity_bq = db.Column(db.String)
    limit_micro_ci = db.Column(db.String)
    device = db.Column(db.Text)
    device_eng = db.Column(db.Text)
    bill_for = db.Column(db.String(128))
    email = db.Column(db.String)
    ike_recieved = db.Column(db.Date)
    results_sent = db.Column(db.Date)
    days_for_analasys = db.Column(db.Integer)
    comments = db.Column(db.Text)
    bill = db.Column(db.String)
    photo_link = db.Column(db.String)

    def math_probe_freq(self, bkg, gross):
        """Функция для рассчета параметра 'Фон част/мин(net_cpm)'
        Принимает аргументы 'Общее част/мин'(gross) и 'Проба част/мин'(bkg) Если один из аргументов
        не введен(является None), то функция возвращает None, так как для рассчета необходимы
        обязательно оба аргумента. В противном случае рассчет идет по принципу gross - bkg,
        функция возвращает целое число.
        """
        if gross is None or bkg is None:
            return None
        else:
            probe_freq = int(gross - bkg)
            return probe_freq

    def days_for_analasys_func(self, d1, d2):
        """Функция для рассчета дней, потребовавшихся для анализа результатов пробы.
        Принимает в себя аргументы d1(ike_recieved, Получено в ИКЭ), d2(report_date, Дата отчета).
        Возвращает потребовавшееся количество дней. В случае, если d2 < d1, при заполнении отчета будет
        показываться ошибка(реализовано в report).
        """
        delta = d2 - d1
        return delta.days

    def removable_activity_ci_func(self, net_cpm, efficiency):
        """Функция для рассчета снимаемого загрязнения, Micro Ci.
        Принимает в себя аргументы net_cpm(Фон част/мин) и efficiency(эффективность конкретного изотопа источника).
        Если net_cpm равен None, то возвращает None, так как для расчета строго необходим этот аргумент.
        В противном случае производит расчет по указанной формуле и возвращет результат в экспоненциальном формате
        с 3 знаками после запятой.
        """
        if net_cpm is None:
            return None
        else:
            removable_ci = net_cpm / (efficiency * 2.22 * 1000000)
            removable_format = "{:.3e}".format(removable_ci)
            return removable_format

    def removable_activity_bq_func(self, removable_ci):
        """Функция для расчета снимаего загрязнения Bq.
        Принимает в себя аргумент- значение removable_ci, если removable_ci равен None, то функция вернет None, так
        как для расчет строго необходим этот аргумент. В противном случае переводит removable_ci во float и производит
        расчет по заданной формуле, возвращает результат в экспоненциальном формате с 3 знаками после запятой.
        """
        if removable_ci is None:
            return None
        else:
            converted_ci = float(removable_ci)
            removable_math = converted_ci * 37 * 1000
            removable_bq_format = "{:.3e}".format(removable_math)
            return removable_bq_format

    def __repr__(self):
        return '<Report #{}>'.format(self.report_number)


class TaskAndPlace(db.Model):
    """Модель для опции заполнения отчета 'Задача и место забора пробы'
    """
    __tablename__ = 'Task and place'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.Text)
    eng = db.Column(db.Text)

    def __repr__(self):
        return f'{self.id}'


class SourceCode(db.Model):
    """Модель для опции заполнения отчета 'Код источника'
    """
    __tablename__ = 'SourceCode'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.Text)
    eng = db.Column(db.Text)
    isotope_id = db.Column(db.Integer, db.ForeignKey('Isotope.id', ondelete='CASCADE'))
    activity_id = db.Column(db.Integer, db.ForeignKey('Activity.id', ondelete='CASCADE'))
    isotope = db.relationship('Isotope', backref='sourcecode')
    activity = db.relationship('Activity', backref='sourcecode')
    efficiency = db.Column(db.Float)

    def __repr__(self):
        return f'{self.rus}'


class Isotope(db.Model):
    """Модель данных 'Изотоп'"""
    __tablename__ = 'Isotope'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.String)
    eng = db.Column(db.String)

    def __repr__(self):
        return f'{self.rus}'


class Activity(db.Model):
    """Модель данных 'Активность'"""
    __tablename__ = 'Activity'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.String)
    eng = db.Column(db.String)

    def __repr__(self):
        return f'{self.rus}'


class WipedObjects(db.Model):
    """Модель для опции заполнения отчета 'Пробы взяты со следующих объектов'"""
    __tablename__ = 'Wiped objects'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.String)
    eng = db.Column(db.String)

    def __repr__(self):
        return f'{self.id}'


class Devices(db.Model):
    """Модель для опции заполнения отчета 'Приборы'"""
    __tablename__ = 'Devices'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.Text)
    eng = db.Column(db.Text)

    def __repr__(self):
        return f'{self.id}'


class Customer(db.Model):
    """Модель для опции заполнения отчета 'Заказчик'"""
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.String)
    eng = db.Column(db.String)

    def __repr__(self):
        return f'{self.id}'


class Documents(db.Model):
    """Модель данных 'Документы'"""
    __tablename__ = 'Documents'
    id = db.Column(db.Integer, primary_key=True)
    rus = db.Column(db.String)
    eng = db.Column(db.String)


class QuartalNumber(db.Model):
    """Модель данных 'Квартальный номер отчета'"""
    __tablename__ = 'QuartalNumber'
    id = db.Column(db.Integer, primary_key=True)
    quartal = db.Column(db.String)


class MicroCiLimit(db.Model):
    """Модель данных для переменной 'Лимит Micro CI'"""
    __tablename__ = 'MicroCiLimit'
    id = db.Column(db.Integer, primary_key=True)
    micro_ci_limit = db.Column(db.String)

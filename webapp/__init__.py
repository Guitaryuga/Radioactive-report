import os
import os.path as op
import pdfkit

from babel.dates import format_date
from flask import Flask, flash, redirect, render_template, request, url_for, make_response, send_from_directory
from flask_admin import Admin
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from sqlalchemy import desc

from webapp.custom_views import (MyAdminIndexView, UserView, QuartalNumberView, ReportView, CustomerView,
                                 TaskAndPlaceView, SourceCodeView, IsotopeView, ActivityView,
                                 WipedObjectsView, DevicesView, DocumentsView, UploadAdmin, MicroCIView,
                                 MainIndexLink)
from webapp.forms import LoginForm, UserCreation, ReportForm, SearchForm
from webapp.models import (db, User, Customer, TaskAndPlace, SourceCode, Isotope, Activity, WipedObjects,
                           Devices, Report, QuartalNumber, MicroCiLimit, Documents)


path = op.join(op.dirname(__file__), 'uploads')


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_pyfile('test_config.py')
    app.config['FLASK_ADMIN_SWATCH'] = 'cosmo'
    app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'index_login'
    login_manager.login_message = u"Please log in to access this page"
    login_manager.login_message_category = 'danger'

    admin = Admin(app, template_mode='bootstrap3',
                  index_view=MyAdminIndexView())
    admin.add_view(UserView(User, db.session))
    admin.add_view(ReportView(Report, db.session))
    admin.add_view(QuartalNumberView(QuartalNumber, db.session))
    admin.add_view(MicroCIView(MicroCiLimit, db.session))
    admin.add_view(DocumentsView(Documents, db.session))
    admin.add_view(CustomerView(Customer, db.session))
    admin.add_view(TaskAndPlaceView(TaskAndPlace, db.session))
    admin.add_view(SourceCodeView(SourceCode, db.session))
    admin.add_view(IsotopeView(Isotope, db.session))
    admin.add_view(ActivityView(Activity, db.session))
    admin.add_view(WipedObjectsView(WipedObjects, db.session))
    admin.add_view(DevicesView(Devices, db.session))
    admin.add_view(UploadAdmin(path, '/uploads/', name='Upload images'))
    admin.add_link(MainIndexLink(name='Main Website'))


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index_login():
        """Стартовая страница с логином пользователя.

        На данную страницу будет перенаправлен любой неавторизованный пользователь.
        """
        page_title = 'Login page'
        form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))
        return render_template('login.html', page_title=page_title, form=form)

    @app.route("/process-login", methods=['POST'])
    def process_login():
        """Функция авторизации пользоватлеля. Возвращает редирект на страницу поиска отчетов
        при успешной авторизации или редирект на страницу с логином пользвателя при неуспешной.
        """
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                login_user(user)
                flash('You successfully logged in', 'success')
                return redirect(url_for("main_page"))
        flash('Wrong username or password', 'danger')
        return redirect(url_for("index_login"))

    @app.route("/logout")
    def logout():
        """Функция логаута(выхода из учетной записи).
        При любой попытке вызова функции перенаправит на страницу логина.
        """
        if current_user.is_authenticated:
            logout_user()
            flash('You successfully logged out', 'success')
            return redirect(url_for("index_login"))
        else:
            flash("You need to sign in first", 'danger')
            return redirect(url_for("index_login"))

    @app.route("/reports", methods=['GET', 'POST'])
    @login_required
    def main_page():
        """Страница с функцией поиска и демонстрации списка отчетов.

        Поиск осуществляется по уникальному номеру отчета или по серийному номеру источника.
        Вывод результатов отличается, если пользователь является администратором или дозимтеристом - для них
        доступны для просмотра отчеты со статусом incomplete - с некоторыми незаполненными полями.
        """
        title = "Search reports"
        form = SearchForm()
        report = form.report_field.data
        try:
            if report and current_user.is_user:
                correct_report = Report.query.\
                    filter((Report.report_number == report) | (Report.source_serial_number == report)).\
                    filter(Report.status == 'complete').\
                    order_by(desc(Report.report_date))
                return render_template('main_page.html', page_title=title,
                                       report=report, form=form,
                                       correct_report=correct_report)
            else:
                correct_report = Report.query.\
                    filter((Report.report_number == report) | (Report.source_serial_number == report)).\
                    order_by(desc(Report.report_date))
                return render_template('main_page.html', page_title=title,
                                       report=report, form=form,
                                       correct_report=correct_report)
        except UnboundLocalError:
            flash('Wrong data', 'danger')
            return redirect(url_for('main_page'))
        return render_template('main_page.html', page_title=title, form=form)

    @app.route("/reports/<report_path>")
    @login_required
    def chosen_report(report_path):
        """Страница подробного отчета.

        Форма поиска остается для быстрого переключения между отчетами.
        Доступна только администраторам и дозиметристам.
        """
        if current_user.is_user:
            flash('Access denied', 'danger')
            return redirect(url_for('main_page'))
        else:
            title = f"Report {report_path}"
            form = SearchForm()
            correct_report = Report.query.filter(Report.report_path == report_path).all()
            return render_template('report_page.html', page_title=title, form=form,
                                   correct_report=correct_report)


    @app.route("/reports/all")
    @login_required
    def all_reports():
        """Страница вывода ВСЕХ существующих отчетов.

        Если текущий пользователь является администратором или дозимтеристом,
        то ему будут доступны отчеты со статусами incomplete и complete,
        другим же пользователям доступны только отчеты со статусом complete.
        """
        title = "All reports"
        if current_user.is_user:
            all_reports = Report.query.filter(Report.status == 'complete').order_by(desc(Report.report_date))
        else:
            all_reports = Report.query.order_by(desc(Report.report_date))
        return render_template('all_reports.html', page_title=title, all_reports=all_reports)

    @app.route("/user_creation", methods=['GET', 'POST'])
    @login_required
    def register():
        """Страница для создания пользователей

        Доступна только администратору. Позволяет создавать пользователей с ролями
        user и dosimetrist.
        """
        if current_user.is_admin:
            title = 'User creation'
            form = UserCreation()
            if request.method == 'GET':
                form = UserCreation()
            elif form.validate_on_submit():
                new_user = User(username=form.username.data,
                                role=form.role.data)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully', 'success')
                return redirect(url_for('register'))
            else:
                flash('Please correct the form', 'danger')
            return render_template('create_user.html', form=form, page_title=title)
        else:
            flash('Access denied', 'danger')
            return redirect(url_for('main_page'))

    @app.route("/report_creation", methods=['GET', 'POST'])
    @login_required
    def report():
        """Страница создания отчета по пробам радиоактивного источника

        Доступна только администраторам и дозиметристам. Размер загружаемого файла ограничен 5 МБ.
        """
        if current_user.is_user:
            flash('Access denied', 'danger')
            return redirect(url_for('main_page'))
        else:
            title = 'Report creation'
            form = ReportForm()
            if request.method == 'GET':
                form = ReportForm()
            elif request.method == 'POST' and request.content_length > 5 * 1024 * 1024:
                flash('Attached file too big!', 'danger')
                return render_template('create_report_wtf.html', page_title=title, form=form)
            elif form.validate_on_submit:
                choices_data = request.form.to_dict()
                quartal_code = QuartalNumber.query.get(1)
                reports_count = Report.query.filter(Report.report_number.like(f'{quartal_code.quartal}%')).count()
                report_number = f'{quartal_code.quartal}-{reports_count + 1}'
                report_date = form.date.data
                customer_query = Customer.query.get(choices_data['customer'])
                task_query = TaskAndPlace.query.get(choices_data['task_and_place'])
                source_code_query = SourceCode.query.get(choices_data['source_code'])
                source_serial_number = form.source_serial_number.data
                wiped_object_query = WipedObjects.query.get(choices_data['wiped_object'])
                wiped_serial_number = form.wiped_serial_number.data
                wipe_date = form.wipe_date.data
                bkg_cpm = form.bkg_cpm.data
                gross_cpm = form.gross_cpm.data
                net_cpm = Report.math_probe_freq(Report, bkg_cpm, gross_cpm)
                removable_ci = Report.removable_activity_ci_func(Report, net_cpm, source_code_query.efficiency)
                removable_bq = Report.removable_activity_bq_func(Report, removable_ci)
                if bkg_cpm is None or gross_cpm is None:
                    status = "incomplete"
                else:
                    status = "complete"
                limit_micro_ci = MicroCiLimit.query.get(1)
                device_query = Devices.query.get(choices_data['device'])
                bill_for = form.bill_for.data
                email = form.email.data
                ike_recieved = form.ike_recieved.data
                results_sent = form.results_sent.data
                report_path = f'{report_date}_{source_code_query.rus}_{source_serial_number}'
                f = form.foto.data
                if f.filename == '':
                    photo_link = 'No file attached'
                else:
                    report_filename = report_number.replace("/", '-')
                    photo_link = secure_filename(f'{report_filename}.jpg')
                    f.save(os.path.join(app.config['UPLOADED_PATH'], photo_link))
                days = Report.days_for_analasys_func(Report, ike_recieved, report_date)
                if days < 0:
                    flash('Correct report date and IKE recieved', 'danger')
                    return render_template('create_report_wtf.html', page_title=title, form=form)
                bill = form.bill.data
                comments = form.comments.data
                report = Report(report_number=report_number, status=status,
                                report_path=report_path, report_date=report_date,
                                customer=customer_query.rus, customer_eng=customer_query.eng,
                                task_and_place=task_query.rus, task_and_place_eng=task_query.eng,
                                source_code=source_code_query.rus, source_code_eng=source_code_query.eng,
                                isotope=str(source_code_query.isotope), isotope_eng=str(source_code_query.isotope.eng),
                                activity=str(source_code_query.activity), activity_eng=str(source_code_query.activity.eng),
                                efficiency=source_code_query.efficiency, source_serial_number=source_serial_number,
                                wiped_object=wiped_object_query.rus, wiped_object_eng=wiped_object_query.eng,
                                wiped_serial_number=wiped_serial_number, wipe_date=wipe_date,
                                bkg_cpm=bkg_cpm, gross_cpm=gross_cpm, net_cpm=net_cpm,
                                removable_activity_micro_ci=removable_ci, removable_activity_bq=removable_bq,
                                limit_micro_ci=limit_micro_ci.micro_ci_limit,
                                device=device_query.rus, device_eng=device_query.eng,
                                bill_for=bill_for, email=email, ike_recieved=ike_recieved,
                                results_sent=results_sent, bill=bill, comments=comments,
                                days_for_analasys=days, photo_link=photo_link)
                db.session.add(report)
                db.session.commit()
                flash(f'Report {report_number} created successfully!', 'success')
                return redirect(url_for('chosen_report', report_path=report_path))
            return render_template('create_report_wtf.html', page_title=title, form=form)

    @app.route('/test')
    def test():
        """Тестовая страничка для проверки отображения материала и результатов запросов"""
        title = "test page"
        test_sample = "It's just a test page #1"
        test_sample2 = "No, really #2"
        test_sample3 = "Just use for whatever reasons #3"
        return render_template('test_template.html', page_title=title, test_sample=test_sample,
                               test_sample2=test_sample2,
                               test_sample3=test_sample3)

    @app.route('/report_generation/<report_path>')
    @login_required
    def pdf_render(report_path):
        """Функция генерации pdf-отчета

        PDF открывается в браузере, с возможностью сохранения, имя файла - уникальный путь к отчету
        (дата отчета_код источника_серийный номер источника)
        """
        report_data = Report.query.filter(Report.report_path == report_path).all()
        for report in report_data:
            date = report.report_date
            wipe_date = report.wipe_date
            date_rus = format_date(date, 'd MMMM yyyy', locale='ru')
            wipe_date_rus = format_date(wipe_date, 'd MMMM yyyy', locale='ru')
            date_eng = format_date(date, 'MMMM d, yyyy', locale='en')
            wipe_date_eng = format_date(wipe_date, 'MMMM d, yyyy', locale='en')
            title = report.report_path
            photo_link = os.path.join(app.config['UPLOADED_PATH'], report.photo_link)
        logo_path = os.path.join(app.config['STATIC_PATH'], 'logo.png')
        signature_path = os.path.join(app.config['STATIC_PATH'], 'signature.png')
        if report.photo_link == 'No file attached':
            rendered = render_template('report_no_img.html', report=report, page_title=title,
                                       date_rus=date_rus,
                                       wipe_date_rus=wipe_date_rus, date_eng=date_eng,
                                       wipe_date_eng=wipe_date_eng, logo_path=logo_path,
                                       signature_path=signature_path)
            css = os.path.join(app.config['STATIC_PATH'], 'css', 'report_no_img.css')
        else:
            rendered = render_template('report.html', report=report, page_title=title,
                                       date_rus=date_rus, wipe_date_rus=wipe_date_rus,
                                       date_eng=date_eng, wipe_date_eng=wipe_date_eng,
                                       logo_path=logo_path, signature_path=signature_path,
                                       photo_link=photo_link)
            css = os.path.join(app.config['STATIC_PATH'], 'css', 'report.css')
        options = {'enable-local-file-access': None}
        ready_pdf = pdfkit.from_string(rendered, False, options=options, css=css)
        response = make_response(ready_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline'

        return response

    @app.route('/uploads/<filename>')
    @login_required
    def uploaded_files(filename):
        """Страница с загруженными на сервер файлами в папаке uploads.
        Принимает в себя название загруженного на сервер файла в качестве аргумента.
        """
        path = app.config['UPLOADED_PATH']
        return send_from_directory(path, filename)

    return app

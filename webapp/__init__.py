import os
import pdfkit
import flask_excel as excel

from babel.dates import format_date
from flask import Flask, flash, redirect, render_template, request, url_for, make_response, send_from_directory
from flask_admin import Admin
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from pyexcel.exceptions import FileTypeNotSupported
from pyexcel_io.exceptions import SupportingPluginAvailableButNotInstalled
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from sqlalchemy import desc

from webapp.custom_views import (MyAdminIndexView, UserView, QuartalNumberView, ReportView, CustomerView,
                                 TaskAndPlaceView, SourceCodeView, IsotopeView, ActivityView,
                                 WipedObjectsView, DevicesView, DocumentsView, UploadAdmin, MicroCIView,
                                 MainIndexLink, XLSXAdmin)
from webapp.forms import LoginForm, UserCreation, ReportForm, SearchForm
from webapp.models import (db, User, Customer, TaskAndPlace, SourceCode, Isotope, Activity, WipedObjects,
                           Devices, Report, QuartalNumber, MicroCiLimit, Documents)


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
    excel.init_excel(app)
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
    admin.add_view(UploadAdmin(app.config['UPLOADED_PATH'], '/uploads/', name='Upload images'))
    admin.add_view(XLSXAdmin(app.config['XLSX_PATH'], '/xlsx/', name='XLSX tables'))
    admin.add_link(MainIndexLink(name='Main Website'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index_login():
        """?????????????????? ???????????????? ?? ?????????????? ????????????????????????.

        ???? ???????????? ???????????????? ?????????? ?????????????????????????? ?????????? ???????????????????????????????? ????????????????????????.
        """
        page_title = 'Login page'
        form = LoginForm()
        if current_user.is_authenticated:
            return redirect(url_for('main_page'))
        return render_template('login.html', page_title=page_title, form=form)

    @app.route("/process-login", methods=['POST'])
    def process_login():
        """?????????????? ?????????????????????? ??????????????????????????. ???????????????????? ???????????????? ???? ???????????????? ???????????? ??????????????
        ?????? ???????????????? ?????????????????????? ?????? ???????????????? ???? ???????????????? ?? ?????????????? ?????????????????????? ?????? ????????????????????.
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
        """?????????????? ??????????????(???????????? ???? ?????????????? ????????????).
        ?????? ?????????? ?????????????? ???????????? ?????????????? ???????????????????????? ???? ???????????????? ????????????.
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
        """???????????????? ?? ???????????????? ???????????? ?? ???????????????????????? ???????????? ??????????????.

        ?????????? ???????????????????????????? ???? ?????????????????????? ???????????? ???????????? ?????? ???? ?????????????????? ???????????? ??????????????????.
        ?????????? ?????????????????????? ????????????????????, ???????? ???????????????????????? ???????????????? ?????????????????????????????? ?????? ?????????????????????????? - ?????? ??????
        ???????????????? ?????? ?????????????????? ???????????? ???? ???????????????? incomplete - ?? ???????????????????? ???????????????????????????? ????????????.
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
        """???????????????? ???????????????????? ????????????.

        ?????????? ???????????? ???????????????? ?????? ???????????????? ???????????????????????? ?????????? ????????????????.
        ???????????????? ???????????? ?????????????????????????????? ?? ??????????????????????????.
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
        """???????????????? ???????????? ???????? ???????????????????????? ??????????????.

        ???????? ?????????????? ???????????????????????? ???????????????? ?????????????????????????????? ?????? ??????????????????????????,
        ???? ?????? ?????????? ???????????????? ???????????? ???? ?????????????????? incomplete ?? complete,
        ???????????? ???? ?????????????????????????? ???????????????? ???????????? ???????????? ???? ???????????????? complete.
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
        """???????????????? ?????? ???????????????? ??????????????????????????

        ???????????????? ???????????? ????????????????????????????. ?????????????????? ?????????????????? ?????????????????????????? ?? ????????????
        user ?? dosimetrist.
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
        """???????????????? ???????????????? ???????????? ???? ???????????? ???????????????????????????? ??????????????????

        ???????????????? ???????????? ?????????????????????????????? ?? ??????????????????????????. ???????????? ???????????????????????? ?????????? ?????????????????? 5 ????.
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
        """???????????????? ?????????????????? ?????? ???????????????? ?????????????????????? ?????????????????? ?? ?????????????????????? ????????????????"""
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
        """?????????????? ?????????????????? pdf-????????????

        PDF ?????????????????????? ?? ????????????????, ?? ???????????????????????? ????????????????????, ?????? ?????????? - ???????????????????? ???????? ?? ????????????
        (???????? ????????????_?????? ??????????????????_???????????????? ?????????? ??????????????????)
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

    @app.route('/import', methods=['GET', 'POST'])
    @login_required
    def doimport():
        """?????????????? ?????????????? ???????????? ?????? ???? ???? xls,xlsx ????????????.

        ?????????????????????? pyexcel, ???????????????? ?? ???????? ???????????????? ??????????????-??????????????????????????????
        ?????? ???????????? ?????????????????????????????? ?????????? ???? ????????????-?????????????? ?? excel-????????????.
        ?????????? ?????????????????? ?? ?????????????????? ???????????????? ???????????????????????????? ????????????????,
        ???????????????????? ?? pyexcel ???????????????????? ???????????? ????????????????????
        SupportingPluginAvailableButNotInstalled."""
        try:
            if current_user.is_admin:
                if request.method == 'POST':
                    def documents_init_func(row):
                        documents = Documents(row['rus'], row['eng'])
                        return documents

                    def customer_init_func(row):
                        customer = Customer(row['rus'], row['eng'])
                        return customer

                    def taskandplace_init_func(row):
                        task_and_place = TaskAndPlace(row['rus'], row['eng'])
                        return task_and_place

                    def source_code_init_func(row):
                        source_code = SourceCode(row['rus'], row['eng'], row['isotope_id'],
                                                 row['activity_id'], row['efficiency'])
                        return source_code

                    def isotope_init_func(row):
                        isotope = Isotope(row['rus'], row['eng'])
                        return isotope

                    def activity_init_func(row):
                        activity = Activity(row['rus'], row['eng'])
                        return activity

                    def wiped_objects_init_func(row):
                        wiped_objects = WipedObjects(row['rus'], row['eng'])
                        return wiped_objects

                    def devices_init_func(row):
                        devices = Devices(row['rus'], row['eng'])
                        return devices

                    tables = [Documents, Customer, TaskAndPlace, SourceCode, Isotope, Activity, WipedObjects, Devices]
                    initializers = [documents_init_func, customer_init_func, taskandplace_init_func,
                                    source_code_init_func, isotope_init_func, activity_init_func,
                                    wiped_objects_init_func, devices_init_func]

                    request.save_book_to_database(field_name='file', session=db.session,
                                                  tables=tables, initializers=initializers)
                    flash('Data uploaded successfully!', 'success')
                    return redirect(url_for('main_page'))
                return render_template('import_data.html', page_title="Import data")
            else:
                flash('Access denied', 'danger')
                return redirect(url_for('main_page'))
        except IOError:
            flash('Unsupported format or no file chosen', 'danger')
            return redirect(url_for('doimport'))
        except FileTypeNotSupported:
            flash('Unsupported format or no file chosen', 'danger')
            return redirect(url_for('doimport'))
        except SupportingPluginAvailableButNotInstalled:
            flash('Unsupported format or no file chosen', 'danger')
            return redirect(url_for('doimport'))

    @app.route('/export_reports', methods=['GET'])
    @login_required
    def reports_export():
        """?????????????? ???????????????? ?????????????? ???? ???? ?? ?????????????? xlsx.

        ???????????????? ???????????? ?????????????? ???????????? ???? ?????????????? ??????????."""
        if current_user.is_admin:
            query_sets = Report.query.all()
            column_names = ['id', 'status', 'report_number', 'report_date', 'customer', 'task_and_place', 'source_code',
                            'isotope', 'activity', 'source_serial_number', 'wiped_object', 'wiped_serial_number',
                            'wipe_date', 'bkg_cpm', 'gross_cpm', 'net_cpm', 'removable_activity_micro_ci',
                            'removable_activity_bq', 'limit_micro_ci', 'device', 'bill_for', 'results_sent',
                            'days_for_analasys', 'comments', 'bill']
            return excel.make_response_from_query_sets(query_sets, column_names, "xlsx")
        else:
            flash('Access denied', 'danger')
            return redirect(url_for('main_page'))

    @app.route('/export_db', methods=['GET'])
    @login_required
    def db_export():
        """?????????????? ???????????????? ???????????????? ????, ?????????????????????? ?????? ???????????????????? ????????????.

        ???????????????? ????????????, ?????????????????? ?????? ????????????????, ???????????????????????????? ???????????????????? tables."""
        if current_user.is_admin:
            tables = [Documents, Customer, TaskAndPlace, SourceCode, Isotope, Activity, WipedObjects, Devices]
            return excel.make_response_from_tables(session=db.session, tables=tables, file_type="xlsx")
        else:
            flash('Access denied', 'danger')
            return redirect(url_for('main_page'))

    @app.route('/xlsx/<filename>', methods=['GET'])
    @login_required
    def table_download(filename):
        """?????????????? ???????????????? xlsx-???????????????? ?????? ????????????????????????????/???????????????? ???????????????? ?????? ???????????????????? ????.
        ???????????????? ???????????? ????????????????????????????, ?????????????????? ?? ???????????????? ?????????????????? ?????? ???????????????????????? ??????????,
        ???????????????????????? ?? ?????????? xlsx ???? ??????????????."""
        if current_user.is_admin:
            return send_from_directory(app.config['XLSX_PATH'], filename)
        else:
            flash('Access denied', 'danger')
            return redirect(url_for('main_page'))

    @app.route('/uploads/<filename>')
    @login_required
    def uploaded_files(filename):
        """???????????????? ?? ???????????????????????? ???? ???????????? ?????????????? ?? ???????????? uploads.
        ?????????????????? ?? ???????????????? ?????????????????? ???????????????? ???????????????????????? ???? ???????????? ?????????? ?? ???????????????? ??????????????????.
        """
        if current_user.is_authenticated:
            path = app.config['UPLOADED_PATH']
            return send_from_directory(path, filename)
        else:
            flash("You need to sign in first", 'danger')
            return redirect(url_for("index_login"))

    return app

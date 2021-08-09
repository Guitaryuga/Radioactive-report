import os

from flask import request, flash, redirect, url_for
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.menu import MenuLink
from webapp.config import UPLOADED_PATH
from werkzeug.utils import secure_filename
from wtforms import FileField, PasswordField
from werkzeug.security import generate_password_hash


class MyAdminIndexView(AdminIndexView):
    """Общий для админки view-класс для ограничения доступа"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class UserView(ModelView):
    """View для User-модели
    Для смены пароля или установки пароля создано отдельное поле
    set_password, которое хеширует пароль для хранения в безопасном виде"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))

    def on_model_change(self, form, User, is_created=False):
        if form.set_password.data:
            User.password = generate_password_hash(form.set_password.data)

    column_exclude_list = ('password')
    form_extra_fields = {'set_password': PasswordField('Update password')}


class QuartalNumberView(ModelView):
    """View для доступа к редактированию и обновлению номера квартальтого отчета"""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class MicroCIView(ModelView):
    """View для доступа к редактированию к обновлению параметра Micro CI Limit,
    необходимого для внутренних вычислений"
    """
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class ReportView(ModelView):
    """View класс для отчетов(модель Report), доступ открыт только для администратора,
    в случае изменения отдельных данных, полученных в резлуьтате вычислений при составлении отчета,
    происходит пересчет значений(см. on_model_change)

    form_extra_fields - доп.поля в форме модели
    column_exclude_list - исключение полей из общего обзора
    column_default_sort - сортировка записей по опр.параметру
    column_searchable_list - поиск по определенному заданному параметру среди записей
    column_filters - набор фильтров
    """
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))

    def on_model_change(self, form, Report, is_created=False):
        Report.report_date = form.report_date.data
        Report.ike_recieved = form.ike_recieved.data
        Report.bkg_cpm = form.bkg_cpm.data
        Report.gross_cpm = form.gross_cpm.data
        if Report.bkg_cpm is None or Report.gross_cpm is None:
            Report.status = "incomplete"
        else:
            Report.status = "complete"
        Report.net_cpm = Report.math_probe_freq(Report.bkg_cpm, Report.gross_cpm)
        Report.removable_activity_micro_ci = Report.removable_activity_ci_func(Report.net_cpm, float(Report.efficiency))
        Report.removable_activity_bq = Report.removable_activity_bq_func(Report.removable_activity_micro_ci)
        Report.days_for_analasys = Report.days_for_analasys_func(Report.ike_recieved, Report.report_date)
        f = form.file.data
        if f.filename == '':
            Report.photo_link = Report.photo_link
        else:
            report_filename = Report.report_number
            photo_link = secure_filename(f'{report_filename}.jpg')
            f.save(os.path.join(UPLOADED_PATH, photo_link))
            Report.photo_link = photo_link

    form_extra_fields = {'file': FileField('File')}

    column_exclude_list = ('device', 'customer_eng', 'task_and_place_eng', 'source_code_eng', 'efficiency',
                           'isotope_eng', 'activity_eng', 'wiped_object_eng', 'device_eng', 'report_path',
                           'task_and_place', 'isotope', 'activity', 'photo_link', 'ike_recieved', 'days_for_analasys',
                           'comments', 'bill')
    column_default_sort = ('report_date', True)
    column_searchable_list = ('report_number', 'source_serial_number')
    column_filters = ('status', 'source_code', 'source_serial_number')


class CustomerView(ModelView):
    """View для доступа к модели Customer для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class TaskAndPlaceView(ModelView):
    """View для доступа к модели TaskAndPlace для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class SourceCodeView(ModelView):
    """View для доступа к модели SourceCode для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class IsotopeView(ModelView):
    """View для доступа к модели Isotope для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class ActivityView(ModelView):
    """View для доступа к модели Activity для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class WipedObjectsView(ModelView):
    """View для доступа к модели WipedObjects для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class DevicesView(ModelView):
    """View для доступа к модели Devices для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class DocumentsView(ModelView):
    """View для доступа к модели Documents для редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('main_page', next=request.url))


class UploadAdmin(FileAdmin):
    """View для доступа к модели Upload images для просмотра, редактирования и обновления."""
    def is_accessible(self):
        try:
            return current_user.is_admin
        except AttributeError:
            flash("You don't have rights to view this page",
                  'danger')

    def inaccessible_callback(self, name, **kwargs):
        flash("You don't have rights to view this page", 'danger')
        return redirect(url_for('material.index', next=request.url))


class MainIndexLink(MenuLink):
    "Ссылка на основное приложение в верхней панели админки"
    def get_url(self):
        return url_for("main_page")

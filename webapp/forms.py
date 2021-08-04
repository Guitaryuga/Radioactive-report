from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField

from wtforms import (BooleanField, StringField, PasswordField, SubmitField,
                     SelectField, IntegerField, FileField)
from wtforms.validators import DataRequired, EqualTo, ValidationError
from wtforms.fields.html5 import DateField

from webapp.models import User, Customer, TaskAndPlace, SourceCode, WipedObjects, Devices


class LoginForm(FlaskForm):
    """Форма логина для авторизации в приложении
    Поля: username, password, remember me, submit.
    """
    username = StringField('Username',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control mt-3",
                                      "placeholder": "Username"})
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control mt-2",
                                        "placeholder": "Password"})
    remember_me = BooleanField('Remember me',
                               default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Login',
                         render_kw={"class": "w-100 btn btn-lg btn-primary"})


class UserCreation(FlaskForm):
    """Форма для создания новых пользователей администратором.
    Поля: username, password, repeat password, choose role(выбор роли пользователя),
    create_user. При создании пользователя происходит проверка уникальности имени пользователя,
    имя должно быть уникальным.
    """
    username = StringField('Username',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control",
                                      "placeholder": "Username"})
    password = PasswordField('Password',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control",
                                        "placeholder": "Password"})
    password2 = PasswordField('Repeat password',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control",
                                         "placeholder": "Repeat password"})
    role = SelectField('Choose role', choices=[('user', 'User'), ('dosimetrist', 'Dosimetrist')],
                       render_kw={"class": "form-select"})
    submit = SubmitField('Create user', render_kw={"class": "w-100 btn btn-lg btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('User with this username already exists')


class ReportForm(FlaskForm):
    """Форма для создания отчетов о пробах источников.
    Поля: Дата отчета, Заказчик, Задача и место забора пробы,
    Код источника, Серийный номер источника, Проба взята со следующего объекта,
    Серийный номер объекта,  Дата взятия пробы, Фон, част/мин, Общее, част/мин,
    Прибор, Счет выставлять на:, E-mail, Получено в ИКЭ:, Результаты отправлены:,
    Прикрепите фото(макс.размер 5МБ), Счет, Комментарии, Создать отчет.
    """
    def customer_choice():
        """Query для выбора заказчика в форме отчета"""
        return Customer.query

    def task_choice():
        """Query для выбора задачи и места забора пробы в форме отчета"""
        return TaskAndPlace.query

    def source_code_choice():
        """Query для выбора кода источника в форме отчета"""
        return SourceCode.query

    def wiped_objects_choice():
        """Query для выбора объекта, с которого взята проба в форме отчета"""
        return WipedObjects.query

    def devices_choice():
        """Query для выбора прибора в форме отчета"""
        return Devices.query

    date = DateField('Дата отчета',
                     format='%Y-%m-%d',
                     validators=[DataRequired()],
                     render_kw={"class": "form-control"})
    customer = QuerySelectField('Заказчик',
                                query_factory=customer_choice,
                                allow_blank=True, get_label='rus',
                                render_kw={"class": "form-multiline",
                                           "style": "width: 100%"})
    task_and_place = QuerySelectField('Задача и меcто забора пробы',
                                      query_factory=task_choice,
                                      allow_blank=True, get_label='rus',
                                      render_kw={"class": "form-multiline",
                                                 "style": "width: 100%"})
    source_code = QuerySelectField('Код источника', query_factory=source_code_choice,
                                   allow_blank=True, get_label='rus',
                                   render_kw={"class": "form-multiline",
                                              "style": "width: 100%"})
    source_serial_number = StringField('Серийный номер источника', validators=[DataRequired()],
                                       render_kw={"class": "form-control"})
    wiped_object = QuerySelectField('Проба взята со следующего объекта',
                                    query_factory=wiped_objects_choice,
                                    allow_blank=True, get_label='rus',
                                    render_kw={"class": "form-multiline",
                                               "style": "width: 100%"})
    wiped_serial_number = StringField('Серийный номер объекта', validators=[DataRequired()],
                                      render_kw={"class": "form-control"})
    wipe_date = DateField('Дата взятия пробы',
                          format='%Y-%m-%d',
                          validators=[DataRequired()],
                          render_kw={"class": "form-control"})
    bkg_cpm = IntegerField('Фон, част/мин',
                           render_kw={"class": "form-control"})
    gross_cpm = IntegerField('Общее, част/мин',
                             render_kw={"class": "form-control"})

    device = QuerySelectField('Прибор', query_factory=devices_choice,
                              allow_blank=True, get_label='rus',
                              render_kw={"class": "form-multiline",
                                         "style": "width: 100%"})
    bill_for = StringField('Счет выставлять на:',
                           render_kw={"class": "form-control"})
    email = StringField('E-mail',
                        render_kw={"class": "form-control"})
    ike_recieved = DateField('Получено в ИКЭ:',
                             format='%Y-%m-%d',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    results_sent = DateField('Результаты отправлены:',
                             validators=[DataRequired()],
                             format='%Y-%m-%d',
                             render_kw={"class": "form-control"})
    foto = FileField('Прикрепите фото(макс.размер 5МБ)', render_kw={"class": "form-control"})
    bill = StringField('Счет', render_kw={"class": "form-control"})
    comments = StringField('Комментарии', render_kw={"class": "form-control"})
    submit = SubmitField('Создать отчет',
                         render_kw={"class": "w-100 btn btn-lg btn-primary"})


class SearchForm(FlaskForm):
    """Форма для поиска отчета по серийному номеру или номеру источника.
    """
    report_field = StringField('Type report #', render_kw={"class": "form-control",
                                                           "placeholder": "Search by report # or source serial #"})
    submit = SubmitField('Search',
                         render_kw={"class": "w-100 btn btn-lg btn-primary"})

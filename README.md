# Radioactive-report

Radioactive report - это веб-приложение, включающее в себя базу данных результатов протирочных тестов радиоактивных источников, а также позволяющее генерировать готовые отчеты по данным тестам в формате PDF.

Пример развернутого приложения можно опробовать тут: https://radioactivereport.herokuapp.com/

Функционал приложения разделен между 3 группами пользователей:
- Администраторы(имеют полный доступ ко всем аспектам управления базой данных и админке)
- Дозиметристы(имеют доступ к поиску, просмотру, и созданию отчетов по результатам тестов)
- Рядовые пользователи(имеют доступ к поиску и просмотру отчетов)
![radioactive1](https://user-images.githubusercontent.com/74609399/128190518-53bb2ebf-2b29-4b1f-b454-9e7ee20bcd08.png)
![radioactive2](https://user-images.githubusercontent.com/74609399/128190650-f51080d0-980c-42c3-bca9-5870f127ab10.png)
![radioactive3](https://user-images.githubusercontent.com/74609399/128191421-db88ebc8-4099-4a27-ae68-fa09cc3da839.png)

# Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/Guitaryuga/Radioactive-report.git
```
2. Создайте и активируйте виртуальное окружение, затем установите зависимости:
```
pip install -r requirements.txt
```
3. Задайте переменные окружения в зависимости от места запуска или деплоя
```
SECRET_KEY="YOUR_VERY_SECRET_KEY_TELL_NOONE"
SQLALCHEMY_DATABASE_URI="Path to you DB"
```
4. Не забудьте сконфигурировать wkhtmltopdf

[wktmltopdf](https://wkhtmltopdf.org/) - модуль, необходимый для генерации отчетов в PDF формате. Он использует для этого заранее подготовленную html-страницу и css, которые можно настроить по своему желанию.
Помимо этого, в зависимости от системы может потребоваться дополнительная установка шрифтов.

# Если вы используете Linux или WSL
- Скачайте и установите .deb пакет, на Ubuntu 20.04 это может выглядеть к примеру так:
```
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb
```
- Рекомендуется установить шрифты Times New Roman и Carlito:

Times New Roman распространяется зачастую в пакете с другими шрифтами, как их установить или отдельно сам шрифт, можно найти [здесь](https://tehnojam.ru/category/software/times-new-roman-linux.html)

Шрифт Carlito распространяется бесплатно, как аналог Calibri:
```
sudo apt update
sudo apt install fonts-crosextra-carlito
```
Для локального запуска создайте в корне проекта файл run.sh:
```
#!/bin/sh
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
```
Сохраните файл и в корне проекта выполните в консоли команду chmod +x run.sh. После этого запуск осуществляется с помощью команды ./run.sh

Если вы пользователь Windows:
- Необходимо вручную скачать и установить версию для Windows c [сайта](https://wkhtmltopdf.org/downloads.html).

После чего в файле __init.py__ в функции pdf_render перед строчкой options нужно прописать 
```
config = pdfkit.configuration(wkhtmltopdf=b'Your\\absolute\\way\\to\\wkhtmltopdf.exe')
```
А после строки options:
```
ready_pdf = pdfkit.from_string(rendered, False, configuration=config, options=options, css=css)
```
Также опционально можно установить шрифт Carlito, либо поменять значения в report.css/report_no_img.css на Calibri

Для локального запуска создайте в корне проекта файл run.bat:
```
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
```
После этого запуск осуществляется из командной строки с помощью команды run

# Если вы хотите деплоить проект c wkhtmltopdf на heroku
- Вам неоходимо подключить соответствующий билдпак, либо через поиск на сайте heroku, либо с помощью Heroku CLI, к примеру:
```
heroku create --buildpack https://github.com/dscout/wkhtmltopdf-buildpack.git
```
После чего в файле __init.py__ в функции pdf_render перед строчкой options нужно прописать 
```
config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')
```
А после строки options:
```
ready_pdf = pdfkit.from_string(rendered, False, configuration=config, options=options, css=css)
```
Для использования шрифтов Times New Roman и Carlito на Heroku создайте в корне проекта папку .fonts и разместите там все необходимые вам файлы шрифтов.

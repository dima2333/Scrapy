1 Установка Python 3.8.1 (следуем инструкциям на сайте https://www.python.org/downloads/)

2 Обновление локального pip установщика
- проверка версии pip 
pip -V (19.2.3)
- обновление версии pip
python -m pip install —upgrade pip
(19.3.1)

3 установка pipenv
pip install pipenv

4 Создаем папку проекта (в ручную, в нашем случае Tesco/mkdir Tesco)

5 перейдя в папку проекта, там создаем виртуальную среду
python3 -m venv .venv

6 активация виртуальной среды + создание файлика pipfile
pipenv shell

7 установка в активированную виртуальную среду всех модулей, необьходимых для scrapy
pipenv install scrapy

8 просмотр что все прошло успешно и все модули в наличии
pip freeze
или
pipenv graph

9 создание нового проекта scrapy
scrapy startproject Tesco(свое имя)
(должна появиться папка с именем проекта)

10 Переходим в каталог проекта + создаем файл самого "паука"
scrapy genspider TescoSpider tesco.com

11 Пишем своего паука (C:\pipenvProject\Tesco\Tesco\Tesco\spiders\TescoSpider.py)

12 Для запуска и контроля ошибок перейдём в каталог с scrapy.cfg и выполним 
scrapy crawl TescoSpider
запуск паука с выводм собранной информации через pipelines в json
scrapy runspider ./Tesco/spiders/TescoSpider.py -o Tesco.json -t json
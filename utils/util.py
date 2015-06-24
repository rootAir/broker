from datetime import datetime
# from django.conf import settings
import glob, os, fnmatch
import time


DayL = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
Month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
Extract_Mycap = ['ABERTURA', 'HORA', 'ATIVO', 'OPERACAO', 'TIPO', 'QTDE. ENVIO', 'QTDE. EXEC.', 'PCO. ENVIO', 'PCO. EXEC.','TOTAL R$','VALIDADE','STATUS']
listOptions = ['petr4', 'vale5', 'bvmf3', 'itub3']


def hour_broker():
    return True # teste mycap
    _hour_init = settings.HOUR_INIT_BROKER
    _hour_final = settings.HOUR_FINAL_BROKER
    _useful_day = datetime.today().date().weekday()
    if _useful_day not in [5, 6] and (_hour_init < time.strftime("%H:%M") < _hour_final):
        return True
    else:
        return False

def remove_files_path(_file_name='*'):
    """
    :param _file_name:
    :return:
    """
    try:
        for file in get_all_files(settings.DIR_LOCAL, _file_name):
            os.remove(file[1])
    except:
        pass

# def celeryd():
#     import os
#     with cd('/usr/local/Cellar/daemonize/1.7.6/sbin'):
#         # Kill existing workers
#         sudo('ps auxww | grep celeryd | grep -v "grep" | awk \'{print $2}\' | xargs kill')
#         # Create new workers
#         sudo('daemonize -u pipeadmin %s/manage.py celery worker' % siteDir)

def get_all_files(path, pattern):
    """
    :param path:
    :param pattern:
    :return:
    """
    datafiles = []
    for root,dirs,files in os.walk(path):
        for file in fnmatch.filter(files, pattern):
            pathname = os.path.join(root, file)
            filesize = os.stat(pathname).st_size
            datafiles.append([file, pathname, filesize])
    if datafiles.__len__() > 0:
        return datafiles
    else:
        return []

def addSecs(tm=None, secs=300):
    """
    :param tm: with defauto secs=300 iguals 5 minute
    :param secs:
    :return:
    """
    import datetime
    if tm is None:
        tm = datetime.datetime.now().time()
    fulldate = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

def this_week():
    """
    :return:
    """
    return datetime.today().isocalendar()[1]

def get_contract():
    _contract = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L'}
    _num_month = datetime.today().month
    return _contract.get(_num_month)

def to_percent(_value):
    """
    :param _value:
    :return:
    """
    return '{percent:.2%}'.format(percent= _value)

def name_day(date):
    name_day = DayL[date.weekday()] + " " + str(date.day) + " " + date.strftime("%B")
    return name_day

def str_to_float(value):
    """
    :param value:
    :return:
    """
    value = float(str(value).replace('.','').replace(',','.'))
    return float("{0:.2f}".format(round(value,2)))

def str_to_date(date_launch):
    """
    :param date_launch:
    :return:
    """
    date = date_launch.replace('/','-')
    _year = date.split('-')[2]
    if _year.__len__() == 2:
        date = date[:-2] + '20' + _year
    date = datetime.strptime(date, '%d-%m-%Y').date()
    return date

def str_to_datetime(_day=None, _month=None, _year=None, _hour=None, _minute=None):
    """
    :param _day:
    :param _month:
    :param _year:
    :param _hour:
    :param _minute:
    :return:
    """
    if _day is None or _month is None or _year is None:
        _date = '%02d-%02d-%s' %(datetime.today().day, datetime.today().month, datetime.today().year)
    if _hour is None or _minute is None:
        _time = datetime.today().time()
        _time = "%02d:%02d" %(_time.hour, _time.minute)
    return datetime.strptime(_date + 'T' + _time + 'Z', '%d-%m-%YT%H:%MZ')

def fix_variacao(_value):
    """
    :param _value:
    :return:
    """
    if _value[:1] == '+':
        return _value.replace('+','')
    else:
        return _value

def to_float(value):
    """
    :param value:
    :return:
    """
    if value.strip() == '-':
        return 0
    elif value[-1] == 'M':
        return float(value.replace('M','').replace(',','.'))
    else:
        return float(value.replace('.','').replace(',','.'))

def isfloat(value):
    """
    :param value:
    :return:
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_stop_loss(_value):
    """
    :param _value: value active now
    :return: value rule to limit the sale loss
    """
    if _value <= 0.5:
        return 0.01
    elif _value <= 1:
        return 0.02
    elif _value <= 5:
        return 0.03
    elif _value <= 10:
        return 0.05
    elif _value <= 15:
        return 0.07
    elif _value <= 20:
        return 0.09
    elif _value > 20:
        return 0.11

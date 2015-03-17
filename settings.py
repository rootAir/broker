import json, os


broker = {
            'BROKER_URL_AMQP': 'YOR_BROKER_URL_AMQP',
            'URL_BROKER': 'YOUR_URL_BROKER',
            'URL_TRADE': 'YOUR_URL_TRADE',
            'BROKER_USERNAME': 'YOUR_BROKER_USERNAME',
            'BROKER_PASSWORD': 'YOUR_BROKER_PASSWORD',
            'HOUR_INIT_BROKER': 'YOUR_HOUR_INIT_BROKER',
            'HOUR_FINAL_BROKER': 'YOUR_HOUR_FINAL_BROKER',
            'MIN_QUANT_PURCHASE': 'YOUR_MIN_QUANT_PURCHASE',
            'MINUTE_FIND_TREND': 3,              # minut find trend in top trade now
            'QUANT_FIND_ACTIVE': 4,              # quantity find best active now in broker (send to wallet)
            'VALUE_MAX_PURCHASE': 10,            # value maximize to intent buy
            'INTERVAL_FIND_OPTION': 10           # interval find option in advfn
}
url = {
            'URL_OPTION': 'http://br.advfn.com/opcoes/bovespa/%s/%s',
            'URL_DROPBOX': 'https://www.dropbox.com/home/YOUR_DEFAULT_FILE_STORAGE'
}

directory = {
            'DIR_LOCAL_SCREENSHOT': 'YOUR_DIR_LOCAL_SCREENSHOT',
            'DIR_CHROME_DRIVER': "/Users/user/Dropbox/projects/rootAir-pack/lib/chromedriver"
}

database = {
            'DATABASE_REMOTE': 'heroku',
            'DATABASE_LOCAL': False,
            'DOC_KEY_DATABASE': 'YOUR_DOC_KEY_DATABASE'
}

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
try:
    from settings_local import *
    local = open(os.path.join(BASE_DIR,'settings_local.py')).read()
    exec(local)
except IOError:
	pass

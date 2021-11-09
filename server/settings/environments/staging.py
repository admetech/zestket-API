import os

from datetime import timedelta

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '))vn+w57l^0o=atfw&@1u2*g=z*9yu#_%$@7^%j%v_m07a=fdc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Make it true for the development API
DEV = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASE_NAME = 'ci'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',         # geo spartial databases
        'OPTIONS': {
            'options': '-c search_path=mrktyz'
        },
        'NAME': DATABASE_NAME,
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    },
    'biztyz_db': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',         # geo spartial databases
        'NAME': DATABASE_NAME,
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

# get the API key from the OS level setting
SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]

HOST_URL = os.environ["HOST_URL"]

SERVICES = {
    'kaleyra':{
        'SID' : 'XXXXXXXXXX',
        'API_KEY' : 'XXXXXXXXXX',
        'API_DOMAIN' : 'XXXXXXXXXX',
    },
    'twilio':{
        'SID' : 'XXXXXXXXXX',
        'AUTH_TOKEN' : 'XXXXXXXXXX',
    },
    'telegram' : {
        'BOT_TOKEN' : 'XXXXXXXXXX',
        'CHAT_ID' : 'XXXXXXX', # default chat
    }
}

SMS = {
    'kaleyra':{
        'SENDER_ID' : 'XXXXXXXXXX',
        'CALLBACK_URL' : '',
        'TEMPLATE_ID' : 'XXXXXXXXXX',
    },
    'twilio':{
        'FROM' : 'XXXXXXXXXX',
        'CALLBACK_URL' : '',
        'TEMPLATE_ID' : 'XXXXXXXXXX',
    }
}

WHATSAPP = {
    'kaleyra':{
        'SENDER_ID' : 'XXXXXXXXXX',
    },
    'twilio':{
        'FROM' : 'XXXXXXXXXX',
    }
}

# storage setting 
STORAGE = {
    'default': {
        'type': 'aws_s3',
        'access_key_id': 'XXXXXXXXXX',
        'secret_access_key': 'XXXXXXXXXX',
        'bucket': 'XXXXXXXXXX',
    },
}
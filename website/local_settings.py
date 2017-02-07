from website.global_definitions import ServerType

DEBUG = True

SERVER_TYPE = ServerType.DEV
NON_PREFIXED_SITE_URL = "127.0.0.1:6827"
SITE_URL = "http://" + NON_PREFIXED_SITE_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'server_name',
        'USER': 'user_name',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        }
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "simple": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler"
        },
        "maced_handler": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "maxBytes": 1024 * 1024 * 1024,  # 1 GB
            "backupCount": 5,
            "filename": "debug.log",
        },
        "error_file": {
            "level": "ERROR",
            "formatter": "verbose",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024 * 1024 * 1024,  # 1 GB
            "backupCount": 5,
            "filename": "errors.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins", "debug_file", "error_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "website": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propogate": True,
        },
        "maced": {
            "handlers": ["maced_handler"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
import logging
from logging.config import dictConfig

dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(pathname)s:%(lineno)d %(asctime)-15s [ %(levelname)s ] : %(message)s',
            },
            'access': {
                'format': '%(pathname)s:%(lineno)d %(asctime)-15s [ %(levelname)s ] : %(message)s',
            },
        },
        'handlers': {
            'console': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'level': logging.INFO,
                'stream': 'ext://sys.stdout',
            },
        },
        'root': {'level': logging.DEBUG, 'handlers': ['console']},
    },
)


logger: logging.Logger = logging.getLogger('src')

import os

# Default settings. Any of them can be overridden by an environment variable with the same name.
# No defaults for TELEGRAM_TOKEN (a secret) and PING_HOST (host to watch): both are passed via the environment (.env).

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
PING_HOST = os.environ.get('PING_HOST')

# Seconds between checks: while the host is online; while it is offline
TIMEOUT_ON_SUCCESS = int(os.environ.get('TIMEOUT_ON_SUCCESS', 60))
TIMEOUT_ON_FAIL = int(os.environ.get('TIMEOUT_ON_FAIL', 20))
# Failed checks in a row before the host is reported offline
RETRY_ON_FAIL = int(os.environ.get('RETRY_ON_FAIL', 3))

# Subscribers list
USERS_FILE = os.environ.get('USERS_FILE', 'users.json')

TELEGRAM_MESSAGE_HELLO = os.environ.get('TELEGRAM_MESSAGE_HELLO', 'Вы подписались на уведомления.')
TELEGRAM_MESSAGE_ONLINE = os.environ.get('TELEGRAM_MESSAGE_ONLINE', '✅ Интернет доступен!')
TELEGRAM_MESSAGE_OFFLINE = os.environ.get('TELEGRAM_MESSAGE_OFFLINE', '❌ Интернет пропал.')

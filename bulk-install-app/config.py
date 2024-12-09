import os

from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

DOMAIN = os.environ.get('GITHUB_DOMAIN') or 'github.com'
GITHUB_APP_NAME = os.environ.get('GITHUB_APP_NAME') or 'hashicorp-vault-radar-checks-app'
USERNAME = os.environ.get('GITHUB_USERNAME')
PASSWORD = os.environ.get('GITHUB_PASSWORD')
DEBUG = bool(int(os.environ.get('DEBUG'))) if os.environ.get('DEBUG') else False
MAX_ORGANIZATIONS = int(os.environ.get('MAX_ORGANIZATIONS')) if os.environ.get('MAX_ORGANIZATIONS') else None

DOMAIN = urlparse(DOMAIN if '//' in DOMAIN else f'//{DOMAIN}').netloc
APPS_LOCATION = 'apps' if DOMAIN == 'github.com' else 'github-apps'

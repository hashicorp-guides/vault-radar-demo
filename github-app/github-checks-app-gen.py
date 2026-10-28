import logging
import sys
from secrets import token_urlsafe
from urllib.parse import urlencode, urlparse


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    h = logging.StreamHandler(sys.stdout)
    logger.addHandler(h)

    return logger


logger = init_logger()


if __name__ == '__main__':
    print("Please select an option GitHub Cloud or GitHub Enterprise Server:")
    print("1. GitHub Cloud")
    print("2. GitHub Enterprise Server")
    choice = input("Enter 1 or 2: ")

    domain = 'github.com'
    webhook_url = 'https://api.hashicorp.cloud/2023-05-01/vault-radar/api/github-apps/events'
    if choice == '2':
        domain = input('Enter your GitHub Enterprise Server domain name (i.e. github.companyname.com): ')
        domain = urlparse(domain if '//' in domain else f'//{domain}').netloc
        webhook_url = webhook_url + f"?domain={domain}"
    elif choice != '1':
        print("Invalid option")
        sys.exit()

    name = input(
        'Enter a unique GitHub app name (lowercase letters and dashes) [hashicorp-vault-radar]: '
    ).strip() or 'hashicorp-vault-radar'

    webhook_secret = token_urlsafe(nbytes=32)

    query_params = {
        'name': name,
        'webhook_url': webhook_url,
        'webhook_active': 'true',
        'url': 'https://www.hashicorp.com/',
        'setup_url': 'https://vault-radar-portal.cloud.hashicorp.com/oauth/github/callback',
        'setup_on_update': 'true',
        'checks': 'write',
        'administration': 'read',
        'contents': 'read',
        'events[]': ['check_run', 'check_suite', 'pull_request', 'push', 'repository'],
        'organization_hooks': 'read',
        'pull_requests': 'read',
        'webhooks': 'read',
    }
    query_param_string = urlencode(query_params, doseq=True, safe=':/?=[]')
    url = f'https://{domain}/settings/apps/new?{query_param_string}'
    logger.info('\nApp registration URL:\n%s', url)
    logger.info(
        '\nManual steps before clicking Create GitHub App:\n'
        '1. Paste this value into the Webhook secret field:\n'
        '   %s\n'
        '2. Under "Where can this GitHub App be installed?", select "Any account".\n'
        '\nStore the webhook secret securely; you will also need it to configure the app in Vault Radar.',
        webhook_secret,
    )

import re
import traceback

from bs4 import BeautifulSoup
from config import DOMAIN, PASSWORD, USERNAME
from debug import save_debug_info


def start_login(session):
    """
    Start the login process by pulling the login form.
    """
    login_response = session.get(f'https://{DOMAIN}/login')
    login_page_soup = BeautifulSoup(login_response.content, 'html.parser')
    save_debug_info(folder='login-data', name='login-start', response=login_response)

    login_form = login_page_soup.find('form', {'action': '/session'})
    return login_form


def complete_login(session, login_form):
    """
    Complete the login process by pulling the authenticity token from the login form,
    and sending username/password.
    """
    authenticity_token = login_form.find('input', {'name': 'authenticity_token'}).get('value')
    login_request_data = {
        'commit': 'Sign in',
        'authenticity_token': authenticity_token,
        'login': USERNAME,
        'password': PASSWORD,
        'trusted_device': '',
        'webauthn-support': 'supported',
        'webauthn-iuvpaa-support': 'supported',
        'return_to': '',
        'allow_signup': '',
        'client_id': '',
        'integration': '',
        'required_field_e106': '',
    }

    login_response = session.post(f'https://{DOMAIN}/session', login_request_data)
    login_page_soup = BeautifulSoup(login_response.content, 'html.parser')
    save_debug_info(folder='login-data', name='login-complete', response=login_response)

    return login_page_soup


def check_login_success(login_page_main):
    """
    Given the resulting login page, check to see if login succeeded.
    """
    login_page_header = login_page_main.find('h1')
    return 'sign in to your account' not in login_page_header.string.lower()


def check_tfa_success(tfa_login_page):
    """
    Given the resulting two-factor login page, check to see if two-factor succeeded.
    """
    tfa_login_page_auth = tfa_login_page.find('div', {'class': re.compile('auth-form-header*', re.IGNORECASE)})
    if not tfa_login_page_auth:
        return True

    tfa_login_page_header = tfa_login_page_auth.find('h1')
    return 'two-factor' not in tfa_login_page_header.string.lower()


def handle_tfa(session, login_page):
    """
    Check if two factor is necessary, and handle if necessary.
    Return boolean for whether two-factor step has succeeded (should return True if two-factor is unnecessary).
    """
    tfa_unnecessary = check_tfa_success(tfa_login_page=login_page)
    if tfa_unnecessary:
        print('Two-factor authentication not required.')
        return True

    otp = input('Two-factor authentication required, input here: ')

    two_factor_form = login_page.find('form', {'action': {'/sessions/two-factor'}})
    authenticity_token = two_factor_form.find('input', {'name': 'authenticity_token'}).get('value')
    two_factor_data = {'authenticity_token': authenticity_token, 'otp': otp}
    tfa_response = session.post('https://github.com/sessions/two-factor', two_factor_data)
    save_debug_info(folder='login-data', name='tfa', response=tfa_response)

    tfa_login_page = BeautifulSoup(tfa_response.content, 'html.parser')

    return check_tfa_success(tfa_login_page=tfa_login_page)


def setup_login(session):
    try:
        login_form = start_login(session=session)
        login_page = complete_login(session=session, login_form=login_form)
        login_page_main = login_page.find('div', {'class': 'application-main'})

        login_success = check_login_success(login_page_main=login_page_main)
        login_success = login_success and handle_tfa(session=session, login_page=login_page)
    except Exception:
        traceback.print_exc()
        login_success = False

    if login_success:
        print(f'Succeeded to login for GitHub user: {USERNAME} \n')
        return
    print(f'Failed to login for GitHub user: {USERNAME} \n')

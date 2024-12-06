import re

from bs4 import BeautifulSoup
from config import APPS_LOCATION, DOMAIN, GITHUB_APP_NAME
from debug import save_debug_info


def organizations_by_page(session):
    """
    Returns a generator of organizations/users to install the app on, by page.
    """
    url = f'https://{DOMAIN}/{APPS_LOCATION}/{GITHUB_APP_NAME}/installations/select_target'
    app_install_response = session.get(url)
    save_debug_info(folder='organization-data', name='page-1', response=app_install_response)
    app_install_page_soup = BeautifulSoup(app_install_response.content, 'html.parser')
    app_install_page_main = app_install_page_soup.find('div', {'class': 'application-main'})
    yield app_install_page_main

    current_elem = app_install_page_soup.find('em', {'class': 'current'})
    if current_elem:
        total_pages = current_elem.get('data-total-pages')
        for page_number in range(2, int(total_pages) + 1):
            app_install_response = session.get(f'{url}?page={page_number}')
            save_debug_info(folder='organization-data', name=f'page-{page_number}', response=app_install_response)
            app_install_page_soup = BeautifulSoup(app_install_response.content, 'html.parser')
            app_install_page_main = app_install_page_soup.find('div', {'class': 'application-main'})
            yield app_install_page_main


def organizations_to_install_on_by_item(app_install_page_soup):
    """
    Given a page of organizations/users to install the app on, returns a generator by item.
    Filters out organizations/users that have already installed the app.
    """
    for row in app_install_page_soup.find_all('a', {'class': re.compile('Box-row*', re.IGNORECASE)}):
        target_name = row.find('img').get('alt').lstrip('@')
        target_url = row.get('href')

        label = row.find('span').get('aria-label')
        if label and 'is installed' in label.lower():
            print(f'Organization/user: {target_name} has already installed app: {GITHUB_APP_NAME}. Skipping. \n')
            continue
        yield target_name, target_url


def organizations_to_uninstall_on_by_item(app_install_page_soup):
    """
    Given a page of organizations/users to uninstall the app on, returns a generator by item.
    Filters out organizations/users that haven't yet installed the app.
    """
    for row in app_install_page_soup.find_all('a', {'class': re.compile('Box-row*', re.IGNORECASE)}):
        target_name = row.find('img').get('alt').lstrip('@')
        target_url = row.get('href')

        label = row.find('span').get('aria-label')
        if not label or 'is installed' not in label.lower():
            print(f'Organization/user: {target_name} has not yet installed app: {GITHUB_APP_NAME}. Skipping. \n')
            continue
        yield target_name, target_url


def organizations(session, uninstall: bool):
    """
    Returns a generator of organizations to install on.
    """
    organizations_by_item_generator = (
        organizations_to_uninstall_on_by_item if uninstall else organizations_to_install_on_by_item
    )

    for app_install_page_soup in organizations_by_page(session=session):
        for organization_tuple in organizations_by_item_generator(app_install_page_soup=app_install_page_soup):
            yield organization_tuple

import argparse
import asyncio
from datetime import datetime

import requests
from config import DOMAIN, GITHUB_APP_NAME, MAX_ORGANIZATIONS
from install import uninstall, install
from login import setup_login
from organization import organizations


if __name__ == '__main__':
    session = requests.Session()
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--uninstall', action='store_true', default=False)
    args = parser.parse_args()
    action = 'Uninstall' if args.uninstall else 'Install'

    print('\n')
    print(f'{datetime.now()} - Bulk {action}')
    print(f'GitHub App: {GITHUB_APP_NAME}, Domain: {DOMAIN}, Max Organizations: {MAX_ORGANIZATIONS}')
    print('\n')

    # Handle logging in
    setup_login(session=session)

    # Get all organizations
    success_counter = 0
    for organization_tuple in organizations(session, uninstall=args.uninstall):
        # Handle installation for one organization
        target_name, target_url = organization_tuple
        action = 'install' if not args.uninstall else 'uninstall'
        print(f'Found organization/user: {target_name}, to {action} app: {GITHUB_APP_NAME}.')

        if not args.uninstall:
            # Marking installation success
            success = install(session=session, target_name=target_name, target_url=target_url)
        else:
            # Marking uninstallation success
            success = uninstall(session=session, target_name=target_name, target_url=target_url)

        if success:
            print(f'Succeeded {action}ation for GitHub organization/user: {target_name}\n')
        elif success is False:
            print(f'Failed {action}ation for GitHub organization/user: {target_name}\n')
        else:
            print(f'Skipped {action}ation for GitHub organization/user: {target_name}\n')

        # Stop early if succeeded on max installations/uninstallations
        success_counter += int(bool(success))
        if MAX_ORGANIZATIONS and success_counter == MAX_ORGANIZATIONS:
            print(f'Hit max organizations: {MAX_ORGANIZATIONS}, finishing. ')
            break

        # Sleep briefly between installations
        delay = 2
        asyncio.run(asyncio.sleep(delay))
    print('\n')

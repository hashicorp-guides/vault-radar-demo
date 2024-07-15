# [Vault Radar](https://developer.hashicorp.com/hcp/docs/vault-radar) GitHub Checks App tools

## Requirements
- [python >= 3.6](https://www.python.org/downloads/)

## Creating a GitHub Enterprise Server App
1. Run `python3 github-checks-app-gen.py`
2. When prompted, select GitHub Enterprise Server or GitHub Cloud
3. GitHub Enterprise Server will require you to input your enterprise server domain. GitHub Cloud will require a unique app name
4. Copy/paste the URL into a browser of your choice
5. Take note of the `webhook_secret=<webhook_secret>` in the URL
    ```
    > python3 creating-github-enterprise-server-app.py
    Enter your GitHub Enterprise Server domain name (i.e. github.companyname.com): github.acme.com
    https://github.acme.com...webhook_secret=Z1KPOYifctpzOjfphKj_hqRlZbrDOBG9AU7hgj7iPrk...
    ```
6. Manually add the `webhook_secret` into the form, since setting webhook secret via query params is no longer supported 
7. Scroll down to click `Create GitHub App`
   
8. Once the app is created, take note of the webhook secret from the URL above, as well as these values from your app settings page
    * app name
    * app ID
    * client ID
    * client secret
    * private key  
 ![GitHub Checks App Settings](github-checks-app-settings.png)
9. Return to the Vault Radar UI, and you should be able to input your app configuration in this form below
 ![Vault Radar UI GitHub Apps Form](vault-radar-ui-github-apps-form.png)


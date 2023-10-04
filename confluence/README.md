# Confluence Testing

## Setup Confluence instance using Docker
This guide assumes you have docker installed and running.

Clone the `confluence.yaml` file, or `cd` to this directory. Run:

```bash
docker-compose -f confluence.yaml up -d
```
> Note: by default the compose file specifies the latest version of confluence. Feel free to adjust as needed for testing. There is a comment in the confluence.yaml file where the change should be made.

This should download the images necessary and spin up a postgres database and a confluence webserver running on port `localhost:8090`. It may take a little bit for everything to startup, but eventually tou should be able to go to [http://localhost:8090](http://localhost:8090) and see confluence landing page.

If not, dig into docker and check out the logs for the postgres and the confluence container.

Assuming everything started up correctly the landing page should be asking you for a license. If you happen to already have a trial or actual license key feel free to use that now and proceed. Otherwise you can click on “Get an evaluation license” and you'll be taken to a different page where you can generate a trial license, you will have to login if you are not already. Use you Hashicorp credentials, no need to create or use an alternate test account. There seems to be no limit on the number of licenses you can create. You may need to provide some information like an organization name (ex. MyOrg is totally fine). When I generated a license I left the rest of the settings as is. Complete generating you license to be taken back to the server. 

Complete the confluence server initialization by selecting "Non-clustered (single-node)" for the deployment type. And expect to wait for a little while here while the server completes its bootstraping. I **do not** recommend refreshing or hitting the "Next" button more than once, if you see the tab is still working then it's probably still setting things up.

You will be landed on a page and asked about whether you want to create an Example site or a Blank site. Choose whichever you prefer. 

You should be prompted about whether you want to manage auth through confluence or through JIRA, select Confluence.

You should be prompted to created the first admin user. Feel free to enter whatever you'd like at this point.

Then next page should ask you to name the Space, again choose whatever you'd like.

When you see a confirmation that the server is setup you should be good to go. Feel free to click the Start button or go to [http://localhost:8090](http://localhost:8090).

## How to get a page id
* Click the "..." button on the top right of the page whose ID you are interested in.
* Select "Page Information"
* The Page ID will be in the URL:
```
http://localhost:8090/pages/viewinfo.action?pageId=12345 # 12345 is the page ID
```

## How to generate a PAT (Confluence 7.9 and above)
* Click your avatar to make your user menu appear and select "Settings"
* From the menu on the left select "Personal Access Tokens"
* Click the button to "Create token"

## Use bootstrap command to populate Confluence server
* `cd` to the `confluence/bootstrap` directory
* edit the `cmd/main.go` file:
  * you will need to set the Auth Variables, like **personalAccessToken**
  * if you are testing a different endpoint change the **confluenceInstanceURL**
  * feel free to change other variables like the number of pages to create, Space Name, Key or Description.
* run `go run cmd/main.go` if there are errors, feel free to reach out, otherwise if it completes without any errors then your instance should be updates with additional content

The command with use the `sample/secrets.yaml` as a source of secrets to occassionally add to the page contents.

## To Do
* Multiple Confluence instances instructions



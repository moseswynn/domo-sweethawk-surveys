# domo-sweethawk-surveys
## A script to pull your Sweethawk NPS surveys from ZenDesk into Domo

You can set this script to run as a service or run it manually on an as needed basis:

## Requirements
- Python 3.8+
- [Poetry](https://python-poetry.org/) for managing virtual environment/dependencies

## Usage:
1. Create a file called 'conf.json' in the same directory as 'script.py' with the following key/value pairs:
```json
{
  "creds": {
    "client_id": "",
    "client_secret": "",
  },
  "dsid": "", 
  "csv_url": ""
}
```
  - Populate as follows:
    1. creds
      - Login to the [Domo developer portal](https://developer.domo.com)
      - Select My Account > Manage Clients (select new client if you have not created any yet)
      - Choose the client id and secret for the client you wish to use.
    2. dsid
      - the script will automatically create the dataset and populate this field, remove this unless you already have a dataset configured and you know the dataset id
    3. csv_url
      - navigate to your ZenDesk support app
      - select the survey in the left sidebar that you want to push to domo
      - select the "Responses" tab
      - Scroll down to the bottom of the page and use the URL for the "download as csv" link
2. Run `poetry install` to setup the virtualenv and install dependencies
3. Run `poetry run python3 script.py` to run the script and push the data to Domo.
4. Setup Service (optional)
- Add a shebang `#!/path/to/virtualenv/bin/python3` at the beginning of the script
- Set permissions of script.py to 755
- create the following unit files and place them in /etc/systemd/system
```ini
# domo-sweethawk.service

[Unit]
Description=Pull <survey name> surveys from Sweethawk/ZenDesk and push to Domo.

[Service]
User=root
WorkingDirectory=/path/to/domo-sweethawk-surveys
ExecStart=/path/to/domo-sweethawk-surveys/script.py


[Install]
WantedBy=multi-user.target
```


```ini
# domo-sweethawk.timer
[Unit]
Description=Timer for domo-sweethawk.service.

[Timer]
Unit=domo-sweethawk.timer
OnCalendar=*-*-* 10:00:00 # every day at 10:00 AM UTC (change as needed)

[Install]
WantedBy=timers.target
```
- run the following commands as root enable the service
```
systemctl daemon-reload
systemctl enable domo-sweethawk.timer
systemctl start domo-sweethawk.timer
```

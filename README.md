# Devpost scraper
Simple scraper that stores devpost data locally and renders it in a web page.

## Usage
- Prepare your environment by executing the requirements.txt file, e.g. `pip install -r requirements.txt`
- Update crondata.p by running `store.py`
- Run the web app as `python app.py`

## Update remote website
If possible schedule a cron task to run `cron.py` periodically. Otherwise run it locally and upload `crondata.p` to the server.




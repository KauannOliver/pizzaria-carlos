# Pizzeria Order Management Desktop App

A desktop application for managing customers, menu items, and orders, with spreadsheet exports and a browser-assisted WhatsApp workflow.

> Public source edition. Configure credentials locally and use empty or synthetic inputs. Company and institution names identify the original integration context; this repository does not claim affiliation or endorsement.

## Capabilities

- Create, view, update, and remove customer, pizza, and order records.
- Persist application data in SQLite.
- Export operational data with Pandas and OpenPyXL.
- Open WhatsApp order conversations through a browser workflow.

## Stack

Python, Flet, SQLite, Pandas, OpenPyXL, Requests, and Selenium.

## Run locally

Requires Python and the dependencies listed in `requirements.txt`. Run `pip install -r requirements.txt`, then `python main.py`. The database tables are initialized locally by the application. Customer databases and receipts are excluded from this public edition; use synthetic records for demonstrations.

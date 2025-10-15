# memmo.info — Anonymous Message Sharing

A Django-based web app for anonymous text sharing.

## Features
- No registration or personal data
- Instant anonymous message creation
- QR code generation for each message
- Edit or delete messages via link parameters (&update, &kill)
- Simple clean UI with line-numbered text input

## Quick start

```bash
git clone https://github.com/artsiomaheyeu/memmo.info.git
cd memmo.info
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

set windows-shell := ["powershell.exe", "-c"]


run:
    export HIDE_PRODUCTION_WARNING=true ; uv run manage.py runserver

runprod:
    uv run gunicorn --workers=2 -b 0.0.0.0:8000 sikari.wsgi

makemigrations:
    uv run manage.py makemigrations

migrate:
    uv run manage.py migrate

format:
    uv run ruff check --select I --fix
    uv run ruff format .

shell:
    uv run manage.py shell -v2

test:
    uv run manage.py test

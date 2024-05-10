from site_and_parser.celery import app

from . import services


@app.task
def simulate_user_app(url: str, products_count: int):
    services.simulate_user(url, products_count)

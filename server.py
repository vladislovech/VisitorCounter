import os
from datetime import datetime
from typing import Awaitable, Callable

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse

from views import index
from visit_counter import VisitCounter

counter = VisitCounter()


@web.middleware
async def add_current_time(request: Request, handler: Callable[[Request], Awaitable[StreamResponse]]) -> StreamResponse:
    """
    Добавляет текущее время (datetime.now()) в объект запроса (request),
    чтобы последующие обработчики могли использовать его для логирования,
    статистики и других целей
    """
    request['current_time'] = datetime.now()
    return await handler(request)


async def handle(request: Request) -> StreamResponse:
    """
    Собирает и возвращает статистику посещений на основе данных из VisitCounter
    """
    client_ip = request.remote
    current_time = request["current_time"]
    counter.update(current_time, client_ip)

    stats = {
        "total_visits": counter.get_total_count(),
        "unique_total_visits": counter.get_unique_total_count(),
        "today_visits": counter.get_day_count(current_time),
        "unique_today": counter.get_unique_day_count(current_time),
        "month_visits": counter.get_month_count(current_time),
        "unique_month": counter.get_unique_month_count(current_time),
        "year_visits": counter.get_year_count(current_time),
        "unique_year": counter.get_unique_year_count(current_time),
    }
    return web.json_response(stats)


def setup_jinja(app: Application) -> None:
    """
    настройка Jinja2
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_dir))


app = web.Application(middlewares=[add_current_time])
setup_jinja(app)
app['counter'] = counter
app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)

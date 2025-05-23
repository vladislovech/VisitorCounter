import os
from datetime import datetime
from typing import Awaitable, Callable

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.abc import Request
from aiohttp.web_app import Application
from aiohttp.web_response import StreamResponse

from views import browsers, days_of_week, hours, index
from visit_counter import VisitCounter


@web.middleware
async def add_current_time(request: Request, handler: Callable[[Request], Awaitable[StreamResponse]]) -> StreamResponse:
    """
    Добавляет текущее время (datetime.now()) в объект запроса (request),
    чтобы последующие обработчики могли использовать его для логирования,
    статистики и других целей
    """
    request['current_time'] = datetime.now()
    return await handler(request)


def setup_jinja(app: Application) -> None:
    """
    настройка Jinja2
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_dir))


def create_app() -> web.Application:
    """
    создание экземпляра приложения
    """
    app = web.Application(middlewares=[add_current_time])
    setup_jinja(app)
    app['counter'] = VisitCounter()
    app.add_routes(
        [
            web.get('/', index),
            web.get('/days_of_week', days_of_week),
            web.get('/hours', hours),
            web.get('/browsers', browsers),
        ]
    )

    return app


if __name__ == '__main__':
    web.run_app(create_app())

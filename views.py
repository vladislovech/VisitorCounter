from typing import Any, Dict

from aiohttp.web import Request
from aiohttp_jinja2 import template


@template('index.html')
async def index(request: Request) -> Dict[str, Any]:
    """
    подставляет значения счетчиков в шаблон страницы index.html
    """
    counter = request.app['counter']
    client_ip = request.remote
    current_time = request['current_time']
    request.app['counter'].update(current_time, client_ip)

    stats = {
        "day_visits": counter.get_day_count(current_time),
        "month_visits": counter.get_month_count(current_time),
        "year_visits": counter.get_year_count(current_time),
        "total_visits": counter.get_total_count(),
        "unique_today": counter.get_unique_day_count(current_time),
        "unique_month": counter.get_unique_month_count(current_time),
        "unique_year": counter.get_unique_year_count(current_time),
        "unique_total_visits": counter.get_unique_total_count(),
    }
    return stats

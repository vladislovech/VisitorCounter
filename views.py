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
    user_agent = request.headers.get('User-Agent', '')
    request.app['counter'].update(current_time, client_ip, user_agent)

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


@template('days_of_week.html')
async def days_of_week(request: Request) -> Dict[str, Any]:
    """
    подставляет значения счетчиков в шаблон страницы days_of_week.html
    """
    counter = request.app['counter']
    client_ip = request.remote
    current_time = request['current_time']
    request.app['counter'].update(current_time, client_ip)

    stats = {
        "monday_visits": counter.get_weekdays_count(0),
        "tuesday_visits": counter.get_weekdays_count(1),
        "wednesday_visits": counter.get_weekdays_count(2),
        "thursday_visits": counter.get_weekdays_count(3),
        "friday_visits": counter.get_weekdays_count(4),
        "saturday_visits": counter.get_weekdays_count(5),
        "sunday_visits": counter.get_weekdays_count(6),
        "unique_monday_visits": counter.get_unique_weekdays_count(0),
        "unique_tuesday_visits": counter.get_unique_weekdays_count(1),
        "unique_wednesday_visits": counter.get_unique_weekdays_count(2),
        "unique_thursday_visits": counter.get_unique_weekdays_count(3),
        "unique_friday_visits": counter.get_unique_weekdays_count(4),
        "unique_saturday_visits": counter.get_unique_weekdays_count(5),
        "unique_sunday_visits": counter.get_unique_weekdays_count(6),
    }
    return stats


@template('hours.html')
async def hours(request: Request) -> Dict[str, Any]:
    """
    Статистика по часам
    """
    counter = request.app['counter']
    client_ip = request.remote
    current_time = request['current_time']
    user_agent = request.headers.get('User-Agent', '')
    request.app['counter'].update(current_time, client_ip, user_agent)

    stats = {"hour_stats": [counter.get_hour_count(hour) for hour in range(24)]}
    return stats


@template('browsers.html')
async def browsers(request: Request) -> Dict[str, Any]:
    """
    Статистика по браузерам
    """
    counter = request.app['counter']
    client_ip = request.remote
    current_time = request['current_time']
    user_agent = request.headers.get('User-Agent', '')
    request.app['counter'].update(current_time, client_ip, user_agent)

    stats = {
        "browser_stats": counter.get_browsers_stats(),
        "unique_browser_stats": counter.get_unique_browsers_stats(),
    }
    return stats

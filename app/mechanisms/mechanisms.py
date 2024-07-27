import aiohttp
from proxies.service import ProxyService
from sites.service import SiteService
import random


async def check_sites(telegram_id):
    sites = await SiteService.find_user_data(telegram_id=telegram_id)
    proxies = await ProxyService.find_user_data(telegram_id=telegram_id)
    results = []

    if len(sites) == 0 or len(proxies) == 0:
        return f"‼️ Добавьте ссылки и прокси в бота!"

    async with aiohttp.ClientSession() as session:
        for site in sites:
            try:
                async with session.get(site.site_name, proxy=random.choice(proxies).proxy, timeout=6) as response:
                    if response.status != site.last_status:
                        results.append(f"‼️ Изменился статус сайта: {site.site_name}.\n‼️ Сейчас: {response.status}\n‼️ Предыдущий: {site.last_status}")
                        await SiteService.change_by_id(site.id, last_status=response.status)
            except Exception as e:
                results.append(f"❌ Не удалось проверить сайт {site.site_name}.\n❌ Ошибка: {str(e)}")

        return "\n".join(results)

from datetime import date, datetime

import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag
from loguru import logger

from core.source import FetchError, Source
from models.feed import FeedItem


class Imhcg(Source):
    name = 'Engineering blogs'
    link = 'https://infos.imhcg.cn'
    description = 'Engineering blogs'

    async def generate(self) -> list[FeedItem]:
        data = []
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.link)
            if resp.status_code != 200:
                logger.exception(
                    f'Failed to fetch {self.link} (status code: {resp.status_code}): {resp.content}'
                )
                raise FetchError()

            bs = BeautifulSoup(resp.content)
            for li in bs.main.ul:  # type: ignore
                if isinstance(li, Tag):
                    title_a: Tag = li.a  # type: ignore
                    link: str = title_a.get('href')  # type: ignore
                    title = title_a.get_text()
                    contents = li.find_all('p')  # type: ignore
                    if len(contents) <= 3:
                        contents.extend([None] * (3 - len(contents)))
                    author = contents[0].get_text() if contents[0] else ''
                    updated_str = contents[1].get_text() if contents[1] else ''
                    try:
                        updated = datetime.strptime(updated_str, '%Y-%m-%d %H:%M:%S')
                    except:
                        updated = datetime.now()
                    description = contents[2].get_text() if contents[2] else ''
                    data.append(
                        FeedItem(
                            title=title,
                            link=link or self.link,
                            description=description,
                            updated=updated,
                            author=author,
                        )
                    )

        return data

    def is_expire(self, t: datetime) -> bool:
        return t.date().isocalendar().week != date.today().isocalendar().week

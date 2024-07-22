from datetime import datetime

import httpx
from loguru import logger

from core.source import FetchError, Source
from models.feed import FeedItem


class DailyBlog(Source):
    name = 'Daily Blogs'
    link = 'https://daily-blog.chlinlearn.top'
    description = '值得一读技术博客'

    async def generate(self) -> list[FeedItem]:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                'https://daily-blog.chlinlearn.top/api/daily-blog/getBlogs/new?type=new&pageNum=1&pageSize=20',
                headers={'Referer': 'https://daily-blog.chlinlearn.top/blogs/1'},
            )
            if resp.status_code != 200:
                logger.exception(
                    f'Failed to fetch {self.link} (status code: {resp.status_code}): {resp.content}'
                )
                raise FetchError()

            return [
                FeedItem(
                    title=item['title'],
                    link=item['url'],
                    description=item['title'],
                    updated=datetime.strptime(item['publishTime'], '%Y-%m-%d'),
                    author=item['author'] or '',
                )
                for item in resp.json()['rows']
            ]

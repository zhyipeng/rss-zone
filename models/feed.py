import datetime
from dataclasses import dataclass

from pydantic import BaseModel

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S %Z'


class Channel(BaseModel):
    title: str
    link: str
    description: str
    updated: datetime.datetime

    @property
    def formatted_updated(self):
        return self.updated.strftime(GMT_FORMAT)


class FeedItem(BaseModel):
    title: str
    link: str
    description: str
    updated: datetime.datetime
    author: str = ''

    @property
    def formatted_updated(self):
        return self.updated.strftime(GMT_FORMAT)


@dataclass
class CacheData:
    channel: Channel
    items: list[FeedItem]

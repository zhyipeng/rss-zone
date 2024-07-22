import abc
from datetime import date, datetime
from typing import ClassVar

from models.feed import CacheData, Channel, FeedItem


class Source(metaclass=abc.ABCMeta):
    name: ClassVar[str]
    link: ClassVar[str]
    description: ClassVar[str]

    _cache: ClassVar[CacheData | None] = None

    @abc.abstractmethod
    async def generate(self) -> list[FeedItem]:
        raise NotImplementedError()

    def is_expire(self, t: datetime) -> bool:
        return t.date() != date.today()

    async def get_data(self) -> CacheData | None:
        if self._cache is None or self.is_expire(self._cache.channel.updated):
            items = await self.generate()
            data = CacheData(
                channel=Channel(
                    title=self.name,
                    link=self.link,
                    description=self.description,
                    updated=datetime.now(),
                ),
                items=items,
            )
            self.__class__._cache = data
            return data
        return self._cache


class FetchError(Exception):
    pass

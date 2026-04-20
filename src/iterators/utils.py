from dataclasses import dataclass, field
from itertools import batched
from typing import Iterable, TypeAlias

SomeRemoteData: TypeAlias = int


@dataclass
class Query:
    per_page: int = 3
    page: int = 1


@dataclass
class Page:
    per_page: int = 3
    results: Iterable[SomeRemoteData] = field(default_factory=list)
    next: int | None = None


def request(query: Query) -> Page:
    data = list(range(0, 10))
    chunks = list(batched(data, query.per_page))
    return Page(
        per_page=query.per_page,
        results=chunks[query.page - 1],
        next=query.page + 1 if query.page < len(chunks) else None,
    )


class RetrieveRemoteData:
    def __init__(self, per_page: int):
        self.query = Query(per_page=per_page)

    def __iter__(self):
        current = self.query

        while True:
            page = request(current)

            for i in page.results:
                yield i

            if page.next is None:
                break

            current.page = page.next


class Fibo:
    def __init__(self, n: int):
        self.stop = n
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.stop:
            raise StopIteration

        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

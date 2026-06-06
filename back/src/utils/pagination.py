"""分页工具。"""

from math import ceil
from typing import Any


def paginate(items: list[Any], page: int, size: int) -> dict:
    """对列表进行分页并返回分页信息。"""

    total = len(items)
    total_pages = max(1, ceil(total / size))
    page = max(1, min(page, total_pages))
    start = (page - 1) * size
    end = start + size

    return {
        "records": items[start:end],
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages,
    }

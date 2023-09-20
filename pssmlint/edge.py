from dataclasses import dataclass
from typing import Any

from apssdag.typings import DeviceType


@dataclass
class Edge:
    from_: DeviceType
    to: DeviceType
    extras: Any

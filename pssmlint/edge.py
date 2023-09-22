from dataclasses import dataclass
from typing import Any

from apssm.typing import DeviceType


@dataclass
class Edge:
    first: tuple[DeviceType, int]
    second: tuple[DeviceType, int]
    extras: Any

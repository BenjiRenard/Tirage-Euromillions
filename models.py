from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Ticket:
    numbers: Tuple[int, int, int, int, int]
    stars: Tuple[int, int]

    def key(self) -> tuple:
        return self.numbers, self.stars

    def as_dict(self) -> dict:
        return {
            "n1": self.numbers[0], "n2": self.numbers[1],
            "n3": self.numbers[2], "n4": self.numbers[3],
            "n5": self.numbers[4], "s1": self.stars[0], "s2": self.stars[1],
        }

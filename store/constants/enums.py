from enum import Enum


class RatingChoices(Enum):
    r1 = '1'
    r2 = '2'
    r3 = '3'
    r4 = '4'
    r5 = '5'

    @classmethod
    def choices(cls):
        return tuple(
            (choice.value, choice.value)
            for choice in cls
        )

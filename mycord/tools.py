import random
from datetime import datetime

class Tools:
    @staticmethod
    def chance(percentage: float) -> bool:
        return random.random() * 100 <= percentage

    @staticmethod
    def timestamp() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


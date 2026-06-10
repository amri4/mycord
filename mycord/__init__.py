import os
import sys
from .bot import MyBot
from .database import DB
from .tools import Tools
from .cog import Cog

Bot = MyBot

# Perform the global injection hack for the core execution file
if '__main__' in sys.modules:
    main_module = sys.modules['__main__']
    setattr(main_module, 'MyBot', MyBot)
    setattr(main_module, 'DB', DB)
    setattr(main_module, 'Tools', Tools)
    setattr(main_module, 'Cog', Cog)

__all__ = ['MyBot', 'Bot', 'DB', 'Tools', 'Cog', 'os']


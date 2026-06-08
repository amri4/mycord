import sys
import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        module_name = cls.__module__
        module = sys.modules.get(module_name)
        
        if module:
            for k, v in discord.__dict__.items():
                if not k.startswith('_') and not hasattr(module, k):
                    setattr(module, k, v)
            
            for k, v in commands.__dict__.items():
                if not k.startswith('_') and not hasattr(module, k):
                    setattr(module, k, v)


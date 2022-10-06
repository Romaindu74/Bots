from .GetLang import Get_Lang
from .Logger  import Log

from typing   import Union

try:
    import discord
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

try:
    import json
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'json'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other) -> bool:
        return False

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return '...'

MISSING: None = _MissingSentinel()

def Save(path: str = MISSING, obj: dict = MISSING) -> bool:
    if path == MISSING or obj == MISSING:
        return False

    try:
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(obj, f, indent=4, sort_keys=True)
            f.close()
        return True
    except FileNotFoundError:
        with open(path, 'w+', encoding="utf-8") as f:
            json.dump(obj, f, indent=4, sort_keys=True)
            f.close()
        return True
    except Exception as e:
        Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)
        return False

def Open(path: str = MISSING, __defalts: dict = {}) -> dict:
    if path == MISSING:
        return {}

    try:
        with open(path, 'r', encoding="utf-8") as f:
            data = json.load(f)
            f.close()
        return data
    except FileNotFoundError:
        with open(path, 'w+', encoding="utf-8") as f:
            json.dump(__defalts, f, indent=4, sort_keys=True)
            f.close()
        return __defalts
    except Exception as e:
        Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)
        return False


async def send(ctx: commands.Context = MISSING, *, message: str = False, embed: discord.Embed = False, reference: bool = True) -> Union[discord.Message, discord.Embed, bool]:
    if ctx == MISSING:
        return False

    if message:
        if reference:
            return await ctx.send(message, reference=ctx.message)
        elif not reference:
            return await ctx.send(message)
    elif embed:
        if reference:
            return await ctx.send(embed=embed, reference=ctx.message)
        elif not reference:
            return await ctx.send(embed=embed)
    else:
        return False

async def purge(ctx: commands.Context = MISSING, nombre: int = MISSING) -> Union[bool, list[discord.Message]]:
    if ctx == MISSING or nombre == MISSING:
        return False
    return await ctx.channel.purge(limit = nombre)

async def channel_send(channel: discord.TextChannel = MISSING, *, message: str = False, embed: discord.Embed = False) -> Union[discord.Message, discord.Embed, bool]:
    if channel == MISSING:
        return False
    if message:
        return await channel.send(content=message)
    elif embed:
        return await channel.send(embed=embed)
    else:
        return False

def _to_str(size: int, suffixes: tuple, base: int, *, precision: int = 1, separator: str = " ") -> str:
    if size == 1:
        return "1 byte"
    elif size < base:
        return "{:,} bytes".format(size)

    for i, suffix in enumerate(suffixes, 2):  # noqa: B007
        unit = base**i
        if size < unit:
            break
    return "{:,.{precision}f}{separator}{}".format(
        (base * size / unit),
        suffix,
        precision=precision,
        separator=separator,
    )

def decimal(size: int, *, precision: int = 1, separator: str = " ") -> str:
    return _to_str(
        size,
        ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
        1000,
        precision=precision,
        separator=separator,
    )

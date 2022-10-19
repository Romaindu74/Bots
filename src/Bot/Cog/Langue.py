from ..GetLang          import Code, Get_User_Lang
from ..Utils            import send, Open, Save
from ..Logger           import Logger
from ..type.Bot         import Bot

_log = Logger(__name__)

import os

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Langue(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot = Bot

        self.client  = self.Bot.Client
        self.options = self.Bot.Options


    def get_list_lang(self) -> list:
        with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Language.json') as r:
            try:
                self.language = r.json()
            except Exception as e:
                self.language = []
                _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
        return self.language

    @commands.command(
        name = "Lang"
    )
    async def _lang(self, ctx: commands.Context, *, Lang: str = False) -> None:
        if not ctx.author.bot:
            self.language = self.get_list_lang()
            if not Lang:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.1.7').format(lang = Get_User_Lang(ctx.author.id).get_lang))

            elif Lang == 'list':
                descrption = ''
                for i in self.language:
                    descrption += '> '+str(i).replace('.json', '')+'\n'
                await send(ctx, embed=discord.Embed(title=Get_User_Lang(ctx.author.id).get('0.0.0.1.8'), description=descrption))

            elif not Lang+'.json' in self.language:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.1.9'))

            else:
                os.makedirs('{0}/User/__User__/'.format(self.options.Path), exist_ok=True)
                user_lang = Open('{0}/User/__User__/{1}.json'.format(self.options.Path, ctx.author.id), {"Language": "English"})

                user_lang['Lang'] = Lang

                Save('{0}/User/__User__/{1}.json'.format(self.options.Path, ctx.author.id), user_lang)

                await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.2.0').format(lang = Lang)))

async def setup(Bot: Bot) -> bool:
    _cog = Langue(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True
import os
from ..GetLang import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger  import Log
from ..Utils   import send, Open, Save

try:
    import discord
    from discord.ext import commands
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'discord'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

__all__ = (
    'setup'
)


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
                Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
        return self.language

    @commands.command(
        name = "Lang"
    )
    async def _lang(self, ctx: commands.Context, *, Lang: str = False) -> None:
        if not ctx.author.bot:
            self.language = self.get_list_lang()
            if not Lang:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.4').format(Lang = Get_User_Lang(ctx.author.id).get_lang))

            elif Lang == 'list':
                descrption = ''
                for i in self.language:
                    descrption += '> '+str(i).replace('.json', '')+'\n'
                await send(ctx, embed=discord.Embed(title=Get_User_Lang(ctx.author.id).get('0.0.0.8.5'), description=descrption))

            elif not Lang+'.json' in self.language:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.8.6'))

            else:
                os.makedirs('{0}/User/__User__/'.format(self.options.Path), exist_ok=True)
                user_lang = Open('{0}/User/__User__/{1}.json'.format(self.options.Path, ctx.author.id), {"Language": "English"})

                user_lang['Lang'] = Lang

                Save('{0}/User/__User__/{1}.json'.format(self.options.Path, ctx.author.id), user_lang)

                await send(ctx, embed = discord.Embed(title = Get_User_Lang(ctx.author.id).get('0.0.0.8.7').format(Lang = Lang)))

async def setup(Bot: Bot) -> bool:
    try:
        await Bot.Client.add_cog(Langue(Bot))
    except Exception:
        return False
    else:
        return True
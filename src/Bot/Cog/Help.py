from ..GetLang  import Get_Lang, Get_User_Lang
from ..type.Bot import Bot
from ..Logger   import Log
from ..Utils    import send, Open, Save

import os

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

class Help(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot              = Bot
        self.client           = self.Bot.Client
        self.options          = self.Bot.Options

        self.client.remove_command('help')

    async def _check(self, ctx: commands.Context) -> bool:
        if not ctx.author.bot:
            return True
        else:
            return False

    @commands.command(
        name = 'Help',
        aliases = [
            'help','hElp','heLp','helP',
            'HElp','hELp','heLP','HelP',
            'HELp','hELP','HeLP','HElP'
        ]
    )
    async def _help(self, ctx: commands.Context) -> None:
        if await self._check(ctx):
            Prefix = self.Bot.Prefix.get('Prefix', ['!'])[0]
            author_lang = Get_User_Lang(ctx.author.id).get_lang
            os.makedirs('{0}/Bot/Help/'.format(self.options.Path), 777, True)
            help   = Open('{0}/Bot/Help/{1}.json'.format(self.options.Path, author_lang))

            if help == {}:
                with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Help/{0}'.format(author_lang+'.json')) as r:
                    try:
                        help = r.json()
                    except Exception as e:
                        Log(50, "An error occurred in file {0}\nError: {1}".format(__file__, e), True)
                        return False

                if 'message' in help and 'code' in help:
                    author_lang = 'English'
                    if not 'English.json' in [f for f in os.listdir('{0}/Bot/Help/'.format(self.options.Path)) if os.path.isfile(os.path.join('{0}/Bot/Help/'.format(self.options.Path), f))]:
                        with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Help/English.json') as r:
                            try:
                                help = r.json()
                            except Exception as e:
                                Log(50, "An error occurred in file {0}\nError: {1}".format(__file__, e), True)
                                return False

                    else:
                        help = Open('{0}/Bot/Help/English.json'.format(self.options.Path))

                Save('{0}/Bot/Help/{1}.json'.format(self.options.Path, author_lang), help)


            Embed = discord.Embed(title = '{0}Help'.format(Prefix), color = ctx.author.color)
            for a in help:
                Name = help[a].get('Name', '')
                Value = ''
                for b in help[a].get('Value', []):
                    if b.get('Name', False):
                        Value += '> `{0}`'.format(b.get('Name'))

                        if b.get('Description', False) or b.get('Url', False):
                            Value += ': '

                    if b.get('Description', False) and not b.get('Url', False):
                        Value += b.get('Description')
                    
                    elif b.get('Description', False) and b.get('Url', False):
                        Value += '[{0}]({1})'.format(b.get('Description'), b.get('Url').format(bot_id = self.client.user.id))

                    elif not b.get('Description', False) and b.get('Url', False):
                        Value += b.get('Url').format(bot_id = self.client.user.id)

                    else:
                        Value += '...'
                    Value += '\n'

                if Value == '':
                    Value = '...'

                Embed.add_field(name = Name, value = Value, inline = help[a].get('Inline', False))

            await send(ctx, embed=Embed)

async def setup(Bot: Bot):
    try:
        await Bot.Client.add_cog(Help(Bot))
    except Exception:
        return False
    else:
        return True
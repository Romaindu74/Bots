from ..GetLang          import Get_User_Lang, Code
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
                        _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = e))
                        return False

                if 'message' in help and 'code' in help:
                    author_lang = 'English'
                    if not 'English.json' in [f for f in os.listdir('{0}/Bot/Help/'.format(self.options.Path)) if os.path.isfile(os.path.join('{0}/Bot/Help/'.format(self.options.Path), f))]:
                        with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Help/English.json') as r:
                            try:
                                help = r.json()
                            except Exception as e:
                                _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = e))
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

async def setup(Bot: Bot) -> bool:
    _cog = Help(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True
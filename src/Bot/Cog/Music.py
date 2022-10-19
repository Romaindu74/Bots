from ..GetLang          import Code, Get_User_Lang
from ..VoiceState       import VoiceState
from ..Logger           import Logger
from ..Utils            import send
from ..type.Bot         import Bot

_log = Logger(__name__)

try:
    import discord
    from discord.ext    import commands
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'discord'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Music(commands.Cog):
    def __init__(self, Bot: Bot) -> None:
        self.Bot     = Bot

        self.client  = self.Bot.Client

        self._guilds = {}

    def get_voice_state(self, ctx: commands.Context) -> None:
        voice_states = self._guilds.get(str(ctx.guild.id), False)
        if not voice_states:
            voice_states = VoiceState(self.Bot, ctx)
            self._guilds[str(ctx.guild.id)] = voice_states

        return voice_states

    def cog_unload(self) -> None:
        for voice in self._guilds.values():
            self.client.loop.create_task(voice.stop())

    async def _check(self, ctx: commands.Context) -> bool:
        if not ctx.author.bot:
            if not ctx.author.voice or not ctx.author.voice.channel:
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.7.3"))
                return False
            elif ctx.voice_client:
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.7.4"))
                    return False
            elif not (ctx.guild):
                await send(ctx, message =  Get_User_Lang(ctx.author.id).get("0.0.0.2.2"))
                return False
            return True
        else:
            return False

    async def cog_before_invoke(self, ctx: commands.Context) -> None:
        self.voice_state = self.get_voice_state(ctx)

    @commands.command(
        name='join',
        aliases = [
            "Join", "jOin", "joIn", "joiN",
            "JOin", "jOIn", "joIN", "JoiN",
            "JOIn", "jOIN", "JoIN", "JOiN",
            "JOIN"
        ],
        invoke_without_subcommand = True
    )
    async def _join(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if await self.voice_state._join(ctx):
                await ctx.message.add_reaction('✅')
                return True
            else:
                await ctx.message.add_reaction('❌')
                return False

    @commands.command(
        name='leave',
        aliases = [
            "Leave", "lEave", "leAve", "leaVe", "leavE"
        ]
    )
    async def _leave(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if await self.voice_state._leave():
                await ctx.message.add_reaction('✅')
                if str(ctx.guild.id) in self._guilds:
                    del self._guilds[str(ctx.guild.id)]
                return True
            else:
                await ctx.message.add_reaction('❌')
                return False

    @commands.command(
        name = "play",
        aliases = [
            "Play", "pLay", "plAy", "plaY",
            "PLay", "pLAy", "plAY", "PlaY",
            "PLAy", "pLAY", "PlAY", "PLaY",
            "PLAY"
        ]
    )
    async def _play(self, ctx: commands.Context, *, search: str) -> None:
        if await self._check(ctx):
            await self.voice_state._play(ctx, search)

    @commands.command(
        name = "loop",
        aliases = [
            "Loop", "lOop", "loOp", "looP",
            "LOop", "lOOp", "loOP", "LooP",
            "LOOp", "lOOP", "LoOP", "LOoP",
            "LOOP"
        ]
    )
    async def _loop(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            if await self.voice_state._loop():
                await ctx.message.add_reaction('✅')
                return True
            else:
                await ctx.message.add_reaction('❌')
                return False

    @commands.command(
        name = "stop",
        aliases = [
            "Stop", "sTop", "stOp", "stoP",
            "STop", "sTOp", "stOP", "StoP",
            "STOp", "sTOP", "StOP", "SToP",
            "STOP"
        ]
    )
    async def _stop(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            if await self.voice_state._stop():
                await ctx.message.add_reaction('✅')
                return True

            else:
                await ctx.message.add_reaction('❌')
                return False


    @commands.command(
        name = 'queue',
        aliases = [
            "Queue", "qUeue", "quEue", "queUe", "queuE"
            ]
        )
    async def _queue(self, ctx: commands.Context, *, page: int = 1) -> bool:
        if await self._check(ctx):
            if self.voice_state.songs == []:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.7.6'))
                return False

            await self.voice_state._queue(ctx, page)

    @commands.command(
        name = "skip",
        aliases = [
            "Skip", "sKip", "skIp", "skiP",
            "SKip", "sKIp", "skIP", "SkiP",
            "SKIp", "sKIP", "SkIP", "SKiP",
            "SKIP"
        ]
    )
    async def _skip(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            await self.voice_state._skip(ctx)

    @commands.command(
        name='volume',
        aliases = [
            "Volume", "vOlume", "voLume", "volUme", "voluMe", "volumE"
        ]
    )
    async def _volume(self, ctx: commands.Context, *, volume: float = False) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            await self.voice_state._volume(ctx, volume)

    @commands.command(
        name = 'pause',
        aliases = [
            "Pause", 'pAuse', 'paUse', 'pauSe', 'pausE'
        ]
    )
    async def _pause(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            if await self.voice_state._pause():
                await ctx.message.add_reaction('⏯')
                return True

            else:
                await ctx.message.add_reaction('❌')
                return False



    @commands.command(
        name='resume',
        aliases = [
            "Resume", 'rEsume', 'reSume', 'resUme', 'resuMe', 'resumE'
        ]
    )
    async def _resume(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            if await self.voice_state._resume():
                await ctx.message.add_reaction('⏯')
                return True

            else:
                await ctx.message.add_reaction('❌')
                return False

    @commands.command(
        name = 'shuffle',
        aliases = [
            "Shuffle", "sHuffle", "shUffle", "shuFfle", "shufFle", "shuffLe", "shufflE"
        ]
    )
    async def _shuffle(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            if len(self.voice_state.songs) == 0:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.6"))
                return False

            if await self.voice_state._shuffle():
                await ctx.message.add_reaction('✅')
                return True

            else:
                await ctx.message.add_reaction('❌')
                return False

    @commands.command(
        name='remove',
        aliases = [
            "Remove", 'rEmove', 'reMove', 'remOve', 'remoVe', 'removE'
        ]
    )
    async def _remove(self, ctx: commands.Context, index: int = False) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            if len(self.voice_state.songs) == 0:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.6"))
                return False

            if index == False:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.7.7'))
                return False

            if index < 1 or len(self.voice_state.songs) < index:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get('0.0.0.7.8').format(max = len(self.voice_state.songs)))
                return False

            await self.voice_state._remove(ctx, index)

    @commands.command(
        name = 'fs',
        aliases = [
            "Fs", "fS",
            "forceskip"
        ]
    )
    async def _forceskip(self, ctx: commands.Context) -> bool:
        if await self._check(ctx):
            if self.voice_state.is_playing:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.7.5"))
                return False

            permition: discord.permissions = ctx.author.guild_permissions
            if not permition.manage_guild:
                await send(ctx, message = Get_User_Lang(ctx.author.id).get("0.0.0.1.1"))
                return False

            await ctx.message.add_reaction('⏭')
            self.voice_state.loop = False
            self.voice_state.voice.stop()

async def setup(Bot: Bot) -> bool:
    _cog = Music(Bot)
    try:
        _log.Info(Code('0.0.0.0.8').format(cog = _cog.__class__.__name__))
        await Bot.Client.add_cog(_cog)
    except Exception:
        _log.Warn(Code('0.0.0.0.9').format(cog = _cog.__class__.__name__))
        return False
    else:
        _log.Info(Code('0.0.0.1.0').format(cog = _cog.__class__.__name__))
        return True
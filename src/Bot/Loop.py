from .Utils     import Save, Open
from .Logger    import Logger
from .GetLang   import Code
from .type.Bot  import Bot

_log = Logger(__name__)

import os
import asyncio
import discord
import threading

from time       import monotonic, sleep
from asyncio    import coroutines

class Loop:
    def __init__(self, Bot: Bot) -> None:
        self.Bot = Bot
        self.proccess: _Loop = None

    def start(self) -> bool:
        _log.Info(Code('0.0.2.2.6'))
        self.proccess = _Loop(self.Bot)
        self.proccess.start()

        _log.Info(Code('0.0.2.2.7'))
        return self.proccess.Ok

    def stop(self) -> bool:
        try:
            _log.Info(Code('0.0.2.2.8'))
            self.proccess.stop = True
        except Exception:
            _log.Error(Code('0.0.2.2.9'))
            return False
        else:
            _log.Info(Code('0.0.2.3.0'))
            self.proccess = None
            return True

class _Loop(threading.Thread):
    def __init__(self, Bot: Bot):
        super(_Loop, self).__init__()
        self.Bot = Bot

        self.Ok   = False
        self.stop = False

    def run(self):
        try:
            (self.loop())
        except Exception:
            self.Ok = False
        else:
            self.Ok = True

    def _await(self, coro) -> None:
        if not coroutines.iscoroutine(coro):
            return coro

        future = asyncio.run_coroutine_threadsafe(coro, self.Bot.Client.loop)

        while not future.done():
            sleep(0.5)

        return future.result()

    def loop(self):
        while not self.stop:
            try:
                for guild in self.Bot.Client.guilds:
                    os.makedirs('{0}/User/{1}/__Guilds__/{2}/'.format(self.Bot.Options.Path, self.Bot.Id, guild.id), 777, True)
                    data = Open('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self.Bot.Options.Path, self.Bot.Id, guild.id))

                    if 'Temps-Mute' in data:
                        for user_id in data['Temps-Mute']:
                            _guild: discord.Guild  = self._await(self.Bot.Client.fetch_guild(guild.id))
                            _user: discord.Member  = self._await(_guild.fetch_member(int(user_id))) if _guild != None else None

                            if _user == None:
                                del data['Temps-Mute'][str(user_id)]
                                Save('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self.Bot.Options.Path, self.Bot.Id, guild.id), data)

                            elif data['Temps-Mute'][str(_user.id)] <= int(monotonic()):
                                try:
                                    self._await(_user.remove_roles(discord.utils.get(_guild.roles, name = 'Mute')))
                                except discord.HTTPException:
                                    pass

                                else:
                                    del data['Temps-Mute'][str(_user.id)]
                                    Save('{0}/User/{1}/__Guilds__/{2}/Main.json'.format(self.Bot.Options.Path, self.Bot.Id, guild.id), data)

                                    self._await(_user.send(embed=discord.Embed(title = 'Tu a été demute du serveur {0}'.format(_guild.name))))
            except Exception as e:
                _log.Error(Code('0.0.2.3.1').format(error = e))

            sleep(1)

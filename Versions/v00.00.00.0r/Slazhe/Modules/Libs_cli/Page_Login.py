from Slazhe import Logger

Log = Logger(__package__)

from .BaseCliModule import SlazheCliModule, get_pm
from .Question      import Page, PageManager, QuestionPage

from .Page_ShowModules  import CliShowModules

from rich.table import Table

from typing import Any

import json, random

from datetime import datetime

from Slazhe.Modules import importer

if hasattr(importer, "PermissionManager"):
    from Slazhe.Modules.Account import PermissionManager, require_permission

def gen_uuid() -> str:
    return ''.join(
        [random.choice('0123456789abcdef') if c == 'x' else random.choice('89ab') 
        if c == 'y' else c for c in 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx']
    )


class SlazheBot:
    is_running: bool = False
    is_bot_started: bool = False
    has_started_error: bool = False
    are_all_intents_enabled: bool = True

    discord_client: Any

    def __init__(self, bot_uuid: str) -> None:
        super(SlazheBot, self).__init__()

        self.bot_uuid: str = bot_uuid

        self.uuid_key: list[int] = None
        self.bot_storage: Any = None

        self.bot_data: dict[str, Any] = {}

        if self.bot_data == {}:
            Log.Error("Bot does not exist.")

        self.bot_info: dict[str, Any] = self.bot_data.get("info", {})

        self.bot_name: str = self.bot_info.get("username", "")
        self.bot_id: str = self.bot_info.get("id", "")

        self.default_guild_ids: list[str] = self.bot_data.get("default_guild", [])
        self.bot_token: str = self.bot_data.get("token", "")

        if self.bot_token == "":
            Log.Error("Bot token is missing.")

        self.command_prefixes: list[str] = self.bot_info.get("prefix", [])

        self.active_cogs: dict[str, Any] = {}
        self.active_commands: dict[str, Any] = {}
        self.cog_listeners: Any = None

        # try:
        #     self.discord_client = Any(self.get_prefix, intents=Any.Intents.all())
        # except Any.errors.PrivilegedIntentsRequired:
        #     self.are_all_intents_enabled = False
        #     self.discord_client = Any(self.get_prefix, intents=Any.Intents.default())

        self.main_commands: Any = None


class UserInfo:
    def __init__(self, user_from_data: str) -> None:
        self.from_data(json.loads(user_from_data))

        self.Bots = [
            SlazheBot(gen_uuid())
        ]

    def from_data(self, user_from_data: dict[str, Any]) -> None:
        self.id: str    = user_from_data.get('id')
        self.uuid: str  = user_from_data.get('uuid')
        self.email: str = user_from_data.get("email", "")
        self.username: str  = user_from_data.get("username")
        self.created_at: str    = user_from_data.get("created_at",  datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        self.updated_at: str    = user_from_data.get("updated_at",  datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        self.preferences: dict[str, Any]    = user_from_data.get("preferences",  {})

        self.bots_length: int = len(user_from_data.get("bots", {}).keys())

    def _edit_profile_info(self, element: str, value: str) -> None:
        if not hasattr(self, element) or element in [ "uuid", "id" ]:
            return Log.Error(f"Unknown attribute: {element}")

        setattr(self, element, value)

class User:
    @classmethod
    def login(self, username: str, password: str) -> None:
        from Slazhe.SlazheModules import importer

        encode_password: list[str] = []
        if getattr(importer, 'SlazheCrypto', False):
            encode_password = importer.SlazheCrypto.GSP(password)
        else:
            Log.Warn('Crypto is not available')
            for char in password:
                encode_password.append(int(ord(char) * 1.141592653589793115997963468544185161590576171875))

        encode_password = "".join([chr(c) for c in encode_password])

        return UserInfo(json.dumps({
            "id": "1122334455566778899",
            "uuid": "avf1dqff-dsqfqs1f-qsf1sqf-1q-q",
            "email": f"{username}@example.com",
            "username": username,
            "created_at": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            "updated_at": datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
        }))

class SlazheLogin(SlazheCliModule):
    """
    CLI module for user login.
    """

    def run(self, username: str, password: str) -> None:
        self.UserClass: UserInfo = User.login(username, password)
        if self.UserClass is None:
            return self.console.print("[red]Connexion échouée[/red]")

        self.quit = False

        def menu():
            self.quit = True

        self.pm = importer.PermissionManager(self.UserClass.uuid, password)

        pages = [
            Page("Se Déconnecter", 1, menu),
            Page("Mon Profile", 2, self.profile),
            Page("Mes Bots", 3, self.bots),
            Page("Page Admin", 4),
            Page("Modules chargés", 5, CliShowModules, attrs={ "parent": self })
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt, title=f"Bonjour {username}")

        while not self.quit:
            page_manager.run()

    def profile(self) -> None:
        self.quit_profile = False

        def profile_quit():
            self.quit_profile = True

        def profile_print():
            Profile_Table = Table(title = "Votre profile", width=int(self.console.width / 2), title_style="")
            Profile_Table.add_column("Name", style="cyan")
            Profile_Table.add_column("Value", style="magenta")

            for Element in dir(self.UserClass):
                if Element not in ["bots_length", "created_at", "email", "id", "username", "uuid"]:
                    continue

                Profile_Table.add_row(Element, str(getattr(self.UserClass, Element)))

            self.console.print(Profile_Table, justify="center")

        pages = [
            Page("Menu", 1, profile_quit),
            Page("Voir mon profile", 2, profile_print),
            Page("Modifier mon profile", 3, self.edit_profile)
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt)

        while not self.quit_profile:
            page_manager.run()

    def edit_profile(self) -> None:
        self.quit_edit_profile = False

        def edit_quit():
            self.quit_edit_profile = True

        pages = [
            Page("Retours", 1, edit_quit),
            Page("Modifier mon Nom", 2, self.UserClass._edit_profile_info, [ QuestionPage("Nouveau Nom", "value", console=self.console, prompt=self.prompt) ], attrs={ "element": "username" }),
            Page("Modifier mon E-mail", 3, self.UserClass._edit_profile_info, [ QuestionPage("Nouvelle E-mail", "value", console=self.console, prompt=self.prompt) ], attrs={ "element": "email" })
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt)

        while not self.quit_edit_profile:
            page_manager.run()

    def bots(self) -> None:
        self.quit_profile = False

        def bots_quit():
            self.quit_profile = True

        def Bots_print():
            Bots_Table = Table(title = "Vos Bots", width=int(self.console.width / 2), title_style="")
            Bots_Table.add_column("Name", style="cyan")
            Bots_Table.add_column("Value", style="magenta")

            for Bot in self.UserClass.Bots:
                for Element in dir(Bot):
                    if Element not in ["is_running", "is_bot_started", "has_started_error", "are_all_intents_enabled", "bot_uuid", "bot_name", "bot_id", "default_guild_ids", "command_prefixes"]:
                        continue

                    Bots_Table.add_row(Element, str(getattr(Bot, Element)))
                Bots_Table.add_row("", "", end_section=True)
            self.console.print(Bots_Table, justify="center")

        pages = [
            Page("Menu", 1, bots_quit),
            Page("Voir les bots", 2, Bots_print),
            Page("Modifier un bot", 3)
        ]

        page_manager = PageManager(pages, console=self.console, prompt=self.prompt)

        while not self.quit_profile:
            page_manager.run()
# Version Globale: v00.00.00.0r
# Version du fichier: v00.00.00.01

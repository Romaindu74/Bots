from Slazhe import Logger

Log = Logger(__name__)

try:
    from requests                   import Session, exceptions, Response as _REP
except ImportError:
    try:
        from pip._vendor.requests   import Session, exceptions, Response as _REP
    except ImportError:
        Log.Error('Module requests is not found.')
        exit(1)
except Exception as e:
    Log.Error('Import Error: ', e)
    exit(1)

from urllib.parse   import quote as _uriquote
from typing         import ClassVar, Optional, Union, Any

class Route:
    BaseUrl: ClassVar[str] = 'https://raw.githubusercontent.com/Romaindu74/Bots/main/v2/'

    def __init__(self, method: str, path: str, BaseUrl: Optional[str] = None, **parameters: Any) -> None:
        self.path:   str            = path
        self.method: str            = method
        self.params: dict[str, Any] = parameters

        if not BaseUrl:
            url = self.BaseUrl + self.path
        else:
            url = BaseUrl + self.path
    
        if parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        self.url: str = url

class HTTPClient:
    def __init__(self) -> None:
        self.session = Session()

    @property
    def headers(self) -> dict[str, Any]:
        return {}

    def request(self, route: Route, base: Optional[str] = None, **params) -> _REP:
        if base:
            route = Route(route.method, route.path, base, **route.params)

        method: str = route.method
        url:    str = route.url

        try:
            result: _REP = self.session.request(method, url, headers = self.headers, **params)
        except exceptions.RequestException:
            pass
        else:
            return result

class Response:
    _Response__data: dict[str, Any]
    commands:        list['DCResponse']

    def __init__(self, data: Union[_REP, dict[str, Any]]) -> None:
        self.success: bool  = False
        self.deleted: bool  = False


        self.__data: dict[str, Any] = data

        if isinstance(data, _REP):
            if data.status_code == 200:
                self.success = True

            if data.status_code == 204:
                self.deleted    = True
                self.__data     = {}

            else:
                self.__data: dict[str, Any] = data.json()

        if isinstance(self.__data, dict):
            for key, value in self.__data.items():
                setattr(self, key, value)

        elif isinstance(self.__data, list):
            self.commands = []

            for item in self.__data:
                if isinstance(item, dict):
                    self.commands.append(Response(item))

class DCResponse(Response):
    id:                         str
    application_id:             str
    version:                    str
    name:                       str
    description:                str
    default_member_permissions: str
    contexts:                   Any
    dm_permission:              bool
    nsfw:                       bool
    type:                       int
    integration_types:          list[int]

    options:                    Optional[list[dict[str, Any]]]

class CGACResponse(DCResponse):
    name_localizations:         Any
    description_localizations:  Any
    guild_id:                   int

class SlashCommand(HTTPClient):
    def __init__(self, BotId: Union[str, int], BotToken: str) -> None:
        self.BotId      = BotId
        self.BotToken   = BotToken

        self.session    = Session()
        self.BASE: str  = 'https://discord.com/api/v10/applications/'

    def request(self, route, **params) -> Response:
        return Response(super().request(route, base = self.BASE, **params))

    ################################

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": "Bot {0}".format(self.BotToken)
        }

    ################################

    def Get_Global_Application_Commands(self) -> Response:
        r = Route(
            'GET',
            '{Id}/commands',
            Id = self.BotId
        )
        return self.request(r)

    def Create_Global_Application_Command(self, value: dict[str, Any]) -> CGACResponse:
        r = Route(
            'POST',
            '{Id}/commands',
            Id = self.BotId
        )
        return self.request(r, json = value)

    def Get_Global_Application_Command(self, CommandId: Union[str, int]) -> CGACResponse:
        r = Route(
            'GET',
            '{Id}/commands/{CommandId}',
            Id          = self.BotId,
            CommandId   = CommandId
        )
        return self.request(r)

    def Edit_Global_Application_Command(self, CommandId: Union[str, int], value: dict[str, Any]) -> CGACResponse:
        r = Route(
            'PATCH',
            '{Id}/commands/{CommandId}',
            Id          = self.BotId,
            CommandId   = CommandId
        )
        return self.request(r, json = value)

    def Delete_Global_Application_Command(self, CommandId: Union[str, int]) -> Response:
        r = Route(
            'DELETE',
            '{Id}/commands/{CommandId}',
            Id          = self.BotId,
            CommandId   = CommandId
        )
        return self.request(r)

    def Get_Guild_Application_Commands(self, GuildId: Union[str, int]) -> Response:
        r = Route(
            'GET',
            '{Id}/guilds/{GuildId}/commands',
            Id          = self.BotId,
            GuildId     = GuildId
        )
        return self.request(r)

    def Create_Guild_Application_Command(self, GuildId: Union[str, int], value: dict[str, Any]) -> CGACResponse:
        r = Route(
            'POST',
            '{Id}/guilds/{GuildId}/commands',
            Id          = self.BotId,
            GuildId     = GuildId
        )
        return self.request(r, json = value)

    def Get_Guild_Application_Command(self, GuildId: Union[str, int], CommandId: Union[str, int]) -> CGACResponse:
        r = Route(
            'GET',
            '{Id}/guilds/{GuildId}/commands/{CommandId}',
            Id          = self.BotId,
            GuildId     = GuildId,
            CommandId   = CommandId
        )
        return self.request(r)

    def Edit_Guild_Application_Command(self, GuildId: Union[str, int], CommandId: Union[str, int], value: dict[str, Any]) -> CGACResponse:
        r = Route(
            'PATCH',
            '{Id}/guilds/{GuildId}/commands/{CommandId}',
            Id          = self.BotId,
            GuildId     = GuildId,
            CommandId   = CommandId
        )
        return self.request(r, json = value)

    def Delete_Guild_Application_Command(self, GuildId: Union[str, int], CommandId: Union[str, int]) -> Response:
        r = Route(
            'DELETE',
            '{Id}/guilds/{GuildId}/commands/{CommandId}',
            Id          = self.BotId,
            GuildId     = GuildId,
            CommandId   = CommandId
        )
        return self.request(r)

    def Get_Guild_Application_Command_Permissions(self, GuildId: Union[str, int]) -> Response:
        r = Route(
            'GET',
            '{Id}/guilds/{GuildId}/commands/permissions',
            Id          = self.BotId,
            GuildId     = GuildId
        )
        return self.request(r)

    def Get_Application_Command_Permissions(self, GuildId: Union[str, int], CommandId: Union[str, int]):
        r = Route(
            'GET',
            '{Id}/guilds/{GuildId}/commands/{CommandId}/permissions',
            Id          = self.BotId,
            GuildId     = GuildId,
            CommandId   = CommandId
        )
        return self.request(r)

    def Edit_Application_Command_Permissions(self, GuildId: Union[str, int], CommandId: Union[str, int], value: dict[str, Any]):
        r = Route(
            'PUT',
            '{Id}/guilds/{GuildId}/commands/{CommandId}/permissions',
            Id          = self.BotId,
            GuildId     = GuildId,
            CommandId   = CommandId
        )
        return self.request(r, json = value)

class SlazheMain(HTTPClient):
    def request(self, route, **params):
        return super().request(route, **params)
    
    @classmethod
    def get_modules(cls) -> list[dict[str, str]]:
        r = Route(
            'GET',
            '/src/modules/PythonModules.json'
        )

        result = cls().request(r)
        return [] if not result or result.status_code != 200 else result.json().get('modules', [])
# Version Globale: v00.00.00.0j
# Version du fichier: v00.00.00.01

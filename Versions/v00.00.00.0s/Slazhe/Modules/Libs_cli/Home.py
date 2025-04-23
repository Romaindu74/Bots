from Slazhe import Logger

Log = Logger(__package__)

from typing import Optional
from .Title import text_to_Chars

from .Question  import Page, PageManager, QuestionPage

from rich.console   import Console
from rich.prompt    import Prompt
from rich.align     import Align

TextCenter = Align.center

from .Page_ShowModules  import CliShowModules
from .Page_Login        import SlazheLogin
from .Page_Exit         import CliExit

class SlazheCli:
    """
    Main CLI class for Slazhe.
    """

    _instance: Optional['SlazheCli'] = None

    def __new__(cls) -> 'SlazheCli':
        """
        Singleton pattern to ensure only one instance of SlazheCli.

        Returns:
            SlazheCli: The singleton instance of SlazheCli.
        """
        if cls._instance is None:
            cls._instance = super(SlazheCli, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Slazhe CLI.
        """
        self.console = Console()
        self.prompt = Prompt(console=self.console)
        self.stop: bool = False

        self.pages = [
            Page("Se Connecter", 1, SlazheLogin, [
                QuestionPage("Votre nom d'utilisateur", "username", console=self.console, prompt=self.prompt),
                QuestionPage("Votre mot de passe", "password", console=self.console, prompt=self.prompt, password=True)
            ], attrs={ "parent": self }),
            Page("Modules chargés", 2, CliShowModules, attrs={ "parent": self }),
            Page("Quitter", 3, CliExit, [ QuestionPage("êtes-vous sûrs ? (oui/non)", "ok", console=self.console, prompt=self.prompt) ], attrs={ "parent": self }),
        ]

        self.allowed_pages = [1, 2, 3]
        self.page_manager = PageManager(self.pages, self.allowed_pages, console=self.console, prompt=self.prompt, title="Bienvenue sur Slazhe Bot's")

    def error(self, text: str) -> None:
        """
        Print an error message to the console.

        Args:
            text (str): The error message to print.
        """
        self.console.print(text, style="red")
        Log.Error(f"Error: {text}")

    def run(self) -> None:
        """
        Run the main CLI loop.
        """
        title = text_to_Chars("Slazhe") + "\n\n"
        self.console.print(TextCenter(title))

        while not self.stop:
            self.page_manager.run()
# Version Globale: v00.00.00.0s
# Version du fichier: v00.00.00.01

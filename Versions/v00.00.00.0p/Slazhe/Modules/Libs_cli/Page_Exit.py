from Slazhe import Logger

Log = Logger(__package__)

from .BaseCliModule import SlazheCliModule

class CliExit(SlazheCliModule):
    """
    CLI module to exit the application.
    """

    def run(self, ok: str = "non") -> None:
        if ok.lower() != "oui":
            return

        """
        Exit the application.
        """
        import sys
        Log.Info("Exiting the application.")
        sys.exit(0)

# Version Globale: v00.00.00.0p
# Version du fichier: v00.00.00.01

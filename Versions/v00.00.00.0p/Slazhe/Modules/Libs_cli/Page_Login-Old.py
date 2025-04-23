from Slazhe import Logger

Log = Logger(__package__)

from .BaseCliModule import SlazheCliModule
from .Question      import Page, PageManager, QuestionPage

from .Page_ShowModules  import CliShowModules

class SlazheLogin(SlazheCliModule):
    """
    CLI module for user login.
    """

    def run(self, username: str, password: str) -> None:
        """
        Placeholder for login functionality.
        """
        pages = [
            Page("Se déconnecter", 1, self.logout),
            Page("Voir les modules chargés", 2, CliShowModules, attrs={ "parent": self }),
            Page("Mon Profil", 3, self.profile)
            # Page("Information", 5, self.information),
            # Page("Modules Python", 6, self.python_module_installer, [
            #     QuestionPage("Entrer le nom du module lors d'un import", "import_name", console=self.console, prompt=self.prompt),
            #     QuestionPage("Entrer le nom du module lors de l'instalation", "pip_name", console=self.console, prompt=self.prompt)
            # ])
        ]

        self.quit = False

        allowed_pages = [i for i in range(1, len(pages) + 1)]
        page_manager = PageManager(pages, allowed_pages, console=self.console, prompt=self.prompt, title=f"Bonjour {username}")

        while not self.quit:
            page_manager.run()

    def logout(self) -> None:
        self.quit = True

    def profile(self) -> None:
        pass

    # def python_module_installer(self, import_name: str, pip_name: str) -> None:
    #     from Slazhe.SlazheModules import importer

    #     if not hasattr(importer, 'InstallerModules'):
    #         return Log.Error("Installer modules not available.")

    #     InstallerModules = importer.InstallerModules([{"pip-name": pip_name, "import-name": import_name}])
    #     InstallerModules.check()

    # def information(self) -> None:
    #     import curses
    #     import psutil
    #     import time

    #     def main(stdscr):
    #         # Clear screen
    #         stdscr.clear()

    #         # Initialize colors
    #         curses.start_color()
    #         curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    #         curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #         curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    #         curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    #         # Main loop
    #         while True:
    #             stdscr.clear()

    #             # Get system information
    #             cpu_percent = psutil.cpu_percent(interval=1)
    #             mem_info = psutil.virtual_memory()

    #             # Display CPU and Memory usage
    #             try:
    #                 stdscr.addstr(0, 0, f"CPU Usage: {cpu_percent}%", curses.color_pair(1))
    #                 stdscr.addstr(1, 0, f"Memory Usage: {mem_info.percent}%", curses.color_pair(2))
    #             except curses.error as e:
    #                 stdscr.addstr(0, 0, f"Error: {e}", curses.color_pair(2))

    #             # Display processes
    #             try:
    #                 stdscr.addstr(3, 0, "PID   NAME               CPU%   MEM%", curses.color_pair(3))
    #             except curses.error as e:
    #                 stdscr.addstr(3, 0, f"Error: {e}", curses.color_pair(2))

    #             stdscr.refresh()
    #             time.sleep(1)

    #     try:
    #         curses.wrapper(main)
    #     except KeyboardInterrupt:
    #         pass
# Version Globale: v00.00.00.0p
# Version du fichier: v00.00.00.01

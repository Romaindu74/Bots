from Slazhe import Logger

Log = Logger(__package__)

from typing import Any, Dict, List, Optional, Callable

from .Libs  import page_not_set

from rich.console   import Console
from rich.prompt    import Prompt
from rich.table     import Table

import inspect

class QuestionPage:
    def __init__(self, question: str, variable: str = None, *, console: Console = None, prompt: Prompt = None, password: bool = False, choices: List[str] = None, case_sensitive: bool = True, show_default: bool = True, show_choices: bool = True):
        self.question   = question
        self.console    = console or Console()
        self.prompt     = prompt or Prompt(console = self.console)
        self.password   = password
        self.choices    = choices
        self.case_sensitive = case_sensitive
        self.show_default   = show_default
        self.show_choices   = show_choices
        self.variable   = variable

    def run(self) -> Any:
        result: Any = None

        while result is None:
            try:
                result = self.prompt.ask(self.question, console = self.console, password = self.password,
                                    choices = self.choices, case_sensitive = self.case_sensitive,
                                    show_default = self.show_default, show_choices = self.show_choices)
            except KeyboardInterrupt:
                Log.Warning("KeyboardInterrupt caught.")
                continue

        return result

class Page:
    """
    Represents a page in the CLI.
    """

    def __init__(self, title: str, page_id: int, page_class: Callable = page_not_set, questions: Optional[List[QuestionPage]] = None, attrs: Dict[str, Any] = {}) -> None:
        """
        Initialize a Page.

        Args:
            title (str): The title of the page.
            page_id (int): The ID of the page.
            page_class (Type[SlazheCliModule]): The class of the page.
            run_method (str): The method to run on the page class.
            questions (Optional[List[str]]): List of questions to ask before running the method.
        """
        self.title = title
        self.page_id = page_id
        self.page_class = page_class
        self.questions = questions or []
        self.attrs = attrs

    def run(self) -> None:
        """
        Run the page.

        Args:
            parent (SlazheCli): The parent CLI instance.
        """
        instance = self.page_class
        kwargs   = {}
        args     = []

        for question in self.questions:
            if not isinstance(question, QuestionPage):
                continue

            if question.variable:
                kwargs[question.variable] = question.run()
            else:
                args.append(question.run())

        if inspect.isfunction(instance) or inspect.ismethod(instance):
            instance(*args, **{**kwargs, **self.attrs.copy()})
        else:
            method = instance(**self.attrs.copy())
            if hasattr(method, 'run'):
                method.run(*args, **kwargs)

class PageManager:
    """
    Manages the pages in the CLI.
    """

    def __init__(self, pages: List[Page], allowed_pages: List[int] = None, *, console: Console = None, prompt: Prompt = None, title: str = "") -> None:
        """
        Initialize the PageManager.

        Args:
            pages (List[Page]): The list of pages.
            allowed_pages (List[int]): The list of allowed page IDs.
        """
        self.pages = pages
        self.allowed_pages = allowed_pages or [i for i in range(1, len(pages) + 1)]
        self.title = title
        self.console = console or Console()
        self.prompt  = prompt  or Prompt(console=self.console)

    def get_table_pages(self) -> Table:
        """
        Create a table of available pages.

        Args:
            console (Console): The console instance.

        Returns:
            Table: A Rich Table object containing the pages.
        """
        table = Table(title=self.title, width=int(self.console.width / 2), title_style="")
        table.add_column("Id", style="cyan", no_wrap=True)
        table.add_column("Nom", style="magenta")

        for page in self.pages:
            style = "strike" if page.page_id not in self.allowed_pages else ""
            table.add_row(str(page.page_id), page.title, style=style)

        Log.Debug("Pages table created.")
        return table

    def get_page_by_id(self, page_id: int) -> Optional[Page]:
        """
        Get a page by its ID.

        Args:
            page_id (int): The ID of the page.

        Returns:
            Optional[Page]: The page if found, otherwise None.
        """
        return next((page for page in self.pages if page.page_id == page_id), None)

    def run(self) -> None:
        self.console.print(self.get_table_pages(), justify="center")
        try:
            option = int(self.prompt.ask("Choisissez une option") or "0")
        except KeyboardInterrupt:
            return Log.Warning("KeyboardInterrupt caught.")
        except ValueError:
            return Log.Warning("Invalid input. Please enter a number.")

        selected_page = self.get_page_by_id(option)
        if not selected_page or option not in self.allowed_pages:
            return Log.Warning(f"Option {option} is not allowed.")

        try:
            selected_page.run()
        except Exception as e:
            return Log.Error(f"Exception in function {selected_page.title}: {e}")

# Version Globale: v00.00.00.0n
# Version du fichier: v00.00.00.01

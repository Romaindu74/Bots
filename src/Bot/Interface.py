from .GetLang       import Code
from .Logger        import Logger
from .Utils         import Save, Open, MISSING
from .type.Bot      import Bot
from .type.Options  import Options

_log = Logger(__name__)

from typing         import Union
from tkinter        import messagebox

import shutil
import tkinter as tk
import os, threading

try:
    from PIL        import Image, ImageTk
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'pillow'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

try:
    import signal
except ImportError:
    _log.Critical(Code('0.0.0.0.0').format(Module = 'signal'), Exit = True)
except Exception as e:
    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)), Exit = True)

class Interface(threading.Thread):
    def __init__(self, options: Options = MISSING) -> None:
        super(Interface, self).__init__()
        _log.Info(Code('0.0.1.3.2'))

        self.check                           = False

        if options == MISSING:
            _log.Critical(Code('0.0.1.3.0').format(error = Code('0.0.1.3.1')))

        else:
            self.check = True

        self.interface__: bool               = False

        self.options:     Options            = options

        self.Initialized: bool               = False
        self._main_:      tk.Tk              = None 

        self.add_bot_LabelFrame              = None
        self.bots_: dict[tk.LabelFrame]      = {}

        self.language_: list                 = []
        self.conf_                           = None
        _log.Info(Code('0.0.1.3.3'))

    def run(self) -> None:
        _log.Info(Code('0.0.1.3.4'))
        try:
            self._main__ = tk.Tk()
        except Exception:
            _log.Critical(Code('0.0.1.3.5'))
            self.interface__ = False
            self.Initialized = False
            return

        self._main_  = tk.Frame(self._main__)
        self._main_.place(width=900, height=500)

        self._main__.title(self.options.Info.get('Windows-Title', 'Sayu#0475'))
        self._main__.geometry('900x500')
        self._main__.resizable(False, False)

        if os.path.exists(self.options.Path+'/Bot/icon.png'):
            _log.Info(Code('0.0.1.3.6'))
            self._main__.iconphoto(False, tk.PhotoImage(file=self.options.Path+'/Bot/icon.png'))

        try:
            self.Initialized = True
            self.interface__ = True
            _log.Info(Code('0.0.1.3.7'))
            self._main__.mainloop()
            self.interface__ = False
            self.stop()
        except Exception:
            self.interface__ = False
            self.Initialized = False

    def _scroll_bar(self) -> None:
        _log.Info(Code('0.0.1.3.8'))
        self.ScrollBar = tk.Scrollbar(self._main__)
        self.ScrollBar.pack(fill = tk.BOTH, side = tk.RIGHT)
        _log.Info(Code('0.0.1.3.9'))

    def stop(self) -> None:
        _log.Info(Code('0.0.1.4.0'))
        if self.interface__ == True:
            _log.Info(Code('0.0.1.4.1'))
            self._main__.destroy()
            self._main__.quit()
        _log.Info(Code('0.0.1.4.2'))
        for Bot in self.options.Bots:
            try:
                if self.options.Bots[Bot].Status_ != '0.0.0.3.3':
                    self.options.Bots[Bot].Stop()
            except Exception as e:
                _log.Critical(Code('0.0.1.3.0').format(error = str(e)))

        os.kill(os.getpid(), signal.SIGTERM)

    def Menu(self, main: tk.Tk) -> tk.Menu:
        _log.Info(Code('0.0.1.4.3'))
        _main_:    tk.Menu = tk.Menu(main)

        _options_: tk.Menu = tk.Menu(_main_, tearoff=0)

        _log.Info(Code('0.0.1.4.4'))
        _options_.add_command(label = Code('0.0.1.4.6'), command = self.change_language)
        _options_.add_command(label = Code('0.0.1.4.7'), command = self.add_bot)
        _options_.add_command(label = Code('0.0.1.4.8'), command = self.stop)

        _main_.add_cascade(label = Code('0.0.1.4.9'), menu = _options_)
        _log.Info(Code('0.0.1.4.5'))

        return _main_

    def add_bot(self) -> None:
        if self.Config != None:
            self.Config.destroy()
            self.Config = None

        _log.Info(Code('0.0.1.5.0'))
        try:
            list(self.bots_.items())[0][1][2].destroy()
        except IndexError:
            pass

        self.bots_ = {}

        _main_ = tk.Frame(self._main_)
        _main_.pack(expand=tk.YES)

        self.Config = _main_

        self._main__.title(Code('0.0.1.4.7'))

        LabelFrame = tk.LabelFrame(_main_, text = Code('0.0.1.4.7'))
        self.add_bot_LabelFrame = LabelFrame
        LabelFrame.pack(fill = tk.BOTH, expand = tk.YES)

        self.Label_1 = tk.Label(LabelFrame, text=Code('0.0.1.5.1'))
        self.Label_1.grid(column = 0, row = 0, sticky=tk.W)

        self.Input_1 = tk.Entry(LabelFrame, width=50)
        self.Input_1.grid(column = 0, row = 1, sticky=tk.W)

        self.Label_2 = tk.Label(LabelFrame, text=Code('0.0.1.5.2'))
        self.Label_2.grid(column = 0, row = 2, sticky=tk.W)

        self.Input_2 = tk.Entry(LabelFrame, width=50)
        self.Input_2.grid(column = 0, row = 3, sticky=tk.W)

        self.Label_3 = tk.Label(LabelFrame, text=Code('0.0.1.5.3'))
        self.Label_3.grid(column = 0, row = 4, sticky=tk.W)

        self.Input_3 = tk.Entry(LabelFrame, width=100)
        self.Input_3.grid(column = 0, row = 5)

        self.Error_1 = tk.Label(LabelFrame)
        self.Error_1.grid(column = 0, row = 6)

        Button_1  = tk.Button(LabelFrame, text=Code('0.0.1.5.4'), command = self.add_bot_add)
        Button_1.grid(column = 0, row = 7, sticky=tk.W)

        Button_2  = tk.Button(LabelFrame, text=Code('0.0.1.5.5'), command=self.add_bot_cancel)
        Button_2.grid(column = 1, row = 7, sticky=tk.E)
        _log.Info(Code('0.0.1.5.6'))

    def add_bot_add(self) -> None:
        if self.add_bot_LabelFrame is not None:
            if self.Input_1.get() == '' or self.Input_2.get() == '' or self.Input_3.get() == '':
                _log.Warn(Code('0.0.1.5.7'))
                self.Error_1.config(text = Code('0.0.1.5.8'), fg = 'red')
            else:
                _log.Info(Code('0.0.1.5.9'))
                if not os.path.exists('{0}/User/Bots/Bots.json'.format(self.options.Path)):
                    os.makedirs('{0}/User/Bots'.format(self.options.Path), exist_ok = True)
                    Save('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': []})

                Bots = Open('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': []}).get('Bots', [])
                Bots.append(str(self.Input_1.get()))
                Save('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': Bots})

                _log.Info(Code('0.0.1.6.0'))
                if not os.path.exists('{0}/User/Bots/{1}/'.format(self.options.Path, str(self.Input_1.get()))):
                    os.makedirs('{0}/User/Bots/{1}/'.format(self.options.Path, str(self.Input_1.get())), exist_ok = True)

                self.Bot_Info = Open('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, str(self.Input_1.get())), {})
                self.Bot_Info['Id']    = str(self.Input_1.get())
                self.Bot_Info['Name']  = str(self.Input_2.get())
                self.Bot_Info['Token'] = str(self.Input_3.get())

                Save('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, str(self.Input_1.get())), self.Bot_Info)
                self.options.add(str(self.Input_1.get()))

                self.add_bot_cancel()

    def add_bot_cancel(self) -> None:
        if self.add_bot_LabelFrame is not None:
            self.add_bot_LabelFrame.destroy()
            self.Bots()

    def Bots(self) -> Union[None, bool]:
        if self.Config != None:
            self.Config.destroy()
            self.Config = None

        container        = tk.Frame(self._main_)
        canvas           = tk.Canvas(container)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.config(
                scrollregion=canvas.bbox('all')
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        self.ScrollBar.config(command = canvas.yview)

        container.pack(fill = tk.BOTH, expand = tk.YES)

        canvas.config(yscrollcommand=self.ScrollBar.set, width=self._main__.winfo_width(), height=self._main__.winfo_height())
        canvas.pack(side='left', fill = tk.BOTH)

        self.Config = container

        self._main__.title(self.options.Info.get('Windows-Title', 'Sayu#0475'))
        if not os.path.exists(self.options.Path+'/User/Bots/Bots.json'):
            _log.Warn(Code('0.0.1.6.1'))
            return False

        _log.Info(Code('0.0.1.6.2'))
        for Bot in self.options.Bots:
            Bot_ = BotConfig(self, self.options.Bots[Bot], self.options)
            Frame: tk.Frame = tk.Frame(scrollable_frame)
            Frame.pack(fill = tk.BOTH, expand = tk.YES)

            LabelFrame: tk.LabelFrame = tk.LabelFrame(Frame, text = self.options.Bots[Bot].Info.get('Name', ''))
            LabelFrame.pack(fill = tk.BOTH, expand = tk.YES)

            if os.path.exists(self.options.Path+'/User/Bots/Images/{0}.png'.format(Bot)):
                Image_ = Image.open(self.options.Path+'/User/Bots/Images/{0}.png'.format(Bot)).resize((64, 64), Image.LINEAR)
                Image__ = ImageTk.PhotoImage(Image_)

                Label_ = tk.Label(LabelFrame, image=Image__)
                Label_.image = Image__
                Label_.grid(column = 0)

            Button_: tk.Button = tk.Button(LabelFrame, text = Code('0.0.1.6.3'), command = Bot_.Config)
            Button_.grid(column = 0, row = 1)

            Label__ = tk.Label(LabelFrame, text = Code('0.0.1.6.4').format(status = Code(self.options.Bots[Bot].Status_)))
            Label__.grid(column = 1, row = 0)

            if self.options.Bots[Bot].Status_ != '0.0.0.3.3':
                Button__: tk.Button = tk.Button(LabelFrame, text = Code('0.0.1.6.5'), command = Bot_.Stop)
            else:
                Button__: tk.Button = tk.Button(LabelFrame, text = Code('0.0.1.6.6'), command = Bot_.Start)

            Button__.grid(column = 1, row = 1)

            self.bots_[Bot] = [Frame, LabelFrame, container]
        _log.Info(Code('0.0.1.6.7'))

    def UpDate_Bot(self, Id: str) -> None:
        _log.Info(Code('0.0.1.6.8').format(bot = Id))
        self.bots_[Id][1].destroy()
        Bot_ = BotConfig(self, self.options.Bots[Id], self.options)

        Frame: tk.Frame = self.bots_[Id][0]

        LabelFrame: tk.LabelFrame = tk.LabelFrame(Frame, text = self.options.Bots[Id].Info.get('Name', ''))
        LabelFrame.pack(fill = tk.BOTH, expand = tk.YES)

        if os.path.exists(self.options.Path+'/User/Bots/Images/{0}.png'.format(Id)):
            Image_ = Image.open(self.options.Path+'/User/Bots/Images/{0}.png'.format(Id)).resize((64, 64), Image.LINEAR)
            Image__ = ImageTk.PhotoImage(Image_)

            Label_ = tk.Label(LabelFrame, image=Image__)
            Label_.image = Image__
            Label_.grid(column = 0)

            Button_: tk.Button = tk.Button(LabelFrame, text = Code('0.0.1.6.3'), command = Bot_.Config)
            Button_.grid(column = 0, row = 1)

            Label__ = tk.Label(LabelFrame, text = Code('0.0.1.6.4').format(status = Code(self.options.Bots[Id].Status_)))
            Label__.grid(column = 1, row = 0)

            if self.options.Bots[Id].Status_ != '0.0.0.3.3':
                Button__: tk.Button = tk.Button(LabelFrame, text = Code('0.0.1.6.5'), command = Bot_.Stop)
            else:
                Button__: tk.Button = tk.Button(LabelFrame, text = Code('0.0.1.6.6'), command = Bot_.Start)

            Button__.grid(column = 1, row = 1)

        self.bots_[Id] = [Frame, LabelFrame, self.bots_[Id][2]]
        _log.Info(Code('0.0.1.6.9').format(bot = Id))

    def change_language(self) -> None:
        if self.Config != None:
            self.Config.destroy()
            self.Config = None

        try:
            list(self.bots_.items())[0][1][2].destroy()
        except IndexError:
            pass

        self.bots_ = {}

        _main_ = tk.Frame(self._main_)
        _main_.pack(expand=tk.YES)

        self.Config = _main_

        self._main__.title(Code('0.0.1.4.6'))

        self._ListBot_ = tk.Listbox(_main_, selectmode=tk.SINGLE)

        self._ListBot_.config(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.config(command=self._ListBot_.yview)

        _log.Info(Code('0.0.1.7.0'))
        if self.language_ == []:
            with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Language.json') as r:
                try:
                    self.language_: list[str] = r.json()
                    _log.Info(Code('0.0.1.7.1'))
                except Exception as e:
                    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                    return False

        index = 0

        for i in self.language_:
            self._ListBot_.insert(index, i.replace('.json', ''))
            index += 1

        self._ListBot_.config(yscrollcommand = self.ScrollBar.set, width=self._main__.winfo_width(), height=self._main__.winfo_height())

        self._ListBot_.pack(side = tk.LEFT, fill = tk.BOTH, expand = tk.YES)

        self._ListBot_.bind('<Double-1>', self.change_language_save)

    def change_language_save(self, event: tk.Event) -> None:
        language = self._ListBot_.get(self._ListBot_.curselection())
        os.makedirs('{0}/Bot/Language/'.format(self.options.Path), 777, True)
        _log.Info(Code('0.0.1.7.2').format(file = str(language)+'.json'))
        if not str(language)+'.json' in [f for f in os.listdir('{0}/Bot/Language/'.format(self.options.Path)) if os.path.isfile(os.path.join('{0}/Bot/Language/'.format(self.options.Path), f))]:
            _log.Info(Code('0.0.1.7.3').format(file = str(language)))
            f = open('{0}/Bot/Language/{1}'.format(self.options.Path, str(language)+'.json'), 'wb+')
            with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Language/{0}'.format(str(language)+'.json')) as r:
                try:
                    f.write(r.content)
                except Exception as e:
                    _log.Critical(Code('0.0.0.0.1').format(file = __file__, error = str(e)))
                    return False
                f.close()
            _log.Info(Code('0.0.1.7.4'))

        else:
            _log.Info(Code('0.0.1.7.5'))

        os.makedirs('{0}/User/__Json__/'.format(self.options.Path), 777, True)
        main = Open('{0}/User/__Json__/Main.json'.format(self.options.Path))
        main['Lang'] = language
        Save('{0}/User/__Json__/Main.json'.format(self.options.Path), main)

        _log.Info(Code('0.0.1.7.6'))
        self._main__.config(menu = self.Menu(self._main__))
        self.cancel()

    def cancel(self) -> None:
        if self._ListBot_ is not None:
            self._ListBot_.destroy()
        self.Bots()


    def Start(self) -> None:
        _log.Info(Code('0.0.1.7.7'))
        self._scroll_bar()
        self._main__.config(menu = self.Menu(self._main__))
        self.Bots()

    @property
    def Config(self) -> Union[tk.Frame, tk.LabelFrame, tk.Label, None]:
        return self.conf_

    @Config.setter
    def Config(self, value: Union[tk.Frame, tk.LabelFrame, tk.Label, None] = MISSING) -> Union[tk.Frame, tk.LabelFrame, tk.Label, None]:
        if not value == MISSING:
            self.conf_ = value
        return self.conf_

class BotConfig(object):
    def __init__(self, main: Interface, Bot: Bot, options: Options):
        self.main    = main
        self.bot     = Bot
        self.options = options

        self.bot.Interface = self.main

    def Config(self) -> None:
        if self.main.Config != None:
            self.main.Config.destroy()
            self.main.Config = None

        _log.Info(Code('0.0.1.8.5'))
        self._main_      = tk.Frame(self.main._main_)
        self._main_.pack(fill=tk.BOTH, expand = tk.YES)

        self.main.Config = self._main_

        self.main._main__.title(self.bot.Info.get('Name', self.options.Info.get('Windows-Title', 'Sayu#0475')))

        self.main.bots_[self.bot.Id][2].destroy()

        self.LabelFrame         = tk.LabelFrame(self._main_, text = Code('0.0.2.1.5'))
        self.LabelFrame.pack(fill = tk.BOTH, expand=tk.YES)

        self.Bot_Name           = tk.Label(self.LabelFrame, text = Code('0.0.2.1.6').format(bot = self.bot.Info.get('Name', '...')))
        self.Bot_Name.grid(sticky='w')

        self.Bot_Id             = tk.Label(self.LabelFrame, text = Code('0.0.2.1.7').format(bot = self.bot.Info.get('Id', '...')))
        self.Bot_Id.grid(sticky='w')

        self.Bot_Statu          = tk.Label(self.LabelFrame, text = Code('0.0.2.1.8').format(status = Code(self.bot.Status_)))
        self.Bot_Statu.grid(sticky='w')

        self.Bot_Prefix         = tk.Label(self.LabelFrame, text = Code('0.0.1.7.8').format(prefix = self.bot.Prefix.get('Prefix', [])))
        self.Bot_Prefix.grid(sticky='w')

        self.Discord_LabelFrame = tk.LabelFrame(self._main_, text = Code('0.0.1.7.9'))
        self.Discord_LabelFrame.pack(fill='both', expand='yes')

        self.Bot_Ms             = tk.Label(self.Discord_LabelFrame, text = Code('0.0.1.8.0').format(ping = self.bot.Ping))
        self.Bot_Ms.grid(sticky='w')

        self.Statut_LabelFrame  = tk.LabelFrame(self._main_, text = Code('0.0.1.8.1'))
        self.Statut_LabelFrame.pack(fill='both', expand='yes')

        try:
            self.Bot_Activite       = tk.Label(self.Statut_LabelFrame, text = Code('0.0.1.8.2').format(activity = self.bot.Status.Activity, text = self.bot.Status.Text))
            self.Bot_Activite.grid(sticky='w')

            self.Bot_Statut         = tk.Label(self.Statut_LabelFrame, text = Code('0.0.1.8.3').format(display = self.bot.Status.Statu))
            self.Bot_Statut.grid(sticky='w')

            self.Bot_Statut_Time    = tk.Label(self.Statut_LabelFrame, text = Code('0.0.1.8.4').format(time = self.bot.Status.Time))
            self.Bot_Statut_Time.grid(sticky='w')


            self.bot.Status.Interface(self.Bot_Activite, self.Bot_Statut, self.Bot_Statut_Time, self.Bot_Ms)
            self.bot.Status.Is_Config = True

        except AttributeError:
            pass

        self.Main               = tk.Button(self._main_, text = Code('0.0.2.1.9'), command=self._Main)
        self.Main.pack(fill = tk.BOTH)


        self._Prefix               = tk.Button(self._main_, text = Code('0.0.2.2.0'), command=self.Prefix)
        self._Prefix.pack(fill = tk.BOTH)

        self._Owner               = tk.Button(self._main_, text = Code('0.0.2.2.1'), command=self.Owner)
        self._Owner.pack(fill = tk.BOTH)


        self._Owner               = tk.Button(self._main_, text = Code('0.0.1.8.7'), command=self.Sup_Bot, fg = 'red')
        self._Owner.pack(fill = tk.BOTH)
        _log.Info(Code('0.0.1.8.6'))

    def Sup_Bot(self):
        if not messagebox.askyesno(Code('0.0.1.8.7'), Code('0.0.1.8.8')):
            return

        if not self.del_():
            messagebox.showerror(Code('0.0.1.8.9'), Code('0.0.1.9.0'))

        self._Main()

    def del_(self) -> bool:
        _log.Info(Code('0.0.1.9.1').format(bot = self.bot.Id))
        if self.bot.Status_ != '0.0.0.6.2':
            if not self.bot.Stop():
                _log.Warn(Code('0.0.1.9.2'))
                return False

        del self.options.Bots[self.bot.Id]
        try:
            self.main.bots_[self.bot.Id][0].destroy()
        except IndexError:
            pass

        _log.Info(Code('0.0.1.9.3'))
        if not os.path.exists('{0}/User/Bots/Bots.json'.format(self.options.Path)):
            os.makedirs('{0}/User/Bots'.format(self.options.Path), exist_ok = True)
            Save('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': []})

        try:
            Bots = Open('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': []}).get('Bots', [])
            Bots.remove(str(self.bot.Id))
            Save('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': Bots})

            _log.Info(Code('0.0.1.9.4'))
            if os.path.exists('{0}/User/Bots/{1}/'.format(self.options.Path, self.bot.Id)):
                shutil.rmtree('{0}/User/Bots/{1}/'.format(self.options.Path, self.bot.Id), ignore_errors=True)

            if os.path.exists('{0}/User/{1}/'.format(self.options.Path, self.bot.Id)):
                shutil.rmtree('{0}/User/{1}/'.format(self.options.Path, self.bot.Id), ignore_errors=True)

        except Exception:
            _log.Error(Code('0.0.1.9.5'))
            return False

        _log.Info(Code('0.0.1.9.6'))
        return True

    def _Main(self) -> None:
        if self.main.Config != None:
            self.main.Config.destroy()
            self.main.Config = None

        self.bot.Status.Is_Config = False
        self.main.Bots()

    def Prefix(self) -> None:
        if self.main.Config != None:
            self.main.Config.destroy()
            self.main.Config = None

        self._main_      = tk.Frame(self.main._main_)
        self._main_.pack(expand = tk.YES, fill=tk.BOTH)

        self.main.Config = self._main_

        self._prefix_ListBox_ = tk.Listbox(self._main_, selectmode=tk.SINGLE)

        self._prefix_ListBox_.config(yscrollcommand=self.main.ScrollBar.set)
        self.main.ScrollBar.config(command=self._prefix_ListBox_.yview)

        index = 0

        _log.Info(Code('0.0.1.9.7'))
        for i in self.bot.Prefix.get('Prefix', []):
            self._prefix_ListBox_.insert(index, i)
            index += 1
        _log.Info(Code('0.0.1.9.8'))

        self._prefix_ListBox_.pack(fill="both", expand="yes")

        self.add_prefix = tk.Button(self._main_, text = Code('0.0.2.0.1'), command = self.New_prefix)
        self.add_prefix.pack(fill=tk.X)

        self._sup_prefix_ = tk.Button(self._main_, text = Code('0.0.2.2.2'), command=self.Sup_Prefix)
        self._sup_prefix_.pack(fill=tk.X)

        self._enter_ = tk.Button(self._main_, text = Code('0.0.2.1.9'), command=self._Main)
        self._enter_.pack(fill=tk.X)

    def Owner(self) -> None:
        if self.main.Config != None:
            self.main.Config.destroy()
            self.main.Config = None

        self._main_      = tk.Frame(self.main._main_)
        self._main_.pack(expand = tk.YES, fill=tk.BOTH)

        self.main.Config = self._main_

        self._owner_ListBox_ = tk.Listbox(self._main_, selectmode=tk.SINGLE)

        self._owner_ListBox_.config(yscrollcommand=self.main.ScrollBar.set)
        self.main.ScrollBar.config(command=self._owner_ListBox_.yview)

        index = 0

        _log.Info(Code('0.0.1.9.9'))
        for i in self.bot.Info.get('Owner', []):
            self._owner_ListBox_.insert(index, i)
            index += 1
        _log.Info(Code('0.0.2.0.0'))

        self._owner_ListBox_.pack(fill="both", expand="yes")

        self.add_owner = tk.Button(self._main_, text = Code('0.0.2.2.3'), command = self.New_owner)
        self.add_owner.pack(fill=tk.X)

        self._sup_owner_ = tk.Button(self._main_, text = ('0.0.2.2.4'), command=self.Sup_owner)
        self._sup_owner_.pack(fill=tk.X)

        self._enter_ = tk.Button(self._main_, text = Code('0.0.2.1.9'), command=self._Main)
        self._enter_.pack(fill=tk.X)

    def Input(self, text: str, text_2: str, command) -> tk.Frame:
        if self.main.Config != None:
            self.main.Config.destroy()
            self.main.Config = None

        _main_      = tk.Frame(self.main._main_)
        _main_.pack(expand = tk.YES, fill=tk.BOTH)

        self.main.Config = _main_

        label = tk.Label(_main_, text = text)
        label.pack()

        self.input_ = tk.Entry(_main_)
        self.input_.pack(fill=tk.BOTH)

        button = tk.Button(_main_, text=text_2, command=command)
        button.pack(fill=tk.BOTH)

        tk.Button(_main_, text = Code('0.0.1.5.5'), command = self.Config).pack(fill=tk.BOTH)

        return _main_

    def New_prefix(self) -> None:
        self.Input(Code('0.0.2.0.1'), Code('0.0.1.5.4'), self.New)

    def Sup_Prefix(self) -> None:
        prefix = self._prefix_ListBox_.curselection()
        if prefix != ():
            name = self._prefix_ListBox_.get(prefix)
            if not messagebox.askyesno(Code('0.0.1.8.7'), Code('0.0.2.0.2').format(prefix = name)):
                return

            _log.Info(Code('0.0.2.0.3').format(prefix = name))
            prefix = self.bot.Prefix.get('Prefix', [])
            if name in prefix:
                prefix.remove(name)
            self.bot.Prefix['Prefix'] = prefix
            Save('{0}/User/Bots/{1}/Prefix.json'.format(self.options.Path, self.bot.Id), self.bot.Prefix)
            self.Prefix()
            _log.Info(Code('0.0.2.0.4').format(prefix = name))

    def New(self) -> None:
        if self.input_ is not None:
            entry = self.input_.get()
            if entry != '':
                _log.Info(Code('0.0.2.0.5').format(prefix = entry))
                prefix = self.bot.Prefix.get('Prefix', [])
                prefix.append(entry)
                self.bot.Prefix['Prefix'] = prefix
                Save('{0}/User/Bots/{1}/Prefix.json'.format(self.options.Path, self.bot.Id), self.bot.Prefix)
                _log.Info(Code('0.0.2.0.6').format(prefix = entry))

            self.Prefix()

    def New_owner(self) -> None:
        self.Input(Code('0.0.2.2.3'), Code('0.0.1.5.4'), self.New_o)

    def Sup_owner(self) -> None:
        owner = self._owner_ListBox_.curselection()
        if owner != ():
            name = self._owner_ListBox_.get(owner)
            if not messagebox.askyesno(Code('0.0.1.8.7'), Code('0.0.2.2.5').format(creator = name)):
                return

            _log.Info(Code('0.0.2.0.7').format(creator = name))
            owner = self.bot.Info.get('Owner', [])
            if name in owner:
                owner.remove(name)
            self.bot.Info['Owner'] = owner
            Save('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, self.bot.Id), self.bot.Info)
            self.Owner()
            _log.Info(Code('0.0.2.0.8').format(creator = name))

    def New_o(self) -> None:
        if self.input_ is not None:
            entry = self.input_.get()
            if entry != '':
                owner = self.bot.Info.get('Owner', [])
                _log.Info(Code('0.0.2.0.9').format(creator = entry))
                owner.append(entry)
                self.bot.Info['Owner'] = owner
                Save('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, self.bot.Id), self.bot.Info)
                _log.Info(Code('0.0.2.1.0').format(creator = entry))

            self.Owner()

    def Stop(self) -> None:
        _log.Info(Code('0.0.2.1.1'))
        if not self.bot.Stop():
            _log.Error(Code('0.0.2.1.2'))

    def Start(self) -> None:
        _log.Info(Code('0.0.2.1.3'))
        if not self.bot.Start():
            _log.Error(Code('0.0.2.1.4'))

from .GetLang      import Get_Lang
from .Logger       import Log
from .Utils        import Save, Open, MISSING
from .type.Bot     import Bot
from .type.Options import Options

from typing import Union

try:
    from PIL import Image, ImageTk
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'pillow'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)

try:
    import signal
except ImportError:
    Log(50, Get_Lang.get('0.0.0.0.0').format(Name = 'signal'), True)
except Exception as e:
    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)), True)


from tkinter import messagebox
import tkinter as tk
import os, threading


class Interface(threading.Thread):
    def __init__(self, options: Options = MISSING) -> None:
        super(Interface, self).__init__()

        self.check                           = False

        if options == MISSING:
            Log(50, Get_Lang.get('0.0.1.5.2').format(Error = Get_Lang.get('0.0.1.5.1')), True)

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


    def run(self) -> None:
        Log(20, Get_Lang.get('0.0.1.5.3'))
        self._main__ = tk.Tk()
        self._main_  = tk.Frame(self._main__)
        self._main_.pack(fill = tk.BOTH, expand=tk.YES)

        self._main__.title(self.options.Info.get('Windows-Title', 'Sayu#0475'))
        self._main__.geometry('900x500')

        if os.path.exists(self.options.Path+'/Bot/icon.png'):
            self._main__.iconphoto(False, tk.PhotoImage(file=self.options.Path+'/Bot/icon.png'))

        try:
            self.Initialized = True
            self.interface__ = True
            Log(20, Get_Lang.get('0.0.1.7.1'))
            self._main__.mainloop()
            self.interface__ = False
            self.stop()
        except Exception:
            self.interface__ = False
            self.Initialized = False

    def _scroll_bar(self) -> None:
        self.ScrollBar = tk.Scrollbar(self._main__)
        self.ScrollBar.place(relx=0.981,height=self._main__.winfo_height(), bordermode = tk.OUTSIDE)

    def stop(self) -> None:
        Log(20, Get_Lang.get('0.0.1.4.6'))
        if self.interface__ == True:
            self._main__.destroy()
            self._main__.quit()
        for Bot in self.options.Bots:
            try:
                self.options.Bots[Bot].Stop()
            except Exception as e:
                Log(50, Get_Lang.get('0.0.1.4.9').format(Error = str(e)))
            else:
                os.kill(os.getpid(), signal.SIGTERM)

    def Menu(self, main: tk.Tk) -> tk.Menu:
        _main_:    tk.Menu = tk.Menu(main)

        _options_: tk.Menu = tk.Menu(_main_, tearoff=0)

        _options_.add_command(label = Get_Lang.get('0.0.1.5.6'), command = self.change_language)
        _options_.add_command(label = Get_Lang.get('0.0.1.5.7'), command = self.add_bot)
        _options_.add_command(label = Get_Lang.get('0.0.1.5.8'), command = self.stop)

        _main_.add_cascade(label = Get_Lang.get('0.0.1.5.9'), menu = _options_)

        return _main_

    def add_bot(self) -> None:
        if self.Config != None:
            self.Config.destroy()
            self.Config = None

        Log(20, Get_Lang.get('0.0.1.5.4'))
        try:
            list(self.bots_.items())[0][1][2].destroy()
        except IndexError:
            pass


        self.bots_ = {}

        _main_ = tk.Frame(self._main_)
        _main_.pack(expand=tk.YES)

        self.Config = _main_

        self._main__.title(Get_Lang.get('0.0.1.5.7'))

        LabelFrame = tk.LabelFrame(_main_, text = Get_Lang.get('0.0.1.5.7'))
        self.add_bot_LabelFrame = LabelFrame
        LabelFrame.pack(fill = tk.BOTH, expand = tk.YES)

        self.Label_1 = tk.Label(LabelFrame, text=Get_Lang.get('0.0.1.6.0'))
        self.Label_1.grid(column = 0, row = 0, sticky=tk.W)

        self.Input_1 = tk.Entry(LabelFrame, width=50)
        self.Input_1.grid(column = 0, row = 1, sticky=tk.W)

        self.Label_2 = tk.Label(LabelFrame, text=Get_Lang.get('0.0.1.6.1'))
        self.Label_2.grid(column = 0, row = 2, sticky=tk.W)

        self.Input_2 = tk.Entry(LabelFrame, width=50)
        self.Input_2.grid(column = 0, row = 3, sticky=tk.W)

        self.Label_3 = tk.Label(LabelFrame, text=Get_Lang.get('0.0.1.6.2'))
        self.Label_3.grid(column = 0, row = 4, sticky=tk.W)

        self.Input_3 = tk.Entry(LabelFrame, width=100)
        self.Input_3.grid(column = 0, row = 5)

        self.Error_1 = tk.Label(LabelFrame)
        self.Error_1.grid(column = 0, row = 6)

        Button_1  = tk.Button(LabelFrame, text=Get_Lang.get('0.0.1.6.3'), command = self.add_bot_add)
        Button_1.grid(column = 0, row = 7, sticky=tk.W)

        Button_2  = tk.Button(LabelFrame, text=Get_Lang.get('0.0.1.6.4'), command=self.add_bot_cancel)
        Button_2.grid(column = 1, row = 7, sticky=tk.E)
        Log(20, Get_Lang.get('0.0.1.5.5'))

    def add_bot_add(self) -> None:
        if self.add_bot_LabelFrame is not None:
            if self.Input_1.get() == '' or self.Input_2.get() == '' or self.Input_3.get() == '':
                self.Error_1.config(text = Get_Lang.get('0.0.1.6.5'), fg = 'red')
            else:
                if not os.path.exists('{0}/User/Bots/Bots.json'.format(self.options.Path)):
                    os.makedirs('{0}/User/Bots'.format(self.options.Path), exist_ok = True)
                    Save('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': []})

                Bots = Open('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': []}).get('Bots', [])
                Bots.append(str(self.Input_1.get()))
                Save('{0}/User/Bots/Bots.json'.format(self.options.Path), {'Bots': Bots})

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
            return False

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

            Button_: tk.Button = tk.Button(LabelFrame, text = Get_Lang.get('0.0.1.6.6'), command = Bot_.Config)
            Button_.grid(column = 0, row = 1)

            Label__ = tk.Label(LabelFrame, text = Get_Lang.get('0.0.1.6.7').format(Statu = Get_Lang.get(self.options.Bots[Bot].Status_)))
            Label__.grid(column = 1, row = 0)

            if self.options.Bots[Bot].Status_ != '0.0.0.6.2':
                Button__: tk.Button = tk.Button(LabelFrame, text = Get_Lang.get('0.0.1.6.8'), command = Bot_.Stop)
            else:
                Button__: tk.Button = tk.Button(LabelFrame, text = Get_Lang.get('0.0.1.6.9'), command = Bot_.Start)

            Button__.grid(column = 1, row = 1)

            self.bots_[Bot] = [Frame, LabelFrame, container]

    def UpDate_Bot(self, Id: str) -> None:
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

        Button_: tk.Button = tk.Button(LabelFrame, text = Get_Lang.get('0.0.1.6.6'), command = Bot_.Config)
        Button_.grid(column = 0, row = 1)

        Label__ = tk.Label(LabelFrame, text = Get_Lang.get('0.0.1.6.7').format(Statu = Get_Lang.get(self.options.Bots[Id].Status_)))
        Label__.grid(column = 1, row = 0)

        if self.options.Bots[Id].Status_ != '0.0.0.6.2':
            Button__: tk.Button = tk.Button(LabelFrame, text = Get_Lang.get('0.0.1.6.8'), command = Bot_.Stop)
        else:
            Button__: tk.Button = tk.Button(LabelFrame, text = Get_Lang.get('0.0.1.6.9'), command = Bot_.Start)

        Button__.grid(column = 1, row = 1)

        self.bots_[Id] = [Frame, LabelFrame, self.bots_[Id][2]]

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

        self._main__.title(Get_Lang.get('0.0.0.1.6'))

        self._ListBot_ = tk.Listbox(_main_, selectmode=tk.SINGLE)

        self._ListBot_.config(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.config(command=self._ListBot_.yview)

        Log(20, Get_Lang.get('0.0.1.7.4'))
        if self.language_ == []:
            with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Language.json') as r:
                try:
                    self.language_: list[str] = r.json()
                    Log(20, Get_Lang.get('0.0.1.7.5'))
                except Exception as e:
                    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
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
        Log(20, Get_Lang.get('0.0.0.2.9').format(Name = str(language)+'.json'))
        if not str(language)+'.json' in [f for f in os.listdir('{0}/Bot/Language/'.format(self.options.Path)) if os.path.isfile(os.path.join('{0}/Bot/Language/'.format(self.options.Path), f))]:
            Log(20, Get_Lang.get('0.0.0.3.0').format(Name = str(language)))
            f = open('{0}/Bot/Language/{1}'.format(self.options.Path, str(language)+'.json'), 'wb+')
            with self.options.Send('https://raw.githubusercontent.com/Romaindu74/Bots/main/Language/{0}'.format(str(language)+'.json')) as r:
                try:
                    f.write(r.content)
                except Exception as e:
                    Log(50, Get_Lang.get('0.0.0.0.1').format(File = __file__, Error = str(e)))
                    return False
                f.close()
            Log(20, Get_Lang.get('0.0.0.3.1'))

        else:
            Log(20, Get_Lang.get('0.0.0.3.2'))

        os.makedirs('{0}/User/__Json__/'.format(self.options.Path), 777, True)
        main = Open('{0}/User/__Json__/Main.json'.format(self.options.Path))
        main['Lang'] = language
        Save('{0}/User/__Json__/Main.json'.format(self.options.Path), main)

        Log(20, Get_Lang.get('0.0.0.3.3'))
        self.cancel()


    def cancel(self) -> None:
        if self._ListBot_ is not None:
            self._ListBot_.destroy()
        self.Bots()


    def Start(self) -> None:
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

        self._main_      = tk.Frame(self.main._main_)
        self._main_.pack(fill=tk.BOTH, expand = tk.YES)

        self.main.Config = self._main_

        self.main._main__.title(self.bot.Info.get('Name', self.options.Info.get('Windows-Title', 'Sayu#0475')))

        self.main.bots_[self.bot.Id][2].destroy()

        self.LabelFrame         = tk.LabelFrame(self._main_, text = 'Information')
        self.LabelFrame.pack(fill = tk.BOTH, expand=tk.YES)

        self.Bot_Name           = tk.Label(self.LabelFrame, text = 'Nom : {0}'.format(self.bot.Info.get('Name', '...')))
        self.Bot_Name.grid(sticky='w')

        self.Bot_Id             = tk.Label(self.LabelFrame, text = 'Id : {0}'.format(self.bot.Info.get('Id', '...')))
        self.Bot_Id.grid(sticky='w')

        self.Bot_Statu          = tk.Label(self.LabelFrame, text = 'Statu : {0}'.format(Get_Lang.get(self.bot.Status_)))
        self.Bot_Statu.grid(sticky='w')

        self.Bot_Prefix         = tk.Label(self.LabelFrame, text = Get_Lang.get('0.0.0.2.1').format(Prefix = self.bot.Prefix.get('Prefix', [])))
        self.Bot_Prefix.grid(sticky='w')

        self.Discord_LabelFrame = tk.LabelFrame(self._main_, text = Get_Lang.get('0.0.0.2.2'))
        self.Discord_LabelFrame.pack(fill='both', expand='yes')

        self.Bot_Ms             = tk.Label(self.Discord_LabelFrame, text = Get_Lang.get('0.0.0.2.3').format(Ping = self.bot.Ping))
        self.Bot_Ms.grid(sticky='w')

        self.Statut_LabelFrame  = tk.LabelFrame(self._main_, text = Get_Lang.get('0.0.0.2.4'))
        self.Statut_LabelFrame.pack(fill='both', expand='yes')

        try:
            self.Bot_Activite       = tk.Label(self.Statut_LabelFrame, text = Get_Lang.get('0.0.0.2.5').format(Activity = self.bot.Status.Activity, Text = self.bot.Status.Text))
            self.Bot_Activite.grid(sticky='w')

            self.Bot_Statut         = tk.Label(self.Statut_LabelFrame, text = Get_Lang.get('0.0.0.2.6').format(Display = self.bot.Status.Statu))
            self.Bot_Statut.grid(sticky='w')

            self.Bot_Statut_Time    = tk.Label(self.Statut_LabelFrame, text = Get_Lang.get('0.0.0.2.7').format(Time = self.bot.Status.Time))
            self.Bot_Statut_Time.grid(sticky='w')


            self.bot.Status.Interface(self.Bot_Activite, self.Bot_Statut, self.Bot_Statut_Time, self.Bot_Ms)
            self.bot.Status.Is_Config = True

        except AttributeError:
            pass

        self.Main               = tk.Button(self._main_, text = 'Menu', command=self._Main)
        self.Main.pack(fill = tk.BOTH)


        self._Prefix               = tk.Button(self._main_, text = 'Prefix', command=self.Prefix)
        self._Prefix.pack(fill = tk.BOTH)

        self._Owner               = tk.Button(self._main_, text = 'Createur', command=self.Owner)
        self._Owner.pack(fill = tk.BOTH)


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

        for i in self.bot.Prefix.get('Prefix', []):
            self._prefix_ListBox_.insert(index, i)
            index += 1

        self._prefix_ListBox_.pack(fill="both", expand="yes")

        self.add_prefix = tk.Button(self._main_, text = 'Ajouter un prefix', command = self.New_prefix)
        self.add_prefix.pack(fill=tk.X)

        self._sup_prefix_ = tk.Button(self._main_, text = 'Suprimer un prefix', command=self.Sup_Prefix)
        self._sup_prefix_.pack(fill=tk.X)

        self._enter_ = tk.Button(self._main_, text = 'Menu', command=self._Main)
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

        for i in self.bot.Info.get('Owner', []):
            self._owner_ListBox_.insert(index, i)
            index += 1

        self._owner_ListBox_.pack(fill="both", expand="yes")

        self.add_owner = tk.Button(self._main_, text = 'Ajouter un Créateur', command = self.New_owner)
        self.add_owner.pack(fill=tk.X)

        self._sup_owner_ = tk.Button(self._main_, text = 'Suprimer un Créateur', command=self.Sup_owner)
        self._sup_owner_.pack(fill=tk.X)

        self._enter_ = tk.Button(self._main_, text = 'Menu', command=self._Main)
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

        tk.Button(_main_, text = 'Annuler', command = self.Config).pack(fill=tk.BOTH)

        return _main_

    def New_prefix(self) -> None:
        self.Input('Ajouter un prefix', 'Ajouter', self.New)

    def Sup_Prefix(self) -> None:
        prefix = self._prefix_ListBox_.curselection()
        if prefix != ():
            name = self._prefix_ListBox_.get(prefix)
            if not messagebox.askyesno('Supprimer', 'Est tu sur de vouloir supprimer ce prefix: {0}'.format(name)):
                return

            prefix = self.bot.Prefix.get('Prefix', [])
            if name in prefix:
                prefix.remove(name)
            self.bot.Prefix['Prefix'] = prefix
            Save('{0}/User/Bots/{1}/Prefix.json'.format(self.options.Path, self.bot.Id), self.bot.Prefix)
            self.Prefix()

    def New(self) -> None:
        if self.input_ is not None:
            entry = self.input_.get()
            if entry != '':
                prefix = self.bot.Prefix.get('Prefix', [])
                prefix.append(entry)
                self.bot.Prefix['Prefix'] = prefix
                Save('{0}/User/Bots/{1}/Prefix.json'.format(self.options.Path, self.bot.Id), self.bot.Prefix)

            self.Prefix()

    def New_owner(self) -> None:
        self.Input('Ajouter un Créateur', 'Ajouter', self.New_o)

    def Sup_owner(self) -> None:
        owner = self._owner_ListBox_.curselection()
        if owner != ():
            name = self._owner_ListBox_.get(owner)
            if not messagebox.askyesno('Supprimer', 'Est tu sur de vouloir supprimer ce Créateur: {0}'.format(name)):
                return

            owner = self.bot.Info.get('Owner', [])
            if name in owner:
                owner.remove(name)
            self.bot.Info['Owner'] = owner
            Save('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, self.bot.Id), self.bot.Info)
            self.Owner()

    def New_o(self) -> None:
        if self.input_ is not None:
            entry = self.input_.get()
            if entry != '':
                owner = self.bot.Info.get('Owner', [])
                owner.append(entry)
                self.bot.Info['Owner'] = owner
                Save('{0}/User/Bots/{1}/Main.json'.format(self.options.Path, self.bot.Id), self.bot.Info)

            self.Owner()

    def Stop(self) -> None:
        Log(20, Get_Lang.get('0.0.1.7.2'))
        if not self.bot.Stop():
            Log(40, 'Le bot ne peux pas s\'etaindre')

    def Start(self) -> None:
        self.bot.Start()
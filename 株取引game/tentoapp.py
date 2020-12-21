import tkinter
import tkinter.font as font
import tkinter.ttk as ttk
from inspect import signature
import re
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import platform

## History
# 2018.10.11 add CheckButton
# 2018.10.15 add Mixin-classes
# 2018.11.03 add RadioButton
# 2019.01.24 add Sound

# http://fakatatuku.hatenablog.com/entry/2015/03/26/233024
class ClassProperty(property):
    pass

class PropertyMeta(type):

    def __new__(cls, name, bases, namespace):
        props = [(k, v) for k, v in namespace.items() if type(v) == ClassProperty]
        for k, v in props:
            setattr(cls, k, v)
            del namespace[k]
        return type.__new__(cls, name, bases, namespace)

## 継承専用クラス
## self.state()で設定するものをプロパティ化するための
class MixinState():
    @property
    def disabled(self):
        if self["state"] == tkinter.DISABLED:
            return true
        else:
            return false

    @disabled.setter
    def disabled(self,arg):
        if arg == True:
            self["state"] = tkinter.DISABLED
        else:
            self["state"] = tkinter.NORMAL


## 継承専用クラス
## self.state()およびself.instate()で設定するものをプロパティ化するための
## ttk.の新しいクラス用
## 11.10 constructorをなくしてMixin化したい。
class AbstractStateTtk(metaclass=PropertyMeta):
    def __init__(self):
        pass
#        self.__disabled = False
#        self.__readonly = False

    @property
    def disabled(self):
#        return self.__disabled
        if self.instate(["disabled"]):
            return True
        else:
            return False

    @disabled.setter
    def disabled(self,arg):
        if arg == True:
            self.state(["disabled"])
            #self.__disabled = True
        else:
            self.state(["!disabled"])
            #self.__disabled = False

    @property
    def readonly(self):
        if self.instate(["readonly"]):
            return True
        else:
            return False

    @readonly.setter
    def readonly(self,arg):
        if arg == True:
            self.state(["readonly"])
            self.__readonly = True
        else:
            self.state(["!readonly"])
            self.__readonly = False

    @property
    def fontsize(self):
        return self.__fontsize

    @fontsize.setter
    def fontsize(self,size):
        style_name = self.stylename()
        self.style = style_name
        ttk.Style().configure(style_name,font=("",size))
        self.__fontsize = size
        ## ttk.Entryがなぜかstyleを受け付けないので。。
        if self.__class__.__name__ in ("Entry", "Spinbox"):
            self.font = ("", size)

    @property
    def bgcolor(self):
        style_name = self.stylename()
        self.style = style_name
        return ttk.Style().lookup(style_name,"background")

    @bgcolor.setter
    def bgcolor(self,arg):
        style_name = self.stylename()
        self.style = style_name
        ttk.Style().configure(style_name,background=arg)
        #print(ttk.Style().lookup(style_name,"background"))
        self.__bgcolor = arg
        
    def stylename(self):
        return str(id(self)) + ".T" + self.__class__.__name__  ## ここなんとかしたい

    @property
    def color(self):
        style_name = self.stylename()
        self.style = style_name
        return ttk.Style().lookup(style_name,"foreground")
       
    @color.setter
    def color(self,arg):
        style_name = self.stylename()
        self.style = style_name
        ttk.Style().configure(style_name ,foreground=arg)


    @ClassProperty
    def allfontsize(cls):
        cname = "T" + cls.__name__  ## ここなんとかしたい
        font = ttk.Style().lookup(cname,"font")
        m = re.search(r"[0-9]+", font)
        if m != None:
            return int(m.group())
        else:
            return None

    @allfontsize.setter
    def allfontsize(cls,size):
        cname = "T" + cls.__name__  ## ここなんとかしたい
        ttk.Style().configure(cname,font=("",size))

    

## 継承専用クラス
## self.configure()で設定するものをプロパティ化するための
class AbstractConfig():
    def __init__(self):
        self.__property = {}

    def __getattr__(self,name):
        cls = globals()[self.__class__.__name__]
#        self.__propcheck()
        if name in cls.props:
            #= setする前のgetに対応
            if name not in self.__property:
                self.__property[name] = None
            return self.__property[name]

    def __setattr__(self,name,value):
        cls = globals()[self.__class__.__name__]
        if name in cls.props:
#            self.__propcheck()
            self.__property[name] = value
            dic = {}
            dic[name] = value
            self.configure(**dic)
        else:
            #== ここはRaiseErrorしたほうがよくないか？？
            super().__setattr__(name,value)

#    def __propcheck(self):
#        if self.__property == None:
#            self.__property = {}

## 継承専用クラス
## Layout関連をまとめるためのクラス
class MixinLayout():
    def pack(self):
        master_class = self.master.__class__.__name__
        if master_class == "XBox":
            super().pack(anchor=tkinter.N+tkinter.W,side="left")
        elif master_class == "YBox":
            super().pack(anchor=tkinter.N+tkinter.W,side="top")
        else:
            super().pack(anchor=tkinter.N+tkinter.W,side="top")
            #super().pack(anchor=tkinter.N+tkinter.W,fill=tkinter.BOTH)

    def place(self,*arg):
        if len(arg) == 2:
            super().place(x=arg[0],y=arg[1])
        elif len(arg) == 4:
            super().place(x=arg[0],y=arg[1],width=arg[2],height=arg[3])

    def grid(self,x,y):
        # set defalt alignment to North+West
        super().grid(column=x,row=y,sticky=tkinter.N+tkinter.W)

    def __get_grid_info__(self, name):
        tcl_obj = self.tk.call("grid","info",self._w)
        li = str(tcl_obj).split()
        dic = dict(zip(li[0::2], li[1::2]))
        return dic["-" + name]


    @property
    def sticky(self):
        return str(self.__get_grid_info__("sticky"))

    @sticky.setter
    def sticky(self,arg):
        self.grid_configure(sticky=arg)
        

    @property
    def colspan(self):
        return int(self.__get_grid_info__("columnspan"))

    @colspan.setter
    def colspan(self,num):
        self.grid_configure(columnspan=num)

    @property
    def rowspan(self):
        return int(self.__get_grid_info__("rowspan"))

    @rowspan.setter
    def rowspan(self,num):
        self.grid_configure(rowspan=num)


    def remove(self):
        self.hide()

    def hide(self):
        self.place_forget()
        self.pack_forget()
        self.grid_forget()

    @property
    def onclick(self):
        return self.__onclick
        #if self.__class__.__name__ == "Button":
        #    return self.command
        #else:
        #    return self.__onclick

    @onclick.setter
    def onclick(self,func):
        sig = signature(func)
        newfunc = None
        if (len(sig.parameters) == 0):
            newfunc = (lambda e:None if e.widget.disabled else func())
        else:
            newfunc = (lambda e:None if e.widget.disabled else func(e))
        self.bind("<Button-1>",newfunc)
        self.__onclick = newfunc
        #if self.__class__.__name__ == "Button":
        #    self.command = func
        #else:
        #    sig = signature(func)
        #    newfunc = func
        #    if (len(sig.parameters) == 0):
        #        newfunc = (lambda event:func())
        #    self.bind("<Button-1>",newfunc)
        #    self.__onclick = newfunc

    @property
    def onkeypress(self):
        return self.__onkeypress

    @onkeypress.setter
    def onkeypress(self,func):
        self.bind("<Any-KeyPress>",func)
        self.__onkeypress = func


# Base for All
class Window(tkinter.Tk):

    def __init__(self,**args):
        super().__init__(**args)
        self.title("tentoapp")

    def start(self):
        super().mainloop()

    def size(self, width, height):
        self.__width = width
        self.__height = height
        super().geometry("%dx%d" % (width, height))
        super().resizable(0,0) # no resize

    @property
    def width(self):
        return __width

    @property
    def height(self):
        return __height
        
# NG with simpledialog
#    @property
#    def title(self):
#        return super().title()
#
#    @title.setter
#    def title(self, arg):
#        self.__title = arg
#        super().title(arg)


    @property
    def geometry(self):
        return super().geometry()

    @geometry.setter
    def geometry(self, arg):
        super().geometry(arg)

    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        super().geometry('{}x{}+{}+{}'.format(width, height, x, y))

    @property
    def onkeypress(self):
        return self.__onkeypress

    @onkeypress.setter
    def onkeypress(self,func):
        self.bind("<Any-KeyPress>",func)
        self.__onkeypress = func



# Alias for Window
class App(Window):
    pass


class Frame(MixinLayout,ttk.Frame,AbstractConfig):
    props = ("borderwidth","cursor","height","padding","relief","style","takefocus","width")
    def __init__(self,*parent,**args):
        ttk.Frame.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)

# horizontal frame
class XBox(MixinLayout,ttk.Frame,AbstractConfig):
    props = ("borderwidth","cursor","height","padding","relief","style","takefocus","width")
    def __init__(self,*parent,**args):
        ttk.Frame.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)
        #self.configure(fill=tkinter.BOTH)
        #self.borderwidth=5
        #self.relief="groove"



# vertical frame
class YBox(MixinLayout,ttk.Frame,AbstractConfig):
    props = ("borderwidth","cursor","height","padding","relief","style","takefocus","width")
    def __init__(self,*parent,**args):
        ttk.Frame.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)
        #self.borderwidth=5
        #self.relief="groove"

# box for `place()` 
class RelativeBox(MixinLayout,ttk.Frame,AbstractConfig):
    props = ("borderwidth","cursor","height","padding","relief","style","takefocus","width")
    def __init__(self,parent,width,height):
        ttk.Frame.__init__(self,parent, width=width,height=height)
        AbstractConfig.__init__(self)
        self.borderwidth=5
        self.relief="groove"

class Image(tkinter.PhotoImage):
    def __init__(self,file):
        super().__init__(file=file)


class Font(font.Font, AbstractConfig):
    props = ("family", "size", "weight","slant", "underline","overstrike")
    def __init__(self,*parent,**args):
        ttk.Frame.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)


class Button(MixinLayout,ttk.Button, AbstractStateTtk,AbstractConfig):
    props = ("text", "image", "command", "compound","cursor","style","takefocus","textvariable","underline","width")

    def __init__(self,*parent,**args):
        ttk.Button.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)



class Label(MixinLayout,ttk.Label,AbstractStateTtk,AbstractConfig):

    props = ("anchor","background","borderwidth","compound","cursor","font","foreground","image","justify","padding","relief","style","takefocus","text","textvariable","underline","width","wraplength")
    def __init__(self,*parent,**args):
        ttk.Label.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)



class CheckButton(MixinLayout,ttk.Checkbutton, AbstractStateTtk,AbstractConfig):
    props = ("command", "compound", "cursor", "image", "offvalue", "onvalue", "style", "takefocus", "text", "textvariable", "underline", "width")

    def __init__(self,*parent,**args):
        ttk.Checkbutton.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)
        self.status = tkinter.IntVar()
        self.status.set(0)
        self["variable"] = self.status

    @property
    def checked(self):
        if self.status.get() == 0:
            return False
        else:
            return True
           
    @checked.setter
    def checked(self, arg):
        if arg == True:
            self.status.set(1)
        else:
            self.status.set(0)

## Todo valueプロパティがない場合はtextを使いたい
class RadioButton(MixinLayout,ttk.Radiobutton,AbstractStateTtk, AbstractConfig):
    props = ("command", "compound", "cursor",  "offvalue", "onvalue", "style", "takefocus", "variable", "value","underline", "width")

    instances = []

    def __init__(self,*parent,**args):
        ttk.Radiobutton.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)
        RadioButton.instances.append(self)
        self.number = len(RadioButton.instances)
        self.groupname = ""
        self.group = ""

    @property
    def group(self):
        return self.groupname

    @group.setter
    def group(self,arg):
        self.groupname = arg
        radios = [r for r in RadioButton.instances if r.groupname == arg and r.number != self.number]
        if len(radios) == 0:
            self.variable = tkinter.StringVar()
        else:
            self.variable = radios[0].variable

    @property
    def groupvalue(self):
        return self.variable.get()

    @property
    def text(self):
        return self["text"]

    @text.setter
    def text(self,arg):
        self["text"] = arg
        if self.value == None:
            self.value = arg
        
    @property
    def selected(self):
        return self.variable.get() == self.value
        
    @selected.setter
    def selected(self,arg):
        self.variable.set(self.value)


class Entry(MixinLayout,ttk.Entry, AbstractStateTtk, AbstractConfig):
    props = ("cursor","exportselection","font","invalidcommand","justify","show","style","takefocus","validate","validatecommand","width","xscrollcommand")

    def __init__(self,*parent,**args):
        ttk.Entry.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)
        self.textvar = tkinter.StringVar()
        self.textvar.set("")
        self["textvariable"] = self.textvar
        self.psw = False

        self.textvar.trace_add("write",self.__validate_length)
        self.__limit = 0

    def __validate_length(self,*args):
        if self.__limit != 0:
            curval = self.textvar.get()
            if len(curval) > self.__limit:
                self.textvar.set(curval[0:self.__limit])

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self,num):
        self.__limit = num

    @property
    def text(self):
        return self.textvar.get()
           
    @text.setter
    def text(self, arg):
        self.textvar.set(arg)

    @property
    def password(self):
        return self.psw

    @password.setter
    def password(self,arg):
        if arg == True:
            self.psw = True
            self.show = "*"
        else:
            self.psw = False
            self.show = ""


class ComboBox(MixinLayout,ttk.Combobox, AbstractStateTtk,AbstractConfig):
    props = ("cursor","exportselection","height","justify","postcommand","style","takefocus","validate","validatecommand","values","width","xscrollcommand")

    def __init__(self,*parent,**args):
        ttk.Combobox.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)
        self.__textvar = tkinter.StringVar()
        self["textvariable"] = self.__textvar

    @property
    def selectedtext(self):
        return self.__textvar.get()

class ListBox(MixinLayout,tkinter.Listbox,MixinState,AbstractConfig):
    props = ("activestyle","background","borderwidth","cursor","disabledforeground","exportselection","font","foreground","height","highlightbackground","highlightcolor","highlightthickness","relief","selectbackground","selectborderwidth","selectforeground","selectmode","state","takefocus","width","xscrollcommand","yscrollcommand")

    def __init__(self,*parent,**args):
        tkinter.Listbox.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)
        self["listvariable"] = tkinter.StringVar()
        self.__values = []
        self.borderwidth = 1
        self.relief = tkinter.SUNKEN
        self.__viewsize = 0 # default height
        self["height"] = 5 # default height

    @property
    def values(self):
        return self.__values

    @values.setter
    def values(self,str_list):
        self.__values = str_list
        self["listvariable"] = tkinter.StringVar(value=str_list)
        if self.__viewsize == 0:
            self["height"] = len(str_list)

    def push(self,arg):
        vals = self.values
        vals.append(arg)
        self.values = vals
        if self.__viewsize == 0:
            self["height"] = len(vals)

    @property
    def viewsize(self):
        return self.__viewsize

    @viewsize.setter
    def viewsize(self,arg):
        self.__viewsize = arg
        self["height"] = arg

class ScrollBar(MixinLayout,ttk.Scrollbar, AbstractStateTtk, AbstractConfig):
    props = ["command", "orient","style","cursor","takefocus"]

    def __init__(self,*parent,**args):
        ttk.Scrollbar.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)
        self.__target = None

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self,widget):
        if widget.__class__.__name__ == "ListBox":
            self.command = widget.yview
            self.orient = tkinter.VERTICAL
            widget.yscrollcommand = self.set

    def cell(self,x,y):
        super().cell(x,y)
        if self.orient == tkinter.VERTICAL:
            self.grid_configure(sticky=(tkinter.N, tkinter.S))

class Text(MixinLayout,tkinter.Text,MixinState,AbstractConfig):
    props = ["autoseparators","background","borderwidth","cursor","exportselection","font","foreground","height","highlightbackground","highlightcolor","highlightthickness","insertbackground","insertborderwidth","insertofftime","insertontime","insertwidth","maxundo","padx","pady","relief","selectbackground","selectborderwidth","selectforeground","spacing1","spacing2","spacing3","state","tabs","takefocus","undo","width","wrap","xscrollcommand","yscrollcommand"]

    def __init__(self,*parent,**args):
        tkinter.Text.__init__(self,*parent,**args)
        AbstractConfig.__init__(self)
        self.borderwidth = 1
        self.relief = tkinter.SUNKEN


    @property
    def text(self):
        return self.get("1.0", tkinter.END)

    @text.setter
    def text(self,arg):
        self.delete("1.0", tkinter.END)
        self.insert("1.0",arg)



class TextBox(Text):
    pass

# python3.7以上ではttk.Spinboxになっている。
class Spinbox(MixinLayout,ttk.Spinbox, AbstractStateTtk, AbstractConfig):
    props = ("width","from_","to","increment","values","format","cursor","font","style","takefocus","validate")

    def __init__(self,*parent,**args):
        ttk.Spinbox.__init__(self,*parent,**args)
        AbstractStateTtk.__init__(self)
        AbstractConfig.__init__(self)
        # default
        self["from_"] = 0
        self["to"] = 99
        self["increment"] = 1

    @property
    def min(self):
        return self["from_"]

    @min.setter
    def min(self,val):
        self["from_"] = val

    @property
    def max(self):
        return self["to"]

    @max.setter
    def max(self,val):
        self["to"] = val


    @property
    def step(self):
        return self["increment"]

    @step.setter
    def step(self,val):
        self["increment"] = val

    @property
    def value(self):
        ## とりあえず！なにもしないとstrが帰る
        return int(self.get())

    @value.setter
    def value(self,val):
        self.set(val)
        

class Dialog():
    
    @classmethod
    def askQuestion(cls,title,text):
        simpledialog.askstring("title","message")

    @classmethod
    def openYesNoDialog(cls):
        pass

    @classmethod
    def openFile(cls):
        pass

    @classmethod
    def saveFile(cls):
        pass


## ここから下が問題

class Canvas(tkinter.Canvas):

    def line(self, *points, **options):
        object_id = super().create_line(*points, **options)
        return CanvasObject(self,object_id, "line")

    def oval(self, x0, y0, x1, y1, **options):
        object_id = super().create_oval(x0,y0,x1,y1,**options)
        return CanvasObject(self,object_id, "oival")
        

    def image(self,image, x,y, **options):
        object_id = super().create_image(x,y,image=image,**options)
        return CanvasObject(self,object_id, "image")
        


class CanvasObject(object):

    original_props = ("canvas", "object_id", "ctype")



    def __init__(self,canvas, object_id, ctype):
        self.canvas = canvas
        self.object_id = object_id
        self.ctype = ctype
        

    def move(self, x, y):
        self.canvas.move(self.object_id, x, y)


    def remove(self):
        self.canvas.delete(self.object_id)

    

    def __getattr__(self,name):
        if name not in CanvasObject.original_props:
            return self.canvas.itemcget(name)
        else:
            print(name)

    def __setattr__(self,name,value):
        if name not in CanvasObject.original_props:
            dic = {}
            dic[name] = value
            self.canvas.itemconfigure(self.object_id, **dic)
        else:
            object.__setattr__(self,name,value)


#== Sound
class Sound():
    
    def __init__(self,wavefilepath):
        self.wf = wavefilepath

    def play(self):
        if platform.system() == "Windows":
            # for Windows
            import winsound
            winsound.PlaySound(self.wf, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif platform.system() == "Darwin":
            # for Mac
            import subprocess
            subprocess.Popen(["afplay", self.wf])
        else:
            pass

    def playuntildone(self):
        if platform.system() == "Windows":
            # for Windows
            import winsound
            winsound.PlaySound(self.wf, winsound.SND_FILENAME)
        elif platform.system() == "Darwin":
            # for Mac
            import subprocess
            subprocess.run(["afplay", self.wf])
        else:
            pass

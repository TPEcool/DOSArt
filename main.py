from ttkbootstrap import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from ttkbootstrap import colorutils as colutil
from PIL import Image, ImageTk, ImageDraw, ImageFont
from charsel import create
from unicodedata import name as unicode_name
from os import path

def getcwd() -> str:
    return path.dirname(__file__)

win = Window('DOSArt Editor', 'cosmo')

editor_pane = Panedwindow(win, orient=HORIZONTAL)
editor_pane.pack(expand=True, fill=BOTH, side=TOP)

tools = Frame(win)
tools.pack(side=RIGHT, fill=BOTH, padx=5, pady=5)

color = Labelframe(tools, text='Color')
color.pack(side=TOP, expand=True)

charcolor = StringVar(win, '#000000')
bgcolor = StringVar(win, '#FFFFFF')
cpicker = ColorChooserDialog(win, 'Pick a character color', charcolor.get())
bg_cpicker = ColorChooserDialog(win, 'Pick a background color', bgcolor.get())

global colorimg
colorimg = ImageTk.PhotoImage(Image.new('RGB', (16, )*2, colutil.color_to_rgb(charcolor.get())))

global bg_colorimg
bg_colorimg = ImageTk.PhotoImage(Image.new('RGB', (16, )*2, colutil.color_to_rgb(bgcolor.get())))

def colorImg(c: tuple):
    '''
    Make a solid-color image to display in the window.
    '''
    global colorimg
    colorimg = ImageTk.PhotoImage(Image.new('RGB', (16, )*2, c))
    setcolorbutton.config(image=colorimg)

def colorImgBg(c: tuple):
    '''
    Make a solid-color image to display in the window.
    '''
    global bg_colorimg
    bg_colorimg = ImageTk.PhotoImage(Image.new('RGB', (16, )*2, c))
    bg_setcolorbutton.config(image=bg_colorimg)

def configcolor():
    '''
    Open color picker and set color if not cancelled by user.
    '''
    cpicker.show()
    cval = cpicker.result
    if cval is not None:
        charcolor.set(cval.hex)
        colorImg(cval.rgb)

    updateCharColors()

def bg_configcolor():
    '''
    Open color picker and set color if not cancelled by user.
    '''
    bg_cpicker.show()
    cval = bg_cpicker.result
    if cval is not None:
        bgcolor.set(cval.hex)
        colorImgBg(cval.rgb)

    updateCharColors()

setcolorbutton = Button(color, text='Foreground', compound=LEFT, style=(OUTLINE, DARK), command = configcolor, image=colorimg)
setcolorbutton.pack(side=TOP, expand=True, padx=5, pady=5)
bg_setcolorbutton = Button(color, text='Background', compound=LEFT, style=(OUTLINE, DARK), command = bg_configcolor, image=bg_colorimg)
bg_setcolorbutton.pack(side=TOP, expand=True, padx=5, pady=5)

chars = ['{} (U+{}: {})'.format(i, '{:4x}'.format(ord(i)).upper(), unicode_name(i).title()) for i in '█▓▒░─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬']
chars += ['{} (U+00{}: {})'.format(i, '{:2x}'.format(ord(i)).upper(), unicode_name(i).title()) for i in 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm~`!@#$%^&*_+-=,.<>?"\'\\/|[]{}()0123456789 ']

charframe = Labelframe(tools, text='Characters')
charframe.pack(side=TOP, expand=True)
charvar = StringVar(win, chars[0][0])

def updateCharColors():
    for i in charselframe.winfo_children():
        for j in i.winfo_children():
            j.config(background=bgcolor.get(), foreground=charcolor.get())

def updateChars(frame: ScrolledFrame, label: Label, text: str):
    for i in frame.winfo_children():
        for j in i.winfo_children():
            j.config(relief=FLAT)

    label.config(relief=SUNKEN)

    charvar.set(text)

def swapColors():
    tempcharc = charcolor.get()

    charcolor.set(bgcolor.get())
    bgcolor.set(tempcharc)

    colorImg(colutil.color_to_rgb(charcolor.get()))
    colorImgBg(colutil.color_to_rgb(bgcolor.get()))

    updateCharColors()

    del tempcharc
    
charselframe = create(chars, charframe, updateChars, charvar.get())
charselframe.pack(side=TOP, expand=True)

swapbutton = Button(color, text='Swap', command = swapColors)
swapbutton.pack(side=LEFT, anchor=S, padx=5, pady=5)

editor = Labelframe(win, text='Editor')
editor.pack(side=LEFT, expand=True, fill=BOTH)

class Character:
    def __init__(self, char: str, foreground: tuple, background: tuple):
        self.char = char
        self.foreground = foreground
        self.background = background
    def render(self, render: Image.Image, position: tuple):
        img = Image.new('RGB', (9, 16), (0, 0, 0))

        #dosfnt = ImageFont.FreeTypeFont('Modern DOS 9x16')
        draw = ImageDraw.ImageDraw(img, 'RGB')

        draw.text((0, 0), self.char, self.foreground, ImageFont.FreeTypeFont(path.join(getcwd(), 'dos.ttf')))

        render.convert('RGB').paste(img.convert('RGB'), (position[0], position[1]))
    def _find(self) -> tuple:

        x = 0
        
        for ind, i in enumerate(chargrid):
            if i == self:
                x = ind
                break

        y = chargrid[x].index(self)
        return (x, y)

#chargrid = [[Character(' ', (0, 0, 0), (255, 255, 255)), ] * 160,] * 160
chargrid: list[list[Character]] = []

preview = ScrolledFrame(editor)
preview.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)

newimgframe = Frame(preview)
newimgframe.pack(expand=True, fill=BOTH)

img_reso = [-1, -1]

newimgframe_xscale = Frame(newimgframe)
newimgframe_xscale.pack(side=TOP, expand=True, pady=5)

img_xres = Spinbox(newimgframe_xscale, from_=1, width=5)
img_xres.pack(side=RIGHT, expand=True)

Label(newimgframe_xscale, text='Width').pack(side=RIGHT, expand=True, padx=20)

newimgframe_yscale = Frame(newimgframe)
newimgframe_yscale.pack(side=TOP, expand=True, pady=5)

img_yres = Spinbox(newimgframe_yscale, from_=1, width=5)
img_yres.pack(side=RIGHT, expand=True)

Label(newimgframe_yscale, text='Height').pack(side=RIGHT, expand=True, padx=20)

def renderChars():
    #renderimg = Image.new('RGB', (len(chargrid), len(chargrid[0])), (0, 0, 0))
    #for x, i in enumerate(chargrid):
    #    for y, j in enumerate(i):
    #        j.render(renderimg, (x * 9, y * 16))

    #for i in chargrid:
    #    for j in i:
    #        print(preview.grid_info())
    pass

editor_pane.add(editor)
editor_pane.add(tools)

def setchar(event):
    chargrid[event.x // 9][event.y // 16].char = charvar.get()
    
    renderChars()

renderChars()

win.bell()
win.focus_set()

win.mainloop()
# import knihoven
# tkinter pro tvorbu oken
import tkinter as tk
# filedialog pro ukládání a otevírání souborů
from tkinter import filedialog
# urllib.request pro čtení dat obrázku ikony
import urllib.request
# Image pro čtení vložených obrázků
from PIL import Image
# ImageTk pro zobrazování obrázků
from PIL import ImageTk

# import ikony
url = "https://cdn-icons-png.flaticon.com/512/25/25645.png"
openurl = urllib.request.urlopen(url)
readicon = openurl.read()
openurl.close()

# třída obsahující hlavní okna programu
class Main:
    
    def mainWindow():
        mainWin = tk.Tk()
        mainWin.geometry("320x100")
        mainWin.configure(bg="#2d3329")
        mainWin.title("ASCII Art Converter")
        mainWin.resizable(False, False)
        icon = ImageTk.PhotoImage(data=readicon)
        mainWin.iconphoto(False, icon)
        
        tk.Button(mainWin, text="Otevřít fotku", bg="#858783", width=15, command=Backend.openFile).place(x=20, y=20)
        tk.Button(mainWin, text="Restart", bg="#858783", width=15, 
                  command=lambda:[mainWin.destroy(), Main.mainWindow()]).place(x=20, y=60)
        field = tk.Text(mainWin, height=20, width=20, bg="#2d3329")
        field.tag_config("warn", foreground="red")
        field.insert(tk.END, "Žádná fotka není otevřena.", "warn")
        field.pack(side=tk.RIGHT)
        mainWin.mainloop()
            
    def displayPhoto(path):
        
        try:
        
            createWin = tk.Tk()
            createWin.geometry("600x500")
            createWin.configure(bg="#2d3329")
            createWin.resizable(False, False)

            createWin.title("Vytvořit art")
        
            image = Image.open(path)
            resimage = image.resize((550,450), Image.ANTIALIAS)
            disimage = ImageTk.PhotoImage(resimage, master=createWin)

            tk.Button(createWin, text="Vytvořit art!", bg="#858783", width=15, command=lambda:[Backend.artConvert(path)]).place(x=250, y=460)
            imageframe = tk.Frame(createWin, width=550, height=450, bg="#2d3329")
            imageframe.pack()
            imlabel = tk.Label(imageframe, image=disimage)
            imlabel.photo = disimage
            imlabel.place(x=10, y=10)
        
        except AttributeError:
            quit()

class Backend:
    
    # funkce artConvert, která pracuje s otevřeným souborem (parametr impath)
    def artConvert(impath):
        
        # otevření a zpracování dat obrázku
        image = Image.open(impath)
        
        # vytvoření seznamu doneart,
        # který bude obsahovat výsledný text (ascii fotografii)
        doneart = []
        # přidělení proměnných pod metodu s velikostí obrázku
        (width, height) = image.size
        
        # cvytvoření ascii artu
        # první smyčka zpracovává číselnou hodnotu od 0
        # do hodnoty celkové délky obrázku
        # a přiřadí každému řádku prázdný prostor
        for h in range(0, height):
            line = ""
            # druhá smyčka dělá to samé s šířkou řádku
            # a poté použije metodu pixelToChar, pomocí které
            # nahradí každý pixel náhodným ascii znakem
            # - tento text poté uloží do seznamu doneart
            for w in range(0, width):
                pix = image.getpixel((w, h))
                line += Backend.pixelToChar(pix)
            doneart.append(line)
        
        # jakmile jsou smyčky ukončeny, je zavolána funkce saveFile
        # z třídy Backend, která uloží daný text ze seznamu jako textový soubor
        Backend.saveFile(doneart)
    
    # funkce pixelToChar nahradí každý pixel obrázku
    # jedním ze znaků ascii
    # - pixely přebírá z funkce artConvert (parametr pixel)
    def pixelToChar(pixel):
            
            # deklarace proměnných pro jednotlivé barevné složky pixelu
            (r, g, b) = pixel
            # skupina ascii znaků je zapsána do jednoho řetězce (stringu)
            characters = "`^,:;Il!i~+_-?][}{1)(|\/XYUJCLQ0OZ*#MW&8%B@$"

            # výpočet jasu pixelu sečtením 
            # všech složek dohromady
            # červená + zelená + modrá => bílá (jas)
            pixel_br = r + g + b
            # deklarace maximálního jasu pixelu
            # 770 je 255x3, protože máme tři
            max_br = 770
            # určení správného jasu pixelu vydělením
            # rozsahu skupiny ascii znaků maximálním jasem
            # - tímto vydělením získáme jednotný jas pro pixel nahrazený znakem
            brightness = len(characters)/max_br
            # nyní vynásobíme jednotný jas
            # konkrétním jasem daného pixelu a odečteme jednu, 
            # jinak bychom dostávali stále stejný index znaku
            pixel_index = int((pixel_br * brightness) - 1)
            
            # následně funkce vrací zvolený ascii znak
            # pomocí hodnoty konkrétního indexu
            return characters[pixel_index]
    
    # funkce openFile pro otevření obrázku
    def openFile():
            
            # spuštění dialogu pro získání cesty k souboru
            # omezeno na obrázky formátu JPEG
            filepath = filedialog.askopenfilename(title="Otevřít fotku",
                                            filetypes=[(".jpg", "*.jpg")])
            
            # spuštění zobrazovacího okna
            # s konkrétním souborem
            Main.displayPhoto(filepath)
    
    # funkce saveFile je opakem funkce openFile
    # parametr art je výsledný text převzatý od funkce artConvert
    def saveFile(art):
        
        # spuštění dialogu pro získání cesty k uložení souboru
        # omezeného jen na textové soubory
        savepath = filedialog.asksaveasfilename(title="Uložit art",
                                          filetypes=[(".txt",
                                          "*.txt")])
        
        # otevření lokace pro uložení
        with open(savepath, "w") as Art:
            # zapsání hotového textu
            for line in art:
                # zapsání každého řádku 
                Art.write(line)
                # a oddělení odstavce pro následující řádek
                Art.write("\n")
            # ukončení procesu po vypsání
            Art.close()

# spuštění uvítacího okna
Main.mainWindow()
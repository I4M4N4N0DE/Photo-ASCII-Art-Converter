# libraries import
# tkinter for creating the windows
import tkinter as tk
# filedialog for making the system opening and saving the files by itself
from tkinter import filedialog
# urllib.request for reading the data of the window icon image
import urllib.request
# Image for reading the data of the input images
from PIL import Image
# ImageTk for displaying the images
from PIL import ImageTk

# importing the icon 
url = "https://cdn-icons-png.flaticon.com/512/25/25645.png"
openurl = urllib.request.urlopen(url)
readicon = openurl.read()
openurl.close()

# class containing the main windows
class Main:
    
    def mainWindow():
        mainWin = tk.Tk()
        mainWin.geometry("320x100")
        mainWin.configure(bg="#2d3329")
        mainWin.title("ASCII Art Converter")
        mainWin.resizable(False, False)
        icon = ImageTk.PhotoImage(data=readicon)
        mainWin.iconphoto(False, icon)
        
        tk.Button(mainWin, text="Open a photo", bg="#858783", width=15, command=Backend.openFile).place(x=20, y=20)
        tk.Button(mainWin, text="Restart", bg="#858783", width=15, 
                  command=lambda:[mainWin.destroy(), Main.mainWindow()]).place(x=20, y=60)
        field = tk.Text(mainWin, height=20, width=20, bg="#2d3329")
        field.tag_config("warn", foreground="red")
        field.insert(tk.END, "No photo opened.", "warn")
        field.pack(side=tk.RIGHT)
        mainWin.mainloop()
            
    def displayPhoto(path):
        
        try:
            
            createWin = tk.Tk()
            createWin.geometry("600x500")
            createWin.configure(bg="#2d3329")
            createWin.resizable(False, False)

            createWin.title("Create an art")
        
            image = Image.open(path)
            resimage = image.resize((550,450), Image.ANTIALIAS)
            disimage = ImageTk.PhotoImage(resimage, master=createWin)

            tk.Button(createWin, text="Create an art!", bg="#858783", width=15, command=lambda:[Backend.artConvert(path)]).place(x=250, y=460)
            imageframe = tk.Frame(createWin, width=550, height=450, bg="#2d3329")
            imageframe.pack()
            imlabel = tk.Label(imageframe, image=disimage)
            imlabel.photo = disimage
            imlabel.place(x=10, y=10)
        except AttributeError:
            quit()

class Backend:
    
    # artConvert function which works with the image path parameter
    def artConvert(impath):
        
        # opening and reading the image
        image = Image.open(impath)
        
        # creating a list called doneart 
        # which contains the output text art string
        doneart = []
        # giving two variables for the image.size method
        (width, height) = image.size
        
        # creating the art
        # the first for loop reads the range from 0 to 
        # the final height of the image
        # and gives an empty space for every pixel in it
        for h in range(0, height):
            line = ""
            # the second for loop does the same thing with the width of the image,
            # but after that it calls the pixelToChar function and
            # represents that place with it's own calculated ASCII character
            # and saves it into the text art list
            for w in range(0, width):
                pix = image.getpixel((w, h))
                line += Backend.pixelToChar(pix)
            doneart.append(line)
        
        # after the loops are finished, saveFile function is called
        # with the list as the parameter for saving it
        Backend.saveFile(doneart)
    
    # the pixelToChar function replaces each pixel of the image
    # by a character from our collection
    # it takes each pixel of the image from the artConvert function
    def pixelToChar(pixel):
            
            # declaring three color variables for our pixel parameter
            (r, g, b) = pixel
            # our character set written as a string
            characters = "`^,:;Il!i~+_-?][}{1)(|\/XYUJCLQ0OZ*#MW&8%B@$"

            # calculating each pixel brightness by adding up 
            # all three color values together
            pixel_br = r + g + b
            # declaring the maximum brightness of each color of the pixel
            # 770 is 255x3, because we have three colors (r,g,b)
            max_br = 770
            # declaring the final pixel brightness by diving 
            # the length of the character set by the maximum brightness
            # by this division we'll get a full brightness level for the appropriate character
            brightness = len(characters)/max_br
            # now we have to multiply the oharacter brightness value
            # by the specific pixel values and jump back by 1 in the set, 
            # because without that we will get the same character every time
            pixel_index = int((pixel_br * brightness) - 1)
            
            # after that the function will return the specific 
            # character from the set
            return characters[pixel_index]
    
    # openFile function for opening the file
    # and giving it for the displaying function
    def openFile():
            
            # opening the file (this will get us the file path)
            filepath = filedialog.askopenfilename(title="Open a photo",
                                            filetypes=[(".jpg", "*.jpg")])
            
            # running the displaying function with the specific
            # file path
            Main.displayPhoto(filepath)
    
    # saveFile function does almost the same thing 
    # as the openFile function
    # the art parameter is the final character list
    # with the finished artwork (from the artConvert function)
    def saveFile(art):
        
        # running a window for choosing the saving location
        # it has to be limited only to .txt files
        savepath = filedialog.asksaveasfilename(title="Save the art",
                                          filetypes=[("Text file", 
                                          "*.txt")])
        
        # opening the location for writing
        with open(savepath, "w") as Art:
            # writing the text art
            for line in art:
                # writing every horizontal line of the text artwork
                Art.write(line)
                # then writing a new empty row for the next line
                Art.write("\n")
            # closing the file
            Art.close()

# running the main window
Main.mainWindow()
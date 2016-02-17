import tkinter as tk
import urllib.request as ul
import os
import time

class Main(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.grid()
        self.getDimensions(parent)
        self.setDefaults()
        self.createWidgets()

    def getDimensions(self, parent):
        # Get window dimensions and center application
        width = 300
        height = 200
        windowWidth = parent.winfo_screenwidth()
        windowHeight = parent.winfo_screenheight()
        x = (windowWidth / 2) - (width / 2)
        y = (windowHeight / 2) - (height / 2)
        parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def setDefaults(self):
        self.root.title('Speed Test') # Title
        self.config(cursor = "plus")  # Cursor
        
    def createWidgets(self):
        startButton = tk.Button(self, text = 'Start Test', \
                                    command = self.openTest)
        startButton.pack()

    def openTest(self):
        self.destroy()
        testWindow = TestWindow(self.root)

class TestWindow(tk.Toplevel):
    def __init__(self, original):
    #def __init__(self):
        tk.Toplevel.__init__(self)
        self.original_frame = original
        #self.geometry('300x200')
        self.getDimensions(original)
        self.createTestWindow()

    def getDimensions(self, parent):
        # Get window dimensions and center application
        width = 300
        height = 200
        windowWidth = parent.winfo_screenwidth()
        windowHeight = parent.winfo_screenheight()
        x = (windowWidth / 2) - (width / 2)
        y = (windowHeight / 2) - (height / 2)
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
    def createTestWindow(self):
        info = tk.Label(self, text = "Downloading File")
        info.pack()
        self.testDownload('https://raw.githubusercontent.com/c-nguyen/c-nguyen.github.io/master/README.md')

    def testDownload(self, url):
        startTime = time.clock()
        ul.urlretrieve(url, 'downloadedFile')    # Download file
        executionTime = time.clock() - startTime # Calculate execution time
        os.remove('downloadedFile')              # Delete file
        
if __name__ == '__main__':
    app = tk.Tk()
    Main(app).pack
    app.mainloop()

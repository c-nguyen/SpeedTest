"""
Contributors: Christine Nguyen
              Nelly Liu Peng
              Michael Dibeh
CS 299 - Team Project
"""

import dropbox
import tkinter as tk
import tkinter.ttk as ttk
import threading
import os
import time

class Main(tk.Frame):
    def __init__(self, parent):
        # Initialize class
        tk.Frame.__init__(self, parent)
        self.root = parent
        self.grid()

        self.fileToDL = 'TESTING (1).txt'
        self.fileToUL = 'TESTING.txt'
        
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
        # Set defaults for window
        self.root.title('Speed Test')      # Title
        self.root.config(cursor = "plus")  # Cursor

    def createWidgets(self):
        # Default Widgets
        self.startButton = tk.Button(self, text = 'Start Test')
        self.startButton.configure(command = self.changeToTest)
        self.startButton.pack()

        # Download Widgets
        self.downloadLabel = tk.Label(text = 'Downloading File')

        # Upload Widgets
        self.uploadLabel = tk.Label(text = 'Uploading File')

        # Threads
        lock = threading.Lock()
        self.dThread = threading.Thread(target = self.startDownload, args = (lock,))
        self.uThread = threading.Thread(target = self.startUpload, args = (lock,))
        
    def changeToTest(self):
        # Change root window to test window
        self.startButton.forget()

        self.client = dropbox.client.DropboxClient('RHOqvKFGSEAAAAAAAAAADKHuSyjNuI-gYmNtYvNIPODkTv1tHsv6KG3TvVyEzvv1')
        
        self.dThread.start() # Start download thread       
        self.uThread.start() # Start upload thread
        
    def startDownload(self, lock):
        with lock:
            # Setup for test
            self.root.config(cursor = 'wait')                               # Change cursor to wait
            self.downloadLabel.pack()                                       # Display download label
            
            # Start Test
            startTime = time.clock()                                        # Start timer
            f, metadata = self.client.get_file_and_metadata(self.fileToDL)  # Download file to computer
            out = open(self.fileToUL, 'wb')
            out.write(f.read())
            out.close()
            executionTime = time.clock() - startTime                        # Calculate total execution time
            # ENTER LINES TO CALCULATE DOWNLOAD RATE
            self.downloadLabel.config(text = 'Downloading File - FINISHED')
            self.root.config(cursor = 'plus')
            self.update()

    def startUpload(self, lock):
        with lock:
            # Setup for test
            self.root.config(cursor = 'wait')                        # Change cursor to wait
            self.uploadLabel.pack()                                  # Display upload label
            
            startTime = time.clock()                                 # Start timer
            f = open(self.fileToUL, 'rb')                            # Upload pic.jpg to Dropbox
            response = self.client.put_file(self.fileToUL, f)
            executionTime = time.clock() - startTime                 # Calculate total execution time
            self.uploadLabel.config(text = 'Upload File - FINISHED')
            # ENTER LINES TO CALCULATE UPLOAD RATE

            # Delete File
            path = self.fileToUL
            self.client.file_delete(path) # Remove file from dropbox
            os.remove(self.fileToUL)      # Remove file from computer

            completeLabel = tk.Label(text = 'Completed')
            completeLabel.pack()
            self.root.config(cursor = 'plus')
            self.update()

if __name__ == '__main__':
    app = tk.Tk()
    Main(app).pack
    app.mainloop()

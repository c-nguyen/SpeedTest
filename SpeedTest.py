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
        self.pack()
        """"
        self.fileToDL = 'TESTING (1).txt'
        self.fileToUL = 'TESTING.txt'
        self.dFileSize = 21
        """

        self.fileToDL = '20MB (1).jpg'
        self.fileToUL = '20MB.jpg'
        self.dFileSize = 20899548
        
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
        self.dProgBar = ttk.Progressbar(self, orient = 'horizontal', length = 250,\
                                        mode = 'determinate', maximum = self.dFileSize)

        # Upload Widgets
        self.uploadLabel = tk.Label(text = 'Uploading File')

        # Threads
        lock = threading.Lock()
        self.dThread = threading.Thread(target = self.startDownload, args = (lock,))
        #self.uThread = threading.Thread(target = self.startUpload, args = (lock,))
        
    def changeToTest(self):
        # Change root window to test window
        self.startButton.forget()

        self.client = dropbox.client.DropboxClient('RHOqvKFGSEAAAAAAAAAADKHuSyjNuI-gYmNtYvNIPODkTv1tHsv6KG3TvVyEzvv1')
        
        self.dThread.start() # Start download thread       
        #self.uThread.start() # Start upload thread
        
    def startDownload(self, lock):
        with lock:
            # Setup for test
            self.root.config(cursor = 'wait')                               # Change cursor to wait
            self.downloadLabel.pack()                                       # Display download label
            self.dProgBar.pack()                                            # Display download progress bar
            
            # Start Test
            startTime = time.clock()                                        # Start timer
            f, metadata = self.client.get_file_and_metadata(self.fileToDL)  # Get file from Dropbox
            
            out = open(self.fileToUL, 'wb')                                 # Open file for writing
            currentSize = 0                                                 # Current size of downloaded file
            while currentSize < self.dFileSize:                             # While downloading file size is less than total size
                out.write(f.read(20))                                       # Read and write 20 bytes of file from Dropbox
                currentSize += 20                                           # Add 20 to current size
                self.dProgBar['value'] = currentSize                        # Increase progress bar by 20
                if currentSize == self.dFileSize:
                    print('done')
            out.close()                                                     # Close file when finished
            executionTime = time.clock() - startTime                        # Calculate total execution time
            # ENTER LINES TO CALCULATE DOWNLOAD RATE
            self.downloadLabel.config(text = 'Downloading File - FINISHED')
            self.dProgBar.stop()
            self.root.config(cursor = 'plus')
            self.update()

    def startUpload(self, lock):
        with lock:
            # Setup for test
            self.root.config(cursor = 'wait')                        # Change cursor to wait
            self.uploadLabel.pack()                                  # Display upload label
            
            startTime = time.clock()                                 # Start timer
            with open(self.fileToUL, 'rb') as f:                     # Upload pic.jpg to Dropbox
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
    app.protocol('WM_DELETE_WINDOW', lambda : app.destroy())
    Main(app).pack
    app.mainloop()

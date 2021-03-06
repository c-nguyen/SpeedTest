"""
Contributors: Christine Nguyen
              Nelly Liu Peng
              Michael Dibeh
CS 299 - Team Project: Speed Test
Winter 2016
"""
from tkinter import *
#from PIL import Image, ImageTk
from io import BytesIO
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

        # Files to be tested
        self.fileToDL_1 = '20MB (1).jpg'
        self.fileToUL_1 = '20MB.jpg'
        self.FileSize_1 = 20899548

        self.fileToDL_2 = '105MB (1).pdf'
        self.fileToUL_2 = '105MB.pdf'
        self.FileSize_2 = 110728540

        # Set remanining settings
        self.getDimensions(parent)
        self.setDefaults()
        self.createWidgets()

    def getDimensions(self, parent):
        # Get window dimensions and center application
        width = 565
        height = 301
        windowWidth = parent.winfo_screenwidth()
        windowHeight = parent.winfo_screenheight()
        x = (windowWidth / 2) - (width / 2)
        y = (windowHeight / 2) - (height / 2)
        parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def setDefaults(self):
        # Set defaults for window
        self.root.title('Speed Test')      # Title
        self.root.config(cursor = "plus")  # Cursor

        #Background image
        background_image=tk.PhotoImage(file='101169 (2).gif')
        background_label = tk.Label(self.root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

    def createWidgets(self):
        # Default Widgets
        self.startButton = tk.Button(self.root, text = 'Start Test')
        self.startButton.configure(highlightthickness=0)
        self.startButton.configure(command = self.changeToTest)
        self.startButton.pack(side="top", padx=110, pady=132)

        # Progress Bar Widget
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('red.Horizontal.TProgressbar', foreground = 'red', background = 'red')

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
            # Display text
            self.infoLabel = tk.Label(text = 'Calculating Download Speed')
            #self.attributes("-alpha", 0.5)
            self.infoLabel.pack()                                            # Display download label

            # Store average data from two files
            dataTime1 = self.startDTest(self.fileToDL_1, self.fileToUL_1, self.FileSize_1)
            dataTime2 = self.startDTest(self.fileToDL_2, self.fileToUL_2, self.FileSize_2)
            avgTime = (dataTime1 + dataTime2) / 2

            # Print results to console
            print("Download times...")
            print("Time (mbps) for file 1:", dataTime1)
            print("Time (mbps) for file 2:", dataTime2)
            print("Average time (mbps):", avgTime)
            print()

    def startDTest(self, fileToDL, fileToUL, FileSize):
        # Setup for test
        self.ProgBar = ttk.Progressbar(self.root, orient = 'horizontal', length = 250,\
                                       mode = 'determinate', maximum = FileSize, style = 'red.Horizontal.TProgressbar')
        self.ProgBar.pack()                                              # Display download progress bar
        self.root.config(cursor = 'wait')                                # Change cursor to wait

        # Start Test
        startTime = time.time()                                          # --Timestamp before downloading file
        f, metadata = self.client.get_file_and_metadata(fileToDL)        # Get file from Dropbox

        BYTES = 1000000 # 1MB                                            # Constant determining how many bytes to read at a time
        out = open(fileToUL, 'wb')                                       # Open file for writing
        currentSize = 0                                                  # Current size of downloaded file
        while currentSize < FileSize:                                    # While downloading file size is less than total size
            out.write(f.read(BYTES))                                     # Read and write BYTES bytes of file from Dropbox
            currentSize += BYTES                                         # Add BYTES to current size
            self.ProgBar['value'] = currentSize                          # Increase progress bar by BYTES

        # Close file when finished
        out.close()

        executionTime = time.time() - startTime                          # --Timestamp after downloading file

        # Display results on console
        speed = FileSize / executionTime            # bytes per second
        finalSpeed = speed / 1000000                # convert to MB
        conversion = finalSpeed * 8                 # convert to megabits

        print("File name:", fileToUL)
        print("Bytes per second:", speed)
        print("Megabytes per second:", finalSpeed)
        print("Megabits per second:", conversion)
        print()

        # self.ProgBar.stop()
        self.root.config(cursor = 'plus')
        self.update()

        # Return time it took to download this file (mbps)
        return conversion

    def startUpload(self, lock):
        with lock:
            # Display text
            self.infoLabel = tk.Label(text = 'Calculating Upload Speed')
            self.infoLabel.pack()                                            # Display upload label

            # Store average data from two files
            dataTime1 = self.startUTest(self.fileToDL_1, self.fileToUL_1, self.FileSize_1)
            dataTime2 = self.startUTest(self.fileToDL_2, self.fileToUL_2, self.FileSize_2)
            avgTime = (dataTime1 + dataTime2) / 2

            # Print results to console
            print("Upload times...")
            print("Time (mbps) for file 1:", dataTime1)
            print("Time (mbps) for file 2:", dataTime2)
            print("Average time (mbps):", avgTime)
            print()

    def startUTest(self, fileToDL, fileToUL, FileSize):
        # Setup for test
        self.ProgBar = ttk.Progressbar(self.root, orient = 'horizontal', length = 250,\
                                       mode = 'determinate', maximum = FileSize, style = 'red.Horizontal.TProgressbar')
        self.ProgBar.pack()                                              # Display upload progress bar
        self.root.config(cursor = 'wait')                                # Change cursor to wait

        # Start test
        startTime = time.time()                                          # --Timestamp before uploading file
        self.ProgBar['value'] = 0
        chunk_size = 1024*1024 # 1MB
        upload_id = None
        offset = 0
        with open(fileToUL, 'rb') as f:
            while offset < FileSize:
                offset, upload_id = self.client.upload_chunk(
                    BytesIO(f.read(chunk_size)),
                    offset = offset, upload_id = upload_id)
                self.ProgBar['value'] = offset
        self.client.commit_chunked_upload('/auto/' + fileToUL, upload_id)
        executionTime = time.time() - startTime                          # --Timestamp after uploading file

        # Display results on console
        speed = FileSize / executionTime            # bytes per second
        finalSpeed = speed / 1000000                # convert to MB
        conversion = finalSpeed * 8                 # convert to megabits

        print("File name:", fileToUL)
        print("Bytes per second:", speed)
        print("Megabytes per second:", finalSpeed)
        print("Megabits per second:", conversion)
        print()

        # Delete File
        self.client.file_delete(fileToUL) # Remove file from dropbox
        os.remove(fileToUL)               # Remove file from computer

        self.root.config(cursor = 'plus')
        self.update()

        # Return time it took to upload this file (mbps)
        return conversion

if __name__ == '__main__':
    app = tk.Tk()
    app.protocol('WM_DELETE_WINDOW', lambda : app.destroy())
    Main(app).pack
    app.mainloop()

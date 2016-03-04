"""
Contributors: Christine Nguyen
              Nelly Liu Peng
              Michael Dibeh
CS 299 - Team Project: Speed Test
Winter 2016
"""

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
        self.dFileSize_1 = 20899548
        
        self.fileToDL_2 = '105MB (1).pdf'
        self.fileToUL_2 = '105MB.pdf'
        self.dFileSize_2 = 110728540

        # Set remanining settings
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
        self.startButton = tk.Button(self.root, text = 'Start Test')
        self.startButton.configure(command = self.changeToTest)
        self.startButton.pack()

        # Progress Bar Widget
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('red.Horizontal.TProgressbar', foreground = 'red', background = 'red')
   #  self.ProgBar = ttk.Progressbar(self.root, orient = 'horizontal', length = 250,\
   #                                mode = 'determinate', maximum = dFileSize, style = 'red.Horizontal.TProgressbar')
        self.infoLabel = tk.Label(text = 'Calculating Download Speed')

        # Threads
        lock = threading.Lock()
        self.dThread = threading.Thread(target = self.startDownload, args = (lock,))
        self.uThread = threading.Thread(target = self.startUpload, args = (lock,))
        
    def changeToTest(self):
        # Change root window to test window
        self.startButton.forget()

        self.client = dropbox.client.DropboxClient('RHOqvKFGSEAAAAAAAAAADKHuSyjNuI-gYmNtYvNIPODkTv1tHsv6KG3TvVyEzvv1')
        
        self.dThread.start() # Start download thread       
   #     self.uThread.start() # Start upload thread

    def startDownload(self, lock):
        with lock:
            # Store average data from two files
            dataTime1 = self.startDTest(self.fileToDL_1, self.fileToUL_1, self.dFileSize_1)
            dataTime2 = self.startDTest(self.fileToDL_2, self.fileToUL_2, self.dFileSize_2)
            avgTime = (dataTime1 + dataTime2) / 2

            # Print results to console
            print("Time (mbps) for file 1:", dataTime1)
            print("Time (mbps) for file 2:", dataTime2)
            print("Average time (mbps):", avgTime)
        
    def startDTest(self, fileToDL, fileToUL, dFileSize):
        # Setup for test
        self.infoLabel.pack()                                            # Display download label
        self.ProgBar = ttk.Progressbar(self.root, orient = 'horizontal', length = 250,\
                                   mode = 'determinate', maximum = dFileSize, style = 'red.Horizontal.TProgressbar')
        self.ProgBar.pack()                                              # Display download progress bar
        self.root.config(cursor = 'wait')                                # Change cursor to wait
            
        # Start Test
        startTime = time.time()                                          # --Timestamp before downloading file
        f, metadata = self.client.get_file_and_metadata(fileToDL)        # Get file from Dropbox
            
        BYTES = 1000000                                                  # Constant determining how many bytes to read at a time
        out = open(fileToUL, 'wb')                                       # Open file for writing
        currentSize = 0                                                  # Current size of downloaded file
        while currentSize < dFileSize:                                   # While downloading file size is less than total size
            out.write(f.read(BYTES))                                     # Read and write BYTES bytes of file from Dropbox
            currentSize += BYTES                                         # Add BYTES to current size
            self.ProgBar['value'] = currentSize                          # Increase progress bar by BYTES
                    
        # Close file when finished
        out.close()
            
        executionTime = time.time() - startTime                          # --Timestamp after downloading file

        # Display results on console
        speed = dFileSize / executionTime           # bytes per second
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

    """
    def startUpload(self, lock):
        with lock:
            
            # Store average data from two files
            dataTime1 = self.startUTest(self.fileToDL_1, self.fileToUL_1, self.dFileSize_1)
            dataTime2 = self.startUTest(self.fileToDL_2, self.fileToUL_2, self.dFileSize_2)
            avgTime = (dataTime1 + dataTime2) / 2

            # Print results to console
            print("Time (mbps) for file 1:", dataTime1)
            print("Time (mbps) for file 2:", dataTime2)
            print("Average time (mbps):", avgTime)

    def startUTest(self):        
            # Setup for test
            self.root.config(cursor = 'wait')                         # Change cursor to wait
            self.infoLabel.config(text = 'Calculating Upload Speed')  # Display upload label
            self.ProgBar['value'] = 0                                 # Display upload progress bar        
            #self.uploadData1.pack()                                  # Display 'Total execution time'
            #self.uploadData2.pack()                                  # Display 'Average time (seconds) per MB'
            #self.uploadData3.pack()                                  # Display 'Average Megabits per second'
            
            startTime = time.time()                                 # Start timer
            with open(self.fileToUL, 'rb') as f:                     # Upload file to Dropbox
                response = self.client.put_file(self.fileToUL, f)
            executionTime = time.time() - startTime                 # Calculate total execution time
            # ENTER LINES TO CALCULATE UPLOAD RATE
            
            offset = 0
            with open(self.fileToUL, 'rb') as f:
                while offset < self.dFileSize:
                    offset = self.client.upload_chunk( \
                        BytesIO(f.read(1000000)), offset = offset)
                    self.ProgBar['value'] = offset

            client.commit_chunked_upload(self.fileToUL)
                
            # Delete File
            path = self.fileToUL
            self.client.file_delete(path) # Remove file from dropbox
            os.remove(self.fileToUL)      # Remove file from computer
            
            completeLabel = tk.Label(text = 'Completed')
            completeLabel.pack()
            self.root.config(cursor = 'plus')
            self.update()
    """

if __name__ == '__main__':
    app = tk.Tk()
    app.protocol('WM_DELETE_WINDOW', lambda : app.destroy())
    Main(app).pack
    app.mainloop()

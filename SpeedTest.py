"""
Contributors: Christine Nguyen
              Nelly Liu Peng
              Michael Dibeh
CS 299 - Team Project: Speed Test
Winter 2016
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
        """
        self.fileToDL = 'TESTING (1).txt'
        self.fileToUL = 'TESTING.txt'
        self.dFileSize = 21
        """
        
        self.fileToDL = '20MB (1).jpg'
        self.fileToUL = '20MB.jpg'
        self.dFileSize = 20899548
        """
        self.fileToDL = '105MB (1).pdf'
        self.fileToUL = '105MB.pdf'
        self.dFileSize = 110728540
        """
        self.getDimensions(parent)
        self.setDefaults()
        self.createWidgets()

    def getDimensions(self, parent):
        # Get window dimensions and center application
        width = 300
        height = 300
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
        self.ProgBar = ttk.Progressbar(self, orient = 'horizontal', length = 250,\
                                        mode = 'determinate', maximum = self.dFileSize)
        self.downloadLabel = tk.Label(text = 'Downloading File')
        self.downloadData1 = tk.Label(text = 'Total execution time:')
        self.downloadData2 = tk.Label(text = 'Average time (seconds) per MB:')
        self.downloadData3 = tk.Label(text = 'Average Megabits per second:')

        # Upload Widgets
        # upload will use same ProgBar widget as above
        self.uploadLabel = tk.Label(text = 'Uploading File')
        self.uploadData1 = tk.Label(text = 'Total execution time:')
        self.uploadData2 = tk.Label(text = 'Average time (seconds) per MB:')
        self.uploadData3 = tk.Label(text = 'Average Megabits per second:')

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
            self.ProgBar.pack()                                             # Display download progress bar        
            self.downloadData1.pack()                                       # Display 'Total execution time'
            self.downloadData2.pack()                                       # Display 'Average time (seconds) per MB'
            self.downloadData3.pack()                                       # Display 'Average Megabits per second'

            readTimes = []                                                  # --List to calculate average download rate
            BYTES = 1000000                                                 # --Number of bytes to read from file at a time
            
            # Start Test
            startTime = time.clock()
            f, metadata = self.client.get_file_and_metadata(self.fileToDL)  # Get file from Dropbox     
            
            out = open(self.fileToUL, 'wb')                                 # Open file for writing
            currentSize = 0                                                 # Current size of downloaded file
            while currentSize < self.dFileSize:                             # While downloading file size is less than total size
                readStartTime = time.clock()                                # --Timestamp before downloading BYTES bytes
                out.write(f.read(BYTES))                                    # Read and write BYTES bytes of file from Dropbox
                readEndTime = time.clock() - readStartTime                  # --Timestamp after downloading BYTES bytes
                currentSize += BYTES                                        # Add BYTES to current size
                self.ProgBar['value'] = currentSize                         # Increase progress bar by BYTES
                readTimes += [readEndTime]                                  # --Add time length it took to download BYTES bytes to list
                if currentSize == self.dFileSize:
                    print('done')
                    
            # Close file when finished
            out.close()
            
            executionTime = time.clock() - startTime                        # Calculate total execution time

            # --Calculate download rate
            totalTimeLength = 0
            for times in readTimes:
                totalTimeLength += times
            avgTimePerBYTES = totalTimeLength/len(readTimes)                # --The avg time it takes to download BYTES bytes from file

            # Display results on console
            avgTimePerKB = 1000*avgTimePerBYTES/BYTES
            avgBYTESPerSec = BYTES/avgTimePerBYTES
            avgMBPerSec = BYTES/avgTimePerBYTES/1000000
            avgmbps = avgMBPerSec*8
            
            print("File name", self.fileToUL)
            print("Average time it takes to download %s bytes:"%(BYTES), avgTimePerBYTES)
            print("Total execution time:", executionTime)
            print("File Size (total number of bytes):", self.dFileSize)
            print("Total splits per file:", len(readTimes))
            print("Average time (seconds) per kilobyte:", avgTimePerKB)
            print("Average BYTES per second:", avgBYTESPerSec)
            print("Average MB per second:", avgMBPerSec)
            print("Average MegaBits per second:", avgmbps)

            # Display results on window
            self.downloadLabel.config(text = 'Downloading File - FINISHED')
            self.downloadData1.config(text = 'Total execution time: ' + str(executionTime))
            self.downloadData2.config(text = 'Average time (seconds) per KB: ' + str(avgTimePerKB))
            self.downloadData3.config(text = 'Average Megabits per second: ' + str(avgmbps))
            
            self.ProgBar.stop()
            self.root.config(cursor = 'plus')
            self.update()

    def startUpload(self, lock):
        with lock:
            # Setup for test
            self.root.config(cursor = 'wait')                        # Change cursor to wait
            self.uploadLabel.pack()                                  # Display upload label
            self.ProgBar.pack()                                      # Display upload progress bar        
            self.uploadData1.pack()                                  # Display 'Total execution time'
            self.uploadData2.pack()                                  # Display 'Average time (seconds) per MB'
            self.uploadData3.pack()                                  # Display 'Average Megabits per second'
            
            startTime = time.clock()                                 # Start timer
            with open(self.fileToUL, 'rb') as f:                     # Upload file to Dropbox
                response = self.client.put_file(self.fileToUL, f)
            executionTime = time.clock() - startTime                 # Calculate total execution time
            self.uploadLabel.config(text = 'Uploading File - FINISHED')
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

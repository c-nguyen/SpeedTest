"""
Contributors: Christine Nguyen
              Nelly Liu Peng
              Michael Dibeh
CS 299 - Team Project: Speed Test
Winter 2016

Dropbox module needed for this app to work (server for storage/transfer of files).
Download at: https://github.com/dropbox/dropbox-sdk-python
"""

from io import BytesIO
import dropbox
import tkinter as tk
import tkinter.ttk as ttk
import threading
import queue
import os
import time

class Main(tk.Frame):
    def __init__(self, parent):
        # Initialize class
        self.root = parent

        self.width = 565
        self.height = 301
        
        self.testCanvas = tk.Canvas(self.root, width = self.width, height = self.height,\
                          bd = 0, highlightthickness = 0)       # Test window
        self.resultCanvas = tk.Canvas(self.root, width = self.width, height = self.height,\
                            bd = 0, highlightthickness = 0)     # Result window

        # Files to be tested
        """
        self.fileToDL_1 = '20MB (1).jpg'
        self.fileToUL_1 = '20MB.jpg'
        self.FileSize_1 = 20899548
        
        self.fileToDL_2 = '105MB (1).pdf'
        self.fileToUL_2 = '105MB.pdf'
        self.FileSize_2 = 110728540
        """
        self.fileToDL_1 = 'TESTING (1).txt'
        self.fileToUL_1 = 'TESTING.txt'
        self.FileSize_1 = 21
        
        self.fileToDL_2 = 'TESTING2 (1).txt'
        self.fileToUL_2 = 'TESTING2.txt'
        self.FileSize_2 = 21
        

        # Set remanining settings
        self.getDimensions(parent)
        self.setDefaults()
        self.createWidgets()

    def getDimensions(self, parent):
        # Get window dimensions and center application
        windowWidth = parent.winfo_screenwidth()
        windowHeight = parent.winfo_screenheight()
        x = (windowWidth / 2) - (self.width / 2)
        y = (windowHeight / 2) - (self.height / 2)
        parent.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

    def setDefaults(self):
        # Set defaults for window
        self.root.title('Internet Speed Test')      # Title
        self.root.config(cursor = "plus")           # Cursor

        # Background image
        self.background_image = tk.PhotoImage(file='bg_image.gif')
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.pack(side = 'top', fill = 'both', expand = 'yes')
        self.background_label.image = self.background_image

    def createWidgets(self):
        # Default Widgets
        self.startButton = tk.Button(self.background_label, text = 'Start Test')
        self.startButton.configure(command = self.changeToTest)
        self.startButton.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

        # Progress Bar Widget
        s = ttk.Style()
        s.theme_use('alt')
        s.configure('blue.Horizontal.TProgressbar', background = 'white')
        self.ProgBar = ttk.Progressbar(self.testCanvas, orient = 'horizontal', length = 250, mode = 'determinate')

        # Threads
        avgTime1 = 0
        avgTime2 = 0
        q = queue.Queue()
        
        lock = threading.Lock()
        self.dThread = threading.Thread(target = self.startDownload, args = (lock, avgTime1, q))
        self.uThread = threading.Thread(target = self.startUpload, args = (lock, avgTime2, q))
        self.rThread = threading.Thread(target = self.changeToResults, args = (lock, q))
        
    def changeToTest(self):
        # Change root window to test window
        self.background_label.forget()
        #self.background_label.destroy()

        self.testText1 = 'Calculating Download Speed'
        self.testText2 = 'Calculating Upload Speed'
        self.fileSizeText1 = 'Testing speed of small file'
        self.fileSizeText2 = 'Testing speed of large file'
        
        self.testCanvas.pack(side = 'top', fill = 'both', expand = 'yes')
        self.testCanvas.create_image(0, 0, image = self.background_image, anchor = 'nw')
        
        self.client = dropbox.client.DropboxClient('RHOqvKFGSEAAAAAAAAAADKHuSyjNuI-gYmNtYvNIPODkTv1tHsv6KG3TvVyEzvv1')
        
        self.dThread.start() # Start download thread       
        self.uThread.start() # Start upload thread
        self.rThread.start() # Show results

    def startDownload(self, lock, avgTime1, q):
        with lock:
            # Display text
            self.text1 = self.testCanvas.create_text(self.width/2, (self.height/2)*0.3, text = self.testText1,\
                         fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 16, 'bold'))
            self.text2 = self.testCanvas.create_text(self.width/2, (self.height/2)*0.5, text = self.fileSizeText1,\
                         fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 14, 'bold'))

            # Store average data from two files
            dataTime1 = self.startDTest(self.fileToDL_1, self.fileToUL_1, self.FileSize_1)
            self.testCanvas.itemconfig(self.text2, text = self.fileSizeText2)
            dataTime2 = self.startDTest(self.fileToDL_2, self.fileToUL_2, self.FileSize_2)
            avgTime1 = (dataTime1 + dataTime2) / 2
            q.put(avgTime1)
            
            # Print results to console
            print("Download times...")
            print("Time (mbps) for file 1:", dataTime1)
            print("Time (mbps) for file 2:", dataTime2)
            print("Average time (mbps):", avgTime1)
            print()
            
        
    def startDTest(self, fileToDL, fileToUL, FileSize):
        # Setup for test
        self.ProgBar['value'] = 0
        self.ProgBar['maximum'] = FileSize
        self.ProgBar.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)   # Display download progress bar
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
        out.close()                                                      # Close file when finished
            
        executionTime = time.time() - startTime                          # --Timestamp after downloading file

        # Display results on console
        speed = FileSize / executionTime            # bytes per second
        finalSpeed = speed / 1000000                # convert to MB
        conversion = finalSpeed * 8                 # convert to megabits  
            
        self.root.config(cursor = 'plus')

        # Return time it took to download this file (mbps)
        return conversion

    def startUpload(self, lock, avgTime2, q):
        with lock:
            # Display correct text
            self.testCanvas.itemconfig(self.text1, text = self.testText2)
            self.testCanvas.itemconfig(self.text2, text = self.fileSizeText1)
            
            # Store average data from two files
            dataTime1 = self.startUTest(self.fileToDL_1, self.fileToUL_1, self.FileSize_1)
            self.testCanvas.itemconfig(self.text2, text = self.fileSizeText2)
            dataTime2 = self.startUTest(self.fileToDL_2, self.fileToUL_2, self.FileSize_2)
            avgTime2 = (dataTime1 + dataTime2) / 2
            q.put(avgTime2)

            # Print results to console
            print("Upload times...")
            print("Time (mbps) for file 1:", dataTime1)
            print("Time (mbps) for file 2:", dataTime2)
            print("Average time (mbps):", avgTime2)
            print()
            

    def startUTest(self, fileToDL, fileToUL, FileSize):
        # Setup for test
        self.ProgBar['value'] = 0
        self.ProgBar['maximum'] = FileSize
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
                
        # Delete File            
        self.client.file_delete(fileToUL) # Remove file from dropbox
        os.remove(fileToUL)               # Remove file from computer

        self.root.config(cursor = 'plus')

        # Return time it took to upload this file (mbps)
        return conversion

    def changeToResults(self, lock, q):
        with lock:
            self.testCanvas.forget()
            #self.testCanvas.destroy()

            self.resultCanvas.pack(side = 'top', fill = 'both', expand = 'yes')
            self.resultCanvas.create_image(0, 0, image = self.background_image, anchor = 'nw')

            # Results title
            self.root.title('Internet Speed Test Results')      # Title
            self.resultCanvas.create_text(self.width/2, (self.height/2)*0.3, text = 'RESULTS',\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 26, 'bold'))

            # Download results
            self.resultCanvas.create_text((self.width/2)*0.4, (self.height/2)*0.8, text = 'Download Speed',\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 20, 'bold'))
            self.resultCanvas.create_text((self.width/2)*0.4, (self.height/2)*1, text = 'Megabits per second:',\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 16, 'bold'))
            self.resultCanvas.create_text((self.width/2)*0.4, (self.height/2)*1.2, text = format(q.get(), '.9f'),\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 16, 'bold'))

            # Upload results
            self.resultCanvas.create_text((self.width/2)*1.6, (self.height/2)*0.8, text = 'Upload Speed',\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 20, 'bold'))
            self.resultCanvas.create_text((self.width/2)*1.6, (self.height/2)*1, text = 'Megabits per second:',\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 16, 'bold'))
            self.resultCanvas.create_text((self.width/2)*1.6, (self.height/2)*1.2, text = format(q.get(), '.9f'),\
                                        fill = 'white', anchor = tk.CENTER, font = ('Arial Narrow', 16, 'bold'))

if __name__ == '__main__':
    app = tk.Tk()
    #app.protocol('WM_DELETE_WINDOW', lambda : app.destroy())
    Main(app)
    app.mainloop()

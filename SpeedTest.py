import dropbox
from time import time       # To calculate upload/download times

# SETTING UP CONNECTION WITH DROPBOX
app_key = '6atbe2goehmkoa4'
app_secret = '34k3mvy7et67wj5'
flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
authorize_url = flow.start()
print('1. Go to: ' + authorize_url)
print('2. Click "Allow" (you might have to log in first)')
print('3. Copy the authorization code.')
code = input("Enter the authorization code here: ").strip()
access_token, user_id = flow.finish(code)
client = dropbox.client.DropboxClient(access_token)
print("Dropbox now ready...")

# UPLOADING FILE
start = time()
filename = 'testing.txt'
f = open(filename, 'rb')
response = client.put_file(filename, f)
print("Upload complete!")
elapse = start - time()
print('Elapsed time:', elapse)

# DELETING FILE
folder_metadata = client.metadata('/')          #displays relevant info in dropbox
contents_list = folder_metadata['contents']     #this contains all files in dropbox. contents_list is a List of dicts

def search(filename, path):             #search thru dict (this method used only if there were already files in dropbox)
    for items in contents_list:         #(this method not needed if dropbox is empty from start->only one file present, no need to search)
        if items['path'] == path:
            return items
path = '/%s'%(filename)
justaddedfile = search(filename,path)   #just addedfile is a dict

def delete(filename):
    client.file_delete(path)
delete(justaddedfile)
print("File deleted!")

""" Replace current search() and delete() for this one if only one file in dropbox.
Ideal to use when dropbox is initially empty. after a file is uploaded, immediately delete it.
I commented this temporarily so we can keep on testing.

def delete():
    for item in contents_list:
        delete(item)
delete()
"""


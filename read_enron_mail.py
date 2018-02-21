import os
import tarfile as t
import shutil
import re


#read email and return sender and message ID
def get_metadata(file):
    message_from = ''
    message_id = ''
    file = open(file)
    #enclose in while loop to ensure metadata doesn't get overwritten by threaded emails below
    while message_from == '' or message_id == '':
        for line in file:
            if line.startswith('From:'):
                start = line.find('From:') + 60
                end = line.find('.com') + 4
                message_from = line[start:end]
            elif line.startswith('Message-ID:'):
                start = line.find('Message-ID: <') + 13
                end = line.find('.JavaMail')
                message_id = line[start:end]
    return message_from, message_id


#iterate over files in from_folder and copy them all to to_folder, renaming each with message_from and message_id
def copy_emails(from_folder, to_folder):
    for file in os.listdir(from_folder):
        message_from, message_id = get_metadata(file)
        shutil.copy2('{}\\{}'.format(from_folder, file), '{}\\{}_{}'.format(to_folder, message_from, message_id))


os.chdir('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir\\allen-p')
copy_emails('sent', 'C:\\Users\\MGOW\\Documents\\PythonProject\\all_emails')


#create new folder folder_name for each employee (useful for data cleanup)
def create_folders(folder_name):
    for folder in os.listdir('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir'):
        os.chdir('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir\\{}'.format(folder))
        os.mkdir('{}'.format(folder_name))


#check for dupes in a folder folder_name
def check_dupes(folder_name):
    pass






#sent_folders = []

#for path, folders, files in os.walk('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir'):
    #for name in folders:
        #if name.endswith('_sent_mail'):
            #print('path: {}, folders: {}, files: {}, count: {}'.format(path, folders, files, len(files)))
            #sent_folders.append(os.path.join(path, name))
        #elif name.endswith('sent'):
            #sent_folders.append(os.path.join(path, name))

#print(sent_folders)

#will contain sender's name, number of emails sent, earliest sent date, latest sent date, average word count of their emails, and person they sent the most emails to
#profiles = []

#check how many sent items each person has
#for folder in sent_folders:
    #for path, folders, files in os.walk(folder):
        #sent_dict = {'name': os.path.dirname(os.path.relpath(path, start='C:\\Users\\MGOW\\Documents\\PythonProject\\maildir')), 'sent_count': len(files)}
        #profiles.append(sent_dict)

#print(sorted(profiles, key = lambda k: k['sent_count'], reverse = True))  #you have to use this weird temporary lambda function to sort by the key of a dict

#check the earliest sent date for a person


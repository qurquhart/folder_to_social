import os
import shutil
import re
import glob
from logger import Logger, creds
from twitter_api import twitter_post_media
from reddit import post_to_reddit


#----------------------------------------------------#
# Config Setup
#----------------------------------------------------#

def post_config(key):
    credentials = open("config/post.config")
    found = 0
    for line in credentials:
        search = re.findall(f'{key}=(.*)',line)
        if search:
            found += 1
            return(search[0])
    if found == 0:
        return "key not found"

#----------------------------------------------------#
# /Config Setup
#----------------------------------------------------#

#----------------------------------------------------#
# Logging Setup
#----------------------------------------------------#

email_list = ['quintonurquhart@gmail.com']

log = Logger("activity.txt",
             "img_poster",
             gmail_email=creds('gmail_email'),
             gmail_password=creds('gmail_password'),
             email_list=email_list,
             email_subject="img_poster error log")

error = Logger("error.txt",
             "img_poster",
             gmail_email=creds('gmail_email'),
             gmail_password=creds('gmail_password'),
             email_list=email_list,
             email_subject="img_poster error log")

#----------------------------------------------------#
# /Logging Setup
#
# log.text('test log.text()', send_mail=False)
# error.text('test error.text()', send_mail=True)
#----------------------------------------------------#

#----------------------------------------------------#
# Directories
#----------------------------------------------------#

def move_it(filename, base_directory, final_directory):

    try:
        # check if the file exists in destination
        log.text(f'Checking if {base_directory}{final_directory}{filename} exists.')
        if os.path.exists(f"{base_directory}{final_directory}{filename}"):
            # if it does exist, remove it and notify user
            os.remove(f"{base_directory}{final_directory}{filename}")
            log.text(f'File name already exists in destination. Deleting the old file at: {final_directory}{filename}.')
        # now that the destination is free of duplicates, move to destination and notify user
        shutil.move(file_location, f'{base_directory}{final_directory}')
        log.text(f'Moved {file_location} to {base_directory}{final_directory}.')
    except Exception as ex:
        error.text(f'Unable to move {file_location} to {base_directory}{final_directory}: {ex}')


def create_dir(base_directory, directory_to_be):

    if not os.path.isdir(f'{base_directory}{directory_to_be}'):
        
        log.text(f'{base_directory}{directory_to_be} directory not found.')
        try:
            os.makedirs(os.path.dirname(f'{base_directory}{directory_to_be}'), exist_ok=True)
            log.text(f'Created {base_directory}{directory_to_be} directory.')
        except Exception as ex:
            error.text(f'Unable to create {base_directory}{directory_to_be} directory! - {ex}')


base_directory = "img/"
invalid_directory = "invalid/"
posted_directory = "posted/"

create_dir(base_directory,"")
create_dir(base_directory, invalid_directory)
create_dir(base_directory, posted_directory)

#----------------------------------------------------#
# /Directories
#----------------------------------------------------#

#----------------------------------------------------#
# Validation
#----------------------------------------------------#

acceptable_filetypes = [".gif",".jpg", ".png"] # ".mp4",
file_list = []

for filetype in acceptable_filetypes:
    for f in glob.glob(base_directory+"*"+filetype):
        file_list.append(f)

if not file_list:
    log.text(f'No files with valid file formats found in "{os.path.abspath(base_directory)}".  Acceptable formats include the following: {acceptable_filetypes}.')
    exit()
else:
    first_file = file_list[0]   

file_location = first_file
file_with_extension = os.path.basename(first_file)

log.text(f'First file in base directory: {file_with_extension}')

#----------------------------------------------------#
# /Validation
#----------------------------------------------------#

#----------------------------------------------------#
# Formatting
#----------------------------------------------------#

filepath_noextension, file_type = os.path.splitext(file_location)
filename = os.path.basename(filepath_noextension)

post_title = filename
file_to_post = file_location

#----------------------------------------------------#
# /Formatting
#----------------------------------------------------#

#----------------------------------------------------#
# Post File
#----------------------------------------------------#

if file_to_post:
    log.text(f'Atempting to post with title: {post_title}')
    # post it
    if post_config('post_to_twitter').lower() == 'true':
        try:
            twitter_post_media(post_config('twitter_key'), post_config('twitter_secret'), post_title, file_to_post)
            log.text('Tweet posted successfully.')
            
        except Exception as ex:
            error.text(f'Tweet unable to post: {ex}')
    
        try:
            post_to_reddit(post_title, file_to_post)
            log.text('Posted to reddit successfully.')

        except Exception as ex:
            error.text(f'Unable to post to Reddit: {ex}')
    
    
    else:
        log.text('No accounts set to post.')

    move_it(f'{os.path.basename(file_location)}',base_directory, posted_directory)
    log.text(f'Moved file to {posted_directory}')

else:
    move_it(f'{os.path.basename(file_location)}',base_directory, invalid_directory)
    error.text(f'Moved file to {invalid_directory}')
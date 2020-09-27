import os
import shutil
import re
from logger import Logger, creds
from twitter_api import twitter_post_media, twitter_config


#----------------------------------------------------#
# Config Setup
#----------------------------------------------------#

def post_config(key):
    credentials = open("post.config")
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
#
# log.text('test log.text()', send_mail=False)
# error.text('test error.text()', send_mail=True)
#
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
#----------------------------------------------------#

#----------------------------------------------------#
# Directories
#----------------------------------------------------#

def move_it(base_directory, final_directory):

    try:
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


base_directory = "./img/"
invalid_directory = "invalid/"
posted_directory = "posted/"

create_dir(base_directory,"")
create_dir(base_directory, invalid_directory)
create_dir(base_directory, posted_directory)

first_file = os.listdir(base_directory)[0]
if first_file == 'invalid':
    log.text('Base directory empty. Exiting.')
    exit()       

file_location = f"{base_directory}{first_file}"

log.text(f'First file in base directory: {first_file}')

#----------------------------------------------------#
# /Directories
#----------------------------------------------------#

#----------------------------------------------------#
# Format Check
#----------------------------------------------------#

def file_type_check(file_location):
    
    file_noextension, file_type = os.path.splitext(file_location)
    filename = os.path.basename(file_noextension)

    acceptable_filetypes = [".mp4",".gif",".jpg", ".png"]

    if file_type in acceptable_filetypes:
        log.text(f"Acceptable file type: {file_type}")
        return filename, file_location
    else:
        error.text(f"Unacceptable file type: {file_type}.  Acceptable file types include {acceptable_filetypes}")   
        

post_title, file_to_post = file_type_check(file_location)

#----------------------------------------------------#
# /Format Check
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
            move_it(base_directory, posted_directory)
        except Exception as ex:
            error.text(f'Tweet unable to post: {ex}')
    else:
        log.text('No accounts set to post.')

else:
    move_it(base_directory, invalid_directory)
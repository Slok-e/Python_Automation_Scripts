from csv import field_size_limit
import os
import sys
import time
import shutil
import logging
import fileinput
from os import listdir
from fileinput import filename
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

source_dir = "/Users/kelsobroderick/Downloads"
dest_image = "/Users/kelsobroderick/Desktop/Download\(Sorted\)/Images"
dest_music = "/Users/kelsobroderick/Desktop/Download\(Sorted\)/Music"
dest_sfx = "/Users/kelsobroderick/Desktop/Download\(Sorted\)/Music/Sfx"
dest_video = "/Users/kelsobroderick/Desktop/Download\(Sorted\)/Video"

#Defines the funcion move
def move(dest, entry, name):
    file_exist = os.path.exists(dest + "/" + name)
    if file_exist:
        unique_name = makeUnique(name)
        os.rename(entry,unique_name)
    shutil.move(entry,dest)

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
       with os.scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            dest = source_dir
            if name.endswith(".wav") or name.endswith(".mp3") or name.endwitg(".mp4"):
                if fileinput
            return super().on_modified(event)
    


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

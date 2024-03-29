from shutil import move
import logging
import time

from os import scandir, rename
from os.path import splitext, exists, join

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#Mac or linux use "/Users/Whatever/Location"  or "C://" for Windows
source_dir = "/Users/kelsobroderick/Downloads"
dest_image = "/Users/kelsobroderick/Desktop/Download_sorted/Images"
dest_music = "/Users/kelsobroderick/Desktop/Download_sorted/Music"
dest_sfx = "/Users/kelsobroderick/Desktop/Download_sorted/Music/Sfx"
dest_video = "/Users/kelsobroderick/Desktop/Download_sorted/Video"
dest_documents = "/Users/kelsobroderick/Desktop/Download_sorted/Documents"

# Function to add 1 to end of duplicate download.
def makeUnique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        path = f"{filename}({str(counter)}){extension}"
        counter += 1
    
    return name

#Function to move a file.
def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = makeUnique(dest,name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry,dest)

# This runs when a directory is modified (scandir) i.e. file added to directory.
# It self checks the file extension type and allocates it to a location specified by th chosen directory.
class Handler(FileSystemEventHandler):
    def on_modified(self, event):
       with scandir(source_dir) as entries:
        for entry in entries:
            name = entry.name
            self.check_all_files(entry, name)

    # Function to scan all file types and extentions.
    def check_all_files(self, entry, name):
        
        # Audio file types:
        audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac", ".mp4"]
        # Video file types:
        video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                            ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
        # Image file types:
        image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                        ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
        # Document file types:
        doc_extensions = [".doc", ".docx", ".odt", ".pages",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
        
        for audio_extensions in audio_extensions:
            if name.endswith(audio_extensions) or name.endswith(audio_extensions.upper()):
                if entry.stat().st_size < 10000000 or "SFX" in name:
                    dest = dest_sfx
                else:
                    dest = dest_music
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: (name)")        
        for video_extensions in video_extensions:
            if name.endswith(video_extensions) or name.endswith(video_extensions.upper()):
                move_file(dest_video, entry, name)
                logging.info(f"Moved video file: {name}")        
        for image_extensions in image_extensions:
            if name.endswith(image_extensions) or name.endswith(image_extensions.upper()):
                move_file(dest_image, entry, name)
                logging.info(f"Moved image file: {name}")        
        for doc_extensions in doc_extensions:
            if name.endswith(doc_extensions) or name.endswith(doc_extensions.upper()):
                move_file(dest_documents, entry, name)
                logging.info(f"Moved document file: {name}")

# Makes the Process Run
if __name__ == "__main__":
    logging.basicConfig(filename='automation.log',
                        filemode='a',
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%m-%d-%Y %H:%M:%S')
    path = source_dir
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
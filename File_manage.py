import os
import sys
import time
import logging
from os import listdir
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
from watchdog.events import DirCreatedEvent

source_dir = "/Users/kelsobroderick/Downloads"

with os.scandir(source_dir) as entries:
    for entry in entries:
        print(entry.name)


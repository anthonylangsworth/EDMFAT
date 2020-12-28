import sys
import os
from typing import Optional, Tuple, Dict, Any
#import requests
try:
    # Python 2
    import Tkinter as tk
except ModuleNotFoundError:
    # Python 3
    import tkinter as tk

import myNotebook
from config import config, appname
import logging

this = sys.modules[__name__]
this.plugin_name = "EDMFS"
this.version_info = (0, 1, 0)
this.version = ".".join(map(str, this.version_info))
this.minorFaction = "EDA Kunti League"

# A Logger is used per 'found' plugin to make it easy to include the plugin's
# folder name in the logging output format.
# NB: plugin_name here *must* be the plugin's folder name as per the preceding
#     code, else the logger won't be properly set up.
logger = logging.getLogger(f'{appname}.{os.path.basename(os.path.dirname(__file__))}')

# If the Logger has handlers then it was already set up by the core code, else
# it needs setting up here.
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)


def plugin_start3(plugin_dir: str) -> str:
    return this.plugin_name


def plugin_app(parent: myNotebook.Notebook) -> Tuple[tk.Label, tk.Label]:
    label = tk.Label(parent, text="%s:" % this.plugin_name)
    this.status = tk.Label(parent, text="v%s - Ready" % this.version, anchor=tk.W)
    return label, this.status


def plugin_prefs(parent: myNotebook.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:

    PADX = 10
    PADY = 2

    frame = myNotebook.Frame(parent)

    myNotebook.Label(frame, text="Elite Dangerous Minor Faction Support").grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY, sticky=tk.W)

    myNotebook.Label(frame).grid(sticky=tk.W)   # spacer

    myNotebook.Label(frame, text="Minor Faction").grid(row=2, padx=PADX, sticky=tk.W)
    myNotebook.Entry(frame).grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky=tk.EW)
    
    return frame

def prefs_changed(cmdr:str, is_beta: bool) -> None:
    # Preferences changed
    return None

def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: Dict[str, Any], state: Dict[str, Any]) -> None:
    # if entry["event"] in ["CarrierJumpRequest", "CarrierJumpCancelled"] and not is_beta:
    # this.status["text"] = "v%s - Ready" % this.version
    return None

  
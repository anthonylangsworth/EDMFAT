import sys
import os
from typing import Optional, Tuple, Dict, Any, Union
import requests
import tkinter as tk
import myNotebook
from config import config, appname
import logging

this = sys.modules[__name__]
this.plugin_name = "Minor Faction Support"
this.version = "0.1"
this.minor_faction = "EDA Kunti League"
this.activity = ""

# Setup logging
logger = logging.getLogger(f'{appname}.{os.path.basename(os.path.dirname(__file__))}')

# Called by EDMC on startup
def plugin_start3(plugin_dir: str) -> str:
    clear_activity()
    return this.plugin_name

# Called by EDMC to show plug-in details on EDMC main window
def plugin_app(parent: myNotebook.Notebook) -> Union[tk.Widget, Tuple[tk.Widget, tk.Widget]]:
    frame = myNotebook.Frame(parent)
    frame.columnconfigure(1, weight=1)
    tk.Label(frame, text=this.minor_faction, anchor=tk.W).grid(row=0, column=0)
    tk.Button(frame, text="Copy", command=copy_activity_to_clipboard).grid(row=0, column=1, sticky=tk.E)
    tk.Label(frame, text="(No activity)", anchor=tk.W, justify=tk.LEFT, pady=10).grid(row=1, column=0, columnspan=2, sticky=tk.W)

    return frame

# Called by EDMC to populate preferences dialog
def plugin_prefs(parent: myNotebook.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    PADX = 10
    PADY = 10
    instructions = "Track missions and activity for or against a minor faction. The minor faction name below must EXACTLY match that in game, including capitalization and spacing."

    frame = myNotebook.Frame(parent)
    frame.columnconfigure(1, weight=1)
    tk.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    tk.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    tk.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    tk.Label(frame, text="Minor Faction").grid(row=3, column=0, padx=PADX, sticky=tk.W)
    tk.Entry(frame, text=this.minor_faction).grid(row=3, column=1, columnspan=7, padx=PADX, pady=PADY, sticky=tk.W)
    
    return frame

# Called by EDMC when a new entry is written to a journal file
def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: Dict[str, Any], state: Dict[str, Any]) -> None:
    # if entry["event"] in ["CarrierJumpRequest", "CarrierJumpCancelled"] and not is_beta:
    # this.status["text"] = "v%s - Ready" % this.version
    return None

# Copied from https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard/4203897#4203897
def copy_activity_to_clipboard() -> None:
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(this.activity)
    root.update()
    root.destroy()

def clear_activity() -> None:
    this.activity = "(No activity)"
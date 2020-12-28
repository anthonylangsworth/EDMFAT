import sys
import os
from typing import Optional, Tuple, Dict, Any, Union
import requests
import tkinter as tk
import myNotebook
from config import config, appname
import logging

this = sys.modules[__name__]
this.plugin_name:str = "Minor Faction Support"
this.minor_faction:tk.StringVar = tk.StringVar()
this.activity_summary:tk.StringVar = tk.StringVar()
this.activity

# Setup logging
logger = logging.getLogger(f'{appname}.{os.path.basename(os.path.dirname(__file__))}')

# Called by EDMC on startup
def plugin_start3(plugin_dir: str) -> str:
    this.minor_faction.set("EDA Kunti League")
    clear_activity_summary()
    return this.plugin_name

# Called by EDMC to show plug-in details on EDMC main window
def plugin_app(parent: tk.Frame) -> Union[tk.Widget, Tuple[tk.Widget, tk.Widget]]:
    frame:tk.Frame = tk.Frame(parent)
    frame.columnconfigure(1, weight=1)
    tk.Label(frame, textvariable=this.minor_faction, anchor=tk.W).grid(row=0, column=0)
    tk.Button(frame, text="Copy", command=copy_activity_to_clipboard).grid(row=0, column=1, sticky=tk.E)
    tk.Label(frame, textvariable=this.activity_summary, anchor=tk.W, justify=tk.LEFT, pady=10).grid(row=1, column=0, columnspan=2, sticky=tk.W)

    return frame

# Called by EDMC to populate preferences dialog
def plugin_prefs(parent: myNotebook.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    PADX:int = 10
    PADY:int = 10
    instructions:str = "Track missions and activity for or against a minor faction. The minor faction name below must EXACTLY match that in game, including capitalization and spacing (and is temporarily read-only)."

    frame = myNotebook.Frame(parent)
    frame.columnconfigure(1, weight=1)
    myNotebook.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    myNotebook.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    myNotebook.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    myNotebook.Label(frame, text="Minor Faction").grid(row=3, column=0, padx=PADX, sticky=tk.W)
    myNotebook.Entry(frame, textvariable=this.minor_faction, state=tk.DISABLED).grid(row=3, column=1, columnspan=7, padx=PADX, pady=PADY, sticky=tk.W)
    
    return frame

# Called by EDMC when a new entry is written to a journal file
def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: Dict[str, Any], state: Dict[str, Any]) -> None:
    # if entry["event"] in ["CarrierJumpRequest", "CarrierJumpCancelled"] and not is_beta:
    return None

# Copied from https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard/4203897#4203897
def copy_activity_to_clipboard() -> None:
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(this.activity_summary.string)
    root.update()
    root.destroy()

def clear_activity_summary() -> None:
    this.activity_summary.set("(No activity)")
    
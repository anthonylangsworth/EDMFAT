import sys
import os
from typing import Optional, Tuple, Dict, Any, Union
import tkinter as tk
import itertools
import myNotebook
from config import config, appname
import logging
import edmfs

this = sys.modules[__name__]
this.plugin_name = "Minor Faction Activity Tracker"
this.minor_faction = tk.StringVar()
this.activity_summary = tk.StringVar()
this.current_station = ""

CONFIG_MINOR_FACTION = "edmfat_minor_faction"

# Setup logging
logger = logging.getLogger(f'{appname}.{os.path.basename(os.path.dirname(__file__))}')

# Called by EDMC on startup
def plugin_start3(plugin_dir: str) -> str:
    saved_minor_faction = config.get(CONFIG_MINOR_FACTION)
    this.tracker = edmfs.Tracker(saved_minor_faction if saved_minor_faction else "EDA Kunti League")
    this.minor_faction.set(this.tracker.minor_faction)
    this.activity_summary.set("(No activity)")
    return this.plugin_name

# Called by EDMC to show plug-in details on EDMC main window
def plugin_app(parent: tk.Frame) -> Union[tk.Widget, Tuple[tk.Widget, tk.Widget]]:
    frame:tk.Frame = tk.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    tk.Label(frame, textvariable=this.minor_faction, anchor=tk.W).grid(row=0, column=0, columnspan=2)
    tk.Button(frame, text="Copy", command=copy_activity_to_clipboard).grid(row=1, column=0, sticky=tk.E, padx=10)
    tk.Button(frame, text="Copy + Reset", command=copy_activity_to_clipboard_and_reset).grid(row=1, column=1, sticky=tk.W, padx=10)
    tk.Label(frame, textvariable=this.activity_summary, anchor=tk.W, justify=tk.LEFT, pady=10).grid(row=2, column=0, columnspan=2, sticky=tk.W)

    return frame

# Called by EDMC to populate preferences dialog
def plugin_prefs(parent: myNotebook.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    PADX:int = 10
    PADY:int = 10
    instructions:str = "Track missions and activity for or against a minor faction. If the desired minor faction does not appear in the list, jump to a system where it is present and reopen this dialog."

    known_minor_factions = set(itertools.chain.from_iterable(star_system.minor_factions for star_system in this.tracker.galaxy_state.systems.values()))
    known_minor_factions.update([this.tracker.minor_faction])
    known_minor_factions = sorted(known_minor_factions)

    frame = myNotebook.Frame(parent)
    frame.columnconfigure(1, weight=1)
    myNotebook.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    myNotebook.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    myNotebook.Label(frame, text=instructions, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=1, column=0, columnspan=8, padx=PADX, sticky=tk.W)
    myNotebook.Label(frame, text="Minor Faction").grid(row=3, column=0, padx=PADX, sticky=tk.W)

    this.minor_faction_list = tk.Listbox(frame)
    this.minor_faction_list.config(height=10, width=50)
    this.minor_faction_list.grid(row=3, column=0, sticky=tk.W, padx=(PADX, 0), pady=PADY)
    this.minor_faction_list.insert(tk.END, *sorted(known_minor_factions))
    selected_index = known_minor_factions.index(this.minor_faction.get())
    this.minor_faction_list.selection_set(selected_index)
    this.minor_faction_list.see(selected_index)

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.config(command=this.minor_faction_list.yview)
    scrollbar.grid(row=3, column=1, sticky=tk.NS + tk.W, pady=PADY)

    this.minor_faction_list.config(yscrollcommand=scrollbar.set)
    
    return frame

def prefs_changed(cmdr: str, is_beta: bool) -> None:
    this.minor_faction.set(this.minor_faction_list.get(this.minor_faction_list.curselection()))
    this.tracker.minor_faction = this.minor_faction.get()
    config.set(CONFIG_MINOR_FACTION, this.minor_faction.get())

# Called by EDMC when a new entry is written to a journal file
def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: Dict[str, Any], state: Dict[str, Any]) -> Optional[str]:
    if not is_beta:
        if this.tracker.on_event(entry):
            this.activity_summary.set(this.tracker.activity)

# Copied from https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard/4203897#4203897
def copy_activity_to_clipboard() -> None:
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(this.tracker.activity)
    root.update()
    root.destroy()

def copy_activity_to_clipboard_and_reset() -> None:
    copy_activity_to_clipboard()
    this.tracker.clear_activity()

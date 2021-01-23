import sys
import os
from typing import Optional, List, Tuple, Dict, Any, Union
import logging

import tkinter as tk
import itertools
import myNotebook
from ttkHyperlinkLabel import HyperlinkLabel

from config import config, appname
import edmfs

this = sys.modules[__name__]
this.plugin_name = "Minor Faction Activity Tracker"
this.minor_factions = tk.StringVar()
this.activity_summary = tk.StringVar()
this.current_station = ""
this.version = (0,9,0)

CONFIG_MINOR_FACTION = "edmfat_minor_faction"
DEFAULT_MINOR_FACTIONS = {"EDA Kunti League"}
NO_ACTIVITY = "(No activity)"
NO_MINOR_FACTIONS = "(Select minor faction(s) in the Settings dialog)"

# Setup logging
logger = logging.getLogger(f'{appname}.{os.path.basename(os.path.dirname(__file__))}')

# Called by EDMC on startup
def plugin_start3(plugin_dir: str) -> str:
    this.tracker = edmfs.Tracker([], logger)
    saved_minor_factions = load_config()
    set_minor_factions(saved_minor_factions if saved_minor_factions != None else DEFAULT_MINOR_FACTIONS)
    clear_activity()
    return this.plugin_name

# Called by EDMC to show plug-in details on EDMC main window
def plugin_app(parent: tk.Frame) -> Union[tk.Widget, Tuple[tk.Widget, tk.Widget]]:
    frame:tk.Frame = tk.Frame(parent)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    tk.Label(frame, textvariable=this.minor_factions, wraplength=300, justify=tk.CENTER, anchor=tk.W).grid(row=0, column=0, columnspan=2)
    tk.Button(frame, text="Copy", command=copy_activity_to_clipboard).grid(row=1, column=0, sticky=tk.E, padx=10)
    tk.Button(frame, text="Copy + Reset", command=copy_activity_to_clipboard_and_reset).grid(row=1, column=1, sticky=tk.W, padx=10)
    tk.Label(frame, textvariable=this.activity_summary, anchor=tk.W, justify=tk.LEFT, pady=10).grid(row=2, column=0, columnspan=2, sticky=tk.W)

    return frame

# Called by EDMC to populate preferences dialog
def plugin_prefs(parent: myNotebook.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    PADX = 10
    PADY = 10
    INSTRUCTIONS = "Track missions and activity for or against minor faction(s). Multiple selection is allowed.\n\nIf the desired minor faction does not appear in the list, jump to a system where it is present and reopen this dialog."
    VERSION = f"Version: {'.'.join(map(str, this.version))}"
    URL = "https://github.com/anthonylangsworth/EDMFAT"

    # known_minor_factions = {"EDA Kunti League", "Kunti Dragons", "LTT 2337 Empire Party", "HR 1597 & Co", "The Fuel Rats Mischief", "The Scovereign Justice League", "Hutton Orbital Truckers", "The Dark Wheel", "Edge Fraternity", "Colonia Citizens Network", "Mobius Colonial Republic Navy", "Tenjin Pioneers Colonia", "Knights of Colonial Karma", "Ed's 38"}
    known_minor_factions = set(itertools.chain.from_iterable(star_system.minor_factions for star_system in this.tracker.galaxy_state.systems.values()))
    known_minor_factions.update(this.tracker.minor_factions)
    known_minor_factions = sorted(known_minor_factions)

    frame = myNotebook.Frame(parent)
    frame.columnconfigure(1, weight=1) # Required for listbox scrollbar

    HyperlinkLabel(
        frame, text=this.plugin_name, background=myNotebook.Label().cget("background"), url=URL, underline=True
    ).grid(row=0, padx=PADX, pady=PADY, sticky=tk.W)
    myNotebook.Label(frame, text=VERSION).grid(row=0, column=3, padx=PADX, sticky=tk.E)

    myNotebook.Label(frame, text=INSTRUCTIONS, wraplength=500, justify=tk.LEFT, anchor=tk.W).grid(row=2, column=0, columnspan=8, padx=PADX, sticky=tk.W)

    this.minor_faction_list = tk.Listbox(frame, selectmode="multiple")
    this.minor_faction_list.config(height=10, width=50)
    this.minor_faction_list.grid(row=5, column=0, sticky=tk.W, padx=(PADX, 0), pady=PADY)
    this.minor_faction_list.insert(tk.END, *sorted(known_minor_factions))

    first_minor_faction_visible = False
    for minor_faction in this.tracker.minor_factions:
        this.minor_faction_list.selection_set(known_minor_factions.index(minor_faction))
        if not first_minor_faction_visible:
            this.minor_faction_list.see(known_minor_factions.index(minor_faction))
            first_minor_faction_visible = True

    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    scrollbar.config(command=this.minor_faction_list.yview)
    scrollbar.grid(row=5, column=1, sticky=tk.NS + tk.W, pady=PADY)

    this.minor_faction_list.config(yscrollcommand=scrollbar.set)
    
    return frame

def prefs_changed(cmdr: str, is_beta: bool) -> None:
    minor_factions = [this.minor_faction_list.get(index) for index in this.minor_faction_list.curselection()]
    set_minor_factions(minor_factions)
    config.set(CONFIG_MINOR_FACTION, minor_factions)

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
    clear_activity()

def set_minor_factions(minor_factions: List[str]) -> None:
    if len(minor_factions) > 0:
        this.minor_factions.set(", ".join(minor_factions))
    else:
        this.minor_factions.set(NO_MINOR_FACTIONS)
    this.tracker.minor_factions = minor_factions

def clear_activity() -> None:
    this.activity_summary.set(NO_ACTIVITY)

def load_config() -> List[str]:
    # Settings at HKEY_CURRENT_USER\SOFTWARE\Marginal\EDMarketConnector\WinSparkle
    saved_minor_factions = config.get(CONFIG_MINOR_FACTION)
    logger.info(f"Loading saved minor factions: '{ saved_minor_factions }'")
    if isinstance(saved_minor_factions, List) and len(saved_minor_factions) == 1 and saved_minor_factions[0] == "":
        # Windows config saves list with a single empty string instead of an empty list when empty
        saved_minor_factions = {}
    elif isinstance(saved_minor_factions, str):
        if len(saved_minor_factions.strip()) > 0:
            saved_minor_factions = set([saved_minor_factions])
        else:
            saved_minor_factions = {}
    return saved_minor_factions

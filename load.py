import sys
import os
from typing import Optional, List, Tuple, Dict, Any, Union
import logging
import functools
import itertools

import tkinter as tk
import myNotebook
from ttkHyperlinkLabel import HyperlinkLabel
from config import config, appname

import edmfs

this = sys.modules[__name__]
this.plugin_name = "Minor Faction Activity Tracker"
this.minor_factions = tk.StringVar()
this.activity_summary = tk.StringVar()
this.current_station = ""
this.version = (0,11,0)

# Setup logging
logger = logging.getLogger(f'{appname}.{os.path.basename(os.path.dirname(__file__))}')

CONFIG_MINOR_FACTION = "edmfat_minor_faction"
DEFAULT_MINOR_FACTIONS = {"EDA Kunti League"}
NO_ACTIVITY = "(No activity)"
NO_MINOR_FACTIONS = "(Select minor faction(s) in the Settings dialog)"
SETTINGS_FILE = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "settings.json")
STAR_SYSTEM_RESOLVER_METHOD = functools.partial(edmfs.resolvers.resolve_star_system_via_edsm, logger)

# Called by EDMC on startup
def plugin_start3(plugin_dir: str) -> str:
    load_settings()
    update_activity()
    update_minor_factions()
    return this.plugin_name

# Called by EDMC to show plug-in details on EDMC main window
def plugin_app(parent: tk.Frame) -> Union[tk.Widget, Tuple[tk.Widget, tk.Widget]]:
    frame = tk.Frame(parent)
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
    INSTRUCTIONS = "Track missions and activity for or against minor faction(s). Click to select or deselect any minor faction (row). Multiple selection is allowed. If the desired minor faction does not appear in the list, jump to a system where the minor faction is present and reopen this dialog."
    VERSION = f"Version: {'.'.join(map(str, this.version))}"
    URL = "https://github.com/anthonylangsworth/EDMFAT"
    MISSION_WARNING = "This plug-in may not record some missions correctly due to Elite: Dangerous limitations."
    MISSIONS_CHALLENGES_URL = "https://github.com/anthonylangsworth/EDMFAT/blob/master/doc/missions.md"

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

    HyperlinkLabel(
        frame, text=MISSION_WARNING, background=myNotebook.Label().cget("background"), url=MISSIONS_CHALLENGES_URL, underline=True
    ).grid(row=7, column=0, columnspan=8, padx=PADX, pady=PADY, sticky=tk.W)
    
    return frame

# Called by EMDC when the user presses "OK" on the settings dialog
def prefs_changed(cmdr: str, is_beta: bool) -> None:
    this.tracker.minor_factions = [this.minor_faction_list.get(index) for index in this.minor_faction_list.curselection()]
    update_minor_factions()
    save_config()

# Called by EDMC when a new entry is written to a journal file
def journal_entry(cmdr: str, is_beta: bool, system: Optional[str], station: Optional[str], entry: Dict[str, Any], state: Dict[str, Any]) -> Optional[str]:
    if not is_beta:
        if this.tracker.on_event(entry):
            this.activity_summary.set(this.tracker.activity)
            save_config()

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
    save_config()
    update_activity()

def update_activity() -> None:
    if len(this.tracker.activity) > 0:
        this.activity_summary.set(this.tracker.activity)
    else:
        this.activity_summary.set(NO_ACTIVITY)

def update_minor_factions() -> None:
    if len(this.tracker.minor_factions) > 0:
        this.minor_factions.set(", ".join(this.tracker.minor_factions))
    else:
        this.minor_factions.set(NO_MINOR_FACTIONS)

def load_settings_from_file() -> edmfs.Tracker:
    tracker = None
    try:
        with open(SETTINGS_FILE, "r") as settings_file:
            tracker = edmfs.TrackerFileRepository().deserialize(settings_file.read(), logger, STAR_SYSTEM_RESOLVER_METHOD)
        logger.info(f"Loaded settings from \"{SETTINGS_FILE}\"")
    except FileNotFoundError:
        logger.info(f"Setings file \"{SETTINGS_FILE}\" not found. This is expected on the first run.")
        pass
    except:
        logger.exception(f"Error loading settings from \"{SETTINGS_FILE}\"")
    return tracker

def load_settings_from_config() -> edmfs.Tracker:
    saved_minor_factions = config.get(CONFIG_MINOR_FACTION)
    if isinstance(saved_minor_factions, List) and len(saved_minor_factions) == 1 and saved_minor_factions[0] == "":
        # Windows config saves list with a single empty string instead of an empty list when empty
        saved_minor_factions = {}
    elif isinstance(saved_minor_factions, str):
        if len(saved_minor_factions.strip()) > 0:
            saved_minor_factions = set([saved_minor_factions])
        else:
            saved_minor_factions = {}
    elif saved_minor_factions == None:
        saved_minor_factions = DEFAULT_MINOR_FACTIONS
        logger.info(f"Defaulting to minor faction(s): { ','.join(saved_minor_factions) }")
    return edmfs.Tracker(saved_minor_factions, logger, STAR_SYSTEM_RESOLVER_METHOD)

def load_settings() -> List[str]:
    this.tracker = load_settings_from_file()
    if not this.tracker:
        this.tracker = load_settings_from_config()

def save_config() -> None:
    with open(SETTINGS_FILE, mode="w") as settings_file:
        settings_file.write(edmfs.TrackerFileRepository().serialize(this.tracker))
    config.delete(CONFIG_MINOR_FACTION)
    logger.info(f"Settings saved to \"{SETTINGS_FILE}\"")


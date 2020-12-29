from edmfs.tracker import Tracker

def test_plugin_start3():
    tracker:Tracker = Tracker("a")
    assert(tracker.minor_faction == "a")
    
import edmfs.tracker

def test_plugin_start3():
    tracker = edmfs.tracker.Tracker("a")
    assert(tracker.name == "a")
    
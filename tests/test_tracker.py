from edmfs.tracker import Tracker

def test_plugin_start3():
    mfam = Tracker("a")
    assert(mfam.a == "a")
    
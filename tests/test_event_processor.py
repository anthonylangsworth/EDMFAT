import pytest

from edmfs.event_processor import LocationEventProcessor, RedeemVoucherEventProcessor

def test_location_event_processor_init():
    location_event_procesor:LocationEventProcessor = LocationEventProcessor()
    assert(location_event_procesor.eventName == "Location")

def test_redeem_voucher_event_processor():
    redeem_voucher_event_procesor:RedeemVoucherEventProcessor = RedeemVoucherEventProcessor()
    assert(redeem_voucher_event_procesor.eventName == "RedeemVoucher")

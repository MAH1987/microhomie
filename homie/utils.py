from mqtt_as import LINUX

if LINUX is False:
    from network import WLAN, AP_IF
    from machine import unique_id
    from ubinascii import hexlify


def disable_ap():
    """Disables any Accesspoint"""
    wlan = WLAN(AP_IF)
    wlan.active(False)
    print("NETWORK: Access Point disabled.")


def get_unique_id():
    if LINUX is False:
        return hexlify(unique_id())
    else:
        raise NotImplementedError(
            "Linux doesn't have a unique id. Provide the DEVICE_ID option in your settings.py."
        )


def get_local_ip():
    try:
        return bytes(WLAN(0).ifconfig()[0], "utf-8")
    except NameError:
        return b"127.0.0.1"


def get_local_mac():
    try:
        return hexlify(WLAN(0).config("mac"), ":")
    except NameError:
        return b"00:00:00:00:00:00"

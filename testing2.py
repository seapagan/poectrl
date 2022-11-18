"""Test the PoECtrl library."""
from poectrl import PoECtrl

PROFILES = {
    "devices": {
        "192.168.0.187": {"user": "ubnt", "password": "ubnt"},
        "192.168.0.190": {"user": "ubnt", "password": "ubnt"},
    },
    "profiles": {
        "camera_on": {
            "192.168.0.187": {4: 24, 5: 24, 8: 48},
            "192.168.0.190": {5: 24, 6: 24, 7: 48},
        },
        "camera_off": {
            "192.168.0.187": {4: 0, 5: 0, 8: 0},
            "192.168.0.190": {5: 0, 6: 0, 7: 0},
        },
    },
}


def activate_profile(profile: str):
    """Activate the specified profile."""
    if profile not in list(PROFILES["profiles"]):
        print(f"The profile '{profile}' does not exist, aborting!")
    else:
        this_profile = dict(PROFILES["profiles"][profile])
        for device in this_profile:
            try:
                auth = PROFILES["devices"][device]
                poe = PoECtrl(device, auth["user"], auth["password"])
                poe.process_device(this_profile[device])
            except KeyError as err:
                print(f" -> Device {err} has not been defined, skipping.")


activate_profile("camera_off")

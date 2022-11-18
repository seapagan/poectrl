"""Test the PoECtrl library."""
from poectrl import PoECtrl
from poectrl.errors import (
    BadAuthenticationError,
    CannotConnectError,
    CannotReadSettingsError,
    CannotWriteSettingsError,
)

PROFILES = {
    "devices": {
        "192.168.0.187": {"user": "ubnt", "password": "ubnt"},
        "192.168.0.190": {"user": "ubnt", "password": "ubnt2"},
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
        print(f"The profile '{profile}' does not exist!")
    else:
        this_profile = dict(PROFILES["profiles"][profile])
        for device in this_profile:
            try:
                auth = PROFILES["devices"][device]
                poe = PoECtrl(device, auth["user"], auth["password"])
                try:
                    poe.process_device(this_profile[device])
                except BadAuthenticationError:
                    print(" -> Cannot connect to this device [Bad user/pass].")
                except CannotConnectError:
                    print(" -> Cannot physically connect to this device.")
                except (CannotReadSettingsError, CannotWriteSettingsError):
                    print(
                        " -> Failure to Read or Write the Settings for device"
                        f"{device}"
                    )
            except KeyError as e:
                print(f" -> Device {e} has not been defined, skipping.")


activate_profile("camera_off")

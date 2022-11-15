# import json
# from json.decoder import JSONDecodeError

from paramiko.ssh_exception import (
    AuthenticationException,
    NoValidConnectionsError,
)

from sshwrapper import Wrapper as SSH

PROFILES = {
    "profiles": {
        "camera_on": {
            "192.168.0.187": {4: 24, 5: 24, 8: 24},
        },
        "camera_off": {
            "192.168.0.187": {4: 0, 5: 0, 8: 0},
        },
    },
}


def process_device(ip: str, port_config: dict):
    """Set the ports for a specific device."""
    print(f"Conncting to {ip}:")
    connection = SSH(ip, "ubnt", "ubnt", 22)
    try:
        connection.connect()
        for port in port_config:
            print(f"  Setting port {port} to {port_config[port]}")
            version, stderr = connection.run(f"poe {port} {port_config[port]}")
    except NoValidConnectionsError:
        print("Cannot connect to this device!")
        quit(1)  # error code 1 "Cant Connect"
    except AuthenticationException:
        print("Wrong User/Password!")
        quit(2)  # Error code 2 "Wrong user/pass"
    finally:
        connection.close()


def activate_profile(profile: str):
    """Activate the specified profile."""
    if profile not in list(PROFILES["profiles"]):
        print(f"The profile '{profile}' does not exist!")
    else:
        this_profile = dict(PROFILES["profiles"][profile])
        for device in this_profile:
            process_device(device, this_profile[device])


activate_profile("camera_off")


# version, stderr = connection.run("cat /etc/version")
# config, stderr = connection.run("cat /tmp/system.cfg")
# if stderr:
#     print("Error getting configuration data, cannot continue.")
#     quit(3)  # Error code 3 "Can't read config"

# try:
#     raw_status, stderr = connection.run("mca-status")

#     status = json.loads(raw_status)["status"]

#     host = status["host"]
#     ports: dict = status["ports"]
# except JSONDecodeError:
#     print("Error decoding status, cannot continue.")
#     quit(4)  # Error code 4 "Can't decode status"

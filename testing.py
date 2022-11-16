from paramiko.ssh_exception import (
    AuthenticationException,
    NoValidConnectionsError,
)

from sshwrapper import Wrapper as SSH

# from json.decoder import JSONDecodeError


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


def get_system_file(connection: SSH) -> str:
    """Return the 'tmp/system.cfg' as an str."""
    system, stderr = connection.run("cat /tmp/system.cfg")
    if stderr:
        print("Error getting configuration data, cannot continue.")
        quit(3)  # Error code 3 "Can't read config"
    return system


def put_system_file(connection: SSH, new_system):
    """write the provided system file back to the device."""
    system, stderr = connection.run(f"echo '{new_system}' > /tmp/system.cfg")
    if stderr:
        print("Error writing updated configuration data, cannot continue.")
        print(stderr)
        quit(4)  # Error code 4 "Can't write config"


def process_system_cfg(system_cfg: str, port_config: dict):
    """Update the PoE status in the system_cfg."""
    prefix = "switch.port."

    main_body = []
    port_data = []
    for line in system_cfg.splitlines():
        if prefix in line:
            port_data.append(line)
        else:
            main_body.append(line)

    # remove the common prefix to clean up next code
    prefix_removed = [x[len(prefix) :] for x in port_data]

    # convert to a dict for better editing
    system_dict = {}
    for entry in prefix_removed:
        port_number, data = entry.split(".", 1)
        key, value = data.split("=")
        if port_number in system_dict:
            system_dict[port_number].update({key: value})
        else:
            system_dict[port_number] = {key: value}

    # update the PoE entries
    for port in port_config:
        system_dict[str(port)]["poe"] = port_config[port]  # type: ignore

    # convert back to list of strings
    system_string_list = []
    for port, values in system_dict.items():
        for value in values.items():
            key, value = value
            entry = f"switch.port.{port}.{key}={value}"
            system_string_list.append(entry)

    new_system_cfg = "\n".join(sorted(main_body + system_string_list))

    return new_system_cfg


def process_device(ip: str, port_config: dict):
    """Set the ports for a specific device."""
    print(f"Conncting to {ip}:")
    connection = SSH(ip, "ubnt", "ubnt", 22)
    try:
        connection.connect()

        for port in port_config:
            print(f"  Setting port {port} to {port_config[port]}")
            _, stderr = connection.run(f"poe {port} {port_config[port]}")

        system_cfg = get_system_file(connection)
        new_cfg = process_system_cfg(system_cfg, port_config)
        put_system_file(connection, new_cfg)
        _, stderr = connection.run("save")
        if stderr:
            print(f"Error Saving - {stderr}")
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


activate_profile("camera_on")


# version, stderr = connection.run("cat /etc/version")


# try:
#     raw_status, stderr = connection.run("mca-status")

#     status = json.loads(raw_status)["status"]

#     host = status["host"]
#     ports: dict = status["ports"]
# except JSONDecodeError:
#     print("Error decoding status, cannot continue.")
#     quit(4)  # Error code 4 "Can't decode status"

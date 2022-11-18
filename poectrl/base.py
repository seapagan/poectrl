"""PoECtrl - a class to control PoE voltage on Ubiquiti Switches.

This has currently only been tested on the TS-8-PRO Toughswitch routers,
though others will be added soon.

IMPORTANT: This library DOES NOT(and CAN NOT) ensure that any device attached to
a port is compatible with the voltage selected. BE VERY CAREFUL that you choose
the correct voltage for your devices or you can DAMAGE THEM. No responsibility
is taken for equipment damaged using this library.

©Grant Ramsay, 2022.

Licensed under MIT (https://opensource.org/licenses/MIT)
"""
from paramiko.ssh_exception import (
    AuthenticationException,
    NoValidConnectionsError,
)

from poectrl.sshwrapper import Wrapper as SSH  # noqa N814

from .errors import (
    BadAuthenticationError,
    CannotConnectError,
    CannotReadSettingsError,
    CannotWriteSettingsError,
)


class PoECtrl:
    """Class to control PoE on Ubiquiti Routers."""

    def __init__(self, ip: str, username: str, password: str, port: int):
        """Initialize the class."""
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

        self.connection = SSH(self.ip, self.username, self.password, self.port)

    def connect(self):
        """Open the SSH connection, or fail if errors."""
        try:
            self.connection.connect()
        except NoValidConnectionsError:
            raise CannotConnectError
        except AuthenticationException:
            raise BadAuthenticationError

    def close(self):
        """Close the SSH connection."""
        self.connection.close()

    def get_system_cfg(self) -> str:
        """Return the 'tmp/system.cfg' as a str.

        Raise CannotReadSettingsError if this fails.
        """
        system, stderr = self.connection.run("cat /tmp/system.cfg")
        if stderr:
            raise CannotReadSettingsError
        return system

    def put_system_file(self, new_system):
        """Write the provided system file back to the device.

        Raise CannotWriteSettingsError if this fails.
        """
        system, stderr = self.connection.run(
            f"echo '{new_system}' > /tmp/system.cfg"
        )
        if stderr:
            raise CannotWriteSettingsError

    def update_system_cfg(self, system_cfg: str, port_config: dict):
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

    def process_device(self, port_config: dict):
        """Set the ports for a specific device."""
        print(f"Conncting to {self.ip}:")

        try:
            self.connect()
            for port in port_config:
                print(f"  Setting port {port} to {port_config[port]}")
                _, stderr = self.connection.run(
                    f"poe {port} {port_config[port]}"
                )

            system_cfg = self.get_system_cfg()
            new_cfg = self.update_system_cfg(system_cfg, port_config)
            self.put_system_file(new_cfg)
            self.connection.run("cfgmtd -w -p /etc/")
        finally:
            self.close()

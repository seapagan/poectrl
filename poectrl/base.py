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
from rich import print

from .errors import (
    BadAuthenticationError,
    CannotConnectError,
    CannotReadSettingsError,
    CannotWriteSettingsError,
)
from .sshwrapper import Wrapper as SSH  # noqa N814


class PoECtrl:
    """Class to control PoE on Ubiquiti Routers."""

    def __init__(
        self, name: str, ip: str, username: str, password: str, port: int = 22
    ):
        """Initialize the class."""
        self.name = name
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

        self.connection = SSH(self.ip, self.username, self.password, self.port)
        self.system_cfg = ""

        self.port_prefix = "switch.port."

    def connect(self):
        """Open the SSH connection, or raise relavant Error.

        At this time we also get the settings into an instance variable.
        """
        try:
            self.connection.connect()
            self.system_cfg = self.read_system_cfg()
        except NoValidConnectionsError:
            raise CannotConnectError
        except AuthenticationException:
            raise BadAuthenticationError

    def close(self):
        """Close the SSH connection."""
        self.connection.close()

    def read_system_cfg(self) -> str:
        """Return the 'tmp/system.cfg' as a str.

        Raise CannotReadSettingsError if this fails.
        """
        system, stderr = self.connection.run("cat /tmp/system.cfg")
        if stderr:
            raise CannotReadSettingsError
        return system

    def write_system_cfg(self, new_system):
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
        main_body = []
        port_data = []
        for line in system_cfg.splitlines():
            if self.port_prefix in line:
                port_data.append(line)
            else:
                main_body.append(line)

        # update the PoE entries in settings. This allows the GUI to update, and
        # the settings to persist over a reboot (after running save!)
        system_dict = self.settings_list_to_dict(port_data)
        for port in port_config:
            system_dict[str(port)]["poe"] = port_config[port]  # type: ignore
        system_string_list = self.dict_to_settings_list(system_dict)
        new_system_cfg = "\n".join(sorted(main_body + system_string_list))

        return new_system_cfg

    def dict_to_settings_list(self, system_dict: dict) -> list:
        """Convert the settings dict into a list of strings."""
        system_string_list = []
        for port, values in system_dict.items():
            for value in values.items():
                key, value = value
                entry = f"switch.port.{port}.{key}={value}"
                system_string_list.append(entry)
        return system_string_list

    def settings_list_to_dict(self, settings_list: list) -> dict:
        """Convert list of settings to a dictionary."""
        settings_list = [x[len(self.port_prefix) :] for x in settings_list]

        system_dict = {}
        for entry in settings_list:
            port_number, data = entry.split(".", 1)
            key, value = data.split("=")
            if port_number in system_dict:
                system_dict[port_number].update({key: value})
            else:
                system_dict[port_number] = {key: value}
        return system_dict

    def process_device(self, port_config: dict):
        """Set the ports for a specific device."""
        print(f"Conncting to {self.name} ({self.ip}):")

        try:
            self.connect()
            for port in port_config:
                print(f"  Setting port {port} to {port_config[port]}V")
                _, stderr = self.connection.run(
                    f"poe {port} {port_config[port]}"
                )

            new_cfg = self.update_system_cfg(self.system_cfg, port_config)
            self.write_system_cfg(new_cfg)

            # save the new settings on the device. The command below is what is
            # actually run when using the alias 'save' from the device command
            # line.
            self.connection.run("cfgmtd -w -p /etc/")
        except BadAuthenticationError:
            print("[red]-> Cannot connect to this device [Bad user/pass].")
        except CannotConnectError:
            print("[red]-> Cannot physically connect to this device.")
        except (CannotReadSettingsError, CannotWriteSettingsError):
            print(
                "[red]-> Failure to Read or Write the Settings for device"
                f" {self.ip}"
            )
        finally:
            self.close()

"""Custom class to encapsulate SSH access to devices."""
from typing import Tuple

import paramiko


class Wrapper:
    """SSH Wrapper Class.

    Wraps an SSH connection, with methods to run remote commands, returning the
    results or errors.
    """

    def __init__(self, host: str, username: str, password: str, port: int):
        """Initialize the Class."""
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.client = paramiko.SSHClient()

        # setup logging
        # paramiko.util.log_to_file("paramiko.log")

    def connect(self):
        """Connect to a remote host via SSH.

        This just opens the connection or raises an exception. The connection
        should be closed by calling the close() method once the required
        commands have been run
        """
        # ignore missing keys with no warning
        self.client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        # open a connection to the specified host
        self.client.connect(
            self.host,
            self.port,
            self.username,
            self.password,
            look_for_keys=False,
            allow_agent=False,
            timeout=10,
            banner_timeout=10,
            auth_timeout=10,
        )

    def close(self):
        """Close the SSH connection to this host."""
        self.client.close()

    def run(self, cmd_str) -> Tuple[str, str]:
        """Run a command on this host over the existing SSH connection.

        Args:
            cmd_str (string): [Command to run]

        Returns:
            output [string]: The output from the command
            stderr [string]: Any errors from the remote stderr
        """
        _, stdout, stderr = self.client.exec_command(cmd_str, timeout=10)

        # convert the streams we want into strings.
        err = stderr.read().decode("utf8").strip("\n")
        out = stdout.read().decode("utf8").strip("\n")
        # return the stdout and stderr as a tuple
        return out, err

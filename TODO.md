# TODO

- replace current method of getting the config file with Paramiko's SFTP
  functionality.
- passwords should not be stored in plain text, though this may be the cleanest
  way. `poectrl.json` is not stored in the Git repo anyway. Find a better
  way to do this.
- add a command and endpoint to list all defined devices (without
  login/passwords!).
- improve the API 'show' response data, instead of simply returning a dict.
- show correct response schema for the API 'show' route with example response
  data.

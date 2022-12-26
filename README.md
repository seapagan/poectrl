# Control PoE status on a Ubiquiti TS-8-Pro Switch <!-- omit in toc -->

[![PyPI version](https://badge.fury.io/py/poectrl.svg)](https://badge.fury.io/py/poectrl)

**Development work** for a system to remotely and automatically control the PoE
status of individual ports on multiple Ubiquiti TS-8-Pro Switch, using
predefined profiles.

This has currently only been tested on the TS-8-PRO ToughSwitch routers,
though others will be added soon.

**IMPORTANT: This library DOES NOT (and CAN NOT) ensure that any device attached
to a port is compatible with the voltage selected. BE VERY CAREFUL that you
choose the correct voltage for your devices or you can DAMAGE THEM. No
responsibility is taken for equipment damaged using this library.**

- [Status](#status)
- [Use Cases](#use-cases)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [As a command-line program](#as-a-command-line-program)
  - [As an API](#as-an-api)
    - [API Routes](#api-routes)
- [Development Plans](#development-plans)
- [Contributing](#contributing)

## Status

This project is in no way ready to be used, and documentation is non-existent.
See the Development Plans below. Until I have a stable useful interface, check
the source code if you are interested 😃

## Use Cases

- Control a set of PoE-powered IP cameras, switches and access points to allow
disabling when not needed or quick enabling if required.

## Installation

The latest version is uploaded to [pypi.org](https://pypi.org) so you can
install this the same as any other package:

```console
pip install poectrl
```

## Configuration

**IMPORTANT : The configuration layout has CHANGED from version 1.2.0. If you
are using config files from previous versions you will need to update the
"devices" section to fit the below schema and change the profile to point to the
name instead of IP address.**

The program is configured using a `poectrl.json` file either in the current
working directory (first priority) or the user's home directory. This is a
simple file that describes all devices and profiles. There is an example in
[poectrl-example.json](poectrl-example.json) :

```json
{
  "devices": {
    "switch_1": {"ip": "192.168.0.187", "user": "ubnt", "password": "ubnt"},
    "switch_2": {"ip": "192.168.0.190", "user": "ubnt", "password": "ubnt"}
  },
  "profiles": {
    "cctv_on": {
      "switch_1": {"4": 24, "5": 24, "8": 48},
      "switch_2": {"5": 24, "6": 24, "7": 48}
    },
    "cctv_off": {
      "switch_1": {"4": 0, "5": 0, "8": 0},
      "switch_2": {"5": 0, "6": 0, "7": 0}
    }
  }
}

```

## Usage

### As a command-line program

Apply a predefined profile, setting the PoE port voltages.

```console
$ poectrl apply cctv_off
Using configuration from /home/seapagan/data/work/own/poectrl/poectrl.json
Conncting to switch_1 (192.168.0.187):
  Setting port 4 to 0V
  Setting port 5 to 0V
  Setting port 8 to 0V
Conncting to switch_2 (192.168.0.190):
  Setting port 5 to 0V
  Setting port 6 to 0V
  Setting port 7 to 0V

```

List all defined profiles:

```console
$ poectrl list
Using configuration from /home/seapagan/data/work/own/ts-8-pro-control/poectrl.json

Valid profiles are :
 - cctv_on
 - cctv_off
```

Show settings for a profile :

```console
$ poectrl show cctv_off
Using configuration from /home/seapagan/data/work/own/ts-8-pro-control/poectrl.json
{
    "switch_1": {
        "4": 0,
        "5": 0,
        "8": 0
    },
    "switch_2": {
        "5": 0,
        "6": 0,
        "7": 0
    }
}
```

### As an API

It is also possible to run this locally as an API, which can then allow easier
control using a web browser.

**Important**: This is only designed for local network use, not over the
internet since there is NO access control set up. If you open this to the
internet then ANYONE can control your PoE!

```console
$ poectrl serve
INFO:     Started server process [49922]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

There are a couple of command-line switches you can use :

`---refresh` - This is useful if you are modifiying or troubleshooting the code,
the API will reload after each source code change.

`--port <int>` - Change the port that the API listens on (default is 8000)

After this, you can access the API on `http://localhost:8000`. Swagger docs are
available at `http://localhost:8000/docs`

#### API Routes

There are currently 3 routes which correspond to the same command in the CLI.

`/list/` - Lists all the defined profiles\
`/show/{profile_name}` - Shows details for the specific profile\
`/apply/{profile_name}` - Apply the specific profile

## Development Plans

Current proposed project plan.

- [x] Write proof-of-concept code to control ports.
- [x] Refactor and tidy the above code into a Library Class.
- [x] Create a basic CLI using this Library
- [x] Continue the CLI to use a config file, show current values, list profiles
  etc.
- [x] Publish on PyPi as a standalone package.
- [x] Wrap this into an API (using FastAPI) for local use only.
- [ ] Create a Web App to interface with the above API.

## Contributing

At this time, the project is barely in it's planning stage but I do have a firm
idea where it's going and how to structure it. As such, other contributions are
not looked for at this time. Hopefully, within a few days this project will be
at a much more advanced stage and that will change 😃.

# Control PoE status on a Ubiquiti TS-8-Pro Switch <!-- omit in toc -->

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
- [Configuration](#configuration)
- [Usage](#usage)
- [Development Plans](#development-plans)
- [Contributing](#contributing)

## Status

This project is in no way ready to be used, and documentation is non-existent.
See the Development Plans below. Until I have a stable useful interface, check
the source code if you are interested 😃

## Use Cases

- Control a set of PoE-powered IP cameras, switches and access points to allow
disabling when not needed or quick enabling if required.

## Configuration

The program is configured using a `poectrl.json` file either in the current
working directory (first priority) or the user's home directory. This is a
simple file that describes all devices and profiles. There is an example in
[poectrl-example.json](poectrl-example.json) :

```json
{
  "devices": {
    "192.168.0.187": {"user": "ubnt", "password": "ubnt"},
    "192.168.0.190": {"user": "ubnt", "password": "ubnt"}
  },
  "profiles": {
    "cctv_on": {
      "192.168.0.187": {"4": 24,"5": 24,"8": 48},
      "192.168.0.190": {"5": 24,"6": 24,"7": 48}
    },
    "cctv_off": {
      "192.168.0.187": {"4": 0,"5": 0,"8": 0},
      "192.168.0.190": {"5": 0,"6": 0,"7": 0}
    }
  }
}
```

## Usage

Apply a predefined profile, setting the PoE port voltages.

```console
$ ./poectrl apply cctv_off
Using configuration from /home/seapagan/data/work/own/ts-8-pro-control/poectrl.json
Conncting to 192.168.0.187:
  Setting port 4 to 0V
  Setting port 5 to 0V
  Setting port 8 to 0V
Conncting to 192.168.0.190:
  Setting port 5 to 0V
  Setting port 6 to 0V
  Setting port 7 to 0V
```

List all defined profiles:

```console
$ ./poectrl list
Using configuration from /home/seapagan/data/work/own/ts-8-pro-control/poectrl.json

Valid profiles are :
 - cctv_on
 - cctv_off
```

Show settings for a profile :

```console
$ ./poectrl show cctv_off
Using configuration from /home/seapagan/data/work/own/ts-8-pro-control/poectrl.json
{
    "192.168.0.187": {
        "4": 0,
        "5": 0,
        "8": 0
    },
    "192.168.0.190": {
        "5": 0,
        "6": 0,
        "7": 0
    }
}

```

## Development Plans

Current proposed project plan.

- [x] Write proof-of-concept code to control ports.
- [x] Refactor and tidy the above code into a Library Class.
- [x] Create a basic CLI using this Library
- [x] Continue the CLI to use a config file, show current values, list profiles
  etc.
- [x] Publish on PyPi as a standalone package.
- [ ] Develop this into a full API (using FastAPI).
- [ ] Modify the command line app to interface with the above API.
- [ ] Create a Web App to interface with the above API.

## Contributing

At this time, the project is barely in it's planning stage but I do have a firm
idea where it's going and how to structure it. As such, other contributions are
not looked for at this time. Hopefully, within a few days this project will be
at a much more advanced stage and that will change 😃.

# Control PoE status on a Ubiquiti TS-8-Pro Switch

**Development work** for a system to remotely and automatically control the PoE
status of individual ports on multiple Ubiquiti TS-8-Pro Switch, using
predefined profiles.

This has currently only been tested on the TS-8-PRO Toughswitch routers,
though others will be added soon.

**IMPORTANT: This library DOES NOT(and CAN NOT) ensure that any device attached
to a port is compatible with the voltage selected. BE VERY CAREFUL that you
choose the correct voltage for your devices or you can DAMAGE THEM. No
responsibility is taken for equipment damaged using this library.**

## Status

This project is in no way ready to be used, and documentation is non-existent.
See the Development Plans below. Until I have a stable useful interface, check
the source code if you are interested 😃
Profiles are (currently) hard-coded in, and only of use to myself.

## Use Cases

- Control a set of PoE-powered IP cameras, switches and access points to allow
disabling when not needed or quick enabling if required.

## Development Plans

Current proposed project plan.

- [X] Write proof-of-concept code to control ports.
- [X] Refactor and tidy the above code into a Library Class.
- [X] Create a basic CLI using this Library
- [ ] Continue the CLI to use a config config file, show current values, list
  profiles etc.
- [ ] Possibly publish the standalone version above on PyPi.
- [ ] Develop this into a full API (using FastAPI).
- [ ] Modify the command line app to interface with the above API.
- [ ] Create a Web App to interface with the above API.

## Contributing

At this time, the project is barely in it's planning stage but I do have a firm
idea where it's going and how to structure it. As such, other contributions are
not looked for at this time. Hopefully, within a few days this project will be
at a much more advanced stage and that will change 😃.

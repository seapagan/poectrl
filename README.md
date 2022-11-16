# Control PoE status on a Ubiquiti TS-8-Pro Switch

**Development work** for a system to remotely and automatically control the PoE
status of individual ports on a Ubiquiti TS-8-Pro Switch, using predefined
profiles.

## Use Cases

- Control a set of IP cameras, switches and access points to enable disabling
when not needed or quick enabling if required.

## Development Plans

Current proposed project plan.

- [x] Write proof-of-concept code to control ports.
- [ ] Refactor and tidy the above code into a Library Class.
- [ ] Create a CLI app to apply profiles from config file, show current values,
  list profiles etc.
- [ ] Develop this into a full API (using FastAPI).
- [ ] Modify the command line app to interface with the above API.
- [ ] Create a Web App to interface with the above API.

## Contributing

At this time, the project is barely in it's planning stage but I do have a firm
idea where it's going and how to structure it. As such, other contributions are
not looked for at this time. Hopefully, within a few days this project will be
in a much more advance stage and that will change 😃.

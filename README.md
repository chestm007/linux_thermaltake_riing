# Linux driver and daemon for Thermaltake Riing

## Compatibility
currently supported devices are (as they show up in thermaltakes TTRGBPLUS software:
    Riing Plus
    Flow Riing RGB
If your's isnt listed, please create an issue!

## Installation

### Pypi
The setup file will create the systemd user unit, and udev rule
`sudo pip install linux-thermaltake-rgb`

then add your user to the `plugdev` group - `sudo usermod -a -G plugdev <user>`

then reconnect your device. (you may need to log out and back in so your
user is recognised as being in the `plugdev` group

## Configuration
default configuration is in `/etc/linux_thermaltake_rgb/config.yml`
edit and configure suitably.

example config:

```
# specify <port_number>:<device_type>
# port number, referring to the usb hub controller your fans connect too.
devices:
  1: Riing Plus
  2: Riing Plus
  3: Riing Plus
  4: Riing Plus
  5: Floe Riing RGB

# these are passed directly into the fan controller factory method in daemon.fan_manager
fan_controller:
  type: temp_target
  target: 20
  sensor_name: k10temp
  multiplier: 5

# alternatively, you can set a permanent speed
# fan_controller:
#   type: locked_speed
#   speed: 80

lighting_controller:
  type: static
  r: 50
  g: 0
  b: 0
```
# Linux driver and daemon for Thermaltake Riing

## Compatibility
currently supported devices are (as they show up in thermaltakes TTRGBPLUS software:
    Riing Plus
    Flow Riing RGB
If your's isnt listed, please create an issue!

## Installation
current installation is cloning the directory and pip installing that way.
 - in the very near future this will be uploaded to pypi

In order for the dbus daemon to function properly, you will need to setup udev rule to
allow your user to claim the usb device without being root. this is most easily done via
a udev rule:

```
# this is specific to the usb controller I have - your mileage may vary.
# /etc/udev/rules.d/90linux-thermaltake-rgb.rules
ACTION=="add", SUBSYSTEMS=="usb", ATTRS{idVendor}=="264a", ATTRS{idProduct}=="1fa5", MODE="660", GROUP="plugdev"
```

then add your user to the `plugdev` group - `sudo usermod -a -G plugdev <user>`

then reconnect your device and you should be able to claim it without using sudo.

## Configuration
create `/etc/linux_thermaltake_rgb/config.yaml` and configure suitably.

example config:

```
# specify <port_number>:<device_type>
devices:
  1: Riing Plus
  2: Riing Plus
  3: Riing Plus
  4: Riing Plus
  5: Floe Riing RGB

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
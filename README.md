# Linux driver and daemon for Thermaltake Riing


## Compatibility
Python3 only.

Currently supported devices are (as they show up in thermaltakes TTRGBPLUS software:  
- Flow Riing RGB  
- Lumi Plus LED Strip  
- Pacific PR22-D5 Plus  
- Pacific Rad Plus LED Panel  
- Pacific V-GTX 1080Ti Plus GPU Waterblock  
- Pacific W4 Plus CPU Waterblock  
- Riing Plus  

If your's isn't listed, please create an issue and I'll implement it ASAP!!  


## Installation

### Pypi

`sudo pip3 install linux_thermaltake_rgb`  
The setup file will create the systemd unit
in `/usr/share/linux_thermaltake_rgb`  
you will need to copy these to the appropriate locations:

```bash
sudo cp /usr/share/linux_thermaltake_rgb/linux-thermaltake-rgb.service /usr/lib/systemd/system/

# and if this is a fresh install copy the default config file:
sudo mkdir /etc/linux_thermaltake_rgb/
sudo cp /usr/share/linux_thermaltake_rgb/config.yml /etc/linux_thermaltake_rgb/
```

### Arch linux

available in the aur as `linux-thermaltake-rgb`

### Starting and Enabling the Daemon

start and enable the systemd service  
`systemctl enable --now linux-thermaltake-rgb.service`  


## Configuration
the configuration file is expected to be in: `/etc/linux_thermaltake_rgb/config.yml`  
edit and configure suitably.  

example config is in `linux_thermaltake_rgb/assets/config.yml`  

### Controller Types
- g3
- riingtrio

### Devices

- Fans
  - Riing Plus
  
- Lights
  - Pacific PR22-D5 Plus
  - Pacific W4 Plus CPU Waterblock
  - Pacific V-GTX 1080Ti Plus GPU Waterblock
  - Pacific Rad Plus LED Panel
  - Lumi Plus LED Strip
  
- Pumps
  - Floe Riing RGB

### Fan Manager Settings

- temp_target
  increases/decreases fan speed in direct response to the difference of actual
  temperature to target temperature multiplied by the specified multiplier
  with an extemely simple - read, dumb - smoothing function
  - settings:
    - sensor_name [name of the sensor to get temperature reading from(names can be found by running `sensors` in a terminal)]
    - target [target temperature]
    - multiplier
    
- locked_speed
  sets the fan speeds to a static speed, regardless of temperature 
  or... anything really
  - settings:
    - speed [0-100]
    
- curve
  allows defining of a fan speed curve
  - settings:
    - points  
      example config:
    
    ```yaml
    fan_manager:
      model: curve
      points:
        - [0, 0]  # [temp(*C), speed(0-100%)]
        - [50, 30]
        - [70, 100]
      sensor_name: k10temp

    ```
    - sensor_name [name of the sensor to get temperature reading from(names can be found by running `sensors` in a terminal)]
    
### Lighting Manager Settings
To save repetition:  
speed: desired refresh speed of the device ['slow', 'normal', 'fast', 'extreme']
g/r/b: RGB values of the desired colour

- alternating  
  alternates between odd_rgb and even_rgb such that every "tick" the lights
  on the device will alternate between the 2 colours
  - settings:  
    - speed  
    - odd_rgb:  
      - g  
      - r  
      - b  
    - even_rgb:  
      - g  
      - r  
      - b  
      
- temperature 
  will set lighting to a colour between blue/green/red and anywhere inbetween
  depending on the temperature of the selected sensor
  - settings: 
    - speed 
    - sensor_name [name of the sensor to get temperature reading from(names can be found by running `sensors` in a terminal)]
    - cold [desired temperature to set lighting to blue]
    - hot [desired temperature to set lighting to red]
    - target [desired temperature to set lighting to green]

- full 
  sets lighting to this colour
  - settings: 
    - r 
    - g 
    - b 
    
- off 
  as it sounds, turns lighting off
  - settings: 

- flow 
  walks each led in the device slowly going around the RGB spectrum individually
  - settings: 
    - speed 
    
- spectrum 
  fades all lights at the same time through the RGB spectrum
  - settings: 
    - speed 
    
- ripple 
  leading led light followed by a trail of fading led's that walk all led's in
  the device
  - settings: 
    - speed 
    - r 
    - g 
    - b 
    
- blink 
  repeatedly flashes the led's in the devices in the selected colour
  - settings: 
    - speed 
    - r 
    - g 
    - b 
    
- pulse 
  same as blink, except using a smooth fade
  - settings: 
    - speed 
    - r 
    - g 
    - b 
  


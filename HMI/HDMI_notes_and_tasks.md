# HMI Programming Notes and Tasks

## Good features to add

- Alarms on error states (Function -> Trigger). 
  - Email on error??
- QR Code for error reporting! Or fiix link??
- Analog Meters for Wheel Positions
  - Indicate main wheel door near main wheel
- Bar Meters for Flap Extension
- Indicator Light for Lights and electricals
- Bitmaps for pneumatics (Kruger flaps, spoilers, ailerons, rudder, thrust reverser, door)
- Enable Screensaver

## Ideas for Pages

- Main Page (?)
- Status Page (all axes, all lights)
- 

## Workflow Notes

- Tag Database: `file > import > tag name database...` to grab tag names from the PLC program

### Objects

#### Text and Visuals

- `Triggered Text` - text object with ON and OFF states based on a tag
- `Dynamic Text` object shows the text in a string tag
- `Lookup Text` object maps the state of a tag to a text string
- `Multi-State Text Indicator` (In indicators) is one-off lookup of strings based on tag value
- `Dynamic Bitmap` is image with ON and OFF states based on a tag
- `Multi-state Bitmap` selects a bitmap from file based on a tag number

#### Buttons and Interfaces
- `Switch` - nice visual indicator of on 
- `Indicator Button` Button with State... not my favorite
- `Try-State Switch` - three interlocking stacks with indication. But with only two tags? Huh.


#### Misc
- `Alarm Call Screen` - pop up a list of alarms. Neat!
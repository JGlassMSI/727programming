# 727 Controller

The working files for developing a PLC/VFD controller for the 727 plane @ MSI.

## (Provisional) Major Parts List

- 1 @ [PS-622](https://www.automationdirect.com/adc/shopping/catalog/programmable_controllers/productivity2000_plcs_(micro-modular)/cpus/p2-622) CPU 
  - 1 @ [P2-04B](https://www.automationdirect.com/adc/shopping/catalog/programmable_controllers/productivity2000_plcs_(micro-modular)/bases/p2-04b) Base
  - 1 @ [P2-08Nd3-1](https://www.automationdirect.com/adc/shopping/catalog/programmable_controllers/productivity2000_plcs_(micro-modular)/dc_i-z-o/p2-08nd3-1) Digital I/O block
- 1 @ [PS-AMC4](https://www.automationdirect.com/adc/shopping/catalog/programmable_controllers/productivity1000_plcs_(stackable_micro)/motion_-a-_specialty_modules/ps-amc4?srsltid=AfmBOorezgSZzr3bKxvrmp9IRJJF_oYx0-t6G30pTALZyFuavVMpTWcr) Four Axis motion controller 
- 4 @ [GS23-20P5](https://www.automationdirect.com/adc/shopping/catalog/drives_-a-_soft_starters/ac_variable_frequency_drives_(vfd)/general_purpose_vfds/gs23-25p0) VFDs
- [C-More HMI??](https://www.automationdirect.com/adc/shopping/catalog/hmi_(human_machine_interface)/graphical_hmi_devices/hmi_panels/cm5-t7w) or [headless HMI](https://www.automationdirect.com/adc/shopping/catalog/hmi_(human_machine_interface)/graphical_hmi_devices/hmi_panels/cm5-t10w)

## Process Phases

### Development

- [ ] Write specification
  - [ ] Power, voltage, speed, and quantity requirements
  - [ ] Fusing and breakers
  - [ ] Airflow available and temperature constraints
  - [ ] Usage/communication model with existing (new?) controller
- [x] Identify potential hardware families for use
- [ ] Identify specific major hardware components
- [ ] Develop state-graph representing operation
- [ ] Develop ladder-logic implementation of state graph

### Process

- [ ] Establish potential timeline with Museum stakeholders
- [ ] Investigate product lead times
- [ ] Estimate implementation time

### Implementation

- [ ] Finalize BOM
- [ ] Order parts and materials
  - [ ] \(?)Develop tabletop-size simulator?
- [ ] De-commission existing equipment in plane as necessary
- [ ] Install new equipment
- [ ] Test and verify

## Resources

### Software

- Ladder logic is being built in Producitvity Suite 4.4.0
- HMI software being built in C-More Programming Software (CM5) v8.23

### Manuals

- [Productivity 2000 Hardware User Manual](https://cdn.automationdirect.com/static/manuals/p2userm/p2userm.pdf)
- [Productivity Suite Online Manual](https://www.automationdirect.com/productivity/software/help)

### Videos

- [Basics of GS Drives and Productivity Suite](https://www.automationdirect.com/videos/video?videoToPlay=UU1bfRmbx7s)
- [PS-Automated Motion Contorller Playlist](https://www.youtube.com/playlist?list=PLPdypWXY_ROqe8nDp227ALBn2Cs9CcP2A)

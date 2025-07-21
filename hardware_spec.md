# Specificiation

## Summary

This specification describes new hardare to be installed into the 727 Exhibit at Griffin MSI. This system will replace (in large part) the existing automation controls for the 727 automation show, and provide new capabilities for control, show quality, and safety. The major motion components themselves will be re-used, for significant cost savings.

## System Description

The automation system consists of:

- 4 electromecanical axes (Main Landing Gear, Nose Gear, Inner Flaps, Outer Flaps)
- 7 Pneumatic axes (Main landing gear door, krueger flaps, spoilers, ailerons, rudder, elevator, and thrust reversers)
- 7 (TODO: Verify number) lighting outputs (Navigation Lights, landing lights, rotating beacon, turnoff lights, wing lights, nosewheel lights, cockpit flasher).

## Use of Existing Hardware and Wiring

The motors, pneumatic cylinders, and lighting fixutres, as well as the wiring which drives and powers them, shall remain the same under the new system. The limit switches which are associated with the electromechanical axes to stay the same

##  New Hardware

The new system shall include:

- An industrial-quality PlC, with:
  - AC or DC Outputs sufficient to directly drive all the pneumatic axes
  - AC or DC Outputs sufficient to directly drive all the lighting axes
  - Sufficient interconnects for the remaining components below>
  - Capability to interface with a remote show-scheduling program via network and/or serial communication
- Four VFDs for dirving the electromechanical axes
- A Motion Control module for interfacing with the VFDs with the PLC
- Encoders or other similar sensors to determine the real position of each electromechanical axis
- (Optionally) an HMI control screen, to be mounted inside the plane, for control and troubleshooting
- (Optionally) a motor control pendant or pickle to be usable from the underside of the plane or floor, for control or troubleshooting

## New Software

*This section has yet to be filled*

## Safety

*This section has yet to be filled*

## Possibilities and UnKnowns

- It shall be investigated whether the proposed electomechanical control solutions permit the use of the existing limit switches to serve for all necessary needs, or whether additional position-sensing contacts will be needed. In particular, whether the Main Gear will need an additional interlock switch to allow the gear door to open and close
- It shall be investigated how the VFD controls integrate with the existing motors, since the motors have an integral brake which currently disengages upon application of AC power. This may require additional wiring from each motor to the plane control cabinets, for independant control of each brake.

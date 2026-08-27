# Doppl-E - Build Log

## Overview
This Build Log documents the development process behind Doppl-E  and the engineering decisions and challenges behind it. Doppl-E has been my introduction to RF systems and electronics, allowing me to deepen my technical knowledge and hands on engineering simultaneously. A synopsis can be found in [README.md](README.md). My hand derivations for each specification within the project can be found in [design_calculations](/docs/design_calculations.md).

## Phase 1 - Design and Planning
Phase 1 was designed specifically to bridge the gap from 2nd year EE directly into RF systems, analog electronic design, and digital signal processing. A significant amount of time was dedicated to learning fundamental concepts and vocabulary. Research time was dedicated into the physics behind radar operation, and how past successful radar systems were designed. Phase 1 wrapped up with designing the KiCad schematic and PCB layout for the analog PCB.<br>
- Landed on initial concept: CW Radar with velocity detection capabilities<br>
- Selected HB100 Microwave Transceiver Module as RF Front end, researched functionality, use cases, and operation <br>
- Laid out basic signal chain design (IF amp, RC LPF) <br>
- Designed KiCad schematic<br>
- Converted schematic to PCB layout, ordered fabrication from PCBWay <br>
## Phase 2 - Hardware Build
Phase 2 contained the entire Doppl-E hardware build. Significant improvements were made in my technical knowledge and experience. The first major roadblock encountered was the poor quality jumper wires I attempted to use as connectors. I elected to replace them with 24 gauge copper wire (as seen on BOM)[BOM](/docs/bom.md). Afterward, the first PCB build had cold solder joints, rendering it inoperable.After diagnosing cold joints and the root cause and refining my soldering technique, PCB v2 was populated using a component-by-component verification approach. The Phase ended with a sucsessful end-to-end signal detection.
- Sourced hardware components
- Prototyped analog pcb system on breadboard
- Began soldering troubleshooping (tip oxidation, jumper wire issues)
- Completed PCB v1: populated, cold join diagnosis
- Completed PCB v2: utilized systematic component verification method, following board bring-up procedure standards
- Executed first HB100 power-on, 32mA draw confirmed 
- First end-to-end signal detection confirmed 
🚧 Coming soon! 🚧
## Phase 3
🚧 Coming soon! 🚧
## Phase 4
🚧 Coming soon! 🚧
## Challenges and key lessons
🚧 Coming soon! 🚧
## Whats next
🚧 Coming soon! 🚧
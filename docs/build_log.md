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
Phase 2 contained the entire Doppl-E hardware build. Significant improvements were made in my technical knowledge and experience. The first major roadblock encountered was the poor quality jumper wires I attempted to use as connectors. I elected to replace them with 24 gauge copper wire (as seen on [BOM](/docs/bom.md)). Afterward, the first PCB build had cold solder joints, rendering it inoperable.After diagnosing cold joints and the root cause and refining my soldering technique, PCB v2 was populated using a component-by-component verification approach. The Phase ended with a sucsessful end-to-end signal detection.
- Sourced hardware components
- Prototyped analog pcb system on breadboard
- Began soldering troubleshooping (tip oxidation, jumper wire issues)
- Completed PCB v1: populated, cold join diagnosis
- Completed PCB v2: utilized systematic component verification method, following board bring-up procedure standards
- Executed first HB100 power-on, 32mA draw confirmed 
- First end-to-end signal detection confirmed 
## Phase 3 - Software Development and Signal Processing
Phase 3 held the bulk of the overall project's software development. An initial 5 second test script was designed in Python, which was developed into a sophisticated pipeline with real-time streaming capabilities. The goal was to create an easy to use front end system, where the user would be able to watch Doppl-E live capture any moving object with results pushed out in real time. In the end, the pipeline produced reliable velocity measurements after attinuating 60Hz power line interference, as seen in [DopplE_Lab](/software/dopple_lab.py).
- Developed Python DSP pipeline
- Discovered 60Hz noise interference, attenuated with a software HPF
- Evolved DSP pipeline into real-time streaming solution
- Began developing Doppl-E Lab GUI
## Phase 4 - Validation and Polishing
Phase 4 ties up loose ends within the project, showing off the story of Doppl-E's development and the future trajectory of the lead engineer. Additional features were added to Doppl-E Lab, allowing users to easily operate and troubleshoot the system, as well as create effective reports directly from the UI. A proper experiment was executed, as seen in [Validation & Results](/docs/validation_results.md). I enlisted the help Daniel Dietze, a Film student at The University of Northern Iowa and close friend of mine, to plan and shoot the demo video. Finally, documentation was completed to showcase the story of Doppl-E, and what is to come in the future.
- Polished Doppl-E Lab, adding report capture feature as well as user guide
- Executed controlled vehicle experiment
- Analyzed error in measurement and identified contibuting sources, including antenna alignment and speedometer reference accuracy
- Completed documentation
- Planned, captured, and executed demo video
- Published project to LinkedIn, reaching [x] impressions
## Challenges and key lessons
On May 7th, 2026 I created a Google Drive folder and named it "Radar project". Frankly, I had no clue what I was in for the next 16 weeks. Through my time at Queen's, I had been involved in 3 group rapid-development engineering projects. I had gravitated to very hardware and technical-heavy roles, but I had never pursued a project independently. <br>
The study of Radio-Frequency Engineering fascinated me, but Queen's offered no courseware until 4th year, after I would have completed my Co-op. I decided to take matters into my own hands and teach myself the fundamentals of RF Engineering.<br>
I flirted with the idea of designing a simple radio system, but a post on Reddit describing a custom-designed radar immediately filled me with inspiration. I spent several days exploring all kinds of radar projects on Github and Reddit, ranging from FMCW designs to custom Phased-Array Apertures. These flashy projects were a little out of my price range and scope, so I decided to strengthen my fundamentals with a CW Doppler Radar design. This little pet projects, soon renamed to Doppl-E, taught me several important lessons through its life.
### The majority of engineering is troubleshooting
The majority of my time working on Doppl-E consisted of reading datasheets, sanity checking on breadboards, and triple checking figures by hand on my IPad. From Python scripts breaking a hundred times, to windows constantly forgetting my ADC exists, to PCBs giving your multimeter numbers straight from left field. In larger scale projects, you spend 10 minutes building the prototype and 3 hours fixing it, and that's okay!
### Systematic verification saves significant time(and sanity)
My first analog PCB threw me a curveball by feeding my multimeter numbers that caused my head to spin. In the end, I chalked it up to my brand new soldering iron only being tinned for 30 seconds, and my PCB population being rushed with little to no component verification. Before populating PCB mark II, I ensured proper care of my tools and workspace. I tinned the iron and increased the soldering temperature to avoid creating cold joints for a second time. I populated the second PCB using systematic verification, making sure every component was connected properly before continuing. The second PCB worked perfectly, and was included in the final build.
### Real-world results aren't as pretty as lab results
When first deploying Doppl-E on a live moving target, I noticed there is a little noticeable error in the final reading. This stems from two main issues:<br>
- The HB100, with its single TX/RX antenna pair and no phased array capability, measures only radial velocity. This means targets moving at an angle to the antenna axis produce diminished Doppler shifting.
- Vehicle speedometers contain error, which is inconsistent car to car and difficult to truly measure
The HB100 is a fantastic transceiver module, especially for its price, but it is far from the most accurate. This does lead to some measurement error, discussed in [Validation & Results](/docs/validation_results.md)
## What's Next
While it certainly wasn't easy, Doppl-E was an incredible first solo project. This project stands as a milestone along my journey as an Engineer, and I am very satisfied with the completion of the project. Within my allotted timeframe, I have successfully completed the goals I initially set for myself, addressing any gaps that could have weaked my results. That being said, I certainly want to launch more advanced projects to build on knowledge developed through Doppl-E.
### Software-Defined Radio
Designing a Software-Defined Radio would be a simple follow up project compared to Doppl-E, however, it would certainly be rewarding in developing my knowledge in true RF communications. An SDR project would be reasonably cheap, especially with the tools I have purchased to design Doppl-E. I plan to research timelines, potentially designing the project in Winter 2026.
### Frequency Modulated Continuous Wave (FMCW) Radar
The natural evolution of Doppl-E, a Frequency Modulated Continuous Wave (FMCW) Radar, contains far more sophisticated hardware. Unlike Doppl-E, a FMCW system reports distance, velocity, and can support direction finding, all with signifigantly higher accuracy. However, this system would be far more complex, expensive, and time-consuming. Doppl-E has developed the RF engineering basics to tackle the project. However, due to an extreme amount of work involved, the best timing for the project would be my Capstone project, a multidisciplinary project during my 4th year of studies.

Doppl-E is the first chapter. There's a lot more to write.
---
*Jubal Clapp | Electrical Engineering @ Queen's University | Summer 2026*
# Doppl-E - Design Calculations

## 1. Radar Range Equation
### 1.1 General Derivation
If you were to imagine trying to find the power density around an isotropic antenna, you would find yourself dividing power by area, which is demonstrated as:<br>
$$S_u = \frac{P_s}{4\pi R_l^2}$$ (1)<br>
Where:<br>
$P_s$ - Transmitted power<br>
$S_u$ - Power density(in any direction)<br>
$R_l$ - Distance(from source)<br>
Next, the directional power density can be found by multiplying 1 by a directional variable, $G$<br>
$$S_y = S_u G = (\frac{P_s}{4\pi R_1^2}) G$$ (2)<br>
Where:<br>
$S_y$ - Directional Power Density<br>
Additionally, Reflected power depends on the Radar Cross Section. As a signal is reflected proportionally to the size of the dish designed to reflect it. The problem can be modeled as a probability system where $\sigma$ mirrors the odds of a wave hitting the Radar<br>
$$P_r = \frac{P_s}{4\pi R_1^2} G \sigma$$ (3)<br>
Where:<br>
$P_r$ - Reflected power<br>
$\sigma$ - Radar Cross Section(RCS)<br>
To switch gears, reflected power can be eyeballed in forward or reverse motion, depending on what is easier for an engineer to see. Meaning, a target can actually be thought of as a radiator of reflected power<br>
$$S_e = \frac{P_r}{4\pi R_2^2}$$ (4)<br>
Where:<br>
$S_e$ - Power density at the target's location<br>
$P_r$ - Reflected Power<br>
$R_2$ - Distance between the target and the source<br>
Similarly to RCS, power received by the antenna aperture depends on several factors, such as material and size, introducing a variable modeling the efficiency of aperture signal capture.<br>
$$P_e = S_e A_w$$ (5)<br>
Where:<br>
$P_e$ - Received Power<br>
$A_w$ - Antenna Aperture Coefficent<br>
The Aperture coefficent can be further described using the Antenna Specific Loss<br>
$$A_w = A K_a$$ (6)<br>
Where:<br>
$A_w$ - Aperture area [m^2]<br>
$K_a$ - Respective antenna specific loss<br>
Equation 6 can be substituted into Equation 5, giving<br>
$$P_e = S_e A  K_a$$<br>
Which can be further described, substituting Equation 4 which gives<br>
$$P_e = \frac{P_r}{4\pi R_2^2} A K_a$$<br>
In which, Equation 3 can be substituted into<br>
$$P_e = ((\frac{(\frac{P_s}{4\pi R_1^2}) G \sigma)}{4\pi R_2^2}) A K_a$$<br>
The two denominators can be combined, leading to<br>
$$P_e = \frac{P_s G \sigma}{(4\pi)^2 R_2 ^2 R_1^2} A K_a$$<br>
It is noted that $R_1$ measures the distance starting from the source to an arbitrary target point, $T$. $R^2$ treats $T$ as a 'source' of reflected energy leading back to the original source, meaning it measures from $T$ back to the source. Therefore:<br>
$$R_2 = R_1 = R$$<br>
and,<br>
$$P_e = \frac{P_s G \sigma}{(4\pi)^2 R^4} A K_a$$<br>
Now recall, Gain, $G$, is equal to $4\pi A K_a / \lambda^2$. This equation can be rearranged into $A K_a = G \lambda^2/4\pi$. Substituting the latter with $A K_a$, the equation simplifies to <br>
$$P_e = \frac{P_s G^2 \lambda^2 \sigma}{(4\pi)^3 R^4}$$<br>
Rearranging the equation in terms of $R$, <br>
$$R = \sqrt[4]{\frac{P_s G^2 \lambda^2 \sigma}{(4\pi)^3 P_e}}$$<br>

### 1.2 Application to Doppl-E
Doppl-E uses the HB100 microwave sensor module as its RF front end device, including Tx, Rx, and Mixer. The HB100's two patch antennas operate at 10.525GHz. Using its datasheet and the derivation above, we can estimate the maximum theoretical range of the HB100<br>
From the above stated derivation, <br>
$$R = \sqrt[4]{\frac{P_s G^2 \lambda^2 \sigma}{(4\pi)^3 P_e}}$$<br>
$P_s$ can be found on the HB100 datasheet on DigiKey, 13 mW<br>
$G$ was experimentally measured to 1.5dBi in an academic study[1] trying to increase the scope of the HB100 chip, including methods such as range amplification. <br>
$\lambda$ of the system is directly correlated to the speed of the propagating EM wave, $c$, and its frequency, $f$, at 10,525GHz,<br>
$$\frac{c}{f} = \frac{3*10^8}{10.525*10^9} = 0.0285m$$  <br>
$\sigma$ must be approximated by selecting a target of a given size. Due to the description of Radar Cross Section derived in 1.1, when an EM wave hits a larger target, such as a car, a smaller amount of energy dissipates into random radiation, making it easier for the radar to "see". For the sake of approximation, the target will be assumed as a human, giving the range a worst-case figure. The RCS of a human can be estimated by considering the surface area of the front of an average person, which we will call $1m^2$<br>
$P_e$ can be found using a resource found very early in the Doppl-E project[2]. From the page containing the Radar Range Equation, we can find that,<br>
$$P_{Emin} = k T B_w \frac{S}{N_{min}} L_{ges}$$<br>
where:<br>
$k$ - 1.38*10^-23 (the Boltzmann constant)<br>
$T$ - room temperature[290K]<br>
$B_w$ - receiver bandwidth aka LPF Bandwidth(2340Hz)<br>
$\frac{S}{N_{min}}$ - The minimum signal to noise ratio for Doppl-E to define a signal as a real target, rather than noise. There isn't a great way to measure it, therefore, I will be using a standard assumption of the ratio of 10dB, rough linear value of 10<br>
$L_{ges}$ - System losses. This term accounts for all of the random errors that feed off of different parts of the signal chain. Cable and connector losses, impedance, soldering error, etc. Once again, there's not an amazing way for me to measure it, so Ill be once again using a fair industry estimation 3dB, rough linear value of 2 <br>
$$P_{Emin} = 1.38\cdot10^{-23}\cdot290\cdot2340\cdot10\cdot2 = 1.87\cdot10^{-16}W$$ <br>
Now, substituting all of the values above into the radar range equation, the theoretical maximum range of the HB100 is <br>
$$R_{maxTheoretical} = \sqrt[4]{\frac{0.013\cdot1.41^2\cdot0.0285^2\cdot1}{(4\pi)^3\cdot1.87\cdot10^{-16}}} = 86.73m$$<br>
Now this theoretical number should be raising eyebrows a little bit. While the HB100 certainly is impressive in its capabilities using such a small amount of space and resources, it is not a precision RF instrument, meaning an ideal maximum range isn't realistic. This theoretical range is not accurate, which can be traced back to the definition of $P_e$, specifically $L_{ges}$<br>
$L_{ges}$ accounts for all error in the reception of the signal, including any interference in the cables, connections, or impedance. Estimating the term at 3dB is certainly an optimistic decision, especially for the HB100, a relatively cheap and simple chip.<br>
Comparing the range to the manufacturer's description, the HB100 effective range is listed at "capable of picking up a human walking 1.28kmh at 15 meters"[3], which is certainly a significantly smaller range than calculated by the "best case" radar range equation.<br>
Now the radar range equation demonstrates how delicate RF systems are, and how easily seemingly small differences in delicate values, such as system loss, can lead to inaccurate and hyperidealized results, such as $R_{maxTheoretical}$. Moving forward in the project, the effective range will be assumed at 15m for a human-sized target, scaling up for larger targets such as cars or semis. This assumption will be further tested in Week 14, as the system is stress-tested with real life targets.

## 2. Doppler Frequency Analysis
### 2.1 Derivation
The Doppler Effect is defined using frequencies as,<br>
$$f_s = f_o\cdot(\frac{v \pm v_o}{v \pm v_s})$$ (7)<br>
Where:<br>
$f_s$ - Shifted frequency<br>
$f_o$ - Original Frequency<br>
$v$ - Propagation speed of the wave<br>
$v_o$ - Speed of the wave receiver(with respect to the source)<br>
$v_s$ - Speed of the wave source(with respect to the source)<br>
Additionally, it should be noted that the plus-minuses in the Doppler Effect equation are reciprocal. Meaning if the numerator is $v+v_o$, then the denominator must be $v-v_s$, and vice versa.<br>
Now for an electromagnetic wave with respect to an antenna aperture, we can fill in some of these values. Generally for precision, a radar is not moving, so $v_s$ can be assumed to be 0. Additionally, EM waves propogate at the speed of light, $c$. Therefore, the equation simplifies to <br>
$$f_s = f_o\cdot(\frac{c \pm v_o}{c})$$ (8)<br>
The mixer inside of the HB100 operates by taking the received signal, $f_{rx}$, and subtracting it from the transmitted signal, $f_{tx}$. This operation allows the creation of the intermediate frequency, $f_{int}$<br>
$$f_{int} = f_{rx} - f_{tx}$$ (9)<br>
From the definition of a radar, $f_{rx}$ can be rewritten as a doppler shift identity, as it is a reflection of the original transmission wave. In the following equation. $v$ refers to the velocity of the target, which Doppl-E is intended to detect.<br>
$$f_{int} = f_{tx}\cdot\frac{c + v}{c} - f_{tx}$$<br>
Which can be simply rewritten into<br>
$$f_{int} = f_{tx}[\frac{c + v}{c} - 1]$$<br>
In which the speed of light fraction can be further simplified into<br>
$$f_{int} = f_{tx}[1 + \frac{v}{c} - 1]$$<br>
Which once again, can be simplified to<br>
$$f_{int} = f_{tx}(\frac{v}{c})$$<br>
Recalling the frequency relationship of EM waves, $f = \frac{c}{v}$, which can be arranged to $\frac{f}{c} = \frac{1}{\lambda}$. Using this principle, the equation can be simplified to<br>
$$f_{int} = \frac{c}{\lambda}\cdot\frac{v}{c}$$<br>
Equalling,<br>
$$f_{int} = \frac{v}{\lambda}$$<br>
Now this relationship only describes the Doppler shift on the outbound path. When the wave reflects off of the target, it experiences a second Doppler shift. To properly describe this two Doppler shift relationship as seen on a radar system, the entire relationship must be multiplied by 2.<br>
$$f_{int} = \frac{2v}{\lambda}$$ (10)<br>

### 2.2 Application to Doppl-E
As derived in [Section 1.2](#12-application-to-doppl-e), the HB100 operates at a wavelength of $\lambda = 0.0285m$. While designing Doppl-E, I decided to select the maximum velocity detectable at around 29m/s(65mph). The inception of Doppl-E included its capabilities to detect a high-speed vehicle. Nothing like an airplane thousands of meters away, rather, trucks and cars driving by a stationary measuring point on a highway. This upper bound gives a realistic use case for Doppl-E, as it could be used to detect passing vehicle velocity. <br>
This table briefly outlines different moving objects and their rough velocities.<br>
| Target | Speed (km/h) | Speed (m/s) | $f_{int}$ (Hz) |
| ------ | :---: | :---: | :---: |
| Walking human | 5 | 1.4 | 98 |
| Jogging human | 15 | 4.2 | 295 |
| Cycling | 30 | 8.3 | 582 |
| Slow moving car | 50 | 13.9 | 975 |
| Car on Highway | 100 | 27.8 | 1951 |
| Highway max speed | 105 | 29.2 | 2050 |  
<br>
As shown in the table, a high estimate for the speed of a car moving on a highway is about 105km/h, or 65mph. To find the corresponding intermediate frequency, we can use Equation 10 found in Section 2.1

$$f_{int} = \frac{2 \cdot 29}{0.0285}$$

$$f_{int} = 2035 \text{ Hz}$$

This frequency is the maximum intermediate frequency Doppl-E will accept. Setting a maximum frequency allows Doppl-E to accept speeds up to a very realistic maximum, all while rejecting out-of-band noise that would otherwise complicate the signal processing pipeline downstream. This value of $f_{int} = 2035$ Hz is the primary design requirement of the Low Pass Filter in section 4, as it is the direct requirement for the maximum frequency that must be allowed to pass through the filter.<br>

## 3. Gain Stage Design
### 3.1 Derivation 
The HB100 unit outputs an IF signal ranging from 0.2 to 5 mV, meaning the IF signal is microscopic compared to the voltage range the Python script needs to interpret velocity figures. To work around this complication, a gain-stage amplifier needs to be designed and implemented.<br>
The ADC functions as an aux-to-USB port, and expects a rough voltage range of 100-500mV, meaning the ADC will expect a significant amplification from raw HB100 IF output. To find the gain required, we can divide the Target by the Source.<br>
$$Gain = \frac{V_{target}}{V_{source}}$$<br>
Now, we must ensure not to overamplify, which can create noise in the ADC. Now interpreting the high and low voltages values of each range, it's noted that a $V_{source}$ highest value should correspond with the $V_{target}$ highest value. This means to find our gain, we don't need to find the worst or best case required gain, but the gain required to match the extrema. The derivation follows:<br>
$$Gain = \frac{V_{TargetHigh}}{V_{SourceHigh}} = \frac{0.5}{0.005} = 100$$<br>
It is possible to execute such a gain stage through one very large amplification, but for both stability and noise-reduction as factors in the output of Doppl-E, it is optimal to split the gain stage into multiple stages, in our case, 2.<br>
In each of the gain stages utilized in Doppl-E, there is a non-inverting op-amp connected to a pair of feedback resistors to calibrate proper gain. The non-inverting op-amp equation follows:<br>
$$G = 1 + \frac{R_2}{R_1}$$<br>
Spreading this across two stages, the equation evolves into<br>
$$G_{total} = G_1 \cdot G_2$$
$$G_{total} = (1 + \frac{R_2}{R_1})(1 + \frac{R_4}{R_3})$$
Since both stages are designed to be equivalent, it can be assumed that $R_2 = R_4$, $R_1 = R_3$, simplifying the equation further into. <br>
$$G_{total} = (1 + \frac{R_2}{R_1})^2$$

### 3.2 Applied to Doppl-E
As discussed in [Section 3.1](#31-derivation), the HB100 datasheet lists the expected IF output between 0.2-5 mV. This outputted signal is very weak and noisy, requiring amplification prior to filtering. Additionally discussed in [Section 3.1](#31-derivation), the ADC expects an outputted signal strength generally between 100-500mV. We also derived the required gain, which lands at 100x amplification. <br>
Now from a practical perspective, the two-stage amplifier circuit is made of two non-inverting amplifiers, with each stages gain described as<br>
$$G = 1 + \frac{R_2}{R_1}$$ 
and the overall gain, <br>
$$G_{total} = (1 + \frac{R_2}{R_1})^2$$
We need to find two resistance values such that $G_{total} \approx 100$ To simplify the amplifier, we can set $R_2 = 10R_1$. <br>
$$G_{total} = (1 + 10)^2$$
$$G_{total} = 121$$
Now that the relationship between $R_1$ and $R_2$ is known, we can select a simple pair of strong, standard resistors. In this case, I selected $10\text{k}\Omega$ and $100\text{k}\Omega$<br>
Op-amp selection is vital to creating a proper gain stage. I selected the MCP6002 I/P. This model features very low noise and rail to rail output. This allows the op-amp to amplify with very little risk of saturation or noise addition. <br>
Substituting the resistance values into the total gain equation, we get,<br>
$$Gain_{total} = (1 + \frac{100\text{k}}{10\text{k}})^2$$
$$Gain_{total} = 121$$
While the required gain derived in Section 3.1 was 100x, selecting a simpler resistor ratio of $R_2 = 10R_1$ will increase the gain 21% up to 121x. This increase causes no meaningful change to the signal reception through the ADC, allowing downstream operations to flow properly.<br>
Now the last finishing touch is to decouple the op-amps. To do this, a pair of  capacitors are placed in parallel with the power supply pins of each op-amp (5v -> pin 8, pin 4 -> GND). These capacitors smooth out any potential voltage spikes that could damage the op-amps. For part selection, size isn't particularly relevant, so selecting a relatively large capacitor at a standard size is ideal. I selected 100nF capacitors for decoupling.

## 4. Low-Pass Filter Design
### 4.1 Derivation
In any signal transmission line, there is the risk of accidental signal noise joining the line from a multitude of different causes(radio waves, bluetooth, etc). Even small traces of these signals can potentially confuse the Python FFT script, and cause it to find inaccurate readings of frequency, and therefore velocity. Now the good news is almost all of these noise sources are very high frequency, meaning they can easily be filtered out by a Low-Pass Filter.<br>
A low-pass filter acts just like the childhood game of limbo. The cutoff frequency is like the bar, allowing any frequency below it to pass freely. Any frequency above, regardless of signal strength, gets filtered out. There are many designs for Low-Pass filters, such as multiple-order quick response low-pass filters like Butterworths. In our instance, a simple RC low-pass filter is ideal.<br>
An RC LPF is made of a single resistor and a single capacitor. The use of these two passive components means the filter uses no additional power, as well as being very small, cheap, and easy to build. The only advantage of using a more complicated filter topology is a steeper roll-off above cutoff frequency, which is unnecessary given Doppl-E's signal range.<br>
The cutoff frequency relationship follows as <br>
$$ f_c = \frac{1}{2\pi RC}$$
To rearrange in terms of capacitance, <br>
$$C = \frac{1}{2\pi \cdot f_c \cdot R}$$

### 4.2 Applied to Doppl-E
As discussed in [Section 2.2](#22-application-to-doppl-e), the cutoff frequency required to capture the speed of vehicles on highways is 2035Hz. To account for component tolerances(5% resistor, 5% film capacitor), and to account for additional error through the form of signal corruption and mechanical interference, I made the design decision to increase the cutoff to 2340Hz. Adding this headroom will allow the system breathing room in case of unforeseen error.<br>
For simplicity's sake, I selected the resistance component of the LPF, R5, to be equal to the rest of the resistors in the PCB.<br>
$$R_5 = 10\text{k}\Omega$$
Now we can substitute $R_5$ into the cutoff frequency relationship in [4.1 Derivation](#41-derivation),<br>
$$C = \frac{1}{2\pi \cdot 2340 \cdot 10000}$$
$$C = 6.8\text{nF}$$
Therefore, the Low Pass Filter will be made of a $10\text{k}\Omega$ resistor and a 6.8nF capacitor. The resistor, like all other resistors inside the PCB, will have a component tolerance of 5%. For the sake of minimizing Low Pass Filter error, the capacitor selected will be a film capacitor with 5% component error. The low component error of resistor and capacitor involved will ensure the Low-Pass Filter error stays to an acceptably low range. <br>
The Low-Pass Filter will help prevent the Python DSP pipeline from getting inaccurate data that could corrupt potential results. However, there are some further tools that can be utilized. An excellent example is the Notch Filter that will be discussed in [6. Notch Filter](#6-notch-filter), which will be used to tune out 60Hz utility noise.
## 5. Power
🚧In progress - Power budget has not been assesed🚧
## 6. Notch Filter
🚧In progress - Notch filter has not been designed🚧
## Citations
[1] P. Z. Petkov, R. Vitanov, and I. Nachev, "One Possibility to Increase 
    the Scope for Radar Module HB100 and Fields of Application," 
    ResearchGate. [Online]. Available: 
    https://www.researchgate.net/publication/334307851<br>
[2]C. Wolff, “The Radar Equation - Radartutorial,” Radartutorial.eu, 2020. 
    https://www.radartutorial.eu/01.basics/The%20Radar%20Range%20Equation.en.html<br>
[3] ST Engineering, "HB100 Microwave Sensor Application Note," MSAN-001, 
    Antenna Test Lab. [Online]. Available: 
    https://antennatestlab.com/wp-content/uploads/2019/07/HB100-Spec-Sheet-Radar-Sensor-Application-Note-Data-Sheet.pdf

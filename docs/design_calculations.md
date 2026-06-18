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
$P_s$ can be found on the HB100 datasheet on DigiKey, 13 mW
$G$ was experimentally measured to 1.5dBi in an academic study[1] trying to increase the scope of the HB100 chip, including methods such as range amplification. 
$\lambda$ of the system is directly correlated to the speed of the propagating EM wave, $c$, and its frequency, $f$, at 10,525GHz,<br>
$$\frac{c}{f}$$, $$\frac{3*10^8}{10.525*10^9} = 0.0285m$$<br>
$\sigma$ must be approximated by selecting a target of a given size. Due to the description of Radar Cross Section derived in 1.1, when an EM wave hits a larger target, such as a car, a smaller amount of energy dissipates into random radiation, making it easier for the radar to "see". For the sake of approximation, the target will be assumed as a human, giving the range a worst-case figure. The RCS of a human can be estimated by considering the surface area of the front of an average person, which we will call $1m^2$<br>
$P_e$ can be found using a resource found very early in the Doppl-E project[2]. From the page containing the Radar Range Equation, we can find that,<br>
$$P_{Emin} = k T B_w \frac{S}{N}_{min} L_{ges}$$<br>
where:<br>
$k$ - 1.38*10^-23 (the Boltzmann constant)<br>
$T$ - room temperature[290K]<br>
$B_w$ - receiver bandwidth aka LPF Bandwidth(2340Hz)<br>
$\frac{S}{N}_{min}$ - The minimum signal to noise ratio for Doppl-E to define a signal as a real target, rather than noise. There isn't a great way to measure it, therefore, I will be using a standard assumption of the ratio of 10dB, rough linear value of 10<br>
$L_{ges}$ - System losses. This term accounts for all of the random errors that feed off of different parts of the signal chain. Cable and connector losses, impedance, soldering error, etc. Once again, there's not an amazing way for me to measure it, so Ill be once again using a fair industry estimation 3dB, rough linear value of 2<br>
$$P_{Emin} = 1.38\cdot10^{-23}\cdot290\cdot2340\cdot10\cdot2 = 1.87\cdot10^{-16}W$$<br>
Now, substituting all of the values above into the radar range equation, the theoretical maximum range of the HB100 is <br>
$$R_{maxTheoretical} = \sqrt[4]{\frac{0.013\cdot1.41^2\cdot0.0285^2\cdot1}{(4\pi)^3\cdot1.87\cdot10^{-16}}} = 86.73m$$<br>
Now this theoretical number should be raising eyebrows a little bit. While the HB100 certainly is impressive in its capabilities using such a small amount of space and resources, it is not a precision RF instrument, meaning an ideal maximum range isn't realistic. This theoretical range is not accurate, which can be traced back to the definition of $P_e$, specifically $L_{ges}$<br>
$L_{ges}$ accounts for all error in the reception of the signal, including any interference in the cables, connections, or impedance. Estimating the term at 3dB is certainly an optimistic decision, especially for the HB100, a relatively cheap and simple chip.<br>
Comparing the range to the manufacturer's description, the HB100 effective range is listed at "capable of picking up a human walking 1.28kmh at 15 meters"[3], which is certainly a significantly smaller range than calculated by the "best case" radar range equation.<br>
Now the radar range equation demonstrates how delicate RF systems are, and how easily seemingly small differences in delicate values, such as system loss, can lead to inaccurate and hyperidealized results, such as $R_{maxTheoretical}$. Moving forward in the project, the effective range will be assumed at 15m for a human-sized target, scaling up for larger targets such as cars or semis. This assumption will be further tested in Week 14, as the system is stress-tested with real life targets.

## 2. Doppler  Frequency Analysis
🚧In progress - Frequency analysis will be conducted shortly🚧
## 3. Gain Stage Design
🚧In progress - Gain stage has been designed, yet to be transcribed🚧
## 4. Low-Pass Filter Design
🚧In progress - Low-Pass Filter has been designed, yet to be transcribed🚧
## 5. Power
🚧In progress - Power budget has not been assesed🚧
## 6. Notch Filter
🚧In progress - Notch filter has not been designed🚧
## Citations
[1] P. Z. Petkov, R. Vitanov, and I. Nachev, "One Possibility to Increase 
    the Scope for Radar Module HB100 and Fields of Application," 
    ResearchGate. [Online]. Available: 
    https://www.researchgate.net/publication/334307851
[2]C. Wolff, “The Radar Equation - Radartutorial,” Radartutorial.eu, 2020. 
    https://www.radartutorial.eu/01.basics/The%20Radar%20Range%20Equation.en.html
[3] ST Engineering, "HB100 Microwave Sensor Application Note," MSAN-001, 
    Antenna Test Lab. [Online]. Available: 
    https://antennatestlab.com/wp-content/uploads/2019/07/HB100-Spec-Sheet-Radar-Sensor-Application-Note-Data-Sheet.pdf

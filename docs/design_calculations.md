# Doppl-E - Design Calculations

## 1. Radar Range Equation
If you were to imagine trying to find the power density around an isotropic antenna, you would find yourself dividing power by area, which is demonstrated as:
$$S_u = \frac{P_s}{4\pi R_l^2}$$ (1)
Where:
$P_s$ - Transmitted power
$S_u$ - Power density(in any direction)
$R_l$ - Distance(from source)
Next, the directional power density can be found by multiplying 1 by a directional variable, $G$
$$S_y = S_u G = (\frac{P_s}{4\pi R_1^2}) G$$ (2)
Where:
$S_y$ - Directional Power Density
Additionally, Reflected power depends on the Radar Cross Section. As a signal is reflected proportionally to the size of the dish designed to reflect it. The problem can be modeled as a probability system where $\sigma$ mirrors the odds of a wave hitting the Radar
$$P_r = \frac{P_s}{4\pi R_1^2} G \sigma$$ (3)
Where:
$P_r$ - Reflected power
$\sigma$ - Radar Cross Section(RCS)
To switch gears, reflected power can be eyeballed in forward or reverse motion, depending on what is easier for an engineer to see. Meaning, a target can actually be thought of as a radiator of reflected power
$$S_e = \frac{P_r}{4\pi R_2^2}$$ (4)
Where:
$S_e$ - Power density at the target's location
$P_r$ - Reflected Power
$R_2$ - Distance between the target and the source
Similarly to RCS, power received by the antenna aperture depends on several factors, such as material and size, introducing a variable modeling the efficiency of aperture signal capture.
$$P_e = S_e A_w$$ (5)
Where:
$P_e$ - Received Power
$A_w$ - Antenna Aperture Coefficent
The Aperture coefficent can be further described using the Antenna Specific Loss
$$A_w = A K_a$$ (6)
Where:
$A_w$ - Aperture area [m^2]
$K_a$ - Respective antenna specific loss
Equation 6 can be substituted into Equation 5, giving
$$P_e = S_e A  K_a$$
Which can be further described, substituting Equation 4 which gives
$$P_e = \frac{P_r}{4\pi R_2^2} A K_a$$
In which, Equation 3 can be substituted into
$$P_e = ((\frac{(\frac{P_s}{4\pi R_1^2}) G \sigma)}{4\pi R_2^2}) A K_a$$
The two denominators can be combined, leading to
$$P_e = \frac{P_s G \sigma}{(4\pi)^2 R_2 ^2 R_1^2} A K_a$$
It is noted that $R_1$ measures the distance starting from the source to an arbitrary target point, $T$. $R^2$ treats $T$ as a 'source' of reflected energy leading back to the original source, meaning it measures from $T$ back to the source. Therefore:
$$R_2 = R_1 = R$$
and,
$$P_e = \frac{P_s G \sigma}{(4\pi)^2 R^4} A K_a$$
Now recall, Gain, $G$, is equal to $4\pi A K_a / \lambda^2$. This equation can be rearranged into $A K_a = G \lambda^2/4\pi$. Substituting the latter with $A K_a$, the equation simplifies to 
$$P_e = \frac{P_s G^2 \lambda^2 \sigma}{(4\pi)^3 R^4}$$
Rearranging the equation in terms of $R$, 
$$R = \sqrt[4]{\frac{P_s G^2 \lambda^2 \sigma}{(4\pi)^3 P_e}}$$

## 2. Doppler  Frequency Analysis

## 3. Gain Stage Design

## 4. Low-Pass Filter Design

## 5. Power

## 6. Notch Filter
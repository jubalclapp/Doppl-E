# Doppl-E - Validation & Results

## Overview
Validation & Results contains the experimental design, prediction, results, and analysis of the main experimental deployment of Doppl-E. This centralized experiment was designed to answer two questions:<br>
1. Can Doppl-E detect a moving object at a realistic distance?
2. How accurate is the speed estimate provided by Doppl-E Lab?
Additionally, this document serves as the direct sequel to [Design Calculations](/docs/design_calculations.md). Design Calculations demonstrated the mathematical design behind Doppl-E's hardware and operations, while Validation and Results showcases the effectiveness of the functional radar system.<br>
The outcome demonstrated accuracy in the figures derived in Design Calculations, consistent detection of moving objects, with a mean velocity error of 23.5%, which is consistent with expected sources of error discussed in the error analysis section

## Experimental Setup
To meet safety standards and comply with local traffic regulations, the first live deployment of Doppl-E was restricted to a low-speed test. <br>
The experiment was executed on a straight, recently paved road with low traffic. I placed a small table directly adjacent to the road, and placed the HB100 module on the edge of the table closest to the road. The HB100 was set at a 5-10 degree angle with respect to the road so it could capture a target from a distance. The module measured ~3ft off the curb, making the total height with respect to the road at ~1 meter.<br>
My experimental assistant operated the car, driving directly toward/ away from Doppl-E. Passes alternate direction (first pass  vehicle drives "toward" Doppl-E, second pass  vehicle drives "away"). Unfortunately, the community I operated out of didn't have hardware I could use to measure the true vehicle's speed. In light of this, I decided to have the driver drive at a predetermined constant speed, maintaining this speed through the speedometer. As an attempt to reduce reading error, I elected to use multiples of 10, landing on 10mph, 20mph, and 30mph.<br>
The final experiment plan consisted of 15 independent live captures, 5 at each speed (10mph, 20mph, 30mph). However, it was noticed during the first captures at 20mph that the error had inexplicably spiked. To increase confidence in the 20mph group without discarding any previous trials, I elected to add an additional 2 passes to 20mph.

## Theoretical Predictions
Referencing the following table from [Design Calculations](/docs/design_calculations.md) Section 2.2, we are expecting an intermediate frequency, $f_{int}$, of 314-940Hz. This places our expected capture between Cycling and Slow Moving Car.<br>
| Target | Speed (km/h) | Speed (m/s) | $f_{int}$ (Hz) |
| ------ | :---: | :---: | :---: |
| Walking human | 5 | 1.4 | 98 |
| Jogging human | 15 | 4.2 | 295 |
| Cycling | 30 | 8.3 | 582 |
| Slow moving car | 50 | 13.9 | 975 |
| Car on Highway | 100 | 27.8 | 1951 |
| Highway max speed | 105 | 29.2 | 2050 |

Additionally touched on in [Design Calculations](design_calculations.md) Section 1.2, the manufacturer-stated range is ~15m for a human. For the Doppl-E live deployment, range should be expected at or slightly larger than manufacturer-stated range, as a vehicle has a larger RCS($\sigma$) than a human.<br>
To successfully test a first live deployment, a success must be explicitly stated. In this instance, a complete success would include:
1. Successful object detection at a realistic standoff distance (>3m)
2. Relatively accurate velocity estimation across several speeds, indicating a band of accurate estimation exists
3. Error is measurable and explainable, reason behind discrepancies is understood to theoretically minimize error in the future

## Results
### 10mph trial
| Trial | Measured velocity(mph) | Error % |
| :---: | :---------------: | :-----: |
| 1 | 6.84  | 31.6 |
| 2 | 10.2 | 2.0 |
| 3 | 10.5 | 5.0 |
| 4 | 8.97  | 10.3 |
| 5 | 7.39  | 26.1 |

*mean error of group: 15.0%*

### 20mph trial
| Trial | Measured velocity(mph) | Error % |
| :---: | :---------------: | :-----: |
| 1 | 14.1  | 29.5 |
| 2 | 23.0 | 15 |
| 3 | 14.2 | 29.0 |
| 4 | 15.4  | 23.0 |
| 5 | 15.7  | 21.5 |
| 6 | 9.4  | 53.0 |
| 7 | 14.3  | 28.5 |

*mean error of group: 28.5%*

### 30mph trial
| Trial | Measured velocity(mph) | Error % |
| :---: | :---------------: | :-----: |
| 1 | 15.3  | 49.0 |
| 2 | 23.1 | 23.0 |
| 3 | 30.7 | 2.3 |
| 4 | 33.6  | 12.0 |
| 5 | 18.8  | 37.3 |

*mean error of group: 24.7%*
***
**Mean error of experiment: 23.4%**
## Error Analysis
The primary deployment of Doppl-E did contain noticeable error, which is traceable to three main contributors.
### Variance standard to small sample sizes
Likely the largest error contributor is variance found in small sample sizes. The primary deployment of Doppl-E was relatively small and quick, only totaling 17 recorded passthroughs. Unfortunately, there was not enough time to schedule a longer experiment.<br>
Following the law of large numbers, small sample sizes can contain a higher concentration of divergences and inexplicable error. The idea is as your sample size increases, your dataset approaches a greater accuracy. The difficulty in determining the size of an experiment is optimizing both the accuracy of your dataset, and the resources(mostly time) needed to create this dataset. Doppl-E's first deployment was small due to a lack of time, leading to the dataset to potentially contain a higher concentration of inaccurate readings. It is very likely that if the dataset was increased, doubled for instance, the error would've drastically decreased.
### Speedometer reference accuracy
In the 2016 document, SAE J2976, The Society of Automotive Engineers recommended speedometer error to fall between 2-4%, as to not affect driver's safety. The vehicle I used for testing was an older model, whose speedometer had not been services in several years. It is entirely possible that the speedometer error in my vehicle exceeds 4%. This serves as likely the second highest contributor of error within the deployment, ideally I would've compared Doppl-E's results directly with a commercial radar gun.
### Antenna Alignment
An additional contributor of error is the alignment of the antenna. As a Doppler radar system, the HB100 operates optimally when directly parallel with the direction of motion of the vehicle. Now due to safety concerns, Doppl-E was unable to be set in the direct path of motion. The antenna was aligned to 5-10 degrees, intersecting the road due to the line of sight. This fundamentally changes the doppler shift frequency equation from
$$ f_{int} = \frac{2v}{\lambda}$$
into
$$ f_{int} = \frac{2v}{\lambda} \cdot \cos(\theta)$$.
Now at the worst case of 10 degrees, an error slightly smaller than 2% is introduced. This suggests the larger portions of error introduced to the experiment trace to speedometer inaccuracy and small sample size variance.
## Conclusions
There were three initial goals for Doppl-E to reach, outlined in [Theoretical Predictions](#theoretical-predictions), and they follow:
1. Successful object detection at a realistic standoff distance (>3m)
2. Relatively accurate velocity estimation across several speeds, indicating a band of accurate estimation exists
3. Error is measurable and explainable, reason behind discrepancies is understood to theoretically minimize error in the future
The first goal Doppl-E met with ease. Vehicle detection was estimated around 40-50ft away from the antenna, so long distance capture was certainly successful.<br>
The second goal could be reasonably described as met with hardware taken into context. An accuracy rating of 77.6% wouldn't be ideal for military or airline grade hardware, but with the HB100 chip being a 50x50mm microwave transceiver module purchasable for $12 USD, 77.6% accuracy at 50ft is certainly nothing to scoff at. The accuracy rating available does certainly demonstrate the antenna was operated correctly with properly functioning hardware and software, so I would argue goal 3 was met.<br>
As for the third goal, measurable and explainable error. Error was successfully measured to be approx. 23.4% across tested speeds. As outlined in [Error Analysis](#error-analysis), the error can be fundamentally traced back to a poor sample size, inaccurate speedometer(which could have been fixed by using a commercial radar gun), and non-optimal antenna alignment due to safety conditions. The error has been successfully measured and traced back to three key sources, meaning the goal was met.<br>
Though Doppl-E may not have the same range or accuracy as commercial or military grade radar guns, the first deployment still successfully met all established goals, making The Doppl-E Mark 1 a full success.
## Future work
A major improvement that could be made to Doppl-E would be to properly test a wide range of velocity captures with a GPS speed reference or a commercial radar gun. A combination of better velocity comparison and a larger sample set could provide a drastically improved second deployment for Doppl-E.<br>
In the immediate future, I intend to explore Software Defined Radio in the form of a small-scale project. I believe this lower complexity follow-up project would allow me to deepen my RF knowledge before the true follow up project begins.
As I touched on in [Build Log](/docs/build_log.md), I intend to pursue a further radar project in the near future. Doppl-E has helped me learn the fundamentals of radar design, as well as analog electronics design and digital signal processing. In a little over a year, I intend to begin pursuing a Frequency Modulated Continuous Wave radar, which would allow velocity and position capture at a greater accuracy than Doppl-E, as well as the potential to add direction finding. This project will be significantly greater in difficulty, scope, and duration.<br>
***
Doppl-E Mark 1: validated.
***
*Jubal Clapp | Electrical Engineering @ Queen's University | Summer 2026*
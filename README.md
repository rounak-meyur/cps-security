# Bayesian Attack Tree Based Cyber-Physical Security Assessment
## Motivation
The advantage of adding modern day information and communication technology (ICT) in the supervisory control and data acquisition (SCADA) system associated with the power network comes at the cost of an increased risk due to cyber
intrusion. A well planned malicious attack on the SCADA system can not only compromise the communication network, but also cause catastrophic effects on the power grid in form of a widespread blackout. In this project, a Bayesian attack tree based approach is used to model cyber attacks in the SCADA network and the associated risk is evaluated as the combined effect on the communication and power system. This avoids the detailed modeling of every component in the CPS and considers only the critical vulnerabilities required to be exploited to perform the attack. Furthermore, the model takes into account the skill level of the adversary and the difficulty in intruding through each type of vulnerability. The proposed cyber attack model is applied on the IEEE-39 bus system with an associated SCADA network. The risk of a cyber attack on the critical vulnerabilities is evaluated for the power system.

## Simple Bayesian Attack Tree Model
![png](figs/fig-simpleattacktree.png)

## Bayesian Attack Tree Models of LAN/SCADA Networks
Substation LAN Model A | Substation LAN Model B 
:---: | :---: 
![png](figs/A-model.png) | ![png](figs/B-model.png)

Substation LAN Model C | Control Center SCADA Model 
:---: | :---: 
![png](figs/C-model.png) | ![png](figs/CC-model.png)

## Mean Time to Compromise
Substation LAN Model A | Substation LAN Model B 
:---: | :---: 
![png](figs/fig-resultA.png) | ![png](figs/fig-resultB.png)

Substation LAN Model C | Control Center SCADA Model 
:---: | :---: 
![png](figs/fig-resultC.png) | ![png](figs/fig-resultCC.png)

## Security Comparison
Substation LAN Models | Substation LAN Models and SCADA 
:---: | :---: 
![png](figs/fig-compare-subs.png) | ![png](figs/fig-compare-model.png)

## Physical Impact of an Attack
IEEE 39 bus system | Impact of attack on different IED sets 
:---: | :---: 
![png](figs/fig-ieee39.png) | ![png](figs/fig-sub2.png) ![png](figs/fig-key-sub2.png)

## Risk Assessment
Attack on Substation LAN Models | Attack on Control Center SCADA 
:---: | :---: 
![png](figs/fig-impact1.png) | ![png](figs/fig-impact2.png)
import numpy as np

import math

#constants
Z0 = 0.0002
alpha = 0.11
H_ref = 10
V_Href = 0 #nader bepaald
def V(alpha,h):
    def loglaw(h):
        V = V_Href *(h/Z0)/(H_ref/Z0)
    def powerlaw(alpha,h):
        Href = 60
        V = loglaw(Z0,60,h,V_Href) * ((h/H_ref))**2

    H_ref_powerlaw = 61
    for i in range(0,H_ref_powerlaw):
        loglaw(i)

    Eind_hoogte= 0
    for i in range(60,Eind_hoogte):
        powerlaw(alpha,i)
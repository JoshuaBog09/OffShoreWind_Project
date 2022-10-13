import numpy as np
import matplotlib.pyplot as plt

alpha = 0.11
z = 0.0002
href = 10
vref = 7
hblend = 60
hrequest = 100

vblend = vref * (np.log(hblend/z)/np.log(href/z))
vrequest = vblend * (hrequest/hblend)**alpha

print(vblend, vrequest)

def get_velocity_at_simple(h_reference, v_reference, h_request, h_blend, z_zero, alpha):
    if h_request <= h_blend:
        return v_reference * (np.log(h_request/z_zero)/np.log(h_reference/z_zero))
    elif h_request > h_blend:
        vblend = v_reference * (np.log(h_blend / z_zero) / np.log(h_reference / z_zero))
        vrequest = vblend * (h_request / h_blend) ** alpha
        return vrequest

def get_velocity_at(h_reference, v_reference, h_request, h_blend, z_zero, alpha):
    heightrange = np.arange(0, h_request + 0.01, 0.01)
    velocities = v_reference * (np.log(heightrange[heightrange <= h_blend] / z_zero) / np.log(h_reference / z_zero))
    velocities = np.append(velocities, velocities[-1] * (heightrange[heightrange > h_blend] / h_blend) ** alpha)
    return velocities[int(np.where(heightrange == h_request)[0])]
def get_velocity_profile(h_reference, v_reference, h_request, h_blend, z_zero, alpha):
    heightrange = np.arange(0, h_request+0.01,0.01)
    velocities = v_reference * (np.log(heightrange[heightrange <= h_blend]/z_zero)/np.log(h_reference/z_zero))
    velocities = np.append(velocities, velocities[-1] * (heightrange[heightrange > h_blend]/h_blend)**alpha)
    requested_point = (velocities[int(np.where(heightrange == h_request)[0])], int(np.where(heightrange == h_request)[0]))
    profile = (velocities, heightrange)
    return profile, requested_point

print(get_velocity_at(10,7,100,60,0.0002,0.11))
print(get_velocity_at_simple(10,7,100,60,0.0002,0.11))


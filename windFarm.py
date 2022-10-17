# external libraries
import numpy as np
import matplotlib.pyplot as plt

# default libraries
import math

# custom libraries
import utils.constants as constants


# TODO
# - ADD CHECKS FOR DIAMETER < HUB_HEIGHT*FACTOR
# - CHECK THE POWER OUTPUTS
# - REMOVE CONST VARIABLES IN CONST SHEET TO OFFER USER MORE CHOICES IN THE GUI


def windfarm(turbine_diameter: float, hub_height: float, v_reference: float, h_reference: float, request: list,
             capacity_factor: float):
    """
    :param turbine_diameter: Turbine blade diameter (the diameter of the swept circle area by the blades) [m]
    :param hub_height: Height of the turbine hub [m]
    :param v_reference: Reference velocity [m/s]
    :param h_reference: Height at which the reference velocity is measured (typically 10m) [m]
    :param request: The locations of how the turbines will be placed in series [m]
    :return: Nice data (TBD)
    """

    class Turbine:
        """
        Wind turbine class to store and calculate relevant values of the wind turbine
        velocity values in the wake are supplied in ranges from the turbine to the next to evaluate the wake and the mixed velocities
        """

        def __init__(self, location: float, diameter: float, localwindspeed: float, power: float, v_hub: float):
            """
            :param location: The location of the turbine in meters [m]
            :param diameter: The diameter of the turbine used [m]
            :param localwindspeed: The local windspeed [m/s]
            :param power: The power[W] of the turbine based on the local windspeed
            Note this is not the rated power! however it is derived from it
            """

            index = 0
            index += 1
            self.id = index

            self.location = location
            self.diameter = diameter
            self.localwindspeed = localwindspeed
            self.power = power * (localwindspeed / v_hub) ** 3
            self.rotorspeed = (2 / 3) * localwindspeed
            self.thrust = self.power / self.rotorspeed
            # Thrust coefficient
            self.ct = self.thrust / (0.5 * constants.rho * (localwindspeed ** 2) * math.pi * ((diameter / 2) ** 2))

        def supplyrange(self, first, last):
            """
            :param first: The location of the current turbine that is to be analysed
            :param last: The location of the next turbine
            :return: The velocity list for the specified range for the requested instance
            """
            self.s_range = np.linspace(first - self.location + (self.diameter * 3 + 1), last - self.location, 1000,
                                       endpoint=True) / self.diameter
            self.u_range = v_hub * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.s_range * constants.alpha) ** 2))
            return self.u_range

        def setuto(self, velocities):
            """
            :param velocities: Set the velocity list equal to the mixed velocity called behind the turbine due to wake effects
            :return: None
            """
            self.u_range = velocities

        def returnlast(self):
            """
            :return: The last velocity element in the velocity list
            """
            return self.u_range[-1]

        def printusefull(self):
            """
            Prints the usefull(windspeed[m/s^2], power[W], thrust[N] and thrust coefficient[-])
            characteristics of the Turbine(...) instance.
            """
            print(f"{self.localwindspeed=}", f"{self.power=}", f"{self.thrust=}", f"{self.ct=}")

        def __str__(self):
            return f"WindTurbine instance created with Turbine(location, diameter, localwindspeed, power)"

    def powerfirst(diameter: float, velocity: float) -> float:
        """
        :param diameter: Diameter of the turbine blades
        :param velocity: Velocity at the turbine hub
        :return: Power of the first turbine based on theoretical performance * efficiency factor of 80%
        """
        return (16 / 27) * (1 / 8) * constants.rho * math.pi * (diameter ** 2) * (velocity ** 3) * 0.8

    def get_velocity_at(h_reference, v_reference, h_request, h_blend=60, z_zero=0.0002, alpha=0.11):
        """
        :param h_reference: Height at which the reference velocity is measured
        :param v_reference: Wind velocity at reference height
        :param h_request: Height of the turbine hub
        :param h_blend: constant
        :param z_zero: constant
        :param alpha: constant
        :return: Get the velocity at the requested height
        """
        h_request = round(h_request, 2)  # ensure h_reference is within accuracy
        heightrange = np.arange(0, h_request + 0.01, 0.01)
        velocities = v_reference * (np.log(heightrange[heightrange <= h_blend] / z_zero) / np.log(h_reference / z_zero))
        velocities = np.append(velocities, velocities[-1] * (heightrange[heightrange > h_blend] / h_blend) ** alpha)
        return velocities[int(np.where(heightrange == h_request)[0])]

    ## -- Main running code -- ##

    turbine_objs = []
    total_power = 0

    spacing = []
    for i in range(len(request)):
        if i < len(request) - 1:
            space = request[i + 1] - request[i]
            if space <= 3 * turbine_diameter:
                error_msg = (f"A turbine was placed to close to its neighbour."
                             f"Distance of {space}m between turbine {i + 1} and turbine {i + 2} was identified"
                             f"which is below the required min. 3*diameter")
                return error_msg, 0
                # raise Exception(f"A turbine was placed to close to its neighbour."
                #                 f"Distance of {space}m between turbine {i + 1} and turbine {i + 2} was identified"
                #                 f"which is below the required min. 3*diameter")
            spacing.append(space)
        else:
            spacing.append(10 * turbine_diameter)

    print(request)
    print(spacing)

    # v_hub = 6
    # power = 14_000_000

    v_hub = get_velocity_at(h_reference, v_reference, hub_height)  # CHECK TODO
    theoretical_power = powerfirst(turbine_diameter, v_hub)  # CHECK TODO

    print(v_hub, theoretical_power, turbine_diameter)

    # add the first turbine since it will always be at the start of the turbine chain (special 1 time operations)
    turbine_objs.append(Turbine(0, turbine_diameter, v_hub, theoretical_power, v_hub))
    turbine_objs[0].printusefull()

    # add data points to plotting list
    y = np.insert(turbine_objs[0].supplyrange(0, request[0]), 0, v_hub, axis=0)
    x = np.insert(turbine_objs[0].s_range * turbine_diameter, 0, 0, axis=0)

    # Evaluation of the velocities in the wake following jensen's model of mixed velocity.
    for location, distance in zip(request, spacing):
        turbine_objs.append(
            Turbine(location, turbine_diameter, turbine_objs[-1].returnlast(), theoretical_power, v_hub))
        turbine_objs[-1].printusefull()

        intermediate = 0
        for turbine in turbine_objs:
            intermediate += (1 - turbine.supplyrange(location, location + distance) / v_hub) ** 2

        turbine_objs[-1].setuto(v_hub * (1 - np.sqrt(intermediate)))

        # add data points to plotting list
        x = np.append(x, turbine_objs[-1].location + (turbine_objs[-1].s_range * turbine_diameter))
        y = np.append(y, turbine_objs[-1].u_range)

    # Plot
    plt.plot(x, y)
    plt.show()

    for turbine in turbine_objs:
        total_power += turbine.power

    farm_efficiency = total_power / (len(turbine_objs) * theoretical_power)
    energy_yr = total_power * 365 * 24 * capacity_factor
    # print(total_power, farm_efficiency)
    return total_power, farm_efficiency, theoretical_power, energy_yr, x, y, 1

# external libraries
import numpy as np
import matplotlib.pyplot as plt

# default libraries
import math

# custom libraries
import utils.constants as constants


class Turbine:
    """
    Wind turbine class to store and calculate relevant values of the wind turbine.
    velocity values in the wake are supplied in ranges from the turbine to the next to evaluate the wake and the mixed velocities.
    """

    def __init__(self, location: float, diameter: float, localwindspeed: float, power: float):
        """
        :param location: The location of the turbine in meters [m]
        :param diameter: The diameter of the turbine used [m]
        :param localwindspeed: The local windspeed [m/s]
        :param power: The power[W] of the turbine based on the local windspeed.
        Note this is not the rated power! however it is derived from it
        """

        index = 0
        index += 1
        self.id = index

        self.location = location
        self.diameter = diameter
        self.localwindspeed = localwindspeed
        self.power = power * (localwindspeed/constants.windspeed)**3
        self.rotorspeed = (2/3)*localwindspeed
        self.thrust = self.power / self.rotorspeed
        # Thrust coefficient
        self.ct = self.thrust / (0.5*constants.rho*(localwindspeed**2)*math.pi*((diameter/2)**2))

    def supplyrange(self, first, last):
        """
        :param first: The location of the current turbine that is to be analysed
        :param last: The location of the next turbine
        :return: The velocity list for the specified range for the requested instance
        """
        self.s_range = np.linspace(first-self.location+(self.diameter * 3 + 1), last-self.location, 10000, endpoint=True) / self.diameter
        self.u_range = constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.s_range * constants.alpha) ** 2))
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
        Prints the usefull(windspeed[m/s^2], power[W], thrust[N] and thrust coeffiecient[-])
        characteristics of the Turbine(...) instance.
        """
        print(f"{self.localwindspeed=}", f"{self.power=}", f"{self.thrust=}", f"{self.ct=}")

    def __str__(self):
        return f"WindTurbine instance created with Turbine(location, diameter, localwindspeed, power)"


def powerfirst(diameter, velocity):
    """
    :param diameter: Diameter of the turbine blades
    :param velocity: Velocity at the turbine hub
    :return: Power of the first turbine based on theoretical performance * efficiency factor of 80%
    """
    return (16/27)*(1/8)*constants.rho*math.pi*(diameter**2)*(velocity**3)*0.8

def windfarm(request: list):

    turbine_objs = []
    total_power = 0

    spacing = []
    for i in range(len(request)):
        if i < len(request)-1:
            space = request[i+1]-request[i]
            if space <= 3*constants.diameter:
                raise Exception(f"A turbine was placed to close to its neighbour."
                                f"Distance of {space}m between turbine {i+1} and turbine {i+2} was identified"
                                f"which is below the required min. 3*diameter")
            spacing.append(space)
        else:
            spacing.append(10*constants.diameter)

    # add the first turbine since it will always be at the start of the turbine chain (special 1 time operations)
    turbine_objs.append(Turbine(0, constants.diameter, constants.windspeed, constants.power))
    turbine_objs[0].printusefull()

    # add data points to plotting list
    y = np.insert(turbine_objs[0].supplyrange(0, spacing[0]), 0, constants.windspeed, axis=0)
    x = np.insert(turbine_objs[0].s_range * turbine_objs[0].diameter, 0, 0, axis=0)

    # Evaluation of the velocities in the wake following jensen's model of mixed velocity.
    for location, distance in zip(request, spacing):
        turbine_objs.append(Turbine(location, constants.diameter, turbine_objs[-1].returnlast(), constants.power))
        turbine_objs[-1].printusefull()

        intermediate = 0
        for turbine in turbine_objs:
            intermediate += (1 - turbine.supplyrange(location, location + distance) / constants.windspeed) ** 2

        turbine_objs[-1].setuto(constants.windspeed * (1 - np.sqrt(intermediate)))

        # add data points to plotting list
        x = np.append(x, turbine_objs[-1].location + (turbine_objs[-1].s_range * turbine_objs[-1].diameter))
        y = np.append(y, turbine_objs[-1].u_range)

    # Plot
    plt.plot(x, y)
    plt.show()

    for turbine in turbine_objs:
        total_power += turbine.power

    farm_efficiency = total_power / (len(turbine_objs)*constants.power)

    print(total_power, farm_efficiency)


# if __name__ == "__main__":
#     request = [2000, 4000, 6000, 10000, 20000]  # requested turbine locations # 1, 1-2, 1-2-3
#     # request = [10000, 20000, 30000, 40000, 50000]
#     windfarm(request)


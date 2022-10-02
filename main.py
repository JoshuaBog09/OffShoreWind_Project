# external libaries
import numpy as np
import matplotlib.pyplot as plt

# default libaries
import math

#custom libaries
import utils.constants as constants


class Turbine:
    """
    """

    def __init__(self, location: float, diameter: float, localwindspeed: float, power: float):

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


    # def evaluatespecific(self, idx):
    #     return constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * idx * constants.alpha) ** 2))
    #
    # def evaluateupto(self, nextturbine):
    #     # nexttrubine is the distance form one turbine to the next one
    #     # distance range
    #     self.s = np.linspace((self.diameter * 3 + 1), nextturbine, 10000, endpoint=True) / self.diameter
    #     self.unext = constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.s * constants.alpha) ** 2))

    def supplyrange(self, first, last):
        self.s_range = np.linspace(first-self.location+(self.diameter * 3 + 1), last-self.location, 10000, endpoint=True) / self.diameter
        self.u_range = constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.s_range * constants.alpha) ** 2))
        return self.u_range

    def setuto(self, velocities):
        self.u_range = velocities

    def returnlast(self):
        return self.u_range[-1]

    def printusefull(self):
        print(f"{self.localwindspeed=}", f"{self.power=}", f"{self.thrust=}", f"{self.ct=}")

    def __str__(self):
        return f"WindTurbine instance created with Turbine(location, diameter, localwindspeed, power)"


class Windfarm:
    """
    """
    pass


def windfarm():

    turbine_objs = []

    request = [2000, 4000, 6000, 10000, 20000]  # requested turbine locations # 1, 1-2, 1-2-3
    spacing = []
    for i in range(len(request)):
        if i < len(request)-1:
            spacing.append(request[i+1]-request[i])
        else:
            spacing.append(2500)

    print(spacing)

    # add the first turbine since it will always be at the start of the turbine chain (special 1 time operations)
    turbine_objs.append(Turbine(0, constants.diameter, constants.windspeed, constants.power))
    turbine_objs[0].printusefull()

    y = np.insert(turbine_objs[0].supplyrange(0, 2000), 0, constants.windspeed, axis=0)
    x = np.insert(turbine_objs[0].s_range * turbine_objs[0].diameter, 0, 0, axis=0)

    plt.plot(x, y)
    plt.show()

    for location, distance in zip(request, spacing):
        turbine_objs.append(Turbine(location, constants.diameter, turbine_objs[-1].returnlast(), constants.power))
        turbine_objs[-1].printusefull()

        intermediate = 0
        for turbine in turbine_objs:
            intermediate += (1 - turbine.supplyrange(location, location + distance) / constants.windspeed) ** 2

        turbine_objs[-1].setuto(constants.windspeed * (1 - np.sqrt(intermediate)))

        x = np.append(x, turbine_objs[-1].location + (turbine_objs[-1].s_range * turbine_objs[-1].diameter))
        y = np.append(y, turbine_objs[-1].u_range)

        plt.plot(x, y)
        plt.show()


# def main():
#
#     T1 = Turbine(0,200, constants.windspeed, constants.power)
#     print(T1.localwindspeed, T1.power, T1.thrust, T1.ct)
#
#     y = np.insert(T1.supplyrange(0, 2000), 0, constants.windspeed, axis=0)
#     x = np.insert(T1.s_range*T1.diameter, 0, 0, axis=0)
#
#     plt.plot(x, y)
#     plt.show()
#
#     T2 = Turbine(2000,200,T1.returnlast(), constants.power)
#     print(T2.localwindspeed, T2.power, T2.thrust, T2.ct)
#
#     T2.setuto(constants.windspeed * (1 - np.sqrt(
#         (1 - T1.supplyrange(2000, 4000) / constants.windspeed) ** 2 + (1 - T2.supplyrange(2000,4000) / constants.windspeed) ** 2)))
#
#     x = np.append(x, T2.location+(T2.s_range*T2.diameter))
#     y = np.append(y, T2.u_range)
#
#     # write some function to do this combined wake madness (with as input a list of the participating objects)
#
#     plt.plot(x, y)
#     plt.show()
#
#     T3 = Turbine(4000, 200, T2.returnlast(), constants.power)
#     print(T3.localwindspeed, T3.power, T3.thrust, T3.ct)
#     T3.setuto(constants.windspeed * (1 - np.sqrt(
#         (1 - T1.supplyrange(4000, 6000) / constants.windspeed) ** 2 +
#         (1 - T2.supplyrange(4000, 6000) / constants.windspeed) ** 2 +
#         (1 - T3.supplyrange(4000, 6000) / constants.windspeed) ** 2)))
#
#     y = np.append(y, T3.u_range)
#     x = np.append(x, T3.location + (T3.s_range * T3.diameter))
#
#     plt.plot(x, y)
#     plt.show()
#
#     T4 = Turbine(6000, 200, T3.returnlast(), constants.power)
#     print(T4.localwindspeed, T4.power, T4.thrust, T4.ct)
#
#     # find the turbines within proximity of first turbine (upto s=13)
#     # store them in a list


if __name__ == "__main__":
    windfarm()

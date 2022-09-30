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


    def evaluatespecific(self, idx):
        return constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * idx * constants.alpha) ** 2))

    def evaluateupto(self, nextturbine):
        # nexttrubine is the distance form one turbine to the next one
        stepsize = 0.1
        # distance range
        self.s = np.arange((self.diameter * 3 + 1), nextturbine + stepsize, stepsize) / self.diameter
        self.unext = constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.s * constants.alpha) ** 2))

    def supplyrange(self, first, last):
        self.sextended = np.arange(first+(self.diameter * 3 + 1), last+0.1,0.1) / self.diameter
        self.unextextended = constants.windspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.sextended * constants.alpha) ** 2))
        return self.unextextended

    def setuto(self, velocities):
        self.unext = velocities

    def returnlast(self):
        return self.unext[-1]


class Windfarm:
    """
    """
    pass



def main():

    T1 = Turbine(0,200, constants.windspeed, constants.power)
    print(T1.localwindspeed, T1.power, T1.thrust, T1.ct)
    T1.evaluateupto(2000)

    x = np.insert(T1.s*T1.diameter, 0, 0, axis=0)
    y = np.insert(T1.unext, 0, constants.windspeed, axis=0)

    plt.plot(x, y)
    plt.show()

    T2 = Turbine(2000,200,T1.returnlast(), constants.power)
    print(T2.localwindspeed, T2.power, T2.thrust, T2.ct)
    T2.evaluateupto(2000)

    x = np.append(x, T2.location+(T2.s*T2.diameter))
    # y = np.append(y, T2.unext)
    # write some function to do this combined wake madness (with as input a list of the participating objects)
    T2.setuto(constants.windspeed*(1-np.sqrt((1-T1.supplyrange(2000,4000)/constants.windspeed)**2+(1-T2.unext/constants.windspeed)**2)))
    y = np.append(y, T2.unext)

    plt.plot(x, y)
    plt.show()

    print(T2.returnlast())

    # T3 = Turbine(4000, 200, T2.returnlast(), constants.power)
    # print(T3.power, T3.thrust, T3.ct)
    # T3.evaluateupto(2000)
    #
    # x = np.append(x, T3.location + (T3.s * T3.diameter))
    # y = np.append(y, T3.unext)
    #
    # plt.plot(x, y)
    # plt.show()

    # find the turbines within proximity of first turbine (upto s=13)
    # store them in a list


if __name__ == "__main__":
    main()

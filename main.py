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
        self.power = power
        self.rotorspeed = (2/3)*self.localwindspeed
        self.thrust = self.power / self.rotorspeed
        # Thrust coefficient
        self.ct = self.thrust / (0.5*constants.rho*(self.localwindspeed**2)*math.pi*((self.diameter/2)**2))


    def evaluatenext(self, initialwindspeed) -> None:
        # create s area from s>3 to s=13
        stepsize = 0.1
        self.s = np.arange(self.diameter * 3 + 1, self.diameter * 13, stepsize) / self.diameter
        self.unext = initialwindspeed * (1 - ((1 - math.sqrt(1 - self.ct)) / (1 + 2 * self.s * constants.alpha) ** 2))

        # return self.unext

    def specificvelocity(self, location) -> float:
        return self.unext[np.where(self.s == location)]


class Windfarm:
    """
    """
    pass



def main():

    vnot = 12

    T1 = Turbine(0,200,vnot, constants.power)
    T1.evaluatenext(vnot)

    plt.plot(T1.s, T1.unext)
    plt.show()

    # T2 = Turbine(2000,200,T1.specificvelocity(2000), constants.power)

    # find the turbines within proximity of first turbine (upto s=13)
    # store them in a list


if __name__ == "__main__":
    main()

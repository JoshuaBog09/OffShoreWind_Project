import utils.constants as constants


class Turbine:
    """
    """
    def __init__(self, location, diameter, localwindspeed, power):
        self.location = location
        self.diameter = diameter
        self.localwindspeed = localwindspeed
        self.power = power
        self.rotorspeed = (2/3)*self.localwindspeed
        self.thrust = self.power / self.rotorspeed
        self.ct = self.thrust / (0.5*constants.rho*(localwindspeed**2)*2*(self.diameter/2)**2)

class Windfarm:
    """
    """
    pass



def main():
    T1 = Turbine(0,200,5.14, constants.power)
    print(T1.thrust)

if __name__ == "__main__":
    main()

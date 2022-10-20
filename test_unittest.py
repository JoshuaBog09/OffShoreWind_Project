import unittest
from windFarm import windfarm


class MyTestCase(unittest.TestCase):
    def test_1(self):
        self.assertEqual(windfarm(200,150,9,10,[2000, 4000, 6000, 10000, 20000], 0.35)[:3],
                         (68248164.83530974, 0.798253398927191, 14249477.865681821))

    def test_2(self):
        self.assertEqual(windfarm(200,150,5,10,[2000, 4000, 6000, 10000, 20000], 0.35)[:3],
                         (11702360.225533228, 0.7982533989271912, 2443326.1086560064))


if __name__ == '__main__':
    unittest.main()
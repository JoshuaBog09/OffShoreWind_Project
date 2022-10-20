# OffShoreWind_Project
OffshoreWind energy project (TuDelft)

## Getting started
First clone the repository using: <br>
``git clone https://github.com/JoshuaBog09/OffShoreWind_Project.git`` (bash)<br>
or ``gh repo clone JoshuaBog09/OffShoreWind_Project`` (GitHub CLI) and then start up a clean virtual environment of your choice(python 3.9 should be used). Afterwards install the following dependencies using pip.<br>
```
pip install matplotlib
pip install numpy
pip install pyqt5
pip install pyqt5-tools
pip install requests
```


___
## Progress and task devsion
| Task                   | Done by           | Current status  | Checked            | Completed          | 
|------------------------|-------------------|-----------------|--------------------|--------------------|
| GUI                    | Joshua and Roel   | Near completion |                    |                    |
| Wake effect model      | Joshua            | Completed       | :heavy_check_mark: | :heavy_check_mark: |
| Velocity profile model | Joshua and Wessel | Completed       | :heavy_check_mark: | :heavy_check_mark: |
| Poster                 | Wessel and Mees   |                 |                    |                    |
| ...                    |                   |                 |                    |                    |
___

## Documentation
1. Insert the reference velocity in meters per second. Generally this is around the 10 m/s on sea.
2. Insert the reference height in meters. This is the height at which the reference velocity is measured. Generally this 
is at 10 meters above the ground.
3. Insert the capacity factor of the farm site. This factor is dimensionless and describes how much the wind turbine 
produces energy at rated power equivalent. For North Sea conditions this factor is around 0.45 [-].
4. Insert the hub height in meters. The hub is where the rotor is connected to the tower. Generally this is 100 to 150 
meters.
5. Insert the rotor diameter in meters. This is generally around 200 meters.
6. Insert the turbine placement in the row of wind turbines. This needs to be at least 3 rotor diameters away from the 
previous wind turbine. The first turbine is by definition placed at 0 meters and should not be implemented in the 
list. 
<br><br>
As output you get the power of the first turbine in line. This is interesting since this turbine the highest power of 
all the turbines in the array. This power is obtained by using the velocity of the wind at the hub height and the wind 
turbine characteristics. The wind velocity at hub height is obtained by using the log-law with a surface roughness of 
0.0002 and the power-law with an exponent of 0.11. These two laws describe the velocity profile below and above 60 
meters (called the blending height) respectively.
<br>The second output is the total farm power. This is not a multiple of the number of 
turbines in the row since wake effects modeled by the Jensen model affect the wind energy at the other turbines. This 
model uses the extraction of momentum of the wind. This results in a wake expansion with a factor of 0.05. 
<br>The third output is efficiency of the array with respect the that of the array without wake effects. This is as if 
there are only power yields equal to the one of the first wind turbine. 
The last output is energy yield over one year in MWh.
---
## Sources
[1] TU Delft, Lecture 4: Windfarms, 2022<br>
[2] TU Delft, Lecture 2: WindWaveResource, 2022<br>

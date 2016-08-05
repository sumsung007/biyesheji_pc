# biyesheji_pc
the  project of bachelor graduate

this is a the sun follow system that the function like the plant of  turnsole,and we can use this demo to advance productiveness of  sun-power system

此系统主要完成的功能是:能够跟随太阳的转到，让整个系统也随之转动，上位机利用C#端所处地区的经纬度，天气等情况，转换成相应的控制信息，通过ZigBee网络传到RaspberryPI系统上，RaspberryPI再根据指令，将控制信息转换成相应的信号脉冲来控制步进电机的转动，另外值得注意的是，我们在RaspberryPI上加装了GY-271电子指南针模块，以配合算法来调整随动系统的转动方式。

美国国家海洋和大气管理局提供的经纬度计算太阳高度角和方位角的算法以及Allidylls/sopo的算法支持,为我提供设计思路


This system is mainly to complete the function : the ability to follow the sun , that will turn the sunlight follow system , the host computer using C# to get the locations, latitude and longitude , the weather , etc., into the corresponding control information transmitted via the ZigBee network on RaspberryPI system , RaspberryPI again according to the instructions , the control information is converted into a corresponding pulse signal to control the rotation of the stepping motor is also worth noting that we have added a GY-271 electronic compass modules on RaspberryPI , to match algorithm rotatably adjust servo system .


specia thanks the NOAA（http://www.noaa.gov/web.html ）that latitude and longitude provided by the solar elevation and azimuth computing algorithms and algorithms supporter Allidylls/sopo

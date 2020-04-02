# robot-drone-collaboration
An inter-machine cooperation project using Python and C.

## Objective
The goal of this project was to have two autonomous vehicles - a land
based robot and an air based drone - cooperate together autonomously
to complete a task. The decided upon task was garbage collection.

## Approach
While we had decided on garbage collection for our specific project,
we wanted to create a system that could be generalized to any type of
autonomous collection. The proposed idea was to have a drone fly above
a given area, use video streaming to find whatever it is that needs to
be collected using image processing and a neural network trained to detect
the desired object(s), and then send commands to our land based robot to
collect it. 

By separating the concerns in this way, the system can easily be adapted
to different scenarios. One example of a simple adaptation could be cleaning
up oil spills on the ocean. The land based robot could be swapped for an
amphibious vehicle and a neural network for detecting oil on top of the
water could be used.

## Hardware
* DJI Phantom 4
* Land robot:
    * Chassis consisting of tracks, servo motors, and breadboard
    * Accelerometers
    * Raspberry Pi 4
    * PiCamera v2
* Laptop

# Flight Systems Starter Project 2025-2026

Hello to prospective members! Follow this readme to learn more about PX4/QGroundControl, flight simulation, and git version control.

**Remember to always ask any questions you may have, and any issue(s) you encounter talk to Andy or Ben for help.**

## Initial Setup

Before you start this project, please follow the [flight systems setup](https://docs.google.com/document/d/1uoVtI-ufLhJ_x0U6aoHlUNn7B5Cyv6jdNhsmGjJOGJo/edit?usp=sharing).
We want to make sure your computer is setup properly to handle everything that is needed for our plane! **Again, if there any issues with setup, please let a lead know and we can help!**

## Setting up the simulation

- PX4 and Gazebo
   > This should be covered in the setup document (the PX4 document). However, the steps will also be reiterated here.
   1. Clone PX4 and Setup Environment
      ```
      git clone https://github.com/PX4/PX4-Autopilot.git --recursive
      cd PX4-Autopilot
      bash ./Tools/setup/ubuntu.sh   # Install dependencies
      '''
   2. Run SITL
      **Windows**
      ```
      sudo apt remove gz-harmonic
      sudo apt install aptitude
      sudo aptitude install gazebo libgazebo11 libgazebo-dev
      export LI5BGL_ALWAYS_SOFTWARE=1
      make px4_sitl gazebo-classic_standard_vtol
      ```
      **MacOS**
      ```
      sudo apt install ignition-fortress
      make px4_sitl gz_standard_vtol
      ```
- QGroundControl
  Start your QGroundControl by opening the application.
  
  **WSL to Windows**
  
  If you are running PX4 on WSL, and QGC on Windows, you will need to make sure mavlink is set up to broadcast, as they are technically on different IPs.
  ``` 
  Open PX4-Autopilot/ROMFS/px4fmu_common/init.d-posix/px4-rc.mavlink
  ```
  Scroll a little, you should see
  ```
  # GCS link
  mavlink start -x -u $udp_gcs_port_local -r 4000000 -f
  ```
  Add a “-p” at the end of that line, so it looks like this:
  ```
  # GCS link
  mavlink start -x -u $udp_gcs_port_local -r 4000000 -f -p
  ```
  It should automatically connect to PX4 SITL via UDP (udp://14550)

  **MacOS**
  
  Please contact Andy for help in running QGroundControl on Mac. Everything we do for this plane sucks on Mac. :neutral_face:

## Running the code





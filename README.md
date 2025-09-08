# Flight Systems Starter Project 2025-2026

Hello to prospective members! Follow this readme to learn more about PX4/QGroundControl, flight simulation, and git version control.

**Remember to always ask any questions you may have, and any issue(s) you encounter talk to Andy or Ben for help.**

## Initial Setup

Before you start this project, please follow the [flight systems setup](https://docs.google.com/document/d/1uoVtI-ufLhJ_x0U6aoHlUNn7B5Cyv6jdNhsmGjJOGJo/edit?usp=sharing).
We want to make sure your computer is setup properly to handle everything that is needed for our plane! **Again, if there any issues with setup, please let a lead know and we can help!**

## Git Version Control

1. Clone the repository
   ```
   git clone https://github.com/M-Fly-Aero-Design/fs-starter-project-2526.git
   cd flight-systems-starter
   ```

2. Create your own branch
   Name your branch after your uniqname.
   ```
   git checkout -b <your-uniqname>
   ```

3. Make your changes (By following the TODO below this readme.)
   Complete the TODO in ops.py by adding your home location and 4 nearby waypoints.

4. Commit your changes
   ```
   git add ops.py
   git commit -m "Added waypoints for <your-uniqname>"
   ```

5. Push your branch
   ```
   git push origin <your-uniqname>
   ```

6. Create a Pull Request (PR)

   Go to the GitHub repository in your browser. You should see a prompt to create a PR for your new branch. Title your PR: "Waypoints - <your-uniqname>" 
   and submit your PR for review.

## Setting up the simulation

- PX4 and Gazebo
   > This should be covered in the setup document (the PX4 document). However, the steps will also be reiterated here.
   1. Clone PX4 and Setup Environment
      ```
      git clone https://github.com/PX4/PX4-Autopilot.git --recursive
      cd PX4-Autopilot
      bash ./Tools/setup/ubuntu.sh   # Install dependencies
      ```
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

## Running a simulation

   In ops.py, go ahead and review the code. The code in ops.py essentially uploads our mission (in this case, fly to waypoints) to the Mavlink system. From there, it is communicated to QGroundControl where we can see the simulation. If you have any questions or comments about the code feel free to discuss with the leads.

   **TODO**
   
   In ops.py, find where the waypoints are initialized. Afterwards, change the waypoints to include your home location (not in Ann Arbor) and add 4 more waypoints near you home location. Save the file, and then run the mission.

   After your mission is completed, save the mission as a file. Navigate to Plan -> 
   

   

   



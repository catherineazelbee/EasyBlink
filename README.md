# EasyBlink
 Respository for EasyBlink Maya Plugin by Catherine Azelby

A plugin designed to quickly animate blinks on different character rigs. Can create three different kinds of blinks (simple, fast, slow). Additional eyebrow and pupil animation can be added to compliment the blinks. Inputs can be saved and loaded to efficiently use the plugin on multiple rigs at a time. Designed in concept for time-efficient animation productions such as televison CG. 

Please note this plugin is not guarenteed to work for all rigs.

# Setup Demo Video

// INSERT MP4 DEMO HERE

# How to Use
1. Download the code and move the **easyBlink.py** file to your scripts folder (likely "..maya/202x/scripts/). Load the script in the script editor in Maya (Windows -> General Editor -> Script Editor). Go to File -> Open script and open the easyBlink.py file and run it (Ctrl + Enter). The EasyBlink plugin window will open.
  
2. Ensure your selected rig has the correct setup. There should be a control for the blink (whatever moves the eyelid down). If controls are seperate, they should both follow the same translations. Set the proper controls for the left and right eyelid by clicking the button when the corresponding control is selected. The name of the selected control will appear next to the button.

3. Set the left and right eye attribute by typing in its exact name. Attributes like "Translate Y" must be input as "translateY". To find the exact name of an attribute, you can set a test key frame on it and see its exact name in the script editor.

4. Set the open, closed, and wide values.
   - The **open value** should be the open eye in its resting state
   - The **closed value** should be the eyes fully closed
   - The **wide value** should be slightly more open than the resting open state

6. For the eyebrows, set  



# Credit
Character rigs used in demo videos:
- Deadpool by Kiel Figgins
- Link by
- The Waitress by 

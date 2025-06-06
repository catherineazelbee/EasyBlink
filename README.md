# EasyBlink
Repository for EasyBlink Maya Plugin by Catherine Azelby

A plugin designed to quickly animate blinks on different character rigs. Can create three different kinds of blinks (simple, fast, slow). Additional eyebrow and pupil animation can be added to complement the blinks. Inputs can be saved and loaded to efficiently use the plugin on multiple rigs at a time. Designed in concept for time-efficient animation productions such as television CG. 

![easyBlink_thumbnail](https://github.com/user-attachments/assets/7a04d632-aade-4955-accb-656646b5bfc1)

Please note that this plugin is not guaranteed to work for all rigs.

# Setup Demo Video
[![Watch the video]([thumbnail-image.png)](https://vimeo.com/YOUR_VIDEO_ID](https://vimeo.com/1079586853/fc75f06453?share=copy))

# How to Use
1. Download the code and move the **easyBlink.py** file to your scripts folder (likely "..maya/202x/scripts/). Load the script in the script editor in Maya (Windows -> General Editor -> Script Editor). Go to File -> Open script and open the easyBlink.py file, and run it (Ctrl + Enter). The EasyBlink plugin window will open. Works with Maya 2024 and 2025.
  
2. Ensure your selected rig has the correct setup. There should be a control for the blink (whatever moves the eyelid down). If controls are separate, they should both follow the same translations. Set the proper controls for the left and right eyelid by clicking the button when the corresponding control is selected. The name of the selected control will appear next to the button.

3. Set the left and right eye attributes by typing in their exact name.
   - Attributes like "Translate Y" must be input as "translateY". To find the exact name of an attribute, you can set a test key frame on it and see its exact name in the script editor.

5. Set the open, closed, and wide numerical values.
   - The **open value** should be the open eye in its resting state
   - The **closed value** should be the eyes fully closed
   - The **wide value** should be slightly more open than the resting open state
  
6. Click the "Save Blink Controls" button.

7. **Optional Eyebrows and Pupils:** To add complementary animation to the eyebrows and pupils during the blink animation, set 
   - The plugin will still work without setting these values

8. After saving all desired attributes, you can set one of the three blink animations. The blinks will be set where the cursor is placed in the timeline.

# Additional Features

- **Reset All To Defaults:** Clears all inputted values back to their base state as empty. 
 
- **Save Setups:** Allows the user to save plugin inputs and name them, allowing them to be loaded later. A separate window will pop up where you can view your stored setups. You can save a maximum of 6 setups.

# Release Log
04/30/25
- First Released Version

# Tested Platforms
- Maya 2025
- Maya 2024

# Credit
Character rigs used in demo video:
- Deadpool by Kiel Figgins
- Link by Christoph Schoch
- The Waitress by François Boquet and Santiago Calle

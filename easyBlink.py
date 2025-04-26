import maya.cmds as mc

# Global dictionary for storing selections and blink values.
easyblink_data = {
    'left_eye': None,
    'right_eye': None,
    'left_attr': 'BlinkAttribute',
    'right_attr': 'BlinkAttribute',
    'open': 0.1,
    'closed': 1.0,
    'wide': 0,
    'left_brow': None,
    'right_brow': None,
    'brow_attr': 'translateY',
    'left_pupil': None,
    'right_pupil': None,
    'pupil_attr': 'translateY'
}

easyblink_setups = {}

def set_control(control_name, label_name, label_prefix):
    """
    Generic setter for scene controls.
    """
    sel = mc.ls(sl=True)
    if not sel:
        mc.warning(f"No object selected for {label_prefix}!")
        return
    easyblink_data[control_name] = sel[0]
    mc.text(label_name, e=True, label=f"{label_prefix}: {sel[0]}")
    mc.inViewMessage(amg=f"{label_prefix} set: {sel[0]}", pos='topCenter', fade=True)

def set_left_eye(*args):   set_control('left_eye',   "leftEyeLabel",   "Left Eye")
def set_right_eye(*args):  set_control('right_eye',  "rightEyeLabel",  "Right Eye")
def set_left_brow(*args):  set_control('left_brow',  "leftBrowLabel",  "Left Brow")
def set_right_brow(*args): set_control('right_brow', "rightBrowLabel", "Right Brow")
def set_left_pupil(*args): set_control('left_pupil', "leftPupilLabel", "Left Pupil")
def set_right_pupil(*args):set_control('right_pupil',"rightPupilLabel","Right Pupil")


def normalize_attr_name(attr):
    """
    Normalize common attribute names.
    """
    attr = attr.strip().replace(" ", "")
    aliases = {
        "translatey":"translateY","translatex":"translateX","translatez":"translateZ",
        "rotatex":"rotateX","rotatey":"rotateY","rotatez":"rotateZ",
        "scalex":"scaleX","scaley":"scaleY","scalez":"scaleZ"
    }
    return aliases.get(attr.lower(), attr)
 
def save_blink_controls(*args):
    """
    Save blink attributes & values.
    """
    l_attr = mc.textField("leftBlinkAttrField",  q=True, text=True)
    r_attr = mc.textField("rightBlinkAttrField", q=True, text=True)
    if not l_attr or not r_attr:
        mc.warning("Blink attributes cannot be empty.")
        return
    easyblink_data['left_attr']  = normalize_attr_name(l_attr)
    easyblink_data['right_attr'] = normalize_attr_name(r_attr)
    easyblink_data['open']   = mc.floatField("openField",   q=True, value=True)
    easyblink_data['closed'] = mc.floatField("closedField", q=True, value=True)
    easyblink_data['wide']   = mc.floatField("wideField",   q=True, value=True)
    mc.inViewMessage(amg="Blink controls saved!", pos='topCenter', fade=True)


def save_extra_controls(*args):
    """
    Save extra attributes for brows and pupils.
    """
    easyblink_data['brow_attr']   = normalize_attr_name(mc.textField("browAttrField",   q=True, text=True))
    easyblink_data['pupil_attr']  = normalize_attr_name(mc.textField("pupilAttrField", q=True, text=True))
    mc.inViewMessage(amg="Eyebrow & pupil attributes saved!", pos='topCenter', fade=True)
 
def clear_all_inputs(*args):
    """
    Reset all inputs to defaults.
    """
    for k in easyblink_data:
        if isinstance(easyblink_data[k], str):
            if "_attr" in k:
                easyblink_data[k] = 'Blink' if 'eye' in k else 'translateY'
            else:
                easyblink_data[k] = None
        elif isinstance(easyblink_data[k], (int, float)):
            easyblink_data[k] = 0.1 if k=='open' else (1.0 if k=='closed' else 0)
    # reset UI
    for lbl in ["leftEyeLabel","rightEyeLabel","leftBrowLabel","rightBrowLabel","leftPupilLabel","rightPupilLabel"]:
        mc.text(lbl, e=True, label=lbl.replace("Label","").replace("left","Left ").replace("right","Right ")+": Not Set")
    mc.textField("leftBlinkAttrField",  e=True, text="Blink")
    mc.textField("rightBlinkAttrField", e=True, text="Blink")
    mc.floatField("openField",   e=True, value=0.1)
    mc.floatField("closedField", e=True, value=1.0)
    mc.floatField("wideField",   e=True, value=0.0)
    mc.textField("browAttrField",  e=True, text="translateY")
    mc.textField("pupilAttrField", e=True, text="translateY")
    mc.inViewMessage(amg="All inputs reset.", pos='topCenter', fade=True)

# Animate blink with optional brows & pupils
def set_simple_blink(*args):
    """
    Creates a default simple blink animation.
    """
    if not all([easyblink_data['left_eye'], easyblink_data['right_eye'],
                easyblink_data['left_attr'], easyblink_data['right_attr']]):
        mc.warning("Please set eyes and blink controls first!")
        return
    t = mc.currentTime(q=True)
    ov, cv, wv = easyblink_data['open'], easyblink_data['closed'], easyblink_data['wide']
    # eyes
    for side in ['left_eye','right_eye']:
        ctrl = easyblink_data[side]
        attr = easyblink_data['left_attr']  if side=='left_eye'  else easyblink_data['right_attr']
        mc.setKeyframe(ctrl, attribute=attr, t=t,   value=ov)
        mc.setKeyframe(ctrl, attribute=attr, t=t+3, value=cv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+5, value=wv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+8, value=ov)
    # brows
    for side in ['left_brow','right_brow']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['brow_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+2, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+5, value=orig)
    # pupils
    for side in ['left_pupil','right_pupil']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['pupil_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+2, value=orig-0.05)
            mc.setKeyframe(ctrl, attribute=attr, t=t+7, value=orig)
    mc.inViewMessage(amg="Simple Blink Set!", pos='topCenter', fade=True)
    
# Animate slow blink
def set_slow_blink(*args):
    """
    Creates a slow blink animation.
    """
    if not all([easyblink_data['left_eye'], easyblink_data['right_eye'],
                easyblink_data['left_attr'], easyblink_data['right_attr']]):
        mc.warning("Please set eyes and blink controls first!")
        return
    t = mc.currentTime(q=True)
    ov, cv, wv = easyblink_data['open'], easyblink_data['closed'], easyblink_data['wide']
    # eyes
    for side in ['left_eye','right_eye']:
        ctrl = easyblink_data[side]
        attr = easyblink_data['left_attr']  if side=='left_eye'  else easyblink_data['right_attr']
        mc.setKeyframe(ctrl, attribute=attr, t=t,   value=ov)
        mc.setKeyframe(ctrl, attribute=attr, t=t+4, value=cv-0.05)
        mc.setKeyframe(ctrl, attribute=attr, t=t+6, value=cv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+10, value=wv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+14, value=ov)
    # brows
    for side in ['left_brow','right_brow']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['brow_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+3, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+5, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+13, value=orig)
    # pupils
    for side in ['left_pupil','right_pupil']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['pupil_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+3, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+13, value=orig)
    mc.inViewMessage(amg="Slow Blink Set!", pos='topCenter', fade=True)
    
# Animate fast blink
def set_fast_blink(*args):
    """
    Creates a fast blink animation.
    """
    if not all([easyblink_data['left_eye'], easyblink_data['right_eye'],
                easyblink_data['left_attr'], easyblink_data['right_attr']]):
        mc.warning("Please set eyes and blink controls first!")
        return
    t = mc.currentTime(q=True)
    ov, cv, wv = easyblink_data['open'], easyblink_data['closed'], easyblink_data['wide']
    # eyes
    for side in ['left_eye','right_eye']:
        ctrl = easyblink_data[side]
        attr = easyblink_data['left_attr']  if side=='left_eye'  else easyblink_data['right_attr']
        mc.setKeyframe(ctrl, attribute=attr, t=t,   value=ov)
        mc.setKeyframe(ctrl, attribute=attr, t=t+2, value=cv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+4, value=wv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+6, value=ov)
    # brows
    for side in ['left_brow','right_brow']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['brow_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+1, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+6, value=orig)
    # pupils
    for side in ['left_pupil','right_pupil']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['pupil_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+1, value=orig-0.05)
            mc.setKeyframe(ctrl, attribute=attr, t=t+6, value=orig)
    mc.inViewMessage(amg="Fast Blink Set!", pos='topCenter', fade=True)

# Help Button 
def helpButton(text):
    """
    Create a small question-mark button that shows helpful information to the user.
    """
    return mc.iconTextButton(
        style='textOnly',
        label='?',
        width=18, height=18,
        annotation=text,
        backgroundColor=(0.75, 0.75, 0.75),
    )


# Prompt window to save setup
def open_save_setup_ui(*args):
    if mc.window("saveSetupWin", exists=True):
        mc.deleteUI("saveSetupWin")
    win = mc.window("saveSetupWin", title="Save EasyBlink Setup", widthHeight=(250, 80))
    mc.columnLayout(adjustableColumn=True, rowSpacing=5)
    mc.text(label="Enter a name for this setup:\n You can save a maximum of 6.")
    mc.textField("setupNameField")
    mc.rowLayout(numberOfColumns=2, columnWidth2=(120,120), columnAlign2=("center","center"))
    mc.button(label="Save", command=save_setup)
    mc.button(label="Cancel", command=lambda *a: mc.deleteUI(win, window=True))
    mc.showWindow(win)
    
# Save setup    
def save_setup(*args):
    name = mc.textField("setupNameField", q=True, text=True).strip()
    mc.deleteUI("saveSetupWin", window=True)
    if not name:
        mc.warning("Name cannot be empty.")
        return
    if name in easyblink_setups:
        mc.warning("That name already exists.")
        return
    if len(easyblink_setups) >= 6:
        mc.warning("Max 6 setups reached.")
        return

    # deep‐copy just the fields you need
    easyblink_setups[name] = {
        'left_eye': easyblink_data['left_eye'],
        'right_eye': easyblink_data['right_eye'],
        'left_attr': easyblink_data['left_attr'],
        'right_attr': easyblink_data['right_attr'],
        'open': easyblink_data['open'],
        'closed': easyblink_data['closed'],
        'wide': easyblink_data['wide'],
        'left_brow': easyblink_data['left_brow'],
        'right_brow': easyblink_data['right_brow'],
        'brow_attr': easyblink_data['brow_attr'],
        'left_pupil': easyblink_data['left_pupil'],
        'right_pupil': easyblink_data['right_pupil'],
        'pupil_attr': easyblink_data['pupil_attr']
    }

    mc.inViewMessage(amg=f"Setup '{name}' saved!", pos='topCenter', fade=True)
    # show the saved setups window automatically
    refresh_saved_setups_ui()
    
# Load or delete setups
def load_setup(name):
    data = easyblink_setups[name]
    easyblink_data.update(data)
    mc.text("leftEyeLabel",  e=True, label="Left Eye: "+str(data['left_eye']))
    mc.text("rightEyeLabel", e=True, label="Right Eye: "+str(data['right_eye']))
    mc.textField("leftBlinkAttrField",  e=True, text=data['left_attr'])
    mc.textField("rightBlinkAttrField", e=True, text=data['right_attr'])
    mc.floatField("openField",   e=True, value=data['open'])
    mc.floatField("closedField", e=True, value=data['closed'])
    mc.floatField("wideField",   e=True, value=data['wide'])
    mc.text("leftBrowLabel",  e=True, label="Left Brow: "+str(data['left_brow']))
    mc.text("rightBrowLabel", e=True, label="Right Brow: "+str(data['right_brow']))
    mc.textField("browAttrField",  e=True, text=data['brow_attr'])
    mc.text("leftPupilLabel",  e=True, label="Left Pupil: "+str(data['left_pupil']))
    mc.text("rightPupilLabel", e=True, label="Right Pupil: "+str(data['right_pupil']))
    mc.textField("pupilAttrField", e=True, text=data['pupil_attr'])
    mc.inViewMessage(amg=f"Loaded setup: {name}", pos='topCenter', fade=True)

def delete_setup(name):
    del easyblink_setups[name]
    refresh_saved_setups_ui()

# Saved Setups Window
def refresh_saved_setups_ui(*args):
    # delete any old floating window
    if mc.window("savedSetupsWin", exists=True):
        mc.deleteUI("savedSetupsWin")
    
    # build a fresh floating window
    win = mc.window(
        "savedSetupsWin",
        title="EasyBlink – Saved Setups",
        widthHeight=(300, 200),
        sizeable=True
    )
    mc.columnLayout(adjustableColumn=True, rowSpacing=5)
    for name in easyblink_setups:
        mc.rowLayout(numberOfColumns=3, columnWidth3=(150, 70, 60))
        mc.text(label=name, align="left")
        mc.button(label="Load",   command=lambda _,n=name: load_setup(n))
        mc.button(label="Delete", command=lambda _,n=name: delete_setup(n))
        mc.setParent("..")
    mc.showWindow(win)

# Build the UI
def create_easyblink_ui():
    if mc.workspaceControl("EasyBlinkWC", q=True, exists=True):
        mc.deleteUI("EasyBlinkWC", control=True)

    # docked workspace setup
    wc = mc.workspaceControl(
        "EasyBlinkWC",
        label="EasyBlink",
        dockToMainWindow=("right", 1),
        initialWidth=360,
        initialHeight=740,
        retain=False
    )

    # create a scrollLayout under the workspaceControl
    scroll = mc.scrollLayout(
        "easyBlinkScroll", 
        parent=wc, 
        childResizable=True, 
        horizontalScrollBarThickness=0, 
        verticalScrollBarThickness=16
    )
    mc.columnLayout(
        "easyBlinkCol", 
        parent=scroll, 
        adjustableColumn=True, 
        rowSpacing=10, 
        columnAlign="center"
    )

    # Eye controls
    mc.separator(style='in')
    mc.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign=(1, "left"), columnAttach=[(1, 'left', 0), (2, 'right', 0)])
    mc.text(label="👁️ Blink Controls", font="boldLabelFont", align="left")
    helpButton(
        "Select your left & right eye rig controls, then choose their blink\n"
        "attribute name. Then set your open/closed/wide values. Make sure\n"
        "names match exactly what Maya shows in the script editor. You can\n"
        "place a keyframe to see the exact name in script editor."
    )
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Left Eye",  command=set_left_eye, backgroundColor = (0.78, 0.75, 0.85))
    mc.text("leftEyeLabel",  label="Left Eye: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Right Eye", command=set_right_eye, backgroundColor = (0.78, 0.75, 0.85))
    mc.text("rightEyeLabel", label="Right Eye: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("leftBlinkAttrField",  text="Blink")
    mc.text(label="← Left Eye Attribute")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("rightBlinkAttrField", text="Blink")
    mc.text(label="← Right Eye Attribute")
    mc.setParent("..")
    mc.rowColumnLayout(numberOfColumns=2)
    mc.text(label="Open Value:")
    mc.floatField("openField", value=easyblink_data['open'])
    mc.text(label="Closed Value:")
    mc.floatField("closedField", value=easyblink_data['closed'])
    mc.text(label="Wide Value:")
    mc.floatField("wideField", value=easyblink_data['wide'])
    mc.setParent("..")
    mc.button(label="Save Blink Controls", command=save_blink_controls, backgroundColor = (0.65, 0.75, 0.65))

    # Eyebrow controls
    mc.separator(style='in')
    mc.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign=(1, "left"), columnAttach=[(1, 'left', 0), (2, 'right', 0)])
    mc.text(label="🥸 Brow Controls", font="boldLabelFont", align="left")
    helpButton("Select your left & right brow controls and set the attribute name exactly as it appears in script editor.")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Left Brow",  command=set_left_brow, backgroundColor = (0.78, 0.75, 0.85))
    mc.text("leftBrowLabel",  label="Left Brow: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Right Brow", command=set_right_brow, backgroundColor = (0.78, 0.75, 0.85))
    mc.text("rightBrowLabel", label="Right Brow: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("browAttrField", text=easyblink_data['brow_attr'])
    mc.text(label="← Brow Attribute")
    mc.setParent("..")
    mc.button(label="Save Brow Controls", command=save_extra_controls, backgroundColor = (0.65, 0.75, 0.65))

    # Pupil controls
    mc.separator(style='in')
    mc.rowLayout(numberOfColumns=2, adjustableColumn=1, columnAlign=(1, "left"), columnAttach=[(1, 'left', 0), (2, 'right', 0)])
    mc.text(label="👀 Pupil Controls", font="boldLabelFont", align="left")
    helpButton("Select your left & right pupil controls and set the attribute name exactly as it appears in script editor.")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Left Pupil",  command=set_left_pupil, backgroundColor = (0.78, 0.75, 0.85))
    mc.text("leftPupilLabel",  label="Left Pupil: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Right Pupil", command=set_right_pupil, backgroundColor = (0.78, 0.75, 0.85))
    mc.text("rightPupilLabel", label="Right Pupil: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("pupilAttrField", text=easyblink_data['pupil_attr'])
    mc.text(label="← Pupil Attribute")
    mc.setParent("..")
    mc.button(label="Save Pupil Controls", command=save_extra_controls, backgroundColor = (0.65, 0.75, 0.65))

    # Animate
    mc.separator(style='in')
    mc.text(label="⚡ Animate", font="boldLabelFont")
    mc.button(label="Set Simple Blink", command=set_simple_blink, height=40, backgroundColor = (0.88, 0.78, 0.68))
    mc.button(label="Set Slow Blink", command=set_slow_blink, height=40, backgroundColor = (0.88, 0.78, 0.68))
    mc.button(label="Set Fast Blink", command=set_fast_blink, height=40, backgroundColor = (0.88, 0.78, 0.68))
    
    # Reset
    mc.separator(style='in')
    mc.text(label="🧹 Reset", font="boldLabelFont")
    mc.button(label="Reset All to Defaults", command=clear_all_inputs, height=30, backgroundColor = (0.78, 0.75, 0.85))
    
    # Save inputs
    mc.separator(style='in')
    mc.text(label="💾 Save Inputs", font="boldLabelFont")
    mc.button(label="Save Setup…", command=open_save_setup_ui, height=30, backgroundColor = (0.65, 0.75, 0.65))
    mc.button(label="View Saved Setups", command=refresh_saved_setups_ui, height=30, backgroundColor = (0.78, 0.75, 0.85))

# Launch UI
create_easyblink_ui()


import maya.cmds as mc

# Global dictionary for storing selections and blink values.
easyblink_data = {
    'left_eye': None,
    'right_eye': None,
    'left_attr': 'Blink',
    'right_attr': 'Blink',
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

# Generic setter for scene controls
def set_control(control_name, label_name, label_prefix):
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

# Normalize common attribute names
def normalize_attr_name(attr):
    attr = attr.strip().replace(" ", "")
    aliases = {
        "translatey":"translateY","translatex":"translateX","translatez":"translateZ",
        "rotatex":"rotateX","rotatey":"rotateY","rotatez":"rotateZ",
        "scalex":"scaleX","scaley":"scaleY","scalez":"scaleZ"
    }
    return aliases.get(attr.lower(), attr)

# Save blink attributes & values
def save_blink_controls(*args):
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

# Save extra attributes for brows and pupils
def save_extra_controls(*args):
    easyblink_data['brow_attr']   = normalize_attr_name(mc.textField("browAttrField",   q=True, text=True))
    easyblink_data['pupil_attr']  = normalize_attr_name(mc.textField("pupilAttrField", q=True, text=True))
    mc.inViewMessage(amg="Eyebrow & pupil attributes saved!", pos='topCenter', fade=True)

# Reset all inputs to defaults
def clear_all_inputs(*args):
    # reset data
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
            mc.setKeyframe(ctrl, attribute=attr, t=t+3, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+8, value=orig)
    # pupils
    for side in ['left_pupil','right_pupil']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['pupil_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+1, value=orig-0.05)
            mc.setKeyframe(ctrl, attribute=attr, t=t+8, value=orig)
    mc.inViewMessage(amg="Blink animated!", pos='topCenter', fade=True)
    
# Animate slow blink
def set_slow_blink(*args):
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
        mc.setKeyframe(ctrl, attribute=attr, t=t+4, value=cv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+5, value=cv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+7, value=wv)
        mc.setKeyframe(ctrl, attribute=attr, t=t+10, value=ov)
    # brows
    for side in ['left_brow','right_brow']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['brow_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+4, value=orig-0.1)
            mc.setKeyframe(ctrl, attribute=attr, t=t+10, value=orig)
    # pupils
    for side in ['left_pupil','right_pupil']:
        ctrl = easyblink_data[side]
        if ctrl:
            attr = easyblink_data['pupil_attr']
            orig = mc.getAttr(f"{ctrl}.{attr}")
            mc.setKeyframe(ctrl, attribute=attr, t=t,   value=orig)
            mc.setKeyframe(ctrl, attribute=attr, t=t+2, value=orig-0.05)
            mc.setKeyframe(ctrl, attribute=attr, t=t+9, value=orig)
    mc.inViewMessage(amg="Blink animated!", pos='topCenter', fade=True)
    
# Prompt window to save setup
def open_save_setup_ui(*args):
    if mc.window("saveSetupWin", exists=True):
        mc.deleteUI("saveSetupWin")
    win = mc.window("saveSetupWin", title="Save EasyBlink Setup", widthHeight=(250, 80))
    mc.columnLayout(adjustableColumn=True, rowSpacing=5)
    mc.text(label="Enter a name for this setup (max 6):")
    mc.textField("setupNameField")
    mc.rowLayout(numberOfColumns=2, columnWidth2=(120,120), columnAlign2=("center","center"))
    mc.button(label="Save", command=save_setup)
    mc.button(label="Cancel", command=lambda *a: mc.deleteUI(win, window=True))
    mc.showWindow(win)

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
def refresh_saved_setups_ui():
    if mc.window("savedSetupsWin", exists=True):
        mc.deleteUI("savedSetupsWin")
    win = mc.window("savedSetupsWin", title="EasyBlink – Saved Setups", widthHeight=(300, 200))
    mc.columnLayout(adjustableColumn=True, rowSpacing=5)
    for name in easyblink_setups:
        mc.rowLayout(numberOfColumns=3, columnWidth3=(150, 70, 60))
        mc.text(label=name, align="left")
        mc.button(label="Load", command=lambda _,n=name: load_setup(n))
        mc.button(label="Delete", command=lambda _,n=name: delete_setup(n))
        mc.setParent("..")
    mc.showWindow(win)

# Build the UI
def create_easyblink_ui():
    if mc.window("EasyBlinkWindow", exists=True):
        mc.deleteUI("EasyBlinkWindow")
    win = mc.window("EasyBlinkWindow", title="EasyBlink", widthHeight=(360, 740))
    mc.scrollLayout(cr=True)
    mc.columnLayout(adjustableColumn=True, rowSpacing=10, columnAlign="center")

    # Eye controls
    mc.separator(style='in')
    mc.text(label="👁️ Blink Controls", font="boldLabelFont")
    mc.text(
        label="Select your left & right eye controls, then choose their blink attribute name. Then set your open/closed/wide values. Make sure names are the same as they are in script editor (place a keyframe with script editor open to see attribute names.",
        align="center",
        wordWrap=True
    )
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Left Eye",  command=set_left_eye)
    mc.text("leftEyeLabel",  label="Left Eye: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Right Eye", command=set_right_eye)
    mc.text("rightEyeLabel", label="Right Eye: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("leftBlinkAttrField",  text="Blink")
    mc.text(label="← Left Eye Attr")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("rightBlinkAttrField", text="Blink")
    mc.text(label="← Right Eye Attr")
    mc.setParent("..")
    mc.rowColumnLayout(numberOfColumns=2)
    mc.text(label="Open Value:")
    mc.floatField("openField", value=easyblink_data['open'])
    mc.text(label="Closed Value:")
    mc.floatField("closedField", value=easyblink_data['closed'])
    mc.text(label="Wide Value:")
    mc.floatField("wideField", value=easyblink_data['wide'])
    mc.setParent("..")
    mc.button(label="Save Blink Controls", command=save_blink_controls)

    # Eyebrow controls
    mc.separator(style='in')
    mc.text(label="🥸 Brow Controls", font="boldLabelFont")
    mc.text(
        label="Select your left & right eyebrow controls and set attribute name.",
        align="center",
        wordWrap=True
    )
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Left Brow",  command=set_left_brow)
    mc.text("leftBrowLabel",  label="Left Brow: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Right Brow", command=set_right_brow)
    mc.text("rightBrowLabel", label="Right Brow: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("browAttrField", text=easyblink_data['brow_attr'])
    mc.text(label="← Brow Attribute")
    mc.setParent("..")
    mc.button(label="Save Brow Attr", command=save_extra_controls)

    # Pupil controls
    mc.separator(style='in')
    mc.text(label="👀 Pupil Controls", font="boldLabelFont")
    mc.text(
        label="Select your left & right pupil controls and set attribute name.",
        align="center",
        wordWrap=True
    )
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Left Pupil",  command=set_left_pupil)
    mc.text("leftPupilLabel",  label="Left Pupil: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.button(label="Set Right Pupil", command=set_right_pupil)
    mc.text("rightPupilLabel", label="Right Pupil: Not Set")
    mc.setParent("..")
    mc.rowLayout(numberOfColumns=2)
    mc.textField("pupilAttrField", text=easyblink_data['pupil_attr'])
    mc.text(label="← Pupil Attribute")
    mc.setParent("..")
    mc.button(label="Save Pupil Attr", command=save_extra_controls)

    # Animate
    mc.separator(style='in')
    mc.text(label="⚡ Animate", font="boldLabelFont")
    mc.button(label="Set Simple Blink", command=set_simple_blink, height=40)
    mc.button(label="Set Slow Blink", command=set_slow_blink, height=40)
    
    # Reset
    mc.separator(style='in')
    mc.text(label="🧹 Reset", font="boldLabelFont")
    mc.button(label="Reset All to Defaults", command=clear_all_inputs, height=30, backgroundColor=(0.4,0.4,0.4))
    
    #Save inputs
    mc.separator(style='in')
    mc.text(label="💾 Save Inputs", font="boldLabelFont")
    mc.button(label="Save Setup…", command=open_save_setup_ui, height=30, backgroundColor=(0.2,0.5,0.2))
    mc.button(label="View Saved Setups", command=refresh_saved_setups_ui, height=30, backgroundColor=(0.2,0.2,0.5))

    mc.showWindow(win)

# Launch UI
create_easyblink_ui()


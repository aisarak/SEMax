# SE formats import / export plugin for 3DSMax
# Developed by DTZxPorter

import os
import os.path
import ctypes
import math
from PySide.QtCore import SIGNAL
from PySide import QtGui, QtCore
import MaxPlus
import struct
import seanim as SEAnim

# We must calculate the ticks to allow for proper timeframe scaling
MAX_FPS = MaxPlus.Core.EvalMAXScript('frameRate').GetInt()
# There are 4800 ticks per second, when keying, set the time to (frame * MAX_TICKS)
MAX_TICKS = 4800 / MAX_FPS

# Basic Call of Duty bindable tags
GUN_BASE_TAGS = ["j_gun", "j_gun1", "tag_weapon", "tag_weapon1"]
VIEW_HAND_TAGS = ["tag_weapon", "tag_weapon1", "tag_weapon_right", "tag_weapon_left"]

# Compare two iterable objects
def first(a, b):
	for elem in a:
		if elem in b:
			return a
	return None

# Ask the user to import a file
def ImportFileSelectDialog():
    # Make dialog
    print "TODO"

# Loads a .seanim file
def LoadSEAnimMakeKeys(filepath=""):
    # Load a seanim file using seanim api
    print("Loading SEAnim file...")
    # Load the file using helper lib
	anim = SEAnim.Anim(filepath)
    # Starting frame
	start_frame = 0
	# End frame
	end_frame = anim.header.frameCount - 1
    # Set scene start and end
    newRange = MaxPlus.Interval((start_frame * MAX_TICKS), (end_frame * MAX_TICKS))
    # Set it
    MaxPlus.Animation.SetRange(newRange)
    # Loop through bones
	for bone in anim.bones:
        # TODO: Parent modifiers
        BoneAnimType = anim.header.animType
        # Fetch this bone in the scene, if it exists
        BoneJoint = MaxPlus.INode.GetINodeByName(bone.name)
        # Check
        if BoneJoint is None:
            # Just skip it
            print "SEAnim -> WARN: Failed to find bone: " + bone.name
            # Skip
            continue
        # Reset rotation values
		if len(bone.rotKeys) > 0:
            # Reset rotation to 0, 0, 0 (SetLocalRotation(...??))
            print "TODO"
        # Grab the bone rest transform
        BoneRestTransform = BoneJoint.GetLocalPosition()
        # Loop through position keys, if any
        if len(bone.posKeys) > 0:
            # Prepare to animate this bone
            MaxPlus.Animation.SetAnimateButtonState(True)
            # Set linear tangents (TODO: Check what values are MAX linear in / out)
            MaxPlus.Animation.SetDefaultTangentType(5, 5)
            # Loop through the keyframes
            for key in bone.posKeys:
                # Set the current scene time
                MaxPlus.Animation.SetTime(key.frame * MAX_TICKS)
                # Check animation type to see what data we need
				if BoneAnimType == SEAnim.SEANIM_TYPE.SEANIM_TYPE_ABSOLUTE:
                    # Add absolute keyframe
                    print "TODO"
                else:
                    # Add relative keyframe
                    print "TODO"
            # End this bone's pos keys
            MaxPlus.Animation.SetAnimateButtonState(False)            
    # TODO: Notifications
    # Reset time back to first frame
    MaxPlus.Animation.SetTime((start_frame * MAX_TICKS), True)
    # Finished
    print("The animation has been loaded")
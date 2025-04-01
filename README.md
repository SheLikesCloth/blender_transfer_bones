# blender_transfer_bones

Add-on for Blender that transfers bones bones from one glb to another.
Adds bones to the active (recipient) armature if they are found in the non-active donor armature but not in the active recipient armature.

# Compatibility

Tested only on Blender 3.6.21.
Probably doesn't work on Blender 4+.

Has not been tested with non-glb models.

# Install

1. Download `blender_transfer_bones.py`
2. In Blender, select Edit > Preferences > Add-ons > Install
3. Select `blender_transfer_bones.py` in the finder and hit “Install add-on”
4. The add-on will then show up in the list as “Armature: Transfer Missing Bones”
5. Make sure the box next to “Armature: Transfer Missing Bones” is checked (activates the add-on)

# Use

1. Import a recipient glb
2. Import a donor glb (important to do this second because Blender might rename some parts of the model if those names are already used by the recipient model)
3. Go into Object Mode if not already in it
4. In the Outliner, click on the donor armature object (usually the top-level object with an orange stick figure icon)
5. In the Outliner, control+click on the recipient armature object
6. Switch to Edit Mode
7. In the Armature menu, select “Transfer Missing Bones”

If two armature objects are selected, the add-on will transfer bones to the active object from the non-active object. You can select the objects while in Edit Mode, but what counts as the active object in that case can be a bit confusing. My understanding: if only one object is set to be edited, that is always the active object. If two are being edited (have the box icon nect to them), then the object selected most recently is the active object.

# License

Author: NotAZebra/SheLikesCloth

I don’t know stuff about licenses. You may modify this add-on for non-commercial purposes. You are free to share the add-on but must credit the author. 

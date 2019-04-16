import bpy

sysp = bpy.context.user_preferences.system

devt = sysp.compute_device_type
dev = sysp.compute_device

# get list of possible values of enum, see http://blender.stackexchange.com/a/2268/599
devt_list = sysp.bl_rna.properties['compute_device_type'].enum_items.keys()
dev_list = sysp.bl_rna.properties['compute_device'].enum_items.keys()

# pretty print
lines=[
("Property", "Value", "Possible Values"),
("Device Type:", devt, str(devt_list)),
("Device:", dev, str(dev_list)),
]
print("\nGPU compute configuration:")
for l in lines:
    print("{0:<20} {1:<20} {2:<50}".format(*l))
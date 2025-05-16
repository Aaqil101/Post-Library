bl_info = {
    "name": "My Addon for Blender 4.2 LTS",
    "blender": (4, 2, 0),
    "category": "Object",
}


def register():
    print("v4_2: Registering things for Blender 4.2")


def unregister():
    print("v4_2: Unregistering things for Blender 4.2")


if __name__ == "__main__":
    register()

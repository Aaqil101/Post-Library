"""
* The ability to add drivers to nodes is made possible by Victor Stepanov
* (https://www.skool.com/cgpython/how-to-add-drivers-to-node-group-sockets-using-python?p=0be0f439)
* His youtube channel (https://www.youtube.com/@CGPython)
"""

import bpy

def add_driver_var(socket, data_path, name="default_value", id_type="SCENE", id=bpy.context.scene):
            """
            Adds a variable to a given socket.

            Parameters
            ----------
            socket : bpy.types.NodeSocket
                The socket to add the variable to.
            data_path : str
                The data path for the variable.
            name : str, optional
                The name of the variable. Defaults to "default_value".
            id_type : str, optional
                The type of ID for the variable. Defaults to "SCENE".
            id : bpy.types.ID, optional
                The ID for the variable. Defaults to bpy.context.scene.

            Returns
            -------
            driver_var : bpy.types.DriverVariable
                The added variable.
            """

            driver_var = socket.variables.new()
            driver_var.name = name
            driver_var.targets[0].id_type = id_type
            driver_var.targets[0].id = id
            driver_var.targets[0].data_path = data_path
            return driver_var
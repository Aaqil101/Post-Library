"""
* The ability to add drivers to nodes is made possible by Victor Stepanov
* (https://www.skool.com/cgpython/how-to-add-drivers-to-node-group-sockets-using-python?p=0be0f439)
* His youtube channel (https://www.youtube.com/@CGPython)
"""

import bpy


class NodeDriverManager:
    """
    Class to manage drivers on a node group.

    Can be used to create drivers on a node group and link them to a specific
    ID type and path.

    :param node_group: The node group to modify
    :type node_group: bpy.types.NodeGroup

    :param id_type: The type of object to link to
    :type id_type: str

    :param id: The object to link to
    :type id: bpy.types.ID

    :param var_name: The name of the variable to create
    :type var_name: str

    :param driver_type: The type of driver to create
    :type driver_type: str
    """

    def __init__(
        self,
        *,
        node_group: str,
        id_type: str,
        id: bpy.types.ID,
        var_name="default_value",
        driver_type="AVERAGE",
    ):
        """
        Constructor for NodeDriverManager

        :param node_group: The node group to modify
        :type node_group: bpy.types.NodeGroup

        :param id_type: The type of object to link to
        :type id_type: str

        :param id: The object to link to
        :type id: bpy.types.ID

        :param var_name: The name of the variable to create
        :type var_name: str

        :param driver_type: The type of driver to create
        :type driver_type: str
        """
        if not isinstance(id, bpy.types.ID):
            raise TypeError("The 'id' must be of type 'bpy.types.ID'")
        self.node_group = node_group
        self.var_name = var_name
        self.driver_type = driver_type
        self.id_type = id_type
        self.id = id
        self.driver = None

    def add_driver(self, *, node_name: str, socket_name: str):
        """
        Adds a driver to a specified node and socket within the node group.

        :param node_name: The name of the node to which the driver will be added.
        :type node_name: str

        :param socket_name: The name of the socket on the node where the driver will be added.
        :type socket_name: str

        :raises ValueError: If the node with the specified name is not found.

        :return: The created driver.
        :rtype: bpy.types.Driver
        """
        node = self.node_group.node_tree.nodes.get(node_name)
        if node is None:
            raise ValueError(f"Node with name {node_name} not found.")
        else:
            self.driver = node.driver_add(socket_name).driver
            self.driver.type = self.driver_type
            return self.driver

    def add_driver_var(self, number: int):
        """
        Adds a variable to the driver associated with the node group.

        This function creates a new variable in the driver and sets its data path
        to point to the default value of the specified input number in the node group.

        Args:
            number (int): The index of the input in the node group whose default value
            will be linked to the driver variable.

        Raises:
            ValueError: If the driver is not initialized or if the input number is out of range.

        Returns:
            bpy.types.DriverVariable: The created driver variable.
        """
        if self.driver is None:
            raise ValueError("Driver not initialized. Call add_driver first.")
        if number < 0 or number >= len(self.node_group.inputs):
            raise ValueError(f"Input number {number} is out of range.")
        driver_var = self.driver.variables.new()
        driver_var.name = self.var_name
        driver_var.targets[0].id_type = self.id_type
        driver_var.targets[0].id = self.id
        driver_var.targets[0].data_path = (
            f'node_tree.nodes["{self.node_group.name}"].inputs[{number}].default_value'
        )
        return driver_var

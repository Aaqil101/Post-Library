from bpy import context

# Ensure all connections exist
def ensure_connection(output_node, output_socket_name, input_node, input_socket_name):
    """
    Ensures that a connection exists between two nodes

    Args:
        output_node (bpy.types.Node): The node that the connection comes from
        output_socket_name (str): The name of the output socket
        input_node (bpy.types.Node): The node that the connection goes to
        input_socket_name (str): The name of the input socket

    Returns:
        None
    """
    # Get the compositor node tree
    node_tree = context.scene.node_tree
    links = node_tree.links

    # Check if a link already exists
    for link in links:
        if (
            link.from_node == output_node
            and link.to_node == input_node
            and link.from_socket.name == output_socket_name
            and link.to_socket.name == input_socket_name
        ):
            return  # Connection already exists

    # Create the link if not found
    links.new(output_node.outputs[output_socket_name], input_node.inputs[input_socket_name])
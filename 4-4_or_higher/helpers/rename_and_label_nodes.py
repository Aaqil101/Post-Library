def rename_and_label_nodes(node_data):
    """
    Renames multiple nodes and assigns labels to them. If a node is a group type, it also renames the node tree.
    If width is provided, it will also set the width of the node.

    Args:
        node_data (list of tuple): A list of tuples, each containing:
            - node (bpy.types.Node): The node to rename and label.
            - name (str): The new name and label for the node.
            - width (int, optional): The new width of the node. Defaults to None.

    Returns:
        dict: A dictionary summarizing the results:
              {'renamed': int, 'errors': list}
    """
    results = {"renamed": 0, "errors": []}

    for entry in node_data:
        if len(entry) < 2:
            results["errors"].append(f"Invalid entry (too few elements): {entry}")
            continue

        node, name, *optional_width = entry
        if not node:
            results["errors"].append(f"Node is None for name '{name}'.")
            continue

        try:
            # Rename and label node
            node.name = name
            node.label = name

            # Rename node tree if applicable
            if hasattr(node, "node_tree") and node.node_tree:
                node.node_tree.name = name

            # Adjust width if provided
            if optional_width:
                node.width = optional_width[0]

            results["renamed"] += 1
        except Exception as e:
            results["errors"].append(f"Error processing node '{name}': {e}")

    return results

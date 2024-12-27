import bpy

def rm_ngs_from_data(ngs_names_to_rm):
    """
    Removes specified node groups from the Blender data.

    Args:
        ngs_names_to_rm (list of str): List of node group names to remove.

    Returns:
        dict: A dictionary with counts and details:
              {'removed': int, 'not_found': int, 'errors': list}
    """
    if not isinstance(ngs_names_to_rm, (list, tuple)):
        raise ValueError("Expected a list or tuple of node group names.")

    results = {
        'removed': 0,
        'not_found': 0,
        'errors': []
    }

    for name in ngs_names_to_rm:
        node_group = bpy.data.node_groups.get(name)
        if node_group:  # Check if the node group exists
            try:
                print(f"Removing node group: {name}")
                bpy.data.node_groups.remove(node_group)
                results['removed'] += 1
            except Exception as e:
                print(f"Error removing node group '{name}': {e}")
                results['errors'].append((name, str(e)))
        else:
            print(f"Node group '{name}' not found.")
            results['not_found'] += 1

    return results
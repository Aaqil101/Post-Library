import bpy

beauty_mixer_node = bpy.context.scene.node_tree.nodes['BeautyMixer']

diff_dir_input_socket = beauty_mixer_node.node_tree.interface.items_tree['DiffDir']
beauty_mixer_node.node_tree.interface.remove(diff_dir_input_socket)

diffuse_socket_panel = beauty_mixer_node.node_tree.interface.items_tree['Diffuse']
beauty_mixer_node.node_tree.interface.remove(diffuse_socket_panel)
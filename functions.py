import bpy
from dictionaries import (COLORS_DICT)

#initialize MultiDenoiser node group
def multidenoiser_node_group(context, operator, group_name):
    
    #enable use nodes
    bpy.context.scene.use_nodes = True
    
    multidenoiser = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    #initialize MultiDenoiser node group

    multidenoiser.color_tag = 'FILTER'
    multidenoiser.description = "A custom node group for denoising each passes seperetely"

    #multidenoiser interface
    #Socket Position
    position_socket = multidenoiser.interface.new_socket(name = "Position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
    position_socket.default_value = (0.0, 0.0, 0.0)
    position_socket.min_value = -3.4028234663852886e+38
    position_socket.max_value = 3.4028234663852886e+38
    position_socket.subtype = 'NONE'
    position_socket.attribute_domain = 'POINT'
    position_socket.hide_value = True

    #Socket Normal
    normal_socket = multidenoiser.interface.new_socket(name = "Normal", in_out='OUTPUT', socket_type = 'NodeSocketVector')
    normal_socket.default_value = (0.0, 0.0, 0.0)
    normal_socket.min_value = -3.4028234663852886e+38
    normal_socket.max_value = 3.4028234663852886e+38
    normal_socket.subtype = 'NONE'
    normal_socket.attribute_domain = 'POINT'
    normal_socket.hide_value = True

    #Socket Vetor
    vetor_socket = multidenoiser.interface.new_socket(name = "Vetor", in_out='OUTPUT', socket_type = 'NodeSocketVector')
    vetor_socket.default_value = (0.0, 0.0, 0.0)
    vetor_socket.min_value = -3.4028234663852886e+38
    vetor_socket.max_value = 3.4028234663852886e+38
    vetor_socket.subtype = 'NONE'
    vetor_socket.attribute_domain = 'POINT'
    vetor_socket.hide_value = True

    #Socket DiffDir
    diffdir_socket = multidenoiser.interface.new_socket(name = "DiffDir", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diffdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffdir_socket.attribute_domain = 'POINT'
    diffdir_socket.hide_value = True

    #Socket DiffInd
    diffind_socket = multidenoiser.interface.new_socket(name = "DiffInd", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diffind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffind_socket.attribute_domain = 'POINT'
    diffind_socket.hide_value = True

    #Socket DiffCol
    diffcol_socket = multidenoiser.interface.new_socket(name = "DiffCol", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    diffcol_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    diffcol_socket.attribute_domain = 'POINT'
    diffcol_socket.hide_value = True

    #Socket GlossDir
    glossdir_socket = multidenoiser.interface.new_socket(name = "GlossDir", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    glossdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glossdir_socket.attribute_domain = 'POINT'
    glossdir_socket.hide_value = True

    #Socket GlossInd
    glossind_socket = multidenoiser.interface.new_socket(name = "GlossInd", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    glossind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glossind_socket.attribute_domain = 'POINT'
    glossind_socket.hide_value = True

    #Socket GlossCol
    glosscol_socket = multidenoiser.interface.new_socket(name = "GlossCol", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    glosscol_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    glosscol_socket.attribute_domain = 'POINT'
    glosscol_socket.hide_value = True

    #Socket TransDir
    transdir_socket = multidenoiser.interface.new_socket(name = "TransDir", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    transdir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transdir_socket.attribute_domain = 'POINT'
    transdir_socket.hide_value = True

    #Socket TransInd
    transind_socket = multidenoiser.interface.new_socket(name = "TransInd", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    transind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transind_socket.attribute_domain = 'POINT'
    transind_socket.hide_value = True

    #Socket TransCol
    transcol_socket = multidenoiser.interface.new_socket(name = "TransCol", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    transcol_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    transcol_socket.attribute_domain = 'POINT'
    transcol_socket.hide_value = True

    #Socket VolumeDir
    volumedir_socket = multidenoiser.interface.new_socket(name = "VolumeDir", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    volumedir_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    volumedir_socket.attribute_domain = 'POINT'
    volumedir_socket.hide_value = True

    #Socket VolumeInd
    volumeind_socket = multidenoiser.interface.new_socket(name = "VolumeInd", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    volumeind_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    volumeind_socket.attribute_domain = 'POINT'
    volumeind_socket.hide_value = True

    #Socket Emit
    emit_socket = multidenoiser.interface.new_socket(name = "Emit", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    emit_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    emit_socket.attribute_domain = 'POINT'
    emit_socket.hide_value = True

    #Socket Env
    env_socket = multidenoiser.interface.new_socket(name = "Env", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    env_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    env_socket.attribute_domain = 'POINT'
    env_socket.hide_value = True

    #Socket AO
    ao_socket = multidenoiser.interface.new_socket(name = "AO", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    ao_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    ao_socket.attribute_domain = 'POINT'
    ao_socket.hide_value = True

    #Socket Position
    position_socket_1 = multidenoiser.interface.new_socket(name = "Position", in_out='INPUT', socket_type = 'NodeSocketVector')
    position_socket_1.default_value = (0.0, 0.0, 0.0)
    position_socket_1.min_value = -1.0
    position_socket_1.max_value = 1.0
    position_socket_1.subtype = 'NONE'
    position_socket_1.attribute_domain = 'POINT'
    position_socket_1.hide_value = True

    #Socket Normal
    normal_socket_1 = multidenoiser.interface.new_socket(name = "Normal", in_out='INPUT', socket_type = 'NodeSocketVector')
    normal_socket_1.default_value = (0.0, 0.0, 0.0)
    normal_socket_1.min_value = -1.0
    normal_socket_1.max_value = 1.0
    normal_socket_1.subtype = 'NONE'
    normal_socket_1.attribute_domain = 'POINT'
    normal_socket_1.hide_value = True

    #Socket Vetor
    vetor_socket_1 = multidenoiser.interface.new_socket(name = "Vetor", in_out='INPUT', socket_type = 'NodeSocketVector')
    vetor_socket_1.default_value = (0.0, 0.0, 0.0)
    vetor_socket_1.min_value = -1.0
    vetor_socket_1.max_value = 1.0
    vetor_socket_1.subtype = 'NONE'
    vetor_socket_1.attribute_domain = 'POINT'
    vetor_socket_1.hide_value = True

    #Socket DiffDir
    diffdir_socket_1 = multidenoiser.interface.new_socket(name = "DiffDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    diffdir_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diffdir_socket_1.attribute_domain = 'POINT'
    diffdir_socket_1.hide_value = True

    #Socket DiffInd
    diffind_socket_1 = multidenoiser.interface.new_socket(name = "DiffInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    diffind_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diffind_socket_1.attribute_domain = 'POINT'
    diffind_socket_1.hide_value = True

    #Socket DiffCol
    diffcol_socket_1 = multidenoiser.interface.new_socket(name = "DiffCol", in_out='INPUT', socket_type = 'NodeSocketColor')
    diffcol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    diffcol_socket_1.attribute_domain = 'POINT'
    diffcol_socket_1.hide_value = True

    #Socket GlossDir
    glossdir_socket_1 = multidenoiser.interface.new_socket(name = "GlossDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    glossdir_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    glossdir_socket_1.attribute_domain = 'POINT'
    glossdir_socket_1.hide_value = True

    #Socket GlossInd
    glossind_socket_1 = multidenoiser.interface.new_socket(name = "GlossInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    glossind_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    glossind_socket_1.attribute_domain = 'POINT'
    glossind_socket_1.hide_value = True

    #Socket GlossCol
    glosscol_socket_1 = multidenoiser.interface.new_socket(name = "GlossCol", in_out='INPUT', socket_type = 'NodeSocketColor')
    glosscol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    glosscol_socket_1.attribute_domain = 'POINT'
    glosscol_socket_1.hide_value = True

    #Socket TransDir
    transdir_socket_1 = multidenoiser.interface.new_socket(name = "TransDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    transdir_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    transdir_socket_1.attribute_domain = 'POINT'
    transdir_socket_1.hide_value = True

    #Socket TransInd
    transind_socket_1 = multidenoiser.interface.new_socket(name = "TransInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    transind_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    transind_socket_1.attribute_domain = 'POINT'
    transind_socket_1.hide_value = True

    #Socket TransCol
    transcol_socket_1 = multidenoiser.interface.new_socket(name = "TransCol", in_out='INPUT', socket_type = 'NodeSocketColor')
    transcol_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    transcol_socket_1.attribute_domain = 'POINT'
    transcol_socket_1.hide_value = True

    #Socket VolumeDir
    volumedir_socket_1 = multidenoiser.interface.new_socket(name = "VolumeDir", in_out='INPUT', socket_type = 'NodeSocketColor')
    volumedir_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    volumedir_socket_1.attribute_domain = 'POINT'
    volumedir_socket_1.hide_value = True

    #Socket VolumeInd
    volumeind_socket_1 = multidenoiser.interface.new_socket(name = "VolumeInd", in_out='INPUT', socket_type = 'NodeSocketColor')
    volumeind_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    volumeind_socket_1.attribute_domain = 'POINT'
    volumeind_socket_1.hide_value = True

    #Socket Emit
    emit_socket_1 = multidenoiser.interface.new_socket(name = "Emit", in_out='INPUT', socket_type = 'NodeSocketColor')
    emit_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    emit_socket_1.attribute_domain = 'POINT'
    emit_socket_1.hide_value = True

    #Socket Env
    env_socket_1 = multidenoiser.interface.new_socket(name = "Env", in_out='INPUT', socket_type = 'NodeSocketColor')
    env_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    env_socket_1.attribute_domain = 'POINT'
    env_socket_1.hide_value = True

    #Socket AO
    ao_socket_1 = multidenoiser.interface.new_socket(name = "AO", in_out='INPUT', socket_type = 'NodeSocketColor')
    ao_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
    ao_socket_1.attribute_domain = 'POINT'
    ao_socket_1.hide_value = True

    #Socket Normal
    normal_socket_2 = multidenoiser.interface.new_socket(name = "Normal", in_out='INPUT', socket_type = 'NodeSocketVector')
    normal_socket_2.default_value = (0.0, 0.0, 0.0)
    normal_socket_2.min_value = -1.0
    normal_socket_2.max_value = 1.0
    normal_socket_2.subtype = 'NONE'
    normal_socket_2.attribute_domain = 'POINT'
    normal_socket_2.hide_value = True

    #Socket Albedo
    albedo_socket = multidenoiser.interface.new_socket(name = "Albedo", in_out='INPUT', socket_type = 'NodeSocketColor')
    albedo_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    albedo_socket.attribute_domain = 'POINT'
    albedo_socket.hide_value = True


    #initialize multidenoiser nodes
    #node diffdir_denoise
    diffdir_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    diffdir_denoise.label = "DiffDir"
    diffdir_denoise.name = "diffdir_denoise"
    diffdir_denoise.use_custom_color = True
    diffdir_denoise.color = COLORS_DICT["DARK_PURPLE"]
    diffdir_denoise.hide = True
    diffdir_denoise.prefilter = 'ACCURATE'
    diffdir_denoise.use_hdr = True

    #node diffind_denoise
    diffind_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    diffind_denoise.label = "DiffInd"
    diffind_denoise.name = "diffind_denoise"
    diffind_denoise.use_custom_color = True
    diffind_denoise.color = COLORS_DICT["DARK_PURPLE"]
    diffind_denoise.hide = True
    diffind_denoise.prefilter = 'ACCURATE'
    diffind_denoise.use_hdr = True

    #node diffcol_denoise
    diffcol_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    diffcol_denoise.label = "DiffCol"
    diffcol_denoise.name = "diffcol_denoise"
    diffcol_denoise.use_custom_color = True
    diffcol_denoise.color = COLORS_DICT["DARK_PURPLE"]
    diffcol_denoise.hide = True
    diffcol_denoise.prefilter = 'ACCURATE'
    diffcol_denoise.use_hdr = True

    #node glossdir_denoise
    glossdir_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    glossdir_denoise.label = "GlossDir"
    glossdir_denoise.name = "glossdir_denoise"
    glossdir_denoise.use_custom_color = True
    glossdir_denoise.color = COLORS_DICT["DARK_PURPLE"]
    glossdir_denoise.hide = True
    glossdir_denoise.prefilter = 'ACCURATE'
    glossdir_denoise.use_hdr = True

    #node glossind_denoise
    glossind_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    glossind_denoise.label = "GlossInd"
    glossind_denoise.name = "glossind_denoise"
    glossind_denoise.use_custom_color = True
    glossind_denoise.color = COLORS_DICT["DARK_PURPLE"]
    glossind_denoise.hide = True
    glossind_denoise.prefilter = 'ACCURATE'
    glossind_denoise.use_hdr = True

    #node glosscol_denoise
    glosscol_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    glosscol_denoise.label = "GlossCol"
    glosscol_denoise.name = "glosscol_denoise"
    glosscol_denoise.use_custom_color = True
    glosscol_denoise.color = COLORS_DICT["DARK_PURPLE"]
    glosscol_denoise.hide = True
    glosscol_denoise.prefilter = 'ACCURATE'
    glosscol_denoise.use_hdr = True

    #node transdir_denoise
    transdir_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    transdir_denoise.label = "TransDir"
    transdir_denoise.name = "transdir_denoise"
    transdir_denoise.use_custom_color = True
    transdir_denoise.color = COLORS_DICT["DARK_PURPLE"]
    transdir_denoise.hide = True
    transdir_denoise.prefilter = 'ACCURATE'
    transdir_denoise.use_hdr = True

    #node transind_denoise
    transind_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    transind_denoise.label = "TransInd"
    transind_denoise.name = "transind_denoise"
    transind_denoise.use_custom_color = True
    transind_denoise.color = COLORS_DICT["DARK_PURPLE"]
    transind_denoise.hide = True
    transind_denoise.prefilter = 'ACCURATE'
    transind_denoise.use_hdr = True

    #node transcol_denoise
    transcol_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    transcol_denoise.label = "TransCol"
    transcol_denoise.name = "transcol_denoise"
    transcol_denoise.use_custom_color = True
    transcol_denoise.color = COLORS_DICT["DARK_PURPLE"]
    transcol_denoise.hide = True
    transcol_denoise.prefilter = 'ACCURATE'
    transcol_denoise.use_hdr = True

    #node volumedir_denoise
    volumedir_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    volumedir_denoise.label = "VolumeDir"
    volumedir_denoise.name = "volumedir_denoise"
    volumedir_denoise.use_custom_color = True
    volumedir_denoise.color = COLORS_DICT["DARK_PURPLE"]
    volumedir_denoise.hide = True
    volumedir_denoise.prefilter = 'ACCURATE'
    volumedir_denoise.use_hdr = True

    #node volumeind_denoise
    volumeind_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    volumeind_denoise.label = "VolumeInd"
    volumeind_denoise.name = "volumeind_denoise"
    volumeind_denoise.use_custom_color = True
    volumeind_denoise.color = COLORS_DICT["DARK_PURPLE"]
    volumeind_denoise.hide = True
    volumeind_denoise.prefilter = 'ACCURATE'
    volumeind_denoise.use_hdr = True

    #node emit_denoise
    emit_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    emit_denoise.label = "Emit"
    emit_denoise.name = "emit_denoise"
    emit_denoise.use_custom_color = True
    emit_denoise.color = COLORS_DICT["DARK_PURPLE"]
    emit_denoise.hide = True
    emit_denoise.prefilter = 'ACCURATE'
    emit_denoise.use_hdr = True

    #node env_denoise
    env_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    env_denoise.label = "Env"
    env_denoise.name = "env_denoise"
    env_denoise.use_custom_color = True
    env_denoise.color = COLORS_DICT["DARK_PURPLE"]
    env_denoise.hide = True
    env_denoise.prefilter = 'ACCURATE'
    env_denoise.use_hdr = True

    #node ao_denoise
    ao_denoise = multidenoiser.nodes.new("CompositorNodeDenoise")
    ao_denoise.label = "AO"
    ao_denoise.name = "ao_denoise"
    ao_denoise.use_custom_color = True
    ao_denoise.color = COLORS_DICT["DARK_PURPLE"]
    ao_denoise.hide = True
    ao_denoise.prefilter = 'ACCURATE'
    ao_denoise.use_hdr = True

    #node Group Input Passes
    group_input_passes = multidenoiser.nodes.new("NodeGroupInput")
    group_input_passes.label = "Group Input Passes"
    group_input_passes.name = "Group Input Passes"
    group_input_passes.use_custom_color = True
    group_input_passes.color = COLORS_DICT["GRAY"]
    group_input_passes.outputs[17].hide = True
    group_input_passes.outputs[18].hide = True
    group_input_passes.outputs[19].hide = True

    #node Group Output MD
    group_output_md = multidenoiser.nodes.new("NodeGroupOutput")
    group_output_md.label = "Group Output MD"
    group_output_md.name = "Group Output MD"
    group_output_md.use_custom_color = True
    group_output_md.color = COLORS_DICT["GRAY"]
    group_output_md.is_active_output = True
    group_output_md.inputs[17].hide = True

    #node Group Input Denoise
    group_input_denoise = multidenoiser.nodes.new("NodeGroupInput")
    group_input_denoise.label = "Group Input Denoise"
    group_input_denoise.name = "Group Input Denoise"
    group_input_denoise.use_custom_color = True
    group_input_denoise.color = COLORS_DICT["GRAY"]
    group_input_denoise.outputs[0].hide = True
    group_input_denoise.outputs[1].hide = True
    group_input_denoise.outputs[2].hide = True
    group_input_denoise.outputs[3].hide = True
    group_input_denoise.outputs[4].hide = True
    group_input_denoise.outputs[5].hide = True
    group_input_denoise.outputs[6].hide = True
    group_input_denoise.outputs[7].hide = True
    group_input_denoise.outputs[8].hide = True
    group_input_denoise.outputs[9].hide = True
    group_input_denoise.outputs[10].hide = True
    group_input_denoise.outputs[11].hide = True
    group_input_denoise.outputs[12].hide = True
    group_input_denoise.outputs[13].hide = True
    group_input_denoise.outputs[14].hide = True
    group_input_denoise.outputs[15].hide = True
    group_input_denoise.outputs[16].hide = True
    group_input_denoise.outputs[19].hide = True

    #node Vector_VectorIn
    vector_vectorin = multidenoiser.nodes.new("CompositorNodeSeparateColor")
    vector_vectorin.label = "Vector_VECTORIN"
    vector_vectorin.name = "Vector_VectorIn"
    vector_vectorin.use_custom_color = True
    vector_vectorin.color = COLORS_DICT["DARK_BLUE"]
    vector_vectorin.hide = True
    vector_vectorin.mode = 'RGB'
    vector_vectorin.ycc_mode = 'ITUBT709'

    #node Vector_VectorOut
    vector_vectorout = multidenoiser.nodes.new("CompositorNodeCombineColor")
    vector_vectorout.label = "Vector_VECTOROUT"
    vector_vectorout.name = "Vector_VectorOut"
    vector_vectorout.use_custom_color = True
    vector_vectorout.color = COLORS_DICT["DARK_BLUE"]
    vector_vectorout.hide = True
    vector_vectorout.mode = 'RGB'
    vector_vectorout.ycc_mode = 'ITUBT709'

    #node Position_Break
    position_break = multidenoiser.nodes.new("CompositorNodeSeparateXYZ")
    position_break.label = "Position_BREAK"
    position_break.name = "Position_Break"
    position_break.use_custom_color = True
    position_break.color = COLORS_DICT["DARK_BLUE"]
    position_break.hide = True

    #node Normal_Break
    normal_break = multidenoiser.nodes.new("CompositorNodeSeparateXYZ")
    normal_break.label = "Normal_BREAK"
    normal_break.name = "Normal_Break"
    normal_break.use_custom_color = True
    normal_break.color = COLORS_DICT["DARK_BLUE"]
    normal_break.hide = True

    #node Position_Combine
    position_combine = multidenoiser.nodes.new("CompositorNodeCombineXYZ")
    position_combine.label = "Position_COMBINE"
    position_combine.name = "Position_Combine"
    position_combine.use_custom_color = True
    position_combine.color = COLORS_DICT["DARK_BLUE"]
    position_combine.hide = True

    #node Normal_Combine
    normal_combine = multidenoiser.nodes.new("CompositorNodeCombineXYZ")
    normal_combine.label = "Normal_COMBINE"
    normal_combine.name = "Normal_Combine"
    normal_combine.use_custom_color = True
    normal_combine.color = COLORS_DICT["DARK_BLUE"]
    normal_combine.hide = True

    #node Position_Inv
    position_inv = multidenoiser.nodes.new("CompositorNodeMath")
    position_inv.label = "Position_INVERT"
    position_inv.name = "Position_Inv"
    position_inv.use_custom_color = True
    position_inv.color = COLORS_DICT["DARK_BLUE"]
    position_inv.hide = True
    position_inv.operation = 'MULTIPLY'
    position_inv.use_clamp = False
    #Value_001
    position_inv.inputs[1].default_value = -1.0

    #node Normal_Inv
    normal_inv = multidenoiser.nodes.new("CompositorNodeMath")
    normal_inv.label = "Normal_INVERT"
    normal_inv.name = "Normal_Inv"
    normal_inv.use_custom_color = True
    normal_inv.color = COLORS_DICT["DARK_BLUE"]
    normal_inv.hide = True
    normal_inv.operation = 'MULTIPLY'
    normal_inv.use_clamp = False
    #Value_001
    normal_inv.inputs[1].default_value = -1.0


    #Set locations
    diffdir_denoise.location = (-127.05178833007812, -476.024658203125)
    diffind_denoise.location = (-127.05178833007812, -521.024658203125)
    diffcol_denoise.location = (-127.05178833007812, -566.024658203125)
    glossdir_denoise.location = (-127.05178833007812, -611.024658203125)
    glossind_denoise.location = (-127.05178833007812, -656.024658203125)
    glosscol_denoise.location = (-127.05178833007812, -701.024658203125)
    transdir_denoise.location = (-127.05178833007812, -746.024658203125)
    transind_denoise.location = (-127.05178833007812, -791.024658203125)
    transcol_denoise.location = (-127.05178833007812, -836.024658203125)
    volumedir_denoise.location = (-127.05178833007812, -881.024658203125)
    volumeind_denoise.location = (-127.05178833007812, -926.0247192382812)
    emit_denoise.location = (-127.05178833007812, -971.0247192382812)
    env_denoise.location = (-127.05178833007812, -1016.0247192382812)
    ao_denoise.location = (-127.05178833007812, -1061.0247802734375)
    group_input_passes.location = (-1062.076171875, -478.6734619140625)
    group_output_md.location = (627.108642578125, -485.0574035644531)
    group_input_denoise.location = (-1062.076171875, -897.6734619140625)
    vector_vectorin.location = (-255.81431579589844, -426.9619140625)
    vector_vectorout.location = (-20.385299682617188, -426.9619140625)
    position_break.location = (-307.9491882324219, -326.2154541015625)
    normal_break.location = (-305.9849548339844, -375.56591796875)
    position_combine.location = (19.604141235351562, -326.2154541015625)
    normal_combine.location = (21.568496704101562, -375.56591796875)
    position_inv.location = (-144.1725311279297, -326.2154541015625)
    normal_inv.location = (-142.20823669433594, -375.56591796875)

    #Set dimensions
    diffdir_denoise.width, diffdir_denoise.height = 140.0, 100.0
    diffind_denoise.width, diffind_denoise.height = 140.0, 100.0
    diffcol_denoise.width, diffcol_denoise.height = 140.0, 100.0
    glossdir_denoise.width, glossdir_denoise.height = 140.0, 100.0
    glossind_denoise.width, glossind_denoise.height = 140.0, 100.0
    glosscol_denoise.width, glosscol_denoise.height = 140.0, 100.0
    transdir_denoise.width, transdir_denoise.height = 140.0, 100.0
    transind_denoise.width, transind_denoise.height = 140.0, 100.0
    transcol_denoise.width, transcol_denoise.height = 140.0, 100.0
    volumedir_denoise.width, volumedir_denoise.height = 140.0, 100.0
    volumeind_denoise.width, volumeind_denoise.height = 140.0, 100.0
    emit_denoise.width, emit_denoise.height = 140.0, 100.0
    env_denoise.width, env_denoise.height = 140.0, 100.0
    ao_denoise.width, ao_denoise.height = 140.0, 100.0
    group_input_passes.width, group_input_passes.height = 142.8135986328125, 100.0
    group_output_md.width, group_output_md.height = 207.4061279296875, 100.0
    group_input_denoise.width, group_input_denoise.height = 140.0, 100.0
    vector_vectorin.width, vector_vectorin.height = 148.082275390625, 100.0
    vector_vectorout.width, vector_vectorout.height = 150.50701904296875, 100.0
    position_break.width, position_break.height = 140.0, 100.0
    normal_break.width, normal_break.height = 140.0, 100.0
    position_combine.width, position_combine.height = 140.0, 100.0
    normal_combine.width, normal_combine.height = 140.0, 100.0
    position_inv.width, position_inv.height = 140.0, 100.0
    normal_inv.width, normal_inv.height = 140.0, 100.0

    #initialize multidenoiser links
    #group_input_passes.DiffDir -> diffdir_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[3], diffdir_denoise.inputs[0])
    
    #diffdir_denoise.Image -> group_output_md.DiffDir
    multidenoiser.links.new(diffdir_denoise.outputs[0], group_output_md.inputs[3])

    #group_input_passes.DiffInd -> diffind_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[4], diffind_denoise.inputs[0])

    #diffind_denoise.Image -> group_output_md.DiffInd
    multidenoiser.links.new(diffind_denoise.outputs[0], group_output_md.inputs[4])

    #group_input_passes.DiffCol -> diffcol_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[5], diffcol_denoise.inputs[0])

    #diffcol_denoise.Image -> group_output_md.DiffCol
    multidenoiser.links.new(diffcol_denoise.outputs[0], group_output_md.inputs[5])

    #group_input_passes.GlossDir -> glossdir_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[6], glossdir_denoise.inputs[0])

    #glossdir_denoise.Image -> group_output_md.GlossDir
    multidenoiser.links.new(glossdir_denoise.outputs[0], group_output_md.inputs[6])

    #group_input_passes.GlossInd -> glossind_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[7], glossind_denoise.inputs[0])

    #glossind_denoise.Image -> group_output_md.GlossInd
    multidenoiser.links.new(glossind_denoise.outputs[0], group_output_md.inputs[7])

    #group_input_passes.GlossCol -> glosscol_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[8], glosscol_denoise.inputs[0])

    #glosscol_denoise.Image -> group_output_md.GlossCol
    multidenoiser.links.new(glosscol_denoise.outputs[0], group_output_md.inputs[8])

    #group_input_passes.TransDir -> transdir_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[9], transdir_denoise.inputs[0])

    #transdir_denoise.Image -> group_output_md.TransDir
    multidenoiser.links.new(transdir_denoise.outputs[0], group_output_md.inputs[9])

    #group_input_passes.TransInd -> transind_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[10], transind_denoise.inputs[0])

    #transind_denoise.Image -> group_output_md.TransInd
    multidenoiser.links.new(transind_denoise.outputs[0], group_output_md.inputs[10])

    #group_input_passes.TransCol -> transcol_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[11], transcol_denoise.inputs[0])

    #transcol_denoise.Image -> group_output_md.TransCol
    multidenoiser.links.new(transcol_denoise.outputs[0], group_output_md.inputs[11])

    #group_input_passes.VolumeDir -> volumedir_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[12], volumedir_denoise.inputs[0])

    #volumedir_denoise.Image -> group_output_md.VolumeDir
    multidenoiser.links.new(volumedir_denoise.outputs[0], group_output_md.inputs[12])

    #group_input_passes.VolumeInd -> volumeind_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[13], volumeind_denoise.inputs[0])

    #volumeind_denoise.Image -> group_output_md.VolumeInd
    multidenoiser.links.new(volumeind_denoise.outputs[0], group_output_md.inputs[13])

    #group_input_passes.Emit -> emit_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[14], emit_denoise.inputs[0])

    #emit_denoise.Image -> group_output_md.Emit
    multidenoiser.links.new(emit_denoise.outputs[0], group_output_md.inputs[14])

    #group_input_passes.Env -> env_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[15], env_denoise.inputs[0])

    #env_denoise.Image -> group_output_md.Env
    multidenoiser.links.new(env_denoise.outputs[0], group_output_md.inputs[15])

    #group_input_passes.AO -> ao_denoise.Image
    multidenoiser.links.new(group_input_passes.outputs[16], ao_denoise.inputs[0])

    #ao_denoise.Image -> group_output_md.AO
    multidenoiser.links.new(ao_denoise.outputs[0], group_output_md.inputs[16])

    #group_input_denoise.Normal -> diffdir_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], diffdir_denoise.inputs[1])

    #group_input_denoise.Albedo -> diffdir_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], diffdir_denoise.inputs[2])

    #group_input_denoise.Normal -> diffind_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], diffind_denoise.inputs[1])

    #group_input_denoise.Albedo -> diffind_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], diffind_denoise.inputs[2])

    #group_input_denoise.Normal -> diffcol_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], diffcol_denoise.inputs[1])

    #group_input_denoise.Albedo -> diffcol_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], diffcol_denoise.inputs[2])

    #group_input_denoise.Normal -> glossdir_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], glossdir_denoise.inputs[1])

    #group_input_denoise.Albedo -> glossdir_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], glossdir_denoise.inputs[2])

    #group_input_denoise.Normal -> glossind_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], glossind_denoise.inputs[1])

    #group_input_denoise.Albedo -> glossind_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], glossind_denoise.inputs[2])

    #group_input_denoise.Normal -> glosscol_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], glosscol_denoise.inputs[1])

    #group_input_denoise.Albedo -> glosscol_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], glosscol_denoise.inputs[2])

    #group_input_denoise.Normal -> transdir_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], transdir_denoise.inputs[1])

    #group_input_denoise.Albedo -> transdir_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], transdir_denoise.inputs[2])

    #group_input_denoise.Normal -> transind_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], transind_denoise.inputs[1])

    #group_input_denoise.Albedo -> transind_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], transind_denoise.inputs[2])

    #group_input_denoise.Normal -> transcol_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], transcol_denoise.inputs[1])

    #group_input_denoise.Albedo -> transcol_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], transcol_denoise.inputs[2])

    #group_input_denoise.Normal -> volumedir_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], volumedir_denoise.inputs[1])

    #group_input_denoise.Albedo -> volumedir_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], volumedir_denoise.inputs[2])

    #group_input_denoise.Normal -> volumeind_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], volumeind_denoise.inputs[1])

    #group_input_denoise.Albedo -> volumeind_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], volumeind_denoise.inputs[2])

    #group_input_denoise.Normal -> emit_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], emit_denoise.inputs[1])

    #group_input_denoise.Albedo -> emit_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], emit_denoise.inputs[2])

    #group_input_denoise.Normal -> env_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], env_denoise.inputs[1])

    #group_input_denoise.Albedo -> env_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], env_denoise.inputs[2])

    #group_input_denoise.Normal -> ao_denoise.Normal
    multidenoiser.links.new(group_input_denoise.outputs[17], ao_denoise.inputs[1])

    #group_input_denoise.Albedo -> ao_denoise.Albedo
    multidenoiser.links.new(group_input_denoise.outputs[18], ao_denoise.inputs[2])

    #normal_break.X -> normal_combine.X
    multidenoiser.links.new(normal_break.outputs[0], normal_combine.inputs[0])

    #vector_vectorin.Blue -> vector_vectorout.Alpha
    multidenoiser.links.new(vector_vectorin.outputs[2], vector_vectorout.inputs[3])

    #vector_vectorin.Blue -> vector_vectorout.Red
    multidenoiser.links.new(vector_vectorin.outputs[2], vector_vectorout.inputs[0])

    #vector_vectorin.Green -> vector_vectorout.Blue
    multidenoiser.links.new(vector_vectorin.outputs[1], vector_vectorout.inputs[2])

    #position_break.Y -> position_inv.Value
    multidenoiser.links.new(position_break.outputs[1], position_inv.inputs[0])

    #normal_inv.Value -> normal_combine.Z
    multidenoiser.links.new(normal_inv.outputs[0], normal_combine.inputs[2])

    #position_inv.Value -> position_combine.Z
    multidenoiser.links.new(position_inv.outputs[0], position_combine.inputs[2])

    #position_break.X -> position_combine.X
    multidenoiser.links.new(position_break.outputs[0], position_combine.inputs[0])

    #normal_break.Y -> normal_inv.Value
    multidenoiser.links.new(normal_break.outputs[1], normal_inv.inputs[0])

    #position_break.Z -> position_combine.Y
    multidenoiser.links.new(position_break.outputs[2], position_combine.inputs[1])

    #vector_vectorin.Alpha -> vector_vectorout.Green
    multidenoiser.links.new(vector_vectorin.outputs[3], vector_vectorout.inputs[1])

    #normal_break.Z -> normal_combine.Y
    multidenoiser.links.new(normal_break.outputs[2], normal_combine.inputs[1])

    #group_input_passes.Vetor -> vector_vectorin.Image
    multidenoiser.links.new(group_input_passes.outputs[2], vector_vectorin.inputs[0])

    #vector_vectorout.Image -> group_output_md.Vetor
    multidenoiser.links.new(vector_vectorout.outputs[0], group_output_md.inputs[2])

    #group_input_passes.Normal -> normal_break.Vector
    multidenoiser.links.new(group_input_passes.outputs[1], normal_break.inputs[0])

    #group_input_passes.Position -> position_break.Vector
    multidenoiser.links.new(group_input_passes.outputs[0], position_break.inputs[0])

    #normal_combine.Vector -> group_output_md.Normal
    multidenoiser.links.new(normal_combine.outputs[0], group_output_md.inputs[1])

    #position_combine.Vector -> group_output_md.Position
    multidenoiser.links.new(position_combine.outputs[0], group_output_md.inputs[0])

    return multidenoiser

#initialize PassMixer node group
def passmixer_node_group(context, operator, group_name):
    
    #enable use nodes
    bpy.context.scene.use_nodes = True

    passmixer = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    passmixer.color_tag = 'CONVERTER'
    passmixer.description = "A node group for mixing up the gloss, diff, trans and volume passes"

	#passmixer interface

    #Socket Opt_
    opt__socket = passmixer.interface.new_socket(name = "Opt_", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    opt__socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    opt__socket.attribute_domain = 'POINT'

    #Socket Direct
    direct_socket = passmixer.interface.new_socket(name = "Direct", in_out='INPUT', socket_type = 'NodeSocketColor')
    direct_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    direct_socket.attribute_domain = 'POINT'
    direct_socket.hide_value = True

    #Socket Indirect
    indirect_socket = passmixer.interface.new_socket(name = "Indirect", in_out='INPUT', socket_type = 'NodeSocketColor')
    indirect_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    indirect_socket.attribute_domain = 'POINT'
    indirect_socket.hide_value = True

    #Socket Color
    color_socket = passmixer.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
    color_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    color_socket.attribute_domain = 'POINT'
    color_socket.hide_value = True


    #initialize passmixer nodes
    #node PMR Group Output
    pmr_group_output = passmixer.nodes.new("NodeGroupOutput")
    pmr_group_output.label = "PMR Group Output"
    pmr_group_output.name = "PMR Group Output"
    pmr_group_output.use_custom_color = True
    pmr_group_output.color = COLORS_DICT["GRAY"]
    pmr_group_output.is_active_output = True
    pmr_group_output.inputs[1].hide = True

    #node PMR Group Input
    pmr_group_input = passmixer.nodes.new("NodeGroupInput")
    pmr_group_output.label = "PMR Group Input"
    pmr_group_input.name = "PMR Group Input"
    pmr_group_input.use_custom_color = True
    pmr_group_input.color = COLORS_DICT["GRAY"]
    pmr_group_input.outputs[3].hide = True

    #node add_passmixer
    add_passmixer = passmixer.nodes.new("CompositorNodeMixRGB")
    add_passmixer.label = "Add_PassMixer"
    add_passmixer.name = "add_passmixer"
    add_passmixer.use_custom_color = True
    add_passmixer.color = COLORS_DICT["BROWN"]
    add_passmixer.blend_type = 'ADD'
    add_passmixer.use_alpha = False
    add_passmixer.use_clamp = False
    add_passmixer.inputs[0].hide = True
    #Fac
    add_passmixer.inputs[0].default_value = 1.0

    #node multiply_passmixer
    multiply_passmixer = passmixer.nodes.new("CompositorNodeMixRGB")
    multiply_passmixer.label = "Multiply_PassMixer"
    multiply_passmixer.name = "multiply_passmixer"
    multiply_passmixer.use_custom_color = True
    multiply_passmixer.color = COLORS_DICT["BROWN"]
    multiply_passmixer.blend_type = 'MULTIPLY'
    multiply_passmixer.use_alpha = False
    multiply_passmixer.use_clamp = False
    multiply_passmixer.inputs[0].hide = True
    #Fac
    multiply_passmixer.inputs[0].default_value = 1.0


    #Set locations
    pmr_group_output.location = (280.0, 0.0)
    pmr_group_input.location = (-280.0, 0.0)
    add_passmixer.location = (-80.0, 0.0)
    multiply_passmixer.location = (100.0, 0.0)

    #Set dimensions
    pmr_group_output.width, pmr_group_output.height = 140.0, 100.0
    pmr_group_input.width, pmr_group_input.height = 140.0, 100.0
    add_passmixer.width, add_passmixer.height = 140.0, 100.0
    multiply_passmixer.width, multiply_passmixer.height = 154.79315185546875, 100.0

    #initialize passmixer links
    #add_passmixer.Image -> multiply_passmixer.Image
    passmixer.links.new(add_passmixer.outputs[0], multiply_passmixer.inputs[1])

    #pmr_group_input.Color -> multiply_passmixer.Image
    passmixer.links.new(pmr_group_input.outputs[2], multiply_passmixer.inputs[2])

    #pmr_group_input.Indirect -> add_passmixer.Image
    passmixer.links.new(pmr_group_input.outputs[1], add_passmixer.inputs[2])

    #pmr_group_input.Direct -> add_passmixer.Image
    passmixer.links.new(pmr_group_input.outputs[0], add_passmixer.inputs[1])

    #multiply_passmixer.Image -> pmr_group_output.Opt_
    passmixer.links.new(multiply_passmixer.outputs[0], pmr_group_output.inputs[0])

    return passmixer

#initialize LensDistortion node group
def lensdistortion_node(context, operator):

    #enable use nodes
    bpy.context.scene.use_nodes = True

    # variables
    scene = bpy.context.scene
    compositor_node_tree = scene.node_tree

    # Add Lens Distortion node
    lensdistortion_node = compositor_node_tree.nodes.new('CompositorNodeLensdist')

    # Get the Lens Distortion node
    lens_distortion_node = context.scene.node_tree.nodes.get("Lens Distortion")

    for node in context.scene.node_tree.nodes:
        if node.type == 'LENSDIST':
            # Adjust the distortion and dispersion values
            node.inputs[1].default_value = 0.01
            node.inputs[2].default_value = 0.005

            # Enable fit option
            node.use_fit = True

            # Set a custom color for the Lens Distortion node
            node.use_custom_color = True # Enable custom color
            node.color = COLORS_DICT["LIGHT_BLUE"] # Set to a red color (R, G, B)

    bpy.ops.node.select(deselect_all=True)

    return lensdistortion_node

#initialize FilmGrain node group
def film_grain_node_group(context, operator, group_name, image_path):

    #enable use nodes
    bpy.context.scene.use_nodes = True

    film_grain = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    film_grain.color_tag = 'FILTER'
    film_grain.description = "A custom node group for film grain effect"

	#film_grain interface
	#Socket Opt_
    opt__socket = film_grain.interface.new_socket(name = "Opt_", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    opt__socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    opt__socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket = film_grain.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Fac
    fac_socket = film_grain.interface.new_socket(name = "Fac", in_out='INPUT', socket_type = 'NodeSocketFloat')
    fac_socket.default_value = 0.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'


    #initialize film_grain nodes
    #node FG Group Output
    fg_group_output = film_grain.nodes.new("NodeGroupOutput")
    fg_group_output.label = "FG Group Output"
    fg_group_output.name = "FG Group Output"
    fg_group_output.use_custom_color = True
    fg_group_output.color = COLORS_DICT["GRAY"]
    fg_group_output.is_active_output = True
    fg_group_output.inputs[1].hide = True

    #node FG Group Input
    fg_group_input = film_grain.nodes.new("NodeGroupInput")
    fg_group_input.label = "FG Group Input"
    fg_group_input.name = "FG Group Input"
    fg_group_input.use_custom_color = True
    fg_group_input.color = COLORS_DICT["GRAY"]
    fg_group_input.outputs[2].hide = True

    #node image_film_grain
    image_film_grain = film_grain.nodes.new("CompositorNodeImage")
    image_film_grain.label = "FG Image"
    image_film_grain.name = "image_film_grain"
    image_film_grain.use_custom_color = True
    image_film_grain.color = COLORS_DICT["LIGHT_RED"]
    image_film_grain.frame_duration = 1
    image_film_grain.frame_offset = -1
    image_film_grain.frame_start = 1
    image_film_grain.use_auto_refresh = True
    image_film_grain.use_cyclic = False
    image_film_grain.use_straight_alpha_output = False
    image_film_grain.outputs[1].hide = True

    # Load the selected image and assign it to the image node
    try:
        image = bpy.data.images.load(image_path)
        image.colorspace_settings.name = 'ACEScg'
    except Exception as e:
        print("Error: unable to load image")
        print(e)

    if image is None:
        print("Error: image is null")
        return None

    image_film_grain.image = image

    #node overlay_film_grain
    overlay_film_grain = film_grain.nodes.new("CompositorNodeMixRGB")
    overlay_film_grain.label = "FG Overlay"
    overlay_film_grain.name = "overlay_film_grain"
    overlay_film_grain.use_custom_color = True
    overlay_film_grain.color = COLORS_DICT["BROWN"]
    overlay_film_grain.blend_type = 'OVERLAY'
    overlay_film_grain.use_alpha = False
    overlay_film_grain.use_clamp = False

    if image_film_grain is None:
        print("Error: image_film_grain is null")
        return None

    if fg_group_input is None:
        print("Error: group_input is null")
        return None

    if fg_group_output is None:
        print("Error: group_output is null")
        return None

    if overlay_film_grain is None:
        print("Error: overlay_film_grain is null")
        return None


    #Set locations
    fg_group_output.location = (238.55990600585938, 67.29718780517578)
    fg_group_input.location = (-142.61561584472656, 19.61834716796875)
    image_film_grain.location = (-304.08319091796875, -69.38165283203125)
    overlay_film_grain.location = (54.53009033203125, 67.29718780517578)

    #Set dimensions
    fg_group_output.width, fg_group_output.height = 140.0, 100.0
    fg_group_input.width, fg_group_input.height = 140.0, 100.0
    image_film_grain.width, image_film_grain.height = 300.8544921875, 100.0
    overlay_film_grain.width, overlay_film_grain.height = 140.0, 100.0

    #initialize film_grain links
    #image_film_grain.Image -> overlay_film_grain.Image
    try:
        film_grain.links.new(image_film_grain.outputs[0], overlay_film_grain.inputs[2])
    except Exception as e:
        print("Error: unable to create link between image_film_grain and overlay_film_grain")
        print(e)

    #fg_group_input.Image -> overlay_film_grain.Image
    try:
        film_grain.links.new(fg_group_input.outputs[0], overlay_film_grain.inputs[1])
    except Exception as e:
        print("Error: unable to create link between fg_group_input and overlay_film_grain")
        print(e)

    #overlay_film_grain.Image -> fg_group_output.Opt_
    try:
        film_grain.links.new(overlay_film_grain.outputs[0], fg_group_output.inputs[0])
    except Exception as e:
        print("Error: unable to create link between overlay_film_grain and group_output")
        print(e)

    #fg_group_input.Fac -> overlay_film_grain.Fac
    try:
        film_grain.links.new(fg_group_input.outputs[1], overlay_film_grain.inputs[0])
    except Exception as e:
        print("Error: unable to create link between fg_group_input and overlay_film_grain")
        print(e)

    return film_grain

#initialize Vignette node group
def vignette_node_group(context, operator, group_name, image_path):

    #enable use nodes
    bpy.context.scene.use_nodes = True

    vignette = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')

    vignette.color_tag = 'FILTER'
    vignette.description = "A custom node group for vignette effect"

	#vignette interface
	#Socket Opt_
    opt__socket = vignette.interface.new_socket(name = "Opt_", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    opt__socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    opt__socket.attribute_domain = 'POINT'

    #Socket Image
    image_socket = vignette.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Fac
    fac_socket = vignette.interface.new_socket(name = "Fac", in_out='INPUT', socket_type = 'NodeSocketFloat')
    fac_socket.default_value = 0.0
    fac_socket.min_value = 0.0
    fac_socket.max_value = 1.0
    fac_socket.subtype = 'FACTOR'
    fac_socket.attribute_domain = 'POINT'


    #initialize vignette nodes
    #node VIG Group Output
    vig_group_output = vignette.nodes.new("NodeGroupOutput")
    vig_group_output.label = "VIG Group Output"
    vig_group_output.name = "VIG Group Output"
    vig_group_output.use_custom_color = True
    vig_group_output.color = COLORS_DICT["GRAY"]
    vig_group_output.is_active_output = True
    vig_group_output.inputs[1].hide = True

    #node VIG Group Input
    vig_group_input = vignette.nodes.new("NodeGroupInput")
    vig_group_input.label = "VIG Group Input"
    vig_group_input.name = "VIG Group Input"
    vig_group_input.use_custom_color = True
    vig_group_input.color = COLORS_DICT["GRAY"]
    vig_group_input.outputs[2].hide = True
    
    #node image_vignette
    image_vignette = vignette.nodes.new("CompositorNodeImage")
    image_vignette.label = "VIG Image"
    image_vignette.name = "Image.012"
    image_vignette.use_custom_color = True
    image_vignette.color = COLORS_DICT["LIGHT_RED"]
    image_vignette.frame_duration = 1
    image_vignette.frame_offset = 39
    image_vignette.frame_start = 1
    image_vignette.use_auto_refresh = True
    image_vignette.use_cyclic = False
    image_vignette.use_straight_alpha_output = False
    image_vignette.outputs[1].hide = True

    # Load the selected image and assign it to the image node
    try:
        image = bpy.data.images.load(image_path)
        image.colorspace_settings.name = 'ACEScg'
    except Exception as e:
        print("Error: unable to load image")
        print(e)

    if image is None:
        print("Error: image is null")
        return None

    image_vignette.image = image

    #node multiply_vignette
    multiply_vignette = vignette.nodes.new("CompositorNodeMixRGB")
    multiply_vignette.label = "VIG Multiply"
    multiply_vignette.name = "multiply_vignette"
    multiply_vignette.use_custom_color = True
    multiply_vignette.color = COLORS_DICT["BROWN"]
    multiply_vignette.blend_type = 'MULTIPLY'
    multiply_vignette.use_alpha = False
    multiply_vignette.use_clamp = False

    if image_vignette is None:
        print("Error: image_vignette is null")
        return None

    if vig_group_input is None:
        print("Error: group_input is null")
        return None

    if vig_group_output is None:
        print("Error: group_output is null")
        return None

    if multiply_vignette is None:
        print("Error: multiply_vignette is null")
        return None


    #Set locations
    vig_group_output.location = (77.98977661132812, 6.222320556640625)
    vig_group_input.location = (-291.3733215332031, -39.500518798828125)
    image_vignette.location = (-420.0, -128.50051879882812)
    multiply_vignette.location = (-94.09931945800781, 6.222320556640625)

    #Set dimensions
    vig_group_output.width, vig_group_output.height = 140.0, 100.0
    vig_group_input.width, vig_group_input.height = 140.0, 100.0
    image_vignette.width, image_vignette.height = 268.69482421875, 100.0
    multiply_vignette.width, multiply_vignette.height = 140.0, 100.0

    #initialize vignette links
    #image_vignette.Image -> multiply_vignette.Image
    try:
        vignette.links.new(image_vignette.outputs[0], multiply_vignette.inputs[2])
    except Exception as e:
        print("Error: unable to create link between image_vignette and multiply_vignette")
        print(e)

    #vig_group_input.Image -> multiply_vignette.Image
    try:
        vignette.links.new(vig_group_input.outputs[0], multiply_vignette.inputs[1])
    except Exception as e:
        print("Error: unable to create link between vig_group_input and multiply_vignette")
        print(e)

    #multiply_vignette.Image -> vig_group_output.Opt_
    try:
        vignette.links.new(multiply_vignette.outputs[0], vig_group_output.inputs[0])
    except Exception as e:
        print("Error: unable to create link between multiply_vignette and vig_group_output")
        print(e)

    #vig_group_input.Fac -> multiply_vignette.Fac
    try:
        vignette.links.new(vig_group_input.outputs[1], multiply_vignette.inputs[0])
    except Exception as e:
        print("Error: unable to create link between vig_group_input and multiply_vignette")
        print(e)

    return vignette

#initialize Vignette-Basic node group
def vignette_basic_node_group(context, operator, group_name):
	
    #enable use nodes
    bpy.context.scene.use_nodes = True

    vignette_basic = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    vignette_basic.color_tag = 'FILTER'
    vignette_basic.description = "A custom node group for basic vignette effect"

	#vignette_basic interface
	#Socket Opt_
    opt__socket = vignette_basic.interface.new_socket(name = "Opt_", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    opt__socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    opt__socket.attribute_domain = 'POINT'
	
    #Socket Image
    image_socket = vignette_basic.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'

    #Socket Amount
    amount_socket = vignette_basic.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
    amount_socket.default_value = 1.0
    amount_socket.min_value = 0.0
    amount_socket.max_value = 1.0
    amount_socket.subtype = 'FACTOR'
    amount_socket.attribute_domain = 'POINT'

    #Socket Distortion
    distortion_socket = vignette_basic.interface.new_socket(name = "Distortion", in_out='INPUT', socket_type = 'NodeSocketFloat')
    distortion_socket.default_value = 1.0
    distortion_socket.min_value = -0.9990000128746033
    distortion_socket.max_value = 1.0
    distortion_socket.subtype = 'NONE'
    distortion_socket.attribute_domain = 'POINT'
	
	
    #initialize vignette_basic nodes
    #node VB Group Output
    vb_group_output = vignette_basic.nodes.new("NodeGroupOutput")
    vb_group_output.label = "VB Group Output"
    vb_group_output.name = "VB Group Output"
    vb_group_output.use_custom_color = True
    vb_group_output.color = COLORS_DICT["GRAY"]
    vb_group_output.is_active_output = True
    vb_group_output.inputs[1].hide = True

    #node VB Group Input
    vb_group_input = vignette_basic.nodes.new("NodeGroupInput")
    vb_group_input.label = "VB Group Input"
    vb_group_input.name = "VB Group Input"
    vb_group_input.use_custom_color = True
    vb_group_input.color = COLORS_DICT["GRAY"]
    vb_group_input.outputs[3].hide = True

    #node VB Multiply
    vb_multiply = vignette_basic.nodes.new("CompositorNodeMixRGB")
    vb_multiply.label = "VB Multiply"
    vb_multiply.name = "VB Multiply"
    vb_multiply.use_custom_color = True
    vb_multiply.color = COLORS_DICT["BROWN"]
    vb_multiply.blend_type = 'MULTIPLY'
    vb_multiply.use_alpha = False
    vb_multiply.use_clamp = False

    #node VB Blur
    vb_blur = vignette_basic.nodes.new("CompositorNodeBlur")
    vb_blur.label = "VB Blur"
    vb_blur.name = "VB Blur"
    vb_blur.use_custom_color = True
    vb_blur.color = COLORS_DICT["DARK_PURPLE"]
    vb_blur.aspect_correction = 'NONE'
    vb_blur.factor = 0.0
    vb_blur.factor_x = 15.0
    vb_blur.factor_y = 15.0
    vb_blur.filter_type = 'FAST_GAUSS'
    vb_blur.size_x = 20
    vb_blur.size_y = 20
    vb_blur.use_bokeh = False
    vb_blur.use_extended_bounds = False
    vb_blur.use_gamma_correction = False
    vb_blur.use_relative = True
    vb_blur.use_variable_size = False
    #Size
    vb_blur.inputs[1].default_value = 1.0

    #node VB Greater Than
    vb_greater_than = vignette_basic.nodes.new("CompositorNodeMath")
    vb_greater_than.label = "VB Greater Than"
    vb_greater_than.name = "VB Greater Than"
    vb_greater_than.use_custom_color = True
    vb_greater_than.color = COLORS_DICT["DARK_BLUE"]
    vb_greater_than.operation = 'GREATER_THAN'
    vb_greater_than.use_clamp = False
    #Value_001
    vb_greater_than.inputs[1].default_value = 0.0

    #node VB Lens Distortion
    vb_lens_distortion = vignette_basic.nodes.new("CompositorNodeLensdist")
    vb_lens_distortion.label = "VB Lens Distortion"
    vb_lens_distortion.name = "VB Lens Distortion"
    vb_lens_distortion.use_custom_color = True
    vb_lens_distortion.color = COLORS_DICT["LIGHT_BLUE"]
    vb_lens_distortion.use_fit = False
    vb_lens_distortion.use_jitter = False
    vb_lens_distortion.use_projector = False
    #Dispersion
    vb_lens_distortion.inputs[2].default_value = 0.0


    #Set locations
    vb_group_output.location = (440.0, 90.0)
    vb_group_input.location = (-520.0, 0.0)
    vb_multiply.location = (274.06396484375, 90.0)
    vb_blur.location = (60.0, -80.0)
    vb_greater_than.location = (-120.0, -80.0)
    vb_lens_distortion.location = (-300.0, -80.0)

    #Set dimensions
    vb_group_output.width, vb_group_output.height = 140.0, 100.0
    vb_group_input.width, vb_group_input.height = 140.0, 100.0
    vb_multiply.width, vb_multiply.height = 140.0, 100.0
    vb_blur.width, vb_blur.height = 140.0, 100.0
    vb_greater_than.width, vb_greater_than.height = 144.892578125, 100.0
    vb_lens_distortion.width, vb_lens_distortion.height = 148.128173828125, 100.0
	
    #initialize vignette_basic links
    #vb_blur.Image -> vb_multiply.Image
    vignette_basic.links.new(vb_blur.outputs[0], vb_multiply.inputs[2])

    #vb_greater_than.Value -> vb_blur.Image
    vignette_basic.links.new(vb_greater_than.outputs[0], vb_blur.inputs[0])

    #vb_lens_distortion.Image -> vb_greater_than.Value
    vignette_basic.links.new(vb_lens_distortion.outputs[0], vb_greater_than.inputs[0])

    #vb_group_input.Image -> vb_multiply.Image
    vignette_basic.links.new(vb_group_input.outputs[0], vb_multiply.inputs[1])

    #vb_group_input.Image -> vb_lens_distortion.Image
    vignette_basic.links.new(vb_group_input.outputs[0], vb_lens_distortion.inputs[0])

    #vb_multiply.Image -> vb_group_output.Opt_
    vignette_basic.links.new(vb_multiply.outputs[0], vb_group_output.inputs[0])

    #vb_group_input.Distortion -> vb_lens_distortion.Distortion
    vignette_basic.links.new(vb_group_input.outputs[2], vb_lens_distortion.inputs[1])

    #vb_group_input.Amount -> vb_multiply.Fac
    vignette_basic.links.new(vb_group_input.outputs[1], vb_multiply.inputs[0])

    return vignette_basic
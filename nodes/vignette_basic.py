import bpy
from functions import COLORS_DICT

#initialize Vignette-Basic node group
def vignette_basic_node_group(context, operator, group_name):
	
    #enable use nodes
    bpy.context.scene.use_nodes = True

    vignette_basic = bpy.data.node_groups.new(group_name, 'CompositorNodeTree')
    
    vignette_basic.color_tag = 'FILTER'
    vignette_basic.default_group_node_width = 165
    vignette_basic.description = "A custom node group for basic vignette effect"

	#vignette_basic interface
	#Socket Image
    image_socket = vignette_basic.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
    image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
    image_socket.attribute_domain = 'POINT'
	
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
    vb_group_output.color = COLORS_DICT["DARK_GRAY"]
    vb_group_output.is_active_output = True
    vb_group_output.inputs[1].hide = True

    #node VB Group Input
    vb_group_input = vignette_basic.nodes.new("NodeGroupInput")
    vb_group_input.label = "VB Group Input"
    vb_group_input.name = "VB Group Input"
    vb_group_input.use_custom_color = True
    vb_group_input.color = COLORS_DICT["DARK_GRAY"]
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

    #vb_multiply.Image -> vb_group_output.Image
    vignette_basic.links.new(vb_multiply.outputs[0], vb_group_output.inputs[0])

    #vb_group_input.Distortion -> vb_lens_distortion.Distortion
    vignette_basic.links.new(vb_group_input.outputs[2], vb_lens_distortion.inputs[1])

    #vb_group_input.Amount -> vb_multiply.Fac
    vignette_basic.links.new(vb_group_input.outputs[1], vb_multiply.inputs[0])

    return vignette_basic
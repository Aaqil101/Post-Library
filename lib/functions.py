import bpy
from dictionaries import (COLORS_DICT)

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
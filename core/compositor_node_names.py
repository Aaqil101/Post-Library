class CompositorNodeNames:
    """
    Class to store the names of every nodes and other items used in the Blender Compositor.
    """
    # Input Nodes
    RENDER_LAYERS = "CompositorNodeRLayers"
    IMAGE = "CompositorNodeImage"
    MASK = "CompositorNodeMask"
    MOVIE_CLIP = "CompositorNodeMovieClip"
    TEXTURE = "CompositorNodeTexture"
    BOKEH_IMAGE = "CompositorNodeBokehImage"
    TRACK_POSITION = "CompositorNodeTrackPos"
    TIME = "CompositorNodeTime"

    # Output Nodes
    COMPOSITE = "CompositorNodeComposite"
    VIEWER = "CompositorNodeViewer"
    FILE_OUTPUT = "CompositorNodeOutputFile"
    LEVELS = "CompositorNodeLevels"

    # Color Nodes
    BRIGHT_CONTRAST = "CompositorNodeBrightContrast"
    HUE_SATURATION = "CompositorNodeHueSat"
    GAMMA = "CompositorNodeGamma"
    INVERT = "CompositorNodeInvert"
    MIX_RGB = "CompositorNodeMixRGB"
    Z_COMBINE = "CompositorNodeZcombine"
    COLOR_BALANCE = "CompositorNodeColorBalance"
    TONE_MAP = "CompositorNodeTonemap"
    COLOR_CORRECTION = "CompositorNodeColorCorrection"
    ALPHA_OVER = "CompositorNodeAlphaOver"

    # Filter Nodes
    BLUR = "CompositorNodeBlur"
    FILTER = "CompositorNodeFilter"
    DILATE_ERODE = "CompositorNodeDilateErode"
    BILATERAL_BLUR = "CompositorNodeBilateralblur"
    DESPECKLE = "CompositorNodeDespeckle"
    DEFOCUS = "CompositorNodeDefocus"
    GLARE = "CompositorNodeGlare"
    LENS_DISTORTION = "CompositorNodeLensdist"
    DENOISE = "CompositorNodeDenoise"

    # Converter Nodes
    MATH = "CompositorNodeMath"
    MIX_RGB = "CompositorNodeMixRGB"
    SEPARATE_RGB = "CompositorNodeSeparateRGB"
    COMBINE_RGB = "CompositorNodeCombineRGB"
    SEPARATE_HSVA = "CompositorNodeSeparateHSVA"
    COMBINE_HSVA = "CompositorNodeCombineHSVA"
    SEPARATE_XYZ = "CompositorNodeSeparateXYZ"
    COMBINE_XYZ = "CompositorNodeCombineXYZ"
    MAP_VALUE = "CompositorNodeMapValue"
    MAP_RANGE = "CompositorNodeMapRange"
    NORMALIZE = "CompositorNodeNormalize"

    # Vector Nodes
    MAP_UV = "CompositorNodeMapUV"
    DISPLACE = "CompositorNodeDisplace"
    VECTOR_BLUR = "CompositorNodeVectorBlur"

    # Matte Nodes
    KEYING = "CompositorNodeKeying"
    KEYING_SCREEN = "CompositorNodeKeyingScreen"
    LUMINANCE_KEY = "CompositorNodeLumaMatte"
    CHROMA_KEY = "CompositorNodeChromaMatte"
    COLOR_SPILL = "CompositorNodeColorSpill"

    # Distort Nodes
    SCALE = "CompositorNodeScale"
    ROTATE = "CompositorNodeRotate"
    TRANSLATE = "CompositorNodeTranslate"
    TRANSFORM = "CompositorNodeTransform"
    CROP = "CompositorNodeCrop"
    LENS_DISTORTION = "CompositorNodeLensdist"

    # Layout Nodes
    FRAME = "NodeFrame"
    REROUTE = "NodeReroute"

    # Group Nodes
    GROUP_INPUT = "NodeGroupInput"
    GROUP_OUTPUT = "NodeGroupOutput"
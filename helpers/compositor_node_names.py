from dataclasses import dataclass


@dataclass
class CompositorNodeNames:
    """
    Class to store the names of every nodes and other items used in the Blender Compositor.
    """

    # Input
    BOKEH_IMAGE: str = "CompositorNodeBokehImage"
    IMAGE: str = "CompositorNodeImage"
    MASK: str = "CompositorNodeMask"
    MOVIE_CLIP: str = "CompositorNodeMovieClip"
    TEXTURE: str = "CompositorNodeTexture"
    GROUP_INPUT: str = "NodeGroupInput"

    # Input.Constant
    RGB: str = "CompositorNodeRGB"
    VALUE: str = "CompositorNodeValue"

    # Input.Scene
    RENDER_LAYERS: str = "CompositorNodeRLayers"
    SCENE_TIME: str = "CompositorNodeSceneTime"
    TIME: str = "CompositorNodeTime"

    # Output
    COMPOSITE: str = "CompositorNodeComposite"
    VIEWER: str = "CompositorNodeViewer"
    FILE_OUTPUT: str = "CompositorNodeOutputFile"
    GROUP_OUTPUT: str = "NodeGroupOutput"

    # Color
    ALPHA_CONVERT: str = "CompositorNodePremulKey"
    COLOR_RAMP: str = "CompositorNodeValToRGB"
    CONVERT_COLOR_SPACE: str = "CompositorNodeConvertColorSpace"
    SET_ALPHA: str = "CompositorNodeSetAlpha"
    INVERT_COLOR: str = "CompositorNodeInvert"
    RGB_TO_BW: str = "CompositorNodeRGBToBW"

    # Color.Adjust
    BRIGHT_CONTRAST: str = "CompositorNodeBrightContrast"
    COLOR_BALANCE: str = "CompositorNodeColorBalance"
    COLOR_CORRECTION: str = "CompositorNodeColorCorrection"
    EXPOSURE: str = "CompositorNodeExposure"
    GAMMA: str = "CompositorNodeGamma"
    HUE_CORRECT: str = "CompositorNodeHueCorrect"
    HUE_SATURATION_VALUE: str = "CompositorNodeHueSat"
    RGB_CURVE: str = "CompositorNodeCurveRGB"
    TONE_MAP: str = "CompositorNodeTonemap"

    # Color.Mix
    ALPHA_OVER: str = "CompositorNodeAlphaOver"
    COMBINE_COLOR: str = "CompositorNodeCombineColor"
    SEPARATE_COLOR: str = "CompositorNodeSeparateColor"
    MIX_RGB: str = "CompositorNodeMixRGB"
    Z_COMBINE: str = "CompositorNodeZcombine"

    # Filter
    ANTI_ALIASING: str = "CompositorNodeAntiAliasing"
    DENOISE: str = "CompositorNodeDenoise"
    DESPECKLE: str = "CompositorNodeDespeckle"
    DILATE_ERODE: str = "CompositorNodeDilateErode"
    INPAINT: str = "CompositorNodeInpaint"
    FILTER: str = "CompositorNodeFilter"
    GLARE: str = "CompositorNodeGlare"
    KUWAHARA: str = "CompositorNodeKuwahara"
    PIXELATE: str = "CompositorNodePixelate"
    POSTERIZE: str = "CompositorNodePosterize"
    SUN_BEAMS: str = "CompositorNodeSunBeams"

    # Filter.Blur
    BILATERAL_BLUR: str = "CompositorNodeBilateralblur"
    BLUR: str = "CompositorNodeBlur"
    BOKEH_BLUR: str = "CompositorNodeBokehBlur"
    DEFOCUS: str = "CompositorNodeDefocus"
    DIRECTIONAL_BLUR: str = "CompositorNodeDBlur"
    VECTOR_BLUR: str = "CompositorNodeVecBlur"

    # Keying
    CHANNEL_KEY: str = "CompositorNodeChannelMatte"
    CHROMA_KEY: str = "CompositorNodeChromaMatte"
    COLOR_KEY: str = "CompositorNodeColorMatte"
    COLOR_SPILL: str = "CompositorNodeColorSpill"
    DIFFERENCE_KEY: str = "CompositorNodeDiffMatte"
    DISTANCE_KEY: str = "CompositorNodeDistanceMatte"
    KEYING: str = "CompositorNodeKeying"
    KEYING_SCREEN: str = "CompositorNodeKeyingScreen"
    LUMINANCE_KEY: str = "CompositorNodeLumaMatte"

    # Mask
    CRYPTO_MATTE_V2: str = "CompositorNodeCryptomatteV2"
    CRYPTO_MATTE: str = "CompositorNodeCryptomatte"
    BOX_MASK: str = "CompositorNodeBoxMask"
    ELLIPSE_MASK: str = "CompositorNodeEllipseMask"
    DOUBLE_EDGE_MASK: str = "CompositorNodeDoubleEdgeMask"
    ID_MASK: str = "CompositorNodeIDMask"

    # Tracking
    PLANE_TRACK_DEFORM: str = "CompositorNodePlaneTrackDeform"
    STABILIZE: str = "CompositorNodeStabilize"
    TRACK_POSITION: str = "CompositorNodeTrackPos"

    # Transform
    ROTATE: str = "CompositorNodeRotate"
    SCALE: str = "CompositorNodeScale"
    TRANSFORM: str = "CompositorNodeTransform"
    TRANSLATE: str = "CompositorNodeTranslate"
    CORNER_PIN: str = "CompositorNodeCornerPin"
    CROP: str = "CompositorNodeCrop"
    DISPLACE: str = "CompositorNodeDisplace"
    FLIP: str = "CompositorNodeFlip"
    MAP_UV: str = "CompositorNodeMapUV"
    LENS_DISTORTION: str = "CompositorNodeLensdist"
    MOVIE_DISTORTION: str = "CompositorNodeMovieDistortion"

    # Utilities
    MAP_RANGE: str = "CompositorNodeMapRange"
    MAP_VALUE: str = "CompositorNodeMapValue"
    MATH: str = "CompositorNodeMath"
    LEVELS: str = "CompositorNodeLevels"
    NORMALIZE: str = "CompositorNodeNormalize"
    SPLIT: str = "CompositorNodeSplit"
    SWITCH: str = "CompositorNodeSwitch"
    SWITCH_STEREO_VIEW: str = "CompositorNodeSwitchView"

    # Vector
    COMBINE_XYZ: str = "CompositorNodeCombineXYZ"
    SEPARATE_XYZ: str = "CompositorNodeSeparateXYZ"
    NORMAL: str = "CompositorNodeNormal"
    VECTOR_CURVE: str = "CompositorNodeCurveVec"

    # Other
    CUSTOM_GROUP: str = "CompositorNodeCustomGroup"
    FRAME = "NodeFrame"
    GROUP: str = "CompositorNodeGroup"
    REROUTE = "NodeReroute"
    TREE: str = "CompositorNodeTree"

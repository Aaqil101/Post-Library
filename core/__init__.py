from importlib import reload

from .filter_node_manager import (
    FilterNodeNames, FilterNodeManager, GlareSettings, GlareType, GlareQuality, 
    BlurSettings, BlurAspectCorrection, BlurFilterType
)
from .color_node_manager import (ColorNodeNames, ColorNodeManager, MixColorSettings, BlendType, HueSatSettings)
from .layout_node_manager import (LayoutNodeNames, LayoutNodeManager, FrameSettings, RerouteSettings)
from .utilities_node_manager import (UtilitiesNodeNames, UtilitiesNodeManager, SwitchSettings)
from .input_node_manager import (InputNodeNames, InputNodeManager, GroupInputSettings)
from .compositor_node_names import CompositorNodeNames

# Proper __all__ definition as strings
__all__ = [
    "FilterNodeNames", "FilterNodeManager", "GlareSettings", "GlareType", "GlareQuality", 
    "BlurSettings", "BlurAspectCorrection", "BlurFilterType",
    "ColorNodeNames", "ColorNodeManager", "MixColorSettings", "BlendType", "HueSatSettings",
    "LayoutNodeNames", "LayoutNodeManager", "FrameSettings", "RerouteSettings",
    "UtilitiesNodeNames", "UtilitiesNodeManager", "SwitchSettings",
    "InputNodeNames", "InputNodeManager", "GroupInputSettings",
    "CompositorNodeNames"
]

# Reload modules if needed (this is optional and mainly useful for development)
from . import (filter_node_manager, color_node_manager, layout_node_manager, utilities_node_manager, input_node_manager, compositor_node_names)

reload(filter_node_manager)
reload(color_node_manager)
reload(layout_node_manager)
reload(utilities_node_manager)
reload(input_node_manager)
reload(compositor_node_names)
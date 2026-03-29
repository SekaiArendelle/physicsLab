"""Python API for Physics-Lab-AR"""

from .physicsLab_version import __version__

from .coordinate_system import *

from .enums import ExperimentType, Category, Tag, OpenMode, ColorOfWire, GetUserMode

from .circuit import *
from .celestial import *
from .electromagnetism import *

# Custom exception classes defined by `physicsLab`.
from .errors import *

from physicsLab.quantum_physics import *
from physicsLab.utils import *

from physicsLab import web

from enum import Enum

from n64tex.formats.rgba import RGBAImage
from n64tex.formats.rgba5551 import RGBA5551Image

class Formats(Enum):
    rgba = RGBAImage
    rgba5551 = RGBA5551Image
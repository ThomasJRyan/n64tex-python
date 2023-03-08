from enum import Enum

from n64tex.formats.i4 import I4Image
from n64tex.formats.rgba import RGBAImage
from n64tex.formats.rgba5551 import RGBA5551Image

class Formats(Enum):
    i4 = I4Image
    rgba = RGBAImage
    rgba5551 = RGBA5551Image
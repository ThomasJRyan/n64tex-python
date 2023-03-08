from typing import TypeVar, TYPE_CHECKING
from abc import ABC, abstractclassmethod

import numpy as np
from PIL import Image

T = TypeVar("T", bound="BaseImage")

if TYPE_CHECKING:
    from n64tex.formats import RGBAImage, RGBA5551Image, I4Image, I8Image


class BaseImage(ABC):
    """Base class to derive image format classes from"""

    def __init__(self, data_array: np.array, width: int, height: int):
        """Initializer that takes in Numpy array, width, and height. This
           shouldn't be called directly unless you know what you're doing.
           Instead, you should call either the `from_image` or `from_bytes`
           class methods.

        Args:
            data_array (np.array): Numpy array
            width (int): Width of image
            height (int): Height of image
        """
        self.data_array = data_array
        self.width = width
        self.height = height

    @abstractclassmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int):
        ...

    @classmethod
    def from_image(cls, image: Image, width: int = None, height: int = None) -> T:
        """Takes a PIL Image and converts it to an object that can be
           converted to other formats.

        Args:
            image (PIL.Image): PIL Image object
            width (int, optional): Optional width, will default to the Image's width
            height (int, optional): Optional height, will default to the Image's height

        Returns:
            T: Formatted Object derived from Image object
        """
        if width is None:
            width = image.width
        if height is None:
            height = image.height

        # TODO: I *hate* this. If anyone sees this and has a better way to do it please have a crack at it
        from n64tex.formats.rgba import RGBAImage

        if not issubclass(cls, RGBAImage):
            return RGBAImage.from_image(image, width, height).convert_to(cls)

        return cls.from_bytes(image.tobytes(), width, height)

    def save(self, filename: str):
        """Saves Format Object to a file using PIL

        Args:
            filename (str): Filename to save to
        """
        if hasattr(self, "to_rgba"):
            image = Image.fromarray(self.to_rgba().data_array)
        else:
            image = Image.fromarray(self.data_array)
        image.save(filename)

    def to_rgba5551(self) -> "RGBA5551Image":
        """Convert to RGBA5551Image

        Returns:
            RGBA5551Image: Converted RGBA5551Image object
        """
        return self.to_rgba().to_rgba5551()

    def to_i4(self) -> "I4Image":
        """Convert to I4Image

        Returns:
            I4Image: Converted I4Image object
        """
        return self.to_rgba().to_i4()

    def to_i8(self) -> "I8Image":
        """Convert to I8Image

        Returns:
            I8Image: Converted I8Image object
        """
        return self.to_rgba().to_i8()

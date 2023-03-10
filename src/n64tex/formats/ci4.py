from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBAImage

import numpy as np

from n64tex.formats.base import BaseImage

class CI4Image(BaseImage):
    """CI4 Image format. Each pixel is 4 bits long, which are pointers to an array of RGBA5551 colours
    
    The image follows this format:
    
    PPPP
    
    Where: 
        P = Address of colour in RGBA5551 array
        
    
    The RGBA5551 array (colour palette) follows this format:
    
    RRRRR GGGGG BBBBB A

    Where:
        R = Red channel from 0-31
        G = Green channel from 0-31
        B = Blue channel from 0-31
        A = Alpha channel from 0-1
    """
    
    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int, palette_bytes: bytes) -> "CI4Image":
        """Generate an CI4Image from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image
            palette_bytes (bytes): Colour palette bytes to use with this image

        Returns:
            CI4Image: CI4Image object
        """
        # Image pointers
        split_bytes = lambda x: ((x & 0xF0) >> 4, x & 0x0F)
        data_array = np.frombuffer(raw_bytes, dtype=">u1")
        data_array = np.ravel(np.column_stack(split_bytes(data_array)))
        data_array = np.resize(data_array, (height, width))
        
        # Image palette
        palette = np.frombuffer(palette_bytes, dtype=">u2")
        
        return cls(data_array, width, height, palette)
    
    def to_rgba(self) -> "RGBAImage":
        """Converts CI4Image to RGBAImage

        Returns:
            RGBAImage: Converted RGBAImage object
        """

        def rgba5551_to_rgba(rgba5551_value):
            r = (rgba5551_value & 0xF800) >> 8
            g = (rgba5551_value & 0x7C0) >> 3
            b = (rgba5551_value & 0x3E) << 2
            a = 255 if rgba5551_value & 0x1 else 0
            return r, g, b, a
        
        rgba_5551_data_array = self.palette.copy()

        palette_data_array = list()
        for pixel_colour in rgba_5551_data_array:
            palette_data_array.append(rgba5551_to_rgba(pixel_colour))
                
        rgba_data_array = list()
        for pointer in self.data_array.flatten():
            rgba_data_array.append(palette_data_array[pointer])
            
        rgba_data_array = np.array(rgba_data_array, dtype=">u1")
        rgba_data_array = np.resize(rgba_data_array, (self.height, self.width, 4))
        
        from n64tex.formats.rgba import RGBAImage

        return RGBAImage(rgba_data_array, self.width, self.height, self.palette)
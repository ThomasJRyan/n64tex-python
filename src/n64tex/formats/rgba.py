from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from n64tex.formats import RGBA5551Image

import numpy as np

from n64tex.formats.base import BaseImage

class RGBAImage(BaseImage):
    """RGBA Image format. Each pixel is 32 bits long and follow this format
    
        RRRRRRRR GGGGGGGG BBBBBBBB AAAAAAAA
        
        Where:
            R = Red channel from 0-255
            G = Green channel from 0-255
            B = Blue channel from 0-255
            A = Alpha channel from 0-255
    """
    @classmethod
    def from_bytes(cls, raw_bytes: bytes, width: int, height: int) -> 'RGBAImage':
        """Generate an RGBAImage from byte data

        Args:
            raw_bytes (bytes): Raw byte data to use
            width (int): Width of image
            height (int): Height of image

        Returns:
            RGBAImage: RGBAImage object
        """
        data_array = np.frombuffer(raw_bytes, dtype='>u1')
        data_array = np.resize(data_array, (height, width, 4))
        return cls(data_array, width, height)
    
    def to_rgba5551(self) -> 'RGBA5551Image':
        """Converts RGBAImage to RGBA5551Image

        Returns:
            RGBA5551Image: Converted RGBA5551Image object
        """
        def rgba_to_rgba5551(rgba_value):
            rgba_value[0] = (rgba_value[0] >> 3) << 11
            rgba_value[1] = (rgba_value[1] >> 3) << 6
            rgba_value[2] = (rgba_value[2] >> 3) << 1
            rgba_value[3] = 1 if rgba_value[3] == 255 else 0
            
        rgba_5551_data_array = self.data_array.copy()
        rgba_5551_data_array = rgba_5551_data_array.astype(np.uint16)
        
        for pixel_row in rgba_5551_data_array:
            for pixel_colour in pixel_row:
                rgba_to_rgba5551(pixel_colour)
                
        rgba_5551_data_array = np.sum(rgba_5551_data_array, axis=2)
        rgba_5551_data_array = rgba_5551_data_array.astype(np.uint16)
                
        from n64tex.formats.rgba5551 import RGBA5551Image
        return RGBA5551Image(rgba_5551_data_array, self.width, self.height)
    

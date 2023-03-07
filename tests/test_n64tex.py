import unittest

import numpy as np

from n64tex.formats import RGBAImage, RGBA5551Image


class TestRGBAImage(unittest.TestCase):
    def setUp(self) -> None:
        self.image = RGBAImage.from_bytes(
            raw_bytes=b"\xff\x00\x00\xff\x00\xff\x00\xff\x00\x00\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00",
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array(
                    [
                        [[255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255]],
                        [[0, 0, 0, 255], [255, 255, 255, 255], [255, 255, 255, 0]],
                    ],
                    dtype=np.uint8,
                )
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.data_array.tobytes(),
            b"\xff\x00\x00\xff\x00\xff\x00\xff\x00\x00\xff\xff\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00",
        )

    def test_conversion_to_rgba5551(self):
        self.assertTrue(
            (
                self.image.to_rgba5551().data_array
                == np.array([[63489, 1985, 63], [1, 65535, 65534]], dtype=np.uint16)
            ).all()
        )


class TestRGBA5551Image(unittest.TestCase):
    def setUp(self) -> None:
        self.image = RGBA5551Image.from_bytes(
            raw_bytes=b'\xf8\x01\x07\xc1\x00?\x00\x01\xff\xff\xff\xfe',
            width=3,
            height=2,
        )
        return super().setUp()

    def test_data_array(self):
        self.assertTrue(
            (
                self.image.data_array
                == np.array([[63489, 1985, 63], [1, 65535, 65534]], dtype=np.uint16)
            ).all(),
        )

    def test_bytes(self):
        self.assertEqual(
            self.image.data_array.tobytes(),
            b'\xf8\x01\x07\xc1\x00?\x00\x01\xff\xff\xff\xfe',
        )

    def test_conversion_to_rgba(self):
        self.assertTrue(
            (
                self.image.to_rgba().data_array
                == np.array(
                    [
                        [[248, 0, 0, 255], [0, 248, 0, 255], [0, 0, 248, 255]],
                        [[0, 0, 0, 255], [248, 248, 248, 255], [248, 248, 248, 0]],
                    ],
                    dtype=np.uint8,
                )
            ).all()
        )


class TestI4Image(unittest.TestCase):
    pass


class TestI8Image(unittest.TestCase):
    pass


class TestIA4Image(unittest.TestCase):
    pass


class TestIA8Image(unittest.TestCase):
    pass


class TestIA16Image(unittest.TestCase):
    pass


class TestCI4Image(unittest.TestCase):
    pass


class TestCI8Image(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()

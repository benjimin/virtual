import unittest

from . import virtual

import numpy as np
import tempfile
import rasterio

class TestVirtualProducts(unittest.TestCase):

    def test_geotiff(self):
        size = 5
        data = np.random.rand(size, size, dtype=np.float32)

        geobox =

        with tempfile.NamedTemporaryFile() as file:

            with rasterio.open(file,
                               driver='GTIFF',
                               width=size,
                               height=size,
                               count=1,
                               dtype=data.dtype,
                               ) as f:





with open('delme.tif', 'w+b') as f:

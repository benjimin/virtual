import datacube.utils.geometry


"""
def LoadableBase:
    self.geobox = None
    def array(self):
        raise NotImplemented
    def coords(self):
        from xarray import IndexVariable as iv
        c = self.geobox.coords
        return [iv(dims=x, data=c[x].values, attrs=dict(units=c[x].units))
                for x in self.geobox.dims]
"""



class VirtualBase:
    measurements = None
    spatial_extent = None
    temporal_range = None
    default_crs = datacube.utils.geometry.CRS('epsg:3577')
    default_resolution = (-25, 25)
    def __call__(self, lat=None, lon=None, time=None, geobox=None):
        """ Convert spatiotemporal extent to xarray data """
        assert (lat is None) == (lon is None) != (geobox is None)
        if geobox is None:
            geobox =

        return self.load(geobox, time)
    def load(self, geobox, timespan):
        """ Produce xarray from sequence of layers (indices and specifications) """
        import xarray
        def coord(x, iv=xarray.IndexVariable):
            c = geobox.coords[x]
            return iv(x, c.values, attrs=dict(units=c.units))
        coords = [coord(x) for x in geobox.dims]
        def present(key, details):
            array = self.load_layer(geobox, details)
            return xarray.DataArray(array, coords=coords, name=key,
                                    attrs=dict(crs=geobox.crs))
        layers = self.find(geobox, timespan)
        return xarray.concat([present(*z) for z in layers])
    def load_layer(self, geobox, details):
        """ Load numpy array from specification """
        raise NotImplemented
    def find(self, geobox, timespan):
        """ Produce indexed sequence data layer descriptors """
        raise NotImplemented

class TraditionalProduct(VirtualBase):
    datacube = None
    def __init__(self, product, datacube=None):
        self.product = product
        import datacube as odc
        if datacube is None:
            self.datacube = odc.DataCube()
        else:
            import mock
            host, database = datacube
            raise NotImplemented
    def load(self, geobox, timespan):
        return self.datacube.load(product=self.product,
                                  geobox=geobox,
                                  time=timespan)


class TimelessBase(VirtualBase):
    def find(**args):
        return [(None,None)]

class RasterFile(TimelessBase):
    def __init__(self, filename):
        self.path = filename
    def load_layer(self, geobox, _):
        import rasterio
        with rasterio.open(self.path) as src:
            assert src.indexes == (1,) # only support single-band
            if geobox is None:
                from datacube.utils.geometry import GeoBox, CRS
                geobox = GeoBox(src.width, src.height, src.affine,
                                CRS(src.crs.wkt))
                array = src.read(1)
            else:
                band = rasterio.band(src, 1)
                array = np.empty((geobox.height, geobox.width),
                                 dtype = band.dtype)
                rasterio.warp.reproject(source=band,
                                        destination=array,
                                        dst_crs=geobox.crs.crs_str,
                                        dst_transform=geobox.affine,
                                        dst_nodata=None)
        return array

class VectorFile(TimelessBase):
    def __init__(self, filename):
        self.path = filename
    def load_table(self):
        import geopandas
        return geopandas.read_file(self.path)
    def load_layer(self, geobox, _):
        from rasterio.features import rasterize
        table = self.load_table().to_crs(geobox.crs._crs.ExportToProj4())
        array = rasterize(shapes=table.geometry,
                          out_shape=(geobox.height, geobox.width),
                          transform=geobox.affine)
        return array


class CompositeProduct(VirtualBase):
    def __init__(self, products, join='inner'):
        assert join in {'inner', 'outer'}
        self.products = products
        self.measurements = [x for p in self.products for x in p.measurements]

class CollectiveProduct(VirtualBase):
    def __init__(self, products):
        self.products = products
        self.measurements = set.intersection(set(p.measurements) for p in self.products)
    def find(self, geobox, timespan):
        # todo: use heapq.merge to preserve order
        return [layer for p in self.products
                      for layer in p.find(geobox, timespan)]
    def load(self, geobox, timespan):
        raise NotImplemented

class WebmapserviceProduct(TimelessBase):
    def __init__(self, address):
        from owslib.wms import WebMapService
        raise NotImplemented

class TemporalClustering(VirtualBase):
    pass

class LatestObservation(TimelessBase):
    pass

def BandmathDecorator(function):
    raise NotImplemented

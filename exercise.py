from pywps import Process, LiteralInput, LiteralOutput, UOM
from pywps import ComplexInput, ComplexOutput
from pywps.app.Common import Metadata
from pywps import Format, FORMATS
from pywps.exceptions import InvalidParameterValue
import xarray as xr


import glob
import os

import logging
LOGGER = logging.getLogger("PYWPS")


class Exercise(Process):
    """A nice process saying 'hello'."""
    def __init__(self):
        inputs = [
            LiteralInput('min_lon', 'Minimum longitude',
                         data_type='float',
                         default=-180,
                         min_occurs=1),
            LiteralInput('max_lon', 'Maximum longitude',
                         data_type='float',
                         default=180,
                         min_occurs=1),
            LiteralInput('min_lat', 'Minimum latitude',
                         data_type='float',
                         default=-90,
                         min_occurs=1),
            LiteralInput('max_lat', 'Maximum latitude',
                         data_type='float',
                         default=90,
                         min_occurs=1),
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like vas (northward near-Surface wind).',
                         data_type='string',
                         allowed_values=['pr', 'tas', 'tasmax', 'tasmin', 'vas', 'uas'],
                         default='tas'),
            LiteralInput('model', 'Model',
                         abstract='Choose a model like HadGEM2-ES.',
                         data_type='string',
                         allowed_values=['HadGEM2-ES',
                                         'HadCM3',
                                         'GFDL-CM2p1',
                                         'bcc-csm1-1-m',
                                         'bcc-csm1-1',
                                         'BNU-ESM',
                                         ],
                         default='HadCM3'),
                         ]
        outputs = [
            ComplexOutput('output', 'NetCDF file',
                          abstract='A single NetCDF file.',
                          as_reference=True,
                          supported_formats=[FORMATS.NETCDF]),]


        super(Exercise, self).__init__(
            self._handler,
            identifier='get_cutout',
            title='Get CMIP5 RCP45 2010s average cutout',
            abstract='WPS process for extracting UK domain from CMIP5 data',
            #keywords=['hello', 'demo'],
            metadata=[
                Metadata('PyWPS', 'https://pywps.org/'),
                Metadata('Birdhouse', 'http://bird-house.github.io/'),
                Metadata('PyWPS Demo', 'https://pywps-demo.readthedocs.io/en/latest/'),
                Metadata('Emu: PyWPS examples', 'https://emu.readthedocs.io/en/latest/'),
            ],
            version='0.1',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    @staticmethod
    def _handler(request, response):
        model = request.inputs['model'][0].data
        variable = request.inputs['variable'][0].data
        nc_files_path = f'badc/cmip5/data/cmip5/output1/MOHC/{model}/rcp45/mon/atmos/Amon/r1i1p1/latest/{variable}/'
        file_path = os.path.join(os.environ.get('HOME'), nc_files_path)
        files = glob.glob(file_path + '*.nc')
        ds = xr.open_mfdataset(files)


        # Throw manually with temporary bbox solution
        if request.inputs['min_lon'][0].data < -180:
            raise InvalidParameterValue('Minimum longitude input cannot be below -180')
        if request.inputs['max_lon'][0].data > 180:
            raise InvalidParameterValue('Maximum longitude input cannot be above 180')
        if request.inputs['min_lat'][0].data < -90:
            raise InvalidParameterValue('Minimum latitude input cannot be below -90')
        if request.inputs['max_lat'][0].data > 90:
            raise InvalidParameterValue('Minimum latitude input cannot be above 90')


        return response

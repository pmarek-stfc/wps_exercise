from pywps import Process, LiteralInput, LiteralOutput, UOM
from pywps import ComplexInput, ComplexOutput
from pywps.app.Common import Metadata
from pywps import Format, FORMATS
from pywps.exceptions import InvalidParameterValue
from wps_exercise.processes.functions import open_mfdatasets, get_years

import glob
import time
import os
import cftime
from pathlib import Path

import logging
LOGGER = logging.getLogger("PYWPS")


class Exercise(Process):
    """A nice process saying 'hello'."""
    def __init__(self):
        inputs = [
            LiteralInput('min_lon', 'Minimum longitude',
                         data_type='integer',
                         default=-180,
                         min_occurs=1),
            LiteralInput('max_lon', 'Maximum longitude',
                         data_type='integer',
                         default=180,
                         min_occurs=1),
            LiteralInput('min_lat', 'Minimum latitude',
                         data_type='integer',
                         default=-90,
                         min_occurs=1),
            LiteralInput('max_lat', 'Maximum latitude',
                         data_type='integer',
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

        # Throw manually with temporary bbox solution
        if request.inputs['min_lon'][0].data < 0:
            raise InvalidParameterValue('Minimum longitude input cannot be below 0')
        if request.inputs['max_lon'][0].data > 360:
            raise InvalidParameterValue('Maximum longitude input cannot be above 360')
        if request.inputs['min_lat'][0].data < -90:
            raise InvalidParameterValue('Minimum latitude input cannot be below -90')
        if request.inputs['max_lat'][0].data > 90:
            raise InvalidParameterValue('Minimum latitude input cannot be above 90')

        d1 = cftime.Datetime360Day(2010, 1, 1)
        d2 = cftime.Datetime360Day(2020, 1, 1)

        nc_files_path = f'xarray'
        files_path = os.path.join(str(Path.home()), nc_files_path)
        files = glob.glob(files_path + '/tas*.nc')

        #response.update_status("Reading through files", 10)
        files_to_open = get_years(files)
        new_dataset = open_mfdatasets(files_to_open)
        #response.update_status("Calculating temporal average", 50)

        sliced_dataset = new_dataset.sel(time=slice(d1, d2), lon=slice(request.inputs['min_lon'][0].data,
                                                                    request.inputs['max_lon'][0].data),
                                                            lat=slice(request.inputs['min_lat'][0].data,
                                                                    request.inputs['max_lat'][0].data))
        # calculate temporal average across the time axis only
        mean_array = sliced_dataset.mean(dim='time')
        print(mean_array)
        response.update_status("Writing results to a new NetCDF4 file", 50)
        # result_nc_file = mean_array.to_netcdf('results.nc')

        response.outputs['output'].nc_file = mean_array.to_netcdf('resultsssss.nc')
        response.update_status("Done.", 100)
        return response

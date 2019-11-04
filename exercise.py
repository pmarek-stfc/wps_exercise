from pywps import Process, LiteralInput, LiteralOutput, UOM
from pywps import ComplexInput, ComplexOutput
from pywps.app.Common import Metadata
from pywps import Format, FORMATS

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
            LiteralInput('pr', 'Precipitation',
                         abstract='at surface; includes both liquid and solid phases from all types of clouds (both large-scale and convective)',
                         uoms='kg m-2 s-1',
                         data_type='float'),
            LiteralInput('tas', 'Near-Surface Air Temperature',
                         uoms='K',
                         data_type='float'),
            LiteralInput('tasmax', 'Daily Maximum Near-Surface Air Temperature',
                         uoms='K',
                         data_type='float'),
            LiteralInput('tasmin', 'Daily Minimum Near-Surface Air Temperature',
                         uoms='K',
                         data_type='float'),
            LiteralInput('uas', 'Eastward Near-Surface Wind',
                         uoms='m s-1',
                         data_type='float'), 
            LiteralInput('vas', 'Northward Near-Surface Wind',
                         uoms='m s-1',
                         data_type='float'),              
            LiteralInput('model', 'Model',
                         abstract='Choose a model like HadGEM2-ES.',
                         data_type='string',
                         allowed_values=['HadGEM2-ES',
                                         'HadCM3',
                                         'GFDL-CM2p1'],
                         default='HadGEM2-ES'),
            LiteralInput('variable', 'Variable',
                         abstract='Choose a variable like tas (temperatue at surface).',
                         data_type='float',
                         allowed_values=['', ''],
                         default='tas')]
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
        LOGGER.info("say hello")
        response.outputs['output'].data = 'Hello ' + request.inputs['name'][0].data
        response.outputs['output'].uom = UOM('unity')
        return response
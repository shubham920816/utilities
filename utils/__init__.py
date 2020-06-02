from pkg_resources import get_distribution, DistributionNotFound
import os.path

try:
    _dist = get_distribution('utils')
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)

    if not here.startswith(os.path.join(dist_loc, 'commonutils')):
        pass
except DistributionNotFound:
    __version__ = 'Please install this project with setup_test.py'
else:
    __version__ = _dist.version

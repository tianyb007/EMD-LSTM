import logging

__version__ = "1.4.0"
logger = logging.getLogger("pyemd")

from PyEMD.CEEMDAN import CEEMDAN  # noqa
from PyEMD.EEMD import EEMD  # noqa
from PyEMD.EMD import EMD  # noqa
from PyEMD.visualisation import Visualisation  # noqa

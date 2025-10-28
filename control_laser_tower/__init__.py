"""Control Laser Tower package

Expose `LaserTower` and a convenience `set_config` function.
"""
from .controller import LaserTower, set_config

__version__ = "0.1.0"

__all__ = ["LaserTower", "set_config", "__version__"]

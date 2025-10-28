"""Laser tower controller

This module provides the LaserTower class which controls two servos and a laser
LED using the `gpiozero` library. It also exposes a small `set_config` helper
to change package-wide default pins before creating instances.

Contract (simple):
- Inputs: integer GPIO pins for base_servo, top_servo, laser
- Outputs: methods to set angles and turn laser on/off
- Error modes: ValueError for out-of-range angles

Note: This package assumes `gpiozero` is available at runtime. If you plan to
use the package on a non-Raspberry Pi machine for development, install a
compatible stub or mock for `gpiozero` in your environment or run tests that
inject a fake module.
"""
from typing import Optional

DEFAULT_CONFIG = {
    "base_pin": 23,  # default GPIO for base servo
    "top_pin": 24,   # default GPIO for top servo
    "laser_pin": 17, # default GPIO for laser LED
}


_GLOBAL_CONFIG = dict(DEFAULT_CONFIG)


def set_config(base_pin: Optional[int] = None, top_pin: Optional[int] = None, laser_pin: Optional[int] = None):
    """Set global defaults for pins used by LaserTower.

    Call this before creating LaserTower instances if you want different
    default GPIO pins across the application.
    """
    global _GLOBAL_CONFIG
    if base_pin is not None:
        _GLOBAL_CONFIG["base_pin"] = int(base_pin)
    if top_pin is not None:
        _GLOBAL_CONFIG["top_pin"] = int(top_pin)
    if laser_pin is not None:
        _GLOBAL_CONFIG["laser_pin"] = int(laser_pin)


class LaserTower:
    """Controls two servos (base, top) and a laser LED.

    Example:
        from control_laser_tower import LaserTower, set_config
        set_config(base_pin=5, top_pin=6, laser_pin=13)
        lt = LaserTower()
        lt.set_base_angle(90)
        lt.set_top_angle(45)
        lt.laser_on()
    """

    def __init__(self, base_pin: Optional[int] = None, top_pin: Optional[int] = None, laser_pin: Optional[int] = None, servo_pulse_settings: Optional[dict] = None):
        # import gpiozero lazily so tests can inject a fake module before import
        try:
            from gpiozero import LED, Servo  # type: ignore
        except Exception as exc:  # pragma: no cover - environment-specific
            raise ImportError("gpiozero is required to use LaserTower") from exc

        # resolve config
        cfg = dict(_GLOBAL_CONFIG)
        if base_pin is not None:
            cfg["base_pin"] = int(base_pin)
        if top_pin is not None:
            cfg["top_pin"] = int(top_pin)
        if laser_pin is not None:
            cfg["laser_pin"] = int(laser_pin)

        # servo pulse settings convenience
        if servo_pulse_settings is None:
            servo_pulse_settings = {"min_pulse_width": 0.0005, "max_pulse_width": 0.0025, "frame_width": 0.02}

        self.base = Servo(cfg["base_pin"], **servo_pulse_settings)
        self.top = Servo(cfg["top_pin"], **servo_pulse_settings)
        self.laser = LED(cfg["laser_pin"])

    def set_base_angle(self, angle: float):
        """Set base servo angle in degrees (0-360).

        The value is mapped linearly to servo.value (-1.0..+1.0):
            servo_value = (angle / 180.0) - 1.0

        If angle is out of range ValueError is raised.
        """
        if angle < 0 or angle > 360:
            raise ValueError("base angle must be between 0 and 360 degrees")
        servo_value = (angle / 180.0) - 1.0
        self.base.value = float(servo_value)

    def set_top_angle(self, angle: float):
        """Set top servo angle in degrees (0-180).

        Mapped to servo.value (-1.0..+1.0): value = (angle / 90.0) - 1.0
        """
        if angle < 0 or angle > 180:
            raise ValueError("top angle must be between 0 and 180 degrees")
        servo_value = (angle / 90.0) - 1.0
        self.top.value = float(servo_value)

    def laser_on(self):
        self.laser.on()

    def laser_off(self):
        self.laser.off()

    def close(self):
        # attempt to close resources if available
        for dev in (self.base, self.top, self.laser):
            try:
                dev.close()
            except Exception:
                pass


__all__ = ["LaserTower", "set_config"]

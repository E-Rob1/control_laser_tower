# control-laser-tower

Lightweight library to control a small laser tower: two servos (base 0–360°, top 0–180°)
and a laser/LED. Uses `gpiozero` for hardware access.

Quick start

```
pip install control-laser-tower

from control_laser_tower import LaserTower, set_config

# optional: change default pins before creating instances
set_config(base_pin=5, top_pin=6, laser_pin=13)

lt = LaserTower()
lt.set_base_angle(180)
lt.set_top_angle(45)
lt.laser_on()
```

Packaging

- Build a wheel: `python -m build` (requires `build` package)
- Upload with `twine upload dist/*`

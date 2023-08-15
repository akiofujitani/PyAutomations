import math, logging
from collections import namedtuple

logger = logging.getLogger('prism_calc')

PrHorVer = namedtuple('PrHorVer', 'hor_value ver_value')


def pr_angle_value_to_hor_ver(angle: int, value: float) -> PrHorVer:
    try:
        angle = int(angle)
        value = float(value)
    except ValueError as error:
        print(f'Value for {angle} or {value} not value due {error}')
        raise error

    hor_value = math.cos(math.radians(angle)) * value
    ver_value = math.sin(math.radians(angle)) * value
    return PrHorVer(f'{hor_value:.2f}', f'{ver_value:.2f}')


if __name__ == '__main__':

    angle = 270
    value = 0.52

    pr_ver_hor = pr_angle_value_to_hor_ver(angle, value)
    print(f'{pr_ver_hor.hor_value} {pr_ver_hor.ver_value}')


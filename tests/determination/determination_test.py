import pytest
import numpy as np
from numpy.typing import NDArray
from orbit_visualiser.core import gibbs_orbit_determination

@pytest.mark.parametrize("r1, r2, r3, mu, expected_elements", [
    (np.array([50_000, 0, 0]), np.array([0, 50_000, 0]), np.array([-50_000, 0, 0]), 398600,
     [0.0, 50000.0, 0.0, 0.0, 0.0]),
    (np.array([-294.32, 4265.1, 5986.7]), np.array([-1365.5, 3637.6, 6346.8]), np.array([-2940.3, 2473.7, 6555.8]), 398600,
     [0.10010368939126256, 7200.464440362424, 0.6981881213115507, 1.047213012806218, 0.5248767645202468])
])
def test_gibbs(
        r1: NDArray[np.float64],
        r2: NDArray[np.float64],
        r3: NDArray[np.float64],
        mu: float,
        expected_elements: list[np.float64]
):
    orbit = gibbs_orbit_determination(r1, r2, r3, mu)
    elements = [
        orbit.eccentricity,
        orbit.radius_of_periapsis,
        orbit.right_ascen_of_ascend_node,
        orbit.inclination,
        orbit.argument_of_periapsis
    ]

    assert np.allclose(elements, expected_elements)
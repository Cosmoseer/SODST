import numpy as np
from numpy.typing import NDArray
from sodst.core.orbit import Orbit
from sodst.core.astrodynamics.determination.determination_error import DeterminationError

def gibbs_orbit_determination(
        r_1: NDArray[np.float64], r_2: NDArray[np.float64], r_3: NDArray[np.float64], mu: float
) -> Orbit:
    """
    Uses the Gibbs orbit determination algorithm to calculate the velocity vector at r_1, and
    returns an Orbit object.

    Parameters
    ----------
    r_1 : NDArray[np.float64]
        First position vector (km)
    r_2 : NDArray[np.float64]
        Second position vector (km)
    r_3 : NDArray[np.float64]
        Third position vector (km)
    mu : float
        Gravitational parameter of the central body (km^3/s^2)

    Returns
    -------
    Orbit
       Orbit object, taking the first position vector and its calculated velocity vector as its arguments.

    Raises
    ------
    DeterminationError
        The Gibbs algorithm relies on the position vectors being pairwise non-collinear. If that
        condition isn't satisfied then the custom error DeterminationError is thrown.
    """
    r1_norm = np.linalg.norm(r_1)
    r2_norm = np.linalg.norm(r_2)
    r3_norm = np.linalg.norm(r_3)
    c_12 = np.cross(r_1, r_2)
    c_23 = np.cross(r_2, r_3)
    c_31 = np.cross(r_3, r_1)

    if np.isclose(np.linalg.norm(c_12), 0) or np.isclose(np.linalg.norm(c_12), 0) or np.isclose(np.linalg.norm(c_12), 0):
        raise DeterminationError("Determination algorithm requires non-collinear position vectors.")

    N = r1_norm*c_23 + r2_norm*c_31 + r3_norm*c_12
    N_norm = np.linalg.norm(N)
    D = c_12 + c_23 + c_31
    D_norm = np.linalg.norm(D)
    S = (r2_norm - r3_norm)*r_1 + (r3_norm - r1_norm)*r_2 + (r1_norm - r2_norm)*r_3
    v_1 = np.sqrt(mu/(N_norm*D_norm))*(np.cross(D, r_1)/r1_norm + S)

    return Orbit(r_1, v_1, mu)


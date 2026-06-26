import numpy as np
from numpy.typing import NDArray
from sodst.core.orbit import Orbit

def gibbs_orbit_determination(
        r_1: NDArray[np.float64], r_2: NDArray[np.float64], r_3: NDArray[np.float64], mu: float
) -> Orbit:
    v_1 = _gibbs_velocity(r_1, r_2, r_3, mu)
    return Orbit(r_1, v_1, mu)

def _gibbs_velocity(
        r_1: NDArray[np.float64], r_2: NDArray[np.float64], r_3: NDArray[np.float64], mu: float
) -> NDArray[np.float64]:
    r1_norm = np.linalg.norm(r_1)
    r2_norm = np.linalg.norm(r_2)
    r3_norm = np.linalg.norm(r_3)
    c_12 = np.cross(r_1, r_2)
    c_23 = np.cross(r_2, r_3)
    c_31 = np.cross(r_3, r_1)
    N = r1_norm*c_23 + r2_norm*c_31 + r3_norm*c_12
    N_norm = np.linalg.norm(N)
    D = c_12 + c_23 + c_31
    D_norm = np.linalg.norm(D)
    S = (r2_norm - r3_norm)*r_1 + (r3_norm - r1_norm)*r_2 + (r1_norm - r2_norm)*r_3
    return np.sqrt(mu/(N_norm*D_norm))*(np.cross(D, r_1)/r1_norm + S)


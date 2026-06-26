import numpy as np
from numpy.typing import NDArray

def promote_to_3d(vector: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Promotes a 2D numpy array to 3D, and returns vectors of other shapes unchanged.

    Parameters
    ----------
    vector : NDArray[np.float64]
        Numpy array

    Returns
    -------
    NDArray[np.float64]
        Promoted array
    """
    if vector.shape[-1] == 2:
        return np.append(vector, 0.0)

    return vector

def restrict(num: float, lower: float = -1.0, upper: float = 1.0) -> float:
    """
    Restricts the input to be within the closed interval [lower, upper]. If the input is below the
    interval then it is brought up to the lower limit, and likewise if its above then it's brought
    down to the upper limit.

    Parameters
    ----------
    num : float
        Input to be restricted
    lower : float, optional
        Interval lower limit, by default -1.0
    upper : float, optional
        Interval upper limit, by default 1.0

    Returns
    -------
    float
        Restricted float
    """
    if upper < lower:
        raise ValueError("Upper limit must be greater than the lower limit")

    if num > upper:
        return upper

    elif num < lower:
        return lower

    return num
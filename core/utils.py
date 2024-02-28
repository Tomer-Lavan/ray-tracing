import numpy as np

# This function gets a vector and returns its normalized form.


def normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


# This function gets a vector and the normal of the surface it hit
# This function returns the vector that reflects from the surface
def reflected(vector: np.ndarray, axis: np.ndarray) -> np.ndarray:
    return vector - 2 * np.dot(vector, axis) * axis

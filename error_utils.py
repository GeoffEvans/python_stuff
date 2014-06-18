from numpy import allclose
from numpy.linalg import norm

def check_is_unit_vector(vector):
    magnitude = norm(vector, axis=0)
    if not allclose(magnitude, 1, atol=1e-15):
        raise ValueError("vector must be unit length")
    
def check_is_of_length(desired, arr):
    length = arr.shape[0]
    if not length == desired:
        raise ValueError("array has wrong size")
    
def check_is_val(var,val):
    if not var == val:
        raise ValueError("variable has wrong value")
def R_matrix(r, n=1):
    """
    This is a generic function.
    This function creates a measurement noise matrix (Measurement Covariance).
    We assume that measurements are uncorrelated, i.e., R is a diagonal matrix.
    
    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type                   Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    r             scalar/vector                   Measurement Variance (standard deviation)
                                                  - if r is a scalar, the same measurement variance is applied for each measured parameter
                                                  - if r is a vector, each element represents the measurement variance for corresponding measured parameter
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    n             scalar integer                  Number of measured parameters (Optional Parameter)
                                                  - if r is a vector, the length of r is the number of measured parameters
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    R             matrix                          measurement noise matrix
                                                  (diagonal matrix)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np

    # create Measurement Uncertainty for each state and each time sample
    if r.size == 1:
        R = np.eye(n)*(r**2)
    elif r.ndim == 1:  # r is a vector
        R = np.diag(r**2)
    elif r.shape[0] == 1 or r.shape[1] == 1:  # r is a vector
        R = np.diag(np.squeeze(r) ** 2)
    else:   # r is a matrix
        raise Exception('r must be a scalar or a vector')

    return R
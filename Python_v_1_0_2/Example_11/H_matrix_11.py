def H_matrix_11(x, Hargs):
    """
    Description
    This function creates H matrix (Observation Matrix) for example 11.

    Inputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x             matrix                          The vehicle position, velocity and acceleration
                                                  (first row is the X axis position, second row is the X axis velocity, third row is is the X axis acceleration)
                                                  (fourth row is the Y axis position, fifth row is the Y axis velocity, sixth row is is the Y axis acceleration)
                                                  (columns represent states at different time samples)
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Hargs                                         Usually constants. Not in use in this example
    -------------------------------------------------------------------------------------------------------------------------------------------------------

    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    H             matrix                          Observation Function Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dH            matrix                          Derivative of H
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """
    import numpy as np

    Hx = np.array([np.sqrt((x[0]**2 + x[3]**2)), np.arctan(x[3]/x[0])])  # range and azimuth angle

    r2 = x[0]**2 + x[3]**2  # squared range

    dHx = np.block([[x[0]/np.sqrt(r2), 0, 0, x[3]/np.sqrt(r2), 0, 0], [-x[3]/r2, 0, 0, x[0]/r2, 0, 0]])

    return Hx, dHx

def H_matrix_13(x, Hargs):
    """
    Description
    This function creates H matrix (Observation Matrix) for example 13.

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

    """
    import numpy as np

    Hx = np.array([np.sqrt((x[0]**2 + x[3]**2)), np.arctan(x[3]/x[0])])  # range and azimuth angle

    return Hx

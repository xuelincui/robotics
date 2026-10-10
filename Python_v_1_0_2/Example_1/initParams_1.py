def initParams_1(paramType):
    """
    Description
    This function initiates example parameters.
    There are three parameter groups:

    1. Parameters related to Kalman Filter
    2. Parameters related to noise generation
    3. Parameters related to scenario generation

    Inputs
    -------------------------------------------------------------------------------------------
    Variable       Variable Type       Units       Description
    -------------------------------------------------------------------------------------------
    paramType      string                          one of the three parameters grroups
    -------------------------------------------------------------------------------------------


    Outputs
    --------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    --------------------------------------------------------------------------------------------
    params        struc                           Parameters Structure
    --------------------------------------------------------------------------------------------
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    """

    import numpy as np

    if paramType == 'KF':
        params = {
            "r": np.array([20]),      # Measurement Noise (standard deviation)
            "x0": 1000                # initial guess
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([189]),  # Random noise generator seed
            "numOfDecimals": 0        # Round measurements to integers for presentation convenience
        }
    elif paramType == 'scenario':
        params = {
            "x_true": np.array(1000),   # true weight
            "n": 10                     # number of iterations
        }

    return params
def initParams_5(paramType):
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
            "r": np.array([5]),        # Measurement Noise (standard deviation)
            "strModel": 'constant',    # Constant dynamic model
            # set filter initial conditions
            "x0": 60,                 # Set building height to 60
            "p0": 15**2,              # Set initial estimate variance
            "q": 0                    # Process noise
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([189]),  # Random noise generator seed
            "numOfDecimals": 2        # Round noise to whole meters (for presentation convenience)
        }
    elif paramType == 'scenario':
        params = {
            "x_true": np.array(50),     # true building height
            "n": 10                     # number of iterations
        }

    return params
def initParams_6(paramType):
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
            "r": np.array([0.1]),       # Measurement Noise (standard deviation)
            "sig_p": np.array([0.01]),  # Process Noise Uncertainty (standard deviation)
            "strModel": 'constant',     # Constant dynamic model
            # set filter initial conditions
            "x0": 60,                   # Initial liquid temperature
            "p0": 100**2                # Set estimate variance
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([189]),   # Random noise generator seed
            "numOfDecimals": 3         # Round noise (for presentation convenience)
        }
    elif paramType == 'scenario':
        params = {
            "x_true": np.array(50),     # true liquid temperature
            "n": 10,                    # number of iterations
            # process noise parameters
            "sig_p": np.array([0.01]),  # Process Noise Uncertainty (standard deviation)
            "seed": np.array([123]),    # Random noise generator seed
            "numOfDecimals": 3          # Round noise (for presentation convenience)
        }

    return params
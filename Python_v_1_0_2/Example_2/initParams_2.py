def initParams_2(paramType):
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
            "dt": 5,                # Time sample period (seconds)
            "r": np.array([150]),   # Measurement Noise (standard deviation)
            "alpha": 0.2,           # 0.8 # 0.2
            "beta": 0.1,            # 0.5 # 0.1
            # set filter initial conditions
            "x0": 30000,            # Set initial position to 30,000
            "v0": 40,               # Set initial velocity to 40
            "a0": 0                 # Set initial acceleration to 0
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([189]),  # Random noise generator seed
            "numOfDecimals": 0        # Round measurements to integers for presentation convenience
        }
    elif paramType == 'scenario':
        params = {
            "isPlotScenario": False,  # set flag to 'True' to plot scenarios
            "x0": 30000,              # initial aircraft range
            "v0": 40,                 # initial aircraft velocity
            "n": 10                   # number of iterations
        }

    return params
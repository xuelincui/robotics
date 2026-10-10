def initParams_3(paramType):
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
            "v0": 50,               # Set initial velocity to 50
            "a0": 0                 # Set initial acceleration to 0
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([189]),  # Random noise generator seed
            "numOfDecimals": 0        # Round measurements to integers for presentation convenience
        }
    elif paramType == 'scenario':
        a1 = np.zeros(4)     # acceleration during the constant velocity part
        a2 = 8 * np.ones(6)  # acceleration during the constant acceleration part
        params = {
            "isPlotScenario": False,       # set flag to 'True' to plot scenarios
            "x0": 30000,                  # initial aircraft range
            "v0": 50,                     # initial aircraft velocity
            "a": np.concatenate((a1,a2))  # combine accelerations
        }

    return params
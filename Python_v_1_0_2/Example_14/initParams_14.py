def initParams_14(paramType):
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
            "dim": 1,                               # One-dimensional model
            "dt": 0.05,                             # Time sample period (seconds)
            "r": np.array([0.01]),                  # Measurement Uncertainty standard deviation (meters)
            "sig_a": np.array([1]),                 # Process Noise Uncertainty (acceleration standard deviation)
            "g": 9.8,                               # Gravitational acceleration constant (m/s^2)

            "seed": np.array([789]),                # Random noise generator seed

            "strModel": 'linear',                   # Constant angular velocity
            "strNoiseModel": 'discrete',            # Discrete noise model (required for process noise matrix computation)

            "sigmaPntAlgo": 'modified',             # 'original' or 'modified' algorithm
            "alpha": 0.1,                           # tuning parameter for the 'modified' sigma-points algorithm
            
            # set filter initial conditions
            "x0": np.array([[5*np.pi/180, 0]]).T,   # Set initial angle to 5 degrees and initial anglular velocity to 0
            "P0": np.eye(2)*5                       # Set high estimate uncertainty, it results in a high Kalman Gain, giving a high weight to the measurement
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([789])     # Random noise generator seed
        }
    elif paramType == 'scenario':
        params = {
            "isPlotScenario": False
        }

    return params
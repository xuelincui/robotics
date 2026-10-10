def initParams_9(paramType):
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
            "dim": 2,                               # Two-dimensional model (X,Y)
            "dt": 1,                                # Time sample period (seconds)
            "r": np.array([3]),                     # Measurement Noise (standard deviation)
            "sig_a": np.array([0.2]),               # Process Noise Uncertainty (acceleration standard deviation)

            "strModel": 'quadratic',                # Constant acceleration
            "strNoiseModel": 'discrete',            # Discrete noise model (required for process noise matrix computation)

            # set filter initial conditions
            "x0": np.array([[0, 0, 0, 0, 0, 0]]).T,  # Set initial position, velocity and acceleration to 0
            "P0": np.eye(6)*500                      # Set high estimate uncertainty, it results in a high Kalman Gain, giving a high weight to the measurement
        }
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([123])    # Random noise generator seed
        }
    elif paramType == 'scenario':
        params = {
            "isPlotScenario": False,    # set flag to 'True' to make scenario plots
            # set scenario initial conditions
            "v": 25,                    # vehicle velocity (m/s)
            "L": 400,                   # length of the trajectory straight part (meters)
            "R": 300,                   # turn radius
            # process noise parameters
            "sig_a": np.array([0.2]),   # Process Noise Uncertainty (standard deviation)
            "seed": np.array([789])     # Random noise generator seed
        }

    return params
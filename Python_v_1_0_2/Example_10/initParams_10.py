def initParams_10(paramType):
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
            "dim": 1,                               # One-dimensional model - only altitude dimension
            "dt": 0.25,                             # Time sample period (seconds)
            "r": np.array([20]),                    # Measurement Noise (standard deviation)
            "sig_a": np.array([0.1]),               # Process Noise Uncertainty (acceleration standard deviation)
            "g": -9.8,                              # Gravitational acceleration constant (m/s^2)

            "strModel": 'linear',                   # Constant velocity
            "strNoiseModel": 'discrete',            # Discrete noise model (required for process noise matrix computation)

            # set filter initial conditions
            "x0": np.array([[0, 0]]).T,             # Set initial altitude and velocity to 0
            "u0": np.array([0]),                    # Set initial control input(acceleration) to 0
            "P0": np.eye(2)*500                     # Set high estimate uncertainty, it results in a high Kalman Gain, giving a high weight to the measurement
        }
    elif paramType == 'noiseGenAlt':                # parameters related to altimeter noise generation
        params = {
            "seed": np.array([456])                 # Random noise generator seed for altimeter measurements
        }
    elif paramType == 'noiseGenAcc':
        params = {
            "seed": np.array([789])                 # Random noise generator seed for accelerometer measurements
        }
    elif paramType == 'scenario':
        params = {
            "isPlotScenario": False,    # set flag to 'True' to make scenario plots
            # set scenario initial conditions
            "g": -9.8,                  # Gravitational acceleration constant (m/s^2)
            "x0": 20,                   # initial altitude (meters)
            "v0": 0,                    # initial velocity (m/s)
            "a": 30,                    # acceleration (m/s^2)
            "N": 30,                    # number of measurements

            # process noise parameters
            "sig_a": np.array([0.1]),   # Process Noise Uncertainty (acceleration standard deviation) for scenario creation
            "seed": np.array([123])     # Random noise generator seed
        }

    return params
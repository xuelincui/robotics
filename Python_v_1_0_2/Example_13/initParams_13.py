def initParams_13(paramType):
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
            "r": np.array([[5, 0.5*np.pi/180]]).T,  # Measurement Uncertainty (standard deviation) - range (meters) and angle(radians)
            "sig_a": np.array([0.2]),               # Process Noise Uncertainty (acceleration standard deviation)

            "strModel": 'quadratic',                # Constant acceleration
            "strNoiseModel": 'discrete',            # Discrete noise model (required for process noise matrix computation)

            "sigmaPntAlgo": 'original',             # 'original' or 'modified' algorithm
            "alpha": 0.01,                          # tunning parameter for the 'modified' sigma-points algorithm

            # set filter initial conditions
            "x0": np.array([[0, 0, 0, 0, 0, 0]]).T,  # Set initial position, velocity and acceleration to 0
            "P0": np.eye(6)*500                      # Set high estimate uncertainty, it results in a high Kalman Gain, giving a high weight to the measurement
        }
        params["x0"][0] = 400           # add ~100m error to the X-position
        params["x0"][3] = -300          # add ~100m error to the Y-position
    elif paramType == 'noiseGen':
        params = {
            "seed": np.array([123])     # Random noise generator seed
        }
    elif paramType == 'scenario':
        params = {
            "isPlotScenario": False     # set flag to 'True' to make scenario plots
        }

    return params
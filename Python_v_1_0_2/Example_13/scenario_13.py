def scenario_13(dt, isPlotScenario = None):
    """
    This function creates scenario for example 11, which is similar to the example 9 scenario.

    Inputs
    ---------------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------
    dt              scalar              seconds     time between samples
    ---------------------------------------------------------------------------------------------
    isPlotScenario  boolean                         Optional input. Indicates whether to make
                                                    scenario plots
    -------------------------------------------------------------------------------------------------------------------------------------------------------

    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X             matrix                           true vehicle position, velocity and  acceleration
                                                   (first row is the X axis position, second row is the X axis velocity, third row is is the X axis acceleration)
                                                   (fourth row is the Y axis position, fifth row is the Y axis velocity, sixth row is is the Y axis acceleration)
                                                   (columns represent states at different time samples)

    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    R             vector                          true vehicle range (meters) - the distance between the radar and the vehicle
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    phi           vector                          true angle between the vehicle and the X-axis (radians)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    import numpy as np
    from Example_9.scenario_9 import scenario_9
    from Example_13.initParams_13 import initParams_13

    params = initParams_13('scenario')

    if (isPlotScenario is None):
        isPlotScenario = params["isPlotScenario"]


    X = scenario_9(dt, isPlotScenario)

    R = np.sqrt(X[0,:]**2 + X[3,:]**2)
    phi = np.arctan(X[3,:]/X[0,:])

    return X, R, phi
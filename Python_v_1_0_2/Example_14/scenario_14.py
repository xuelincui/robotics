def scenario_14(dt):
    """
    Description
    This function creates scenario for example 12

    Inputs
    --------------------------------------------------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------------------------------------------
    dt              scalar              seconds     Time between samples
    ---------------------------------------------------------------------------------------------------------------------------------


    Outputs
    ---------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------------------------------------------
    X             matrix                          true pendulum angle and angular velocity + process noise
                                                  (first row is the pendulum angle, second row is the pendulum angular velocity)
    ----------------------------------------------------------------------------------------------------------------------------------
    L             scalar              meters      Pendulum string length
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np
    from Example_12.scenario_12 import scenario_12
    from Example_14.initParams_14 import initParams_14

    params = initParams_14('scenario')
    X, L = scenario_12(dt, params["isPlotScenario"])
    return X, L
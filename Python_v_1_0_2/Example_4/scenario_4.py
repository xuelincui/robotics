def scenario_4(dt):
    """
    This function creates scenario for examples 3 and 4.

    The scenario is divided into two parts:

    1. The aircraft moves with a constant speed for 3 time samples.
    2. The aircraft moves with a constant acceleration for 12 time samples.

    Inputs
    ---------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    ---------------------------------------------------------------------------------------
    dt              scalar              seconds     time between samples
    ---------------------------------------------------------------------------------------

    Outputs
    ------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------
    x             vector              meters      aircraft range
    ------------------------------------------------------------------------------------------
    v             vector              m/s         aircraft velocity
    ------------------------------------------------------------------------------------------
    a             vector              m/(s^2)     aircraft acceleration
    ------------------------------------------------------------------------------------------

    """
    from Example_3.scenario_3 import scenario_3
    from Example_4.initParams_4 import initParams_4

    # create scenario
    params = initParams_4('scenario')
    x, v, a = scenario_3(dt, params["isPlotScenario"])

    return x, v, a
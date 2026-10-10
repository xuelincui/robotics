def scenario_5():
    """
    Description
    This function creates scenario for example 5

    Outputs
    --------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    --------------------------------------------------------------------------------------------
    x_true        vector              gram        The true building height
    --------------------------------------------------------------------------------------------

    """
    import numpy as np
    from Example_5.initParams_5 import initParams_5

    # init parameters
    params = initParams_5('scenario')
    x_true = np.tile(params["x_true"], params["n"])

    return x_true
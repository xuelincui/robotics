def scenario_1():
    """
    Description
    This function creates scenario for example 1 - weighting the gold bar

    Outputs
    --------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    --------------------------------------------------------------------------------------------
    x_true        vector              gram        The true gold bar weight
    --------------------------------------------------------------------------------------------

    """
    import numpy as np
    from Example_1.initParams_1 import initParams_1

    # init parameters
    params = initParams_1('scenario')
    x_true = np.tile(params["x_true"], params["n"])

    return x_true
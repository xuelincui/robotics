def scenario_6():
    """
    The scenario creates heating liquid temperature for 100 measurements

    Outputs
    ---------------------------------------------------------------------------------------------------
    Variable       Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------------
    x              vector              deg         actual liquid temperature
    ---------------------------------------------------------------------------------------------------

    """
    import numpy as np
    from KF_common.addNoise import addNoise
    from Example_6.initParams_6 import initParams_6

    # init parameters
    params = initParams_6('scenario')

    x_true = np.tile(params["x_true"], params["n"])

    # create true values with process noise
    x = addNoise(x_true, params["sig_p"], params)

    return x

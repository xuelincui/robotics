def example_5():
    """
    Description

    In this example we will estimate the height of a building using one-dimensional Kalman Filter.
    We will ignore the process noise.
    
    """
    from KF_common.addNoise import addNoise
    from KF_OneDim.KF_1D import KF_1D
    from Example_5.initParams_5 import initParams_5
    from Example_5.scenario_5 import scenario_5
    from Example_5.plots_5 import plots_5

    # load example parameters
    params = initParams_5('KF')

    # create scenario
    x_true = scenario_5()

    # create measurements
    ngParams = initParams_5('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)


    # run the 1D Kalman Filter
    x_est, x_pred, p_est, p_pred, k = KF_1D(z, params["r"], params["x0"], params["p0"], 0, params["strModel"])

    # make plots
    plots_5(x_true, x_est, x_pred, p_est, k, z, params["r"])


if __name__ == '__main__':
    example_5()


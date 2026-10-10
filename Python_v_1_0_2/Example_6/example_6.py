def example_6():
    """
    Description

    In this example we will estimate the temperature of the liquid in a tank using one-dimensional Kalman Filter.
    We take the process noise into consideration.

    """
    import numpy as np
    from KF_common.addNoise import addNoise
    from KF_OneDim.KF_1D import KF_1D
    from Example_6.plots_6 import plots_6
    from Example_6.scenario_6 import scenario_6
    from Example_6.initParams_6 import initParams_6

    # load example parameters
    params = initParams_6('KF')

    # create scenario
    x_true = scenario_6()

    # create measurements
    ngParams = initParams_6('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)

    # run the 1D Kalman Filter
    x_est, x_pred, p_est, p_pred, k = KF_1D(z, params["r"], params["x0"], params["p0"], params["sig_p"]**2, params["strModel"])

    # make plots
    plots_6(x_true, x_est, p_est, k, z)


if __name__ == '__main__':
    example_6()

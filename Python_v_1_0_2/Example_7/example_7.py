def example_7():
    """
    Description

    Like in the previous example, in this example we are going to estimate the temperature of a liquid in a tank.
    In this case, though, the system dynamics is not constant - the liquid is heating at a rate of 0.1deg every second.

    """
    from KF_common.addNoise import addNoise
    from KF_OneDim.KF_1D import KF_1D
    from Example_7.initParams_7 import initParams_7
    from Example_7.scenario_7 import scenario_7
    from Example_7.plots_7 import plots_7

    # load example parameters
    params = initParams_7('KF')

    # create scenario
    x_true = scenario_7(params["dt"])

    # create measurements
    ngParams = initParams_7('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)

    # run the 1D Kalman Filter
    x_est, x_pred, p_est, p_pred, k = KF_1D(z, params["r"], params["x0"], params["p0"], params["sig_p"]**2, params["strModel"])

    # make plots
    plots_7(x_true, x_est, p_est, k, z)


if __name__ == '__main__':
    example_7()


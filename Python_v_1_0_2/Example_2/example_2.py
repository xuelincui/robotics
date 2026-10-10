def example_2():
    """
    Description

    In this example, we are going to track a constant-velocity aircraft in one dimension using the α-β filter.

    """
    from KF_common.addNoise import addNoise
    from KF_OneDim.alphaBetaGammaFilter import alphaBetaGammaFilter
    from Example_2.scenario_2 import scenario_2
    from Example_2.initParams_2 import initParams_2
    from Example_2.plots_2 import plots_2

    # load example parameters
    params = initParams_2('KF')

    # create scenario
    x_true, v_true = scenario_2(params["dt"])

    # create measurements
    ngParams = initParams_2('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)

    # run the alpha-beta-gamma filter
    x_est, v_est, _, x_pred, v_pred, _ = alphaBetaGammaFilter(params["dt"], params["x0"], params["v0"], params["a0"], z, params["alpha"], params["beta"])

    # make plots
    plots_2(x_true, v_true, x_est, v_est, x_pred, v_pred, z, params["dt"])


if __name__ == '__main__':
    example_2()

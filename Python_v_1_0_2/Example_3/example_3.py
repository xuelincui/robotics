def example_3():
    """
    Description

    In this example, we are going to track an aircraft that is moving with constant acceleration with the α−β filter
    that was already explained in the previous example.
    
    """
    from KF_common.addNoise import addNoise
    from KF_OneDim.alphaBetaGammaFilter import alphaBetaGammaFilter
    from Example_3.initParams_3 import initParams_3
    from Example_3.scenario_3 import scenario_3
    from Example_2.plots_2 import plots_2

    # load example parameters
    params = initParams_3('KF')

    # create scenario
    x_true, v_true, _ = scenario_3(params["dt"])

    # create measurements
    ngParams = initParams_3('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)

    # run the alpha-beta-gamma filter
    x_est, v_est, _, x_pred, v_pred, _ = alphaBetaGammaFilter(params["dt"], params["x0"], params["v0"], params["a0"], z, params["alpha"], params["beta"])

    # make plots
    plots_2(x_true, v_true, x_est, v_est, x_pred, v_pred, z, params["dt"])


if __name__ == '__main__':
    example_3()

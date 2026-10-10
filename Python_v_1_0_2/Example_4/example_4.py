def example_4():
    """
    Description
    
    In this example, we are going to track an aircraft that is moving with constant acceleration with the α−β−γ filter.

    """
    from KF_common.addNoise import addNoise
    from KF_OneDim.alphaBetaGammaFilter import alphaBetaGammaFilter
    from Example_4.scenario_4 import scenario_4
    from Example_4.initParams_4 import initParams_4
    from Example_4.plots_4 import plots_4

    # load example parameters
    params = initParams_4('KF')

    # create scenario
    x_true, v_true, a_true = scenario_4(params["dt"])

    # create measurements
    ngParams = initParams_4('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)

    # run the alpha-beta-gamma filter
    x_est, v_est, a_est, x_pred, v_pred, a_pred = alphaBetaGammaFilter(params["dt"], params["x0"], params["v0"], params["a0"], z, params["alpha"], params["beta"], params["gamma"])

    # make plots
    plots_4(x_true, v_true, a_true, x_est, v_est, a_est, x_pred, v_pred, a_pred, z, params["dt"])


if __name__ == '__main__':
    example_4()


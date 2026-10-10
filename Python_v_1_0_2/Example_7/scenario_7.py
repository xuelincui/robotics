def scenario_7(dt):
    """
    The scenario creates heating liquid temperature for 100 measurements

    Inputs
    ---------------------------------------------------------------------------------------------------
    dt              scalar              seconds     time between samples
    ---------------------------------------------------------------------------------------------------


    Outputs
    ---------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------------
    x             vector              deg         liquid temperature
    ---------------------------------------------------------------------------------------------------

    """
    import numpy as np
    import matplotlib.pyplot as plt
    from Example_7.initParams_7 import initParams_7
    from KF_common.addNoise import addNoise

    # init parameters
    params = initParams_7('scenario')

    # init parameters
    n = np.arange(1, params["n"]+1)    # number of time samples
    x = np.tile(params["x_true"], n.size) + params["heatRate"] * n * dt

    # create true values with process noise
    x = addNoise(x, params["sig_p"], params)

    if params["isPlotScenario"]:
        # plot of the liquid temperature
        fig = plt.figure(figsize=(17, 9))

        plt.plot(n, x, '-g', linewidth=3)

        plt.xlabel('Measurement Number', fontsize=22)
        plt.ylabel('Temperature ($^o$C)', fontsize=22)
        plt.title('Liquid Temperature vs. Time', fontsize=26)

        # plt.show()

    return x

def example_1():
    """
    Description

    In this example, we are going to estimate the weight of a gold bar. We have unbiased scales, i.e. 
    the scales’ measurements don't have a systematic error, but the measurements do include random noise. 
    
    In this example, the system is the gold bar and the system's state is the weight of the gold bar. 
    The system's dynamic model is constant, since we assume that the weight doesn't change over short periods of time.

    """
    from KF_common.addNoise import addNoise
    from KF_OneDim.avgFilter import avgFilter
    from Example_1.initParams_1 import initParams_1
    from Example_1.scenario_1 import scenario_1
    from Example_1.plots_1 import plots_1

    # load example parameters
    params = initParams_1('KF')

    # create weights vector
    x_true = scenario_1()

    # create measurements
    ngParams = initParams_1('noiseGen')  # parameters related to noise generation
    z = addNoise(x_true, params["r"], ngParams)

    x_est = avgFilter(z, params["x0"])

    plots_1(x_true, x_est, z)


if __name__ == '__main__':
    example_1()

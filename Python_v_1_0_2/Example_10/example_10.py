def example_10():
    """
    Description

    In this example, we will estimate the altitude of a rocket. The rocket is equipped with an onboard altimeter that
    provides altitude measurements. In addition to an altimeter, the rocket is equipped with an accelerometer that
    measures the rocket acceleration.

    The accelerometer serves as a control input to the Kalman Filter.
    We assume constant acceleration dynamics.

    """

    import numpy as np
    from KF_common.addNoise import addNoise
    from Example_10.scenario_10 import scenario_10
    from Example_10.H_matrix_10 import H_matrix_10
    from KF_MultiDim.R_matrix import R_matrix
    from KF_MultiDim.motion_F_matrix import motion_F_matrix
    from KF_MultiDim.motion_G_matrix import motion_G_matrix
    from KF_MultiDim.motion_Q_matrix import motion_Q_matrix
    from KF_MultiDim.sanityCheck import sanityCheck
    from KF_MultiDim.KF import KF
    from Example_10.plots_10 import plots_10
    from Example_10.initParams_10 import initParams_10


    # load example parameters
    params = initParams_10('KF')

    # create scenario
    X_true, A_true = scenario_10(params["dt"])

    # create measurements
    ngParams = initParams_10('noiseGenAlt')            # parameters related to altimeter noise generation
    Z = addNoise(X_true[0, :], params["r"], ngParams)  # altimeter measurements
    ngParams = initParams_10('noiseGenAcc')            # parameters related to altimeter noise generation
    A = addNoise(A_true, params["sig_a"], ngParams)    # accelerometer measurements

    U = A + params["g"]   # Accelerometers don't sense gravity. An accelerometer at rest on a table would measure 1g upwards.

    #  Prepare KF building blocks
    F = motion_F_matrix(params["dt"], params["strModel"], params["dim"])  # create F matrix (State Transition Matrix)
    G = motion_G_matrix(params["dt"], params["strModel"])                 # create G matrix (Control Matrix)
    Q = motion_Q_matrix(params["dt"], params["sig_a"], params["strModel"],
                        params["dim"], params["strNoiseModel"])           # create Q matrix (Process Noise Matrix)
    R = R_matrix(params["r"])                                             # create r matrix (measurement Noise Matrix)
    H = H_matrix_10()                                                     # create H matrix (Observation Matrix)

    # sanity check - before running the Kalman Filter, check correctness of all building blocks
    Z, x0, U, u0 = sanityCheck(Z, R, H, F, Q, params["P0"], params["x0"], G, U, params["u0"])

    # run the Kalman Filter
    X_est, X_pred, P_est, P_pred, K = KF(Z, R, H, F, Q, params["P0"], x0, G, U, u0)

    # make plots
    plots_10(X_true, K, X_est, P_est, Z, params["dt"])


if __name__ == '__main__':
    example_10()

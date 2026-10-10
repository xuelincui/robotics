def example_9():
    """
    Description

    In this example, we would like to estimate the location of the vehicle in
    the XY plane using a multi-dimensional Kalman Filter.

    The vehicle has an onboard location sensor that reports X and Y coordinates of the system.
    We assume constant acceleration dynamics.

    """

    import numpy as np
    from KF_common.addNoise import addNoise
    from Example_9.scenario_9 import scenario_9
    from Example_9.H_matrix_9 import H_matrix_9
    from KF_MultiDim.R_matrix import R_matrix
    from KF_MultiDim.motion_F_matrix import motion_F_matrix
    from KF_MultiDim.motion_Q_matrix import motion_Q_matrix
    from KF_MultiDim.sanityCheck import sanityCheck
    from KF_MultiDim.KF import KF
    from Example_9.initParams_9 import initParams_9
    from Example_9.plots_9 import plots_9

    # load example parameters
    params = initParams_9('KF')

    # create scenario
    X_true = scenario_9(params["dt"])

    # create measurements
    ngParams = initParams_9('noiseGen')  # parameters related to noise generation
    Z = addNoise(X_true[[0, 3], :], params["r"], ngParams)

    #  Prepare KF building blocks
    F = motion_F_matrix(params["dt"], params["strModel"], params["dim"])  # create F matrix (State Transition Matrix)
    Q = motion_Q_matrix(params["dt"], params["sig_a"],
                        params["strModel"], params["dim"],
                        params["strNoiseModel"])                          # create Q matrix (Process Noise Matrix)
    R = R_matrix(params["r"], Z.shape[0])                                 # create r matrix (measurement Noise Matrix)
    H = H_matrix_9()                                                      # create H matrix (Observation Matrix)


    # sanity check - before running the Kalman Filter, check correctness of all building blocks
    Z, x0, U, u0 = sanityCheck(Z, R, H, F, Q, params["P0"], params["x0"])

    # run the Kalman Filter
    X_est, X_pred, P_est, P_pred, K = KF(Z, R, H, F, Q, params["P0"], params["x0"])

    # make plots
    plots_9(X_true, X_est, P_est, Z, params["dt"])


if __name__ == '__main__':
    example_9()

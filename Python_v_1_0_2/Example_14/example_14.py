def example_14():
    """
    Description

    In this example, we would like to estimate the angle and the angular velocity of the pendulum
    using an Extended Kalman Filter.

    The pendulum position measurements are the EKF input.

    """

    import numpy as np
    from KF_common.addNoise import addNoise
    from Example_12.scenario_12 import scenario_12
    from Example_14.H_matrix_14 import H_matrix_14
    from Example_14.F_matrix_14 import F_matrix_14
    from KF_MultiDim.R_matrix import R_matrix
    from KF_MultiDim.motion_Q_matrix import motion_Q_matrix
    from KF_MultiDim.sanityCheck import sanityCheck
    from UKF.UKF import UKF
    from Example_12.plots_12 import plots_12
    from Example_14.scenario_14 import scenario_14
    from Example_14.initParams_14 import initParams_14

    # load example parameters
    params = initParams_14('KF')

    # create scenario
    X_true, L = scenario_14(params["dt"])

    # create measurement
    Z = L * np.sin(X_true[0, :])
    Z = addNoise(Z, params["r"], params)  # measurements

    #  Prepare KF building blocks
    Q = motion_Q_matrix(params["dt"], params["sig_a"], params["strModel"],
                        params["dim"], params["strNoiseModel"])  # create Q matrix (Process Noise Matrix)
    R = R_matrix(params["r"])  # create r matrix (measurement Noise Matrix)

    # create input arguments for H marix and F marix creation functions

    # In EKF we need to compute H and F matrices derivatives (dH/dx and dF/dx) that depend on x.
    # For the sake of generality, we pass H and F matrix creation function handles to the EKF function
    # As well, we pass functions input arguments
    Hargs = (L,)
    Fargs = (params["g"], L, params["dt"])

    # sanity check
    # before running the Kalman Filter, check correctness of all building blocks
    Z, _, _, _ = sanityCheck(Z, R, None, None, Q, params["P0"], params["x0"])

    # run the Extended Kalman Filter
    X_est, X_pred, P_est, P_pred, K = UKF(Z, R, H_matrix_14, Hargs, F_matrix_14, Fargs, Q,
                                          params["P0"], params["x0"], params["sigmaPntAlgo"], params["alpha"])

    # make plots
    plots_12(X_true, X_est, P_est, Z, params["dt"], L)


if __name__ == '__main__':
    example_14()

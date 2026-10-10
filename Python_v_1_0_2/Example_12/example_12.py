def example_12():
    """
    Description

    In this example, we would like to estimate the angle and the angular velocity of the pendulum
    using an Extended Kalman Filter.

    The pendulum position measurements are the EKF input.

    """

    import numpy as np
    from KF_common.addNoise import addNoise
    from Example_12.scenario_12 import scenario_12
    from Example_12.H_matrix_12 import H_matrix_12
    from Example_12.F_matrix_12 import F_matrix_12
    from KF_MultiDim.R_matrix import R_matrix
    from KF_MultiDim.motion_Q_matrix import motion_Q_matrix
    from KF_MultiDim.sanityCheck import sanityCheck
    from EKF.EKF import EKF
    from Example_12.plots_12 import plots_12
    from Example_12.initParams_12 import initParams_12

    # load example parameters
    params = initParams_12('KF')

    # create scenario
    X_true, L = scenario_12(params["dt"])

    # create measurement
    Z = L * np.sin(X_true[0,:])
    Z = addNoise(Z, params["r"], params)    # measurements

    #  Prepare KF building blocks
    Q = motion_Q_matrix(params["dt"], params["sig_a"], params["strModel"],
                        params["dim"], params["strNoiseModel"])    # create Q matrix (Process Noise Matrix)
    R = R_matrix(params["r"])                                      # create r matrix (measurement Noise Matrix)


    # create input arguments for H marix and F marix creation functions

    # In EKF we need to compute H and F matrices derivatives (dH/dx and dF/dx) that depend on x.
    # For the sake of generality, we pass H and F matrix creation function handles to the EKF function
    # As well, we pass functions input arguments
    Hargs = (L,)
    Fargs = (params["g"], L, params["dt"])

    # sanity check
    # just for the sanity check, create H and F matrices, not realy needed here. Computed inside EKF function
    _, dHx = H_matrix_12(params["x0"], Hargs)  # create H matrix (Observation Function Matrix) derivative at x0
    _, dFx = F_matrix_12(params["x0"], Fargs)  # create F matrix (State Transition Function Matrix) derivative at x0

    # before running the Kalman Filter, check correctness of all building blocks
    Z, _, _, _ = sanityCheck(Z, R, dHx, dFx, Q, params["P0"], params["x0"])

    # run the Extended Kalman Filter
    X_est, X_pred, P_est, P_pred, K = EKF(Z, R, H_matrix_12, Hargs, F_matrix_12, Fargs, Q, params["P0"], params["x0"])

    # make plots
    plots_12(X_true, X_est, P_est, Z, params["dt"], L)


if __name__ == '__main__':
    example_12()

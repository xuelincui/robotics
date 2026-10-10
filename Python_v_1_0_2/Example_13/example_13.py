def example_13():
    """
    Description

    In this example, we would like to estimate the location of the vehicle in
    the XY plane using an Extended Kalman Filter.

    The vehicle position is measured by the radar, that located at origin of the XY plane.
    The radar measures the range to the vehicle and the azimuthal angle to the vehicle.

    We assume constant acceleration dynamics.
    """

    import numpy as np
    from KF_common.addNoise import addNoise
    from Example_13.scenario_13 import scenario_13
    from Example_13.H_matrix_13 import H_matrix_13
    from Example_13.F_matrix_13 import F_matrix_13
    from KF_MultiDim.R_matrix import R_matrix
    from KF_MultiDim.motion_Q_matrix import motion_Q_matrix
    from KF_MultiDim.sanityCheck import sanityCheck
    from UKF.UKF import UKF
    from Example_11.plots_11 import plots_11
    from Example_13.initParams_13 import initParams_13

    # load example parameters
    params = initParams_13('KF')

    # create scenario
    X_true, R_true, phi_true = scenario_13(params["dt"])

    # create measurement
    Z = np.stack((R_true, phi_true))
    ngParams = initParams_13('noiseGen')  # parameters related to noise generation
    Z = addNoise(Z, params["r"], ngParams)

    #  Prepare KF building blocks
    Q = motion_Q_matrix(params["dt"], params["sig_a"],
                        params["strModel"], params["dim"],
                        params["strNoiseModel"])  # create Q matrix (Process Noise Matrix)
    R = R_matrix(params["r"], Z.shape[0])  # create r matrix (measurement Noise Matrix)


    # create input arguments for H marix and F marix creation functions
    # In EKF we need to compute H and F matrices derivatives (dH/dx and dF/dx) that depend on x.
    # For the sake of generality, we pass H and F matrix creation function handles to the EKF function
    # As well, we pass functions input arguments
    Hargs = ()
    Fargs = (params["dt"], params["strModel"], params["dim"])

    # sanity check
    # before running the Kalman Filter, check correctness of all building blocks
    sanityCheck(Z, R, None, None, Q, params["P0"], params["x0"])

    # run the Extended Kalman Filter
    X_est, X_pred, P_est, P_pred, K = UKF(Z, R, H_matrix_13, Hargs, F_matrix_13, Fargs, Q, params["P0"], params["x0"],
                                          params["sigmaPntAlgo"], params["alpha"])


    # make plots
    plots_11(X_true, X_est, P_est, Z, params["dt"])


if __name__ == '__main__':
    example_13()

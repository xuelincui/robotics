def EKF(Z, R, Hhndl, Hargs, Fhndl, Fargs, Q, P0, x0):
    """

    Description
    This is a generic function.
    This function runs the Extended Kalman Filter in the loop for all measurements.


    Inputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Size                Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Z             matrix              n_z * n_m           measurements
                                                          rows represent different states)
                                                          (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    R             matrix              n_z * n_z           Measurement Noise Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Hhndl                                                 Handle to Observation Matrix function
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Hargs                                                 Input arguments Handle to Observation Matrix function
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Fhndl                                                 Handle to Dynamic Model Matrix function
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Fargs                                                 Input arguments Dynamic Model Matrix function
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Q             matrix              n_x * n_x           Process Noise Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P0            matrix              n_x * n_x           Initial Estimate Covariance Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x0            vector              n_x * 1             Initial State Vector
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------


    n_x is the number of states
    n_z is the number of measured parameters
    n_m is the number of measurements


    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Size                Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X_est         matrix              n_x * n_m           Record of the State Vector estimations for each KF iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X_pred        matrix              n_x * (n_m+1)       Record of the State Vector predictions for each KF iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P_est      	  matrix              n_x * n_x * n_m     Record of the estimation covariance for each KF iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P_pred        matrix              n_x * n_x * (n_m+1) Record of the estimation covariance for each KF iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    K             matrix/vector       n_x * n_z * n_m     Record of the Kalman Gains for each KF iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np

    # filter init
    x = x0
    P = P0

    # dimensions
    n_z = Z.shape[0]
    n_x = x0.shape[0]
    n_m = Z.shape[1]

    # init variables that will keep the record of historical x, P and K
    X_est = np.zeros((n_x, n_m))
    X_pred = np.zeros((n_x, n_m + 1))
    P_est = np.zeros((n_x, n_x, n_m))
    P_pred = np.zeros((n_x, n_x, n_m + 1))
    K = np.zeros((n_x, n_z, n_m))

    # Run the filter
    for i in range(n_m):

        # predict
        Fx, dFx = Fhndl(x, Fargs)

        x_p = Fx
        P_p = dFx @ P @ dFx.T + Q

        # update
        Hx, dHx = Hhndl(x_p, Hargs)

        PHT = P_p @ dHx.T  # compute once - saves double matrix multiplication in the Kalman Gain computation
        k = PHT @ np.linalg.inv((dHx @ PHT + R))

        x = x_p + k @ (Z[:, i:i + 1] - Hx)

        kH = np.eye(n_x) - k @ dHx  # compute once - saves double matrix multiplication in the Covariance Update computation
        P = kH @ P_p @ kH.T + k @ R @ k.T

        # update the record
        X_est[:, i:i + 1] = x
        P_est[:, :, i:i + 1] = P[..., np.newaxis]
        K[:, :, i:i + 1] = k[..., np.newaxis]
        X_pred[:, i:i + 1] = x_p
        P_pred[:, :, i:i + 1] = P_p[..., np.newaxis]

    # predict the next state
    Fx, dFx = Fhndl(x, Fargs)

    X_pred[:, i + 1:i + 2] = Fx
    P_p = dFx @ P @ dFx.T + Q
    P_pred[:, :, i + 1:i + 2] = P_p[..., np.newaxis]

    return X_est, X_pred, P_est, P_pred, K
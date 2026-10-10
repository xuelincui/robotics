def KF(Z, R, H, F, Q, P0, x0, G=None, U=None, u0=None):
    """
    This is a generic function.
    This function runs the Kalman Filter in the loop for all measurements.
    
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
    H             matrix              n_z * n_x           Observation Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    F             matrix              n_x * n_x           Dynamic Model Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Q             matrix              n_x * n_x           Process Noise Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P0            matrix              n_x * n_x           Initial Estimate Covariance Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x0            vector              n_x * 1             Initial State Vector
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    G             vector              n_x * n_u           Control Matrix
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    U             matrix              n_u * n_m           Control Input
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    u0            vector              n_u * 1             Initial Control Input
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

    # dimensions
    if G is None:
        # no control input
        G = np.array([[0]])                 # Control Matrix
        U = np.zeros((1, Z.shape[1] + 1))   # Control Input
    else:
        U = np.concatenate([u0, U], axis=1)

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
        x_p = F @ x + G @ U[:, i:i+1]
        P_p = F @ P @ F.T + Q

        # update
        PHT = P_p @ H.T  # compute once - saves double matrix multiplication in the Kalman Gain computation
        k = PHT @ np.linalg.inv((H @ PHT + R))

        x = x_p + k @ (Z[:, i:i+1] - H @ x_p)

        kH = np.eye(n_x) - k @ H  # compute once - saves double matrix multiplication in the Covariance Update computation
        P = kH @ P_p @ kH.T + k @ R @ k.T

        # update the record
        X_est[:, i:i+1] = x
        P_est[:, :, i:i+1] = P[..., np.newaxis]
        K[:, :, i:i+1] = k[..., np.newaxis]
        X_pred[:, i:i+1] = x_p
        P_pred[:, :, i:i+1] = P_p[..., np.newaxis]


    # predict the next state
    X_pred[:, i+1:i+2] =  F @ x + G @ U[:, i+1:i+2]
    P_p = F @ P @ F.T + Q
    P_pred[:, :, i+1:i+2] = P_p[..., np.newaxis]

    return X_est, X_pred, P_est, P_pred, K
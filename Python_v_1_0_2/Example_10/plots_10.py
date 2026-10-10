def plots_10(X_true, K, X_est, P_est, Z, dt):
    """
    This function creates altitude, velocity and Kalman Gain plots for example 10.

    The altitude plot describes the rocket altitude vs. time and compares between true altitude, measured altitude and estimated altitude
    The velocity plot describes the rocket velocity vs. time and compares between true velocity and estimated velocity
    The Kalman Gain plot describes the Kalman Gain convergence vs. time


    Inputs
    --------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    --------------------------------------------------------------------------------------------
    X_true         matrix                         true rocket altitude and velocity
                                                  (first row is the altitude)
                                                  (second row is the velocity)
    --------------------------------------------------------------------------------------------
    X_est         matrix                          estimated rocket altitude and velocity
                                                  (first row is the altitude)
                                                  (second row is the velocity)
    --------------------------------------------------------------------------------------------
    P_est         matrix                          estimation covariance for each KF iteration
    --------------------------------------------------------------------------------------------
    Z             vector                          Altitude Measurements
    --------------------------------------------------------------------------------------------
    K             matrix                          Kalman Gain
    --------------------------------------------------------------------------------------------
    dt            scalar              seconds     time between samples
    --------------------------------------------------------------------------------------------

    """

    import numpy as np
    import matplotlib.pyplot as plt
    from KF_common.plotConfInt import plotConfInt

    t = np.arange(0, X_true.shape[1] * dt, dt)

    # altitude
    fig = plt.figure(figsize=(17, 9))

    plt.plot(t, X_true[0, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')

    plt.plot(t, Z[0,: ], '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6,
             label='Measurements')

    plt.plot(t, X_est[0, :],  '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    # plot 95% confidence intervals
    plotConfInt(X_est[0, :], np.squeeze(P_est[0, 0,:]), t, 95)

    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Altitude (m)', fontsize=14, color='darkred')
    plt.title('Rocket Altitude', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.grid(which='both', color='0.95', linestyle='-')

    # plt.show()

    # velocity
    fig = plt.figure(figsize=(17, 9))
    plt.plot(t, X_true[1, :],'-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')
    plt.plot(t, X_est[1, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    # plot 95% confidence intervals
    plotConfInt(X_est[1, :], np.squeeze(P_est[1, 1, :]), t, 95)

    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Velocity (m/s)', fontsize=14, color='darkred')
    plt.title('Rocket Velocity', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.grid(which='both', color='0.95', linestyle='-')

    # plt.show()

    # Kalman Gain
    K = np.squeeze(K)

    fig = plt.figure(figsize=(17, 9))

    plt.plot(t, K[0,:], 'k', markerfacecolor=(0.5, 0.5, 0.5), linewidth=3, markeredgewidth=3, markersize=10)

    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Kalman Gain', fontsize=14, color='darkred')
    plt.title('Kalman Gain', fontsize=22, color='darkred', fontweight='bold')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.show()
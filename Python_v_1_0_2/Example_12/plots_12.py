def plots_12(X_true, X_est, P_est, Z, dt, L):
    """
    Description
    This function creates angle and angular velocity plots for example 12.

    The position plot describes XY vehicle position and compares between true position, measured position and estimated position
    The velocity plot describes Vx vs. time and Vy vs. time vehicle velocity and compares between true velocity and estimated velocity
    The acceleration plot describes Ax vs. time and Ay vs. time vehicle acceleration and compares between true acceleration and estimated acceleration


    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X_true        matrix                          true pendulum angle and angular velocity
                                                  (first row is the pendulum angle, second row is the pendulum angular velocity)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X_est         matrix                          estimated pendulum angle and angular velocity
                                                  (first row is the pendulum angle, second row is the pendulum angular velocity)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P_est         matrix                          estimation covariance for each KF iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Z             vector              meters      measured value: L*sin(theta)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dt            scalar              seconds     time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    L             scalar              meters      Pendulum string length
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    from matplotlib import pyplot as plt
    import numpy as np
    from KF_common.plotConfInt import plotConfInt

    t = np.arange(0, X_true.shape[1] * dt, dt)

    # calculate measured angle
    theta_meas = np.arcsin(Z / L)

    # pendulum angle plot
    fig = plt.figure(figsize=(17, 9))

    plt.plot(t, theta_meas[0,:], '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6,
             label='Measurements')
    plt.plot(t, X_est[0, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(t, X_true[0, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')
    plt.grid(which='both', color='0.95', linestyle='-')

    # plot 95% confidence intervals
    plotConfInt(X_est[0,:], np.squeeze(P_est[0, 0,:]), t, 95)


    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Theta (rad)', fontsize=14, color='darkred')
    plt.title('Pendulum  Angle', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')


    # pendulum angular velocity plot
    fig = plt.figure(figsize=(17, 9))

    plt.plot(t, X_est[1, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(t, X_true[1, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8, label='True values')
    plt.grid(which='both', color='0.95', linestyle='-')

    # plot confidence 95% intervals
    plotConfInt(X_est[1, :], np.squeeze(P_est[1, 1, :]), t, 95)

    plt.xlabel('Time (s)', fontsize=14, color='darkred')
    plt.ylabel('Angular Velocity (rad/s)', fontsize=14, color='darkred')
    plt.title('Pendulum  Angular Velocity', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.show()

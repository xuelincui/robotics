def plots_11(X_true, X_est, P_est, Z, dt):
    """
    This function creates position, velocity and acceleration plots for example 11.

    The position plot describes XY vehicle position and compares between true position, measured position and estimated position
    The velocity plot describes Vx vs. time and Vy vs. time vehicle velocity and compares between true velocity and estimated velocity
    The acceleration plot describes Ax vs. time and Ay vs. time vehicle acceleration and compares between true acceleration and estimated acceleration


    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X_true        matrix                          true vehicle position, velocity and acceleration
                                                  (first row is the X axis position, second row is the X axis velocity, third row is is the X axis acceleration)
                                                  (fourth row is the Y axis position, fifth row is the Y axis velocity, sixth row is is the Y axis acceleration)
                                                  (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X_est         matrix                          estimated vehicle position, velocity and acceleration
                                                  (first row is the X axis position, second row is the X axis velocity, third row is is the X axis acceleration)
                                                  (fourth row is the Y axis position, fifth row is the Y axis velocity, sixth row is is the Y axis acceleration)
                                                  (columns represent states at different time samples)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    P_est         matrix                          covariance of the estimated vehicle position, velocity and acceleration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Z             matrix                          measured vehicle range and azimuth
                                                  (first row is the vehicle range, second row is the vehicle azimuth)
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    dt            scalar              seconds     time between samples
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    from matplotlib import pyplot as plt
    import numpy as np
    from KF_common.plotConfEllipse import plotConfEllipse

    t = np.arange(0, X_true.shape[1] * dt, dt)

    # calculate measured x and y parameters
    X_meas = np.zeros((2, Z.shape[1]))
    X_meas[0,:] = Z[0, :]*np.cos(Z[1, :])  # X
    X_meas[1,:] = Z[0, :]*np.sin(Z[1, :])  # Y


    fig = plt.figure(figsize=(17, 9))

    # position and velocity plot

    # position
    plt.subplot(121)
    h1, = plt.plot(X_meas[0, :], X_meas[1, :], '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6)
    h2, = plt.plot(X_est[0, :], X_est[3, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8)
    h3, = plt.plot(X_true[0, :], X_true[3, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8)
    plt.grid(which='both', color='0.95', linestyle='-')

    # plot uncertainty ellipses
    elpsCenter = np.array([X_est[0, :], X_est[3, :]])  # the actual value is an ellipse center
    covXY = np.array([[P_est[0, 0, :], P_est[0, 3, :]], [P_est[3, 0, :], P_est[3, 3, :]]])

    h4 = plotConfEllipse(elpsCenter, covXY, 1, 95)
    h5 = plotConfEllipse(elpsCenter, covXY, 2)

    plt.xlabel('X (m)', fontsize=18, color='darkred')
    plt.ylabel('Y (m)', fontsize=18, color='darkred')
    plt.title('Vehicle  Position', fontsize=22, color='darkred', fontweight='bold')


    plt.legend([h1, h2, h3, h4, h5], ['Measurements', 'Estimates', 'True values', '95% confidence ellipse', 'Covariance ellipse'],
               fontsize='x-large', bbox_to_anchor=(2, 1))


    plt.gca().set_aspect('equal')

    # velocity
    plt.subplot(222)
    plt.plot(t, X_est[1, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(t, X_true[1,:], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.xlabel('Time (s)', fontsize=18, color='darkred')
    plt.ylabel('Vx (m/s)', fontsize=18, color='darkred')
    plt.title('Vehicle  X-axis velocity', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.subplot(224)
    plt.plot(t, X_est[4, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(t, X_true[4, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.xlabel('Time (s)', fontsize=18, color='darkred')
    plt.ylabel('Vy (m/s)', fontsize=18, color='darkred')
    plt.title('Vehicle  Y-axis velocity', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    fig.tight_layout()

    # acceleration plot
    fig = plt.figure(figsize=(17, 9))


    plt.subplot(211)
    plt.plot(t, X_est[2, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(t, X_true[2, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.xlabel('Time (s)', fontsize=18, color='darkred')
    plt.ylabel('Ax ($m/s^2$)', fontsize=18, color='darkred')
    plt.title('Vehicle  X-axis acceleration', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.subplot(212)
    plt.plot(t, X_est[5, :], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    plt.plot(t, X_true[5, :], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.xlabel('Time (s)', fontsize=18, color='darkred')
    plt.ylabel('Ay ($m/s^2$)', fontsize=18, color='darkred')
    plt.title('Vehicle  Y-axis acceleration', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    fig.tight_layout()
    plt.show()
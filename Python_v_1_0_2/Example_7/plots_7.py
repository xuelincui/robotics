def plots_7(x_true, x_est, p_est, k, z):
    """
    This function creates position, velocity and acceleration plots for example 6.

    Inputs
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_true        vector              The true value
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    x_est         vector              Record of estimations for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    p_est         vector              Record of estimates uncertainties for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    k             vector              Records of the Kalman Gain for each filter iteration
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    z             vector              Range measurements
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np
    import matplotlib.pyplot as plt
    from KF_common.plotConfInt import plotConfInt

    n = np.arange(1, 11)          # partial scale plot
    N = np.arange(1, z.size + 1)  # full scale plot

    # temperature - partial scale plot
    fig = plt.figure(figsize=(17, 9))

    plt.plot(n, x_true[0:n.size], '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')
    plt.plot(n, z[0:n.size], '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6,
             label='Measurements')
    plt.plot(n, x_est[0:n.size], '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    # plot 95% confidence intervals
    plotConfInt(x_est[0:n.size], p_est[0:n.size], n, 95)

    plt.xlabel('Measurement number', fontsize=14, color='darkred')
    plt.ylabel('Temperature ($^oC$)', fontsize=14, color='darkred')
    plt.title('The Liquid  Temperature', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')



    plt.grid(which='both', color='0.95', linestyle='-')

    # plt.show()

    # temperature - full scale plot
    fig = plt.figure(figsize=(17, 9))

    plt.plot(N, x_true, '-gd', markerfacecolor='lime', linewidth=3, markeredgewidth=2, markersize=8,
             label='True values')
    plt.plot(N, z, '-bs', markerfacecolor='c', linewidth=3, markeredgewidth=2, markersize=6,
             label='Measurements')
    plt.plot(N, x_est, '-ro', markerfacecolor='m', linewidth=3, markeredgewidth=2, markersize=8,
             label='Estimates')

    # plot 95% confidence intervals
    plotConfInt(x_est, p_est, N, 95)

    plt.xlabel('Measurement number', fontsize=14, color='darkred')
    plt.ylabel('Temperature ($^oC$)', fontsize=14, color='darkred')
    plt.title('The Liquid  Temperature', fontsize=22, color='darkred', fontweight='bold')
    plt.legend(fontsize='x-large')

    plt.grid(which='both', color='0.95', linestyle='-')

    # plt.show()

    # Kalman gain
    fig = plt.figure(figsize=(17, 9))

    plt.plot(N, k, '-k', linewidth=3)

    plt.xlabel('Measurement number', fontsize=14, color='darkred')
    plt.ylabel('Kalman Gain', fontsize=14, color='darkred')
    plt.title('Kalman Gain', fontsize=22, color='darkred', fontweight='bold')

    plt.grid(which='both', color='0.95', linestyle='-')

    plt.show()
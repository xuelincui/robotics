def scenario_12(dt, isPlotScenario = None):
    """
    Description
    This function creates scenario for example 12

    Inputs
    --------------------------------------------------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------------------------------------------
    dt              scalar              seconds     Time between samples
    ---------------------------------------------------------------------------------------------------------------------------------
    isPlotScenario  boolean                         Optional input. Indicates whether to make
                                                    scenario plots
    ---------------------------------------------------------------------------------------------------------------------------------


    Outputs
    ---------------------------------------------------------------------------------------------------------------------------------
    Variable      Variable Type       Units       Description
    ---------------------------------------------------------------------------------------------------------------------------------
    X             matrix                          true pendulum angle and angular velocity + process noise
                                                  (first row is the pendulum angle, second row is the pendulum angular velocity)
    ----------------------------------------------------------------------------------------------------------------------------------
    L             scalar              meters      Pendulum string length
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np
    from matplotlib import pyplot as plt
    from KF_common.addNoise import addNoise
    from Example_12.initParams_12 import initParams_12

    # init parameters
    params = initParams_12('scenario')

    # initial conditions
    theta0 = params["theta0"]       # initial angle (radians)
    omega0 = params["omega0"]       # initial angular velocity

    L = params["L"]                 # Pendulum string length (meters)
    g = params["g"]                 # Gravitational acceleration constant (m/s^2)

    # calculate the ideal true angle and the angular velocity
    n = np.arange(0, params["n"]+1)

    t = n * dt
    k = np.sqrt(g / L)

    theta = theta0 * np.cos(k * t) + omega0 * np.sin(k * t) / k
    omega = -k * theta0 * np.sin(k * t) + omega0 * np.cos(k * t)

    X = np.array([theta, omega])

    # add process noise to the ideal true angle and angular velocity
    sig_theta = params["sig_a"] * 0.5 * dt**2  # convert angular acceleration sigma to the angle sigma
    sig_omega = params["sig_a"] * dt  # convert angular acceleration sigma to the angular velocity sigma

    r = np.array([sig_theta, sig_omega])

    X = addNoise(X, r, params)  # add process noise


    if (isPlotScenario is None):
        isPlotScenario = params["isPlotScenario"]

    if isPlotScenario:
        # pendulum angle plot
        fig = plt.figure(figsize=(17, 9))
        plt.subplot(211)
        plt.plot(t, X[0, :], 'lime', linewidth=3)

        plt.xlabel('Time (s)', fontsize=14, color='darkred', fontweight='bold')
        plt.ylabel('Theta (rad)', fontsize=14, color='darkred', fontweight='bold')
        plt.title('Pendulum  True Angle', fontsize=20, color='darkred', fontweight='bold')
        plt.grid(which='both', color='0.95', linestyle='-')

        # pendulum angular velocity plot
        plt.subplot(212)
        plt.plot(t, X[1, :], 'lime', linewidth=3)

        plt.xlabel('Time (s)', fontsize=14, color='darkred', fontweight='bold')
        plt.ylabel('Angular Velocity (rad/s)', fontsize=14, color='darkred', fontweight='bold')
        plt.title('Pendulum  True Angular Velocity', fontsize=20, color='darkred', fontweight='bold')
        plt.grid(which='both', color='0.95', linestyle='-')

        fig.tight_layout()
        # plt.show()

    return X, L
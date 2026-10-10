def scenario_10(dt):
    """
        This function creates scenario for example 10.
        The scenario describes the vertical motion of the rocket with constant acceleration.

        Inputs
        ----------------------------------------------------------------------------------------------------------
        Variable      Variable Type       Units       Description
        ----------------------------------------------------------------------------------------------------------
        dt            scalar              seconds     time between samples
        ----------------------------------------------------------------------------------------------------------

        Outputs
        ------------------------------------------------------------------------------------------------------------
        Variable      Variable Type       Units       Description
        ------------------------------------------------------------------------------------------------------------
        X             matrix                          true rocket altitude and velocity
                                                      (first row is the altitude)
                                                      (second row is the velocity)
        ------------------------------------------------------------------------------------------------------------
        a             matrix              m/(s^2)     rocket acceleration
        ------------------------------------------------------------------------------------------------------------

    """

    import numpy as np
    import matplotlib.pyplot as plt
    from KF_common.addNoise import addNoise
    from Example_10.initParams_10 import initParams_10

    # init parameters
    params = initParams_10('scenario')

    x0 = params["x0"]  # initial altitude (meters)
    v0 = params["v0"]  # initial velocity (m / s)
    a = params["a"]    # acceleration (m / s ^ 2)
    N = params["N"]    # number of measurements
    g = params["g"]    # Gravitational acceleration constant (m/s^2)

    # create trajectory
    t = np.arange(0, dt*N, dt)          # time samples

    a = np.tile(a, t.size)  # the rocket acceleration

    # create true values with process noise
    a = addNoise(a, params["sig_a"], params)

    x = x0 + t * v0 + 0.5 * a * t**2    # the rocket altitude
    v = v0 + t * a                      # the rocket velocity
    a = a - g                           # Accelerometers don't sense gravity. An accelerometer at rest on a table would measure 1g upwards.

    X = np.vstack((x, v))

    if params["isPlotScenario"]:
        # plots of the rocket position, velocity and acceleration
        fig, axs = plt.subplots(3, figsize=(17, 9))
        axs[0].plot(t, x, 'g', linewidth=3)
        axs[0].set_xlabel('t (s)', fontsize=14)
        axs[0].set_ylabel('x (m)', fontsize=14)
        axs[0].set_title('Rocket Altitude', fontsize=22)

        axs[1].plot(t, v, 'g', linewidth=3)
        axs[1].set_xlabel('t (s)', fontsize=14)
        axs[1].set_ylabel('v (m/s)', fontsize=14)
        axs[1].set_title('Rocket Velocity', fontsize=22)

        axs[2].plot(t, a, 'g', linewidth=3)
        axs[2].set_xlabel('t (s)', fontsize=14)
        axs[2].set_ylabel('a ($m/s^2$)', fontsize=14)
        axs[2].set_title('Rocket Acceleration', fontsize=22)

        fig.tight_layout()
        # plt.show()


    return X, a
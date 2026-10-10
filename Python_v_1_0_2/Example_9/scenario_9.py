def scenario_9(dt, isPlotScenario = None):
    """
    This function creates scenario for example 9.
    The scenario is divided into two parts:
    
    1. The vehicle moves 400m in a straight line in the Y direction with a constant speed of 25m/s.
    
    2. The vehicle turns left, with a turning radius of 300 meters, while moving at the same speed. 
       The vehicle experiences acceleration due to the circular motion (the angular acceleration).
       The scenario ends when the vehicle finishes the turning maneuver (quarter circle).
    
    The vehicle route simulation considerations:
    
       For the sake of simplicity of circular movement generation, we would like to have a circle center in 
       the plane origin (x=0,y=0). Therefore, the turning maneuver should start at point (x=300; y=0), 
       and end at a point(x=0; y=300).
       Consequently, the straight-line part ends where the turning maneuver begins (x=300; y=0). 
       Therefore, the straight line should start at point (x=300; y=-400)

    
    Inputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    dt              scalar              seconds     time between samples
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    isPlotScenario  boolean                         Optional input. Indicates whether to make
                                                    scenario plots
    -------------------------------------------------------------------------------------------------------------------------------------------------------

    Outputs
    -------------------------------------------------------------------------------------------------------------------------------------------------------
    Variable        Variable Type       Units       Description
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------
    X               matrix                          true vehicle position, velocity and  acceleration
                                                    (first row is the X axis position, second row is the X axis velocity, third row is is the X axis acceleration)
                                                    (fourth row is the Y axis position, fifth row is the Y axis velocity, sixth row is is the Y axis acceleration)
                                                    (columns represent states at different time samples)

    ------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    import numpy as np
    import matplotlib.pyplot as plt
    from KF_common.addNoise import addNoise
    from Example_9.initParams_9 import initParams_9

    # init parameters
    params = initParams_9('scenario')
    v = params["v"]
    L = params["L"]
    R = params["R"]

    # Part 1 - the straight part
    mX0 = R   # start position: X axis
    mY0 = -L  # start position: Y axis

    T = L / v  # the straight part duration

    t = np.arange(0, T, dt)     # the straight part time samples (don't consider last point where t=T, since it overlaps with the first point of the secon part)

    x1 = np.zeros(t.size)       # vehicle X axis location if it starts at the plane origin (0,0)
    x1 = x1 + mX0               # vehicle X axis location shifted by 300m

    y1 = v * t                  # vehicle Y axis location if it starts at the plane origin (0,0)
    y1 = y1 + mY0               # vehicle Y axis location shifted by -400m

    Vx1 = np.zeros(x1.size)     # vehicle X axis velocity (m/s) - constant velocity
    Vy1 = v * np.ones(y1.size)  # vehicle Y axis velocity (m/s) - constant velocity

    Ax1 = np.zeros(x1.size)     # vehicle X axis acceleration (m/s^2)
    Ay1 = np.zeros(y1.size)     # vehicle Y axis acceleration (m/s^2)

    # Part 2 - the turning maneuver part
    # Due to the circular motion, the velocity and acceleration are not constant.

    omega = v / R  # angular velocity (radians per second)

    T = 0.5 * np.pi * R / v  # the turning maneuver part duration (time that takes to complete the quoter circle perimeter)

    t = np.arange(0, T, dt)  # time samples of the turning maneuver part

    x2 = R * np.cos(omega * t)  # vehicle X axis location
    y2 = R * np.sin(omega * t)  # vehicle Y axis location

    # derive target velocity:
    Vx2 = -omega * R * np.sin(omega * t)  # Vx = dx/dt = d(R*cos(omega*t))/dt = -omega*R*sin(omega*t)
    Vy2 = omega * R * np.cos(omega * t)   # Vy = dy/dt = d(R*sin(omega*t))/dt =  omega*R*cos(omega*t)

    # derive target acceleration:
    Ax2 = -(omega**2) * R * np.cos(omega * t)  # Ax = dVx/dt = d(-omega*R*sin(omega*t))/dt = -omega^2*R*cos(omega*t)
    Ay2 = -(omega**2) * R * np.sin(omega * t)  # Ay = dVy/dt = d( omega*R*cos(omega*t))/dt = -omega^2*R*sin(omega*t)

    # add process noise to the ideal motion
    Ax1 = addNoise(Ax1, params["sig_a"], params)  # add process noise
    params["seed"] = params["seed"] + 1           # change seed
    Ay1 = addNoise(Ay1, params["sig_a"], params)  # add process noise
    params["seed"] = params["seed"] + 1  # change seed
    Ax2 = addNoise(Ax2, params["sig_a"], params)  # add process noise
    params["seed"] = params["seed"] + 1  # change seed
    Ay2 = addNoise(Ay2, params["sig_a"], params)  # add process noise

    x1 = x1 + 0.5 * Ax1 * dt**2  # Add process noise to position
    y1 = y1 + 0.5 * Ay1 * dt**2  # Add process noise to position
    x2 = x2 + 0.5 * Ax2 * dt**2  # Add process noise to position
    y2 = y2 + 0.5 * Ay2 * dt**2  # Add process noise to position

    Vx1 = Vx1 + Ax1 * dt  # Add process noise to velocity
    Vy1 = Vy1 + Ay1 * dt  # Add process noise to velocity

    Vx2 = Vx2 + Ax2 * dt  # Add process noise to velocity
    Vy2 = Vy2 + Ay2 * dt  # Add process noise to velocity

    # combine two parts
    x = np.concatenate((x1, x2))
    y = np.concatenate((y1, y2))
    Vx = np.concatenate((Vx1, Vx2))
    Vy = np.concatenate((Vy1, Vy2))
    Ax = np.concatenate((Ax1, Ax2))
    Ay = np.concatenate((Ay1, Ay2))

    # stack into the state vector
    X = np.vstack((x, Vx, Ax, y, Vy, Ay))

    if (isPlotScenario is None):
        isPlotScenario = params["isPlotScenario"]

    if isPlotScenario:
        # plots of the vehicle position, velocity and acceleration

        # position
        fig = plt.figure
        plt.plot(X[0,:], X[3,:], 'g', linewidth=3,)
        plt.xlabel('X (m)', fontsize=18, color='darkred')
        plt.ylabel('Y (m)', fontsize=18, color='darkred')
        plt.title('Vehicle Position', fontsize=22, color='darkred', fontweight='bold')

        #plt.legend(fontsize='x-large')
        plt.gca().set_aspect('equal')
        plt.grid(which='both', color='0.95', linestyle='-')



        # velocity
        t = np.arange(0, X.shape[1], dt)  # time samples

        fig, axs = plt.subplots(2, figsize=(17, 9))
        axs[0].plot(t, X[1,:], 'g', linewidth=3)
        axs[0].set_title('Vehicle  X-axis velocity', fontsize=22, color='darkred', fontweight='bold')
        axs[0].set_xlabel('t (s)', fontsize=14, color='darkred')
        axs[0].set_ylabel('Vx (m/s)', fontsize=14, color='darkred')
        axs[0].grid(which='both', color='0.95', linestyle='-')

        axs[1].plot(t, X[4,:], 'g', linewidth=3)
        axs[1].set_title('Vehicle  Y-axis velocity', fontsize=22, color='darkred', fontweight='bold')
        axs[1].set_xlabel('t (s)', fontsize=14, color='darkred')
        axs[1].set_ylabel('Vy (m/s)', fontsize=14, color='darkred')
        axs[1].grid(which='both', color='0.95', linestyle='-')

        fig.tight_layout()


        # acceleration
        t = np.arange(0, X.shape[1], dt)  # time samples

        fig, axs = plt.subplots(2, figsize=(17, 9))
        axs[0].plot(t, X[2,:], 'g', linewidth=3)
        axs[0].set_title('Vehicle  X-axis velocity', fontsize=22, color='darkred', fontweight='bold')
        axs[0].set_xlabel('t (s)', fontsize=14, color='darkred')
        axs[0].set_ylabel('A ($m/s^2$)', fontsize=14, color='darkred')
        axs[0].grid(which='both', color='0.95', linestyle='-')

        axs[1].plot(t, X[5,:], 'g', linewidth=3)
        axs[1].set_title('Vehicle  Y-axis velocity', fontsize=22, color='darkred', fontweight='bold')
        axs[1].set_xlabel('t (s)', fontsize=14, color='darkred')
        axs[1].set_ylabel('A ($m/s^2$)', fontsize=14, color='darkred')
        axs[1].grid(which='both', color='0.95', linestyle='-')

        fig.tight_layout()
        # plt.show()

    return X
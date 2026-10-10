def confEllipse(mu, C, confInterval = 0):
    """
        This function creates a 2D confidence ellipses for a set of estimations

        Inputs
        ----------------------------------------------------------------------------------------------------------------------------------
        Variable        Variable Type       Units       Description
        ----------------------------------------------------------------------------------------------------------------------------------
        mu              matrix                          ellipse centers
                                                        (first row is the X axis coordinates)
                                                        (second row is the Y axis coordinates)
                                                        (columns represent estimates at different time samples)
        ----------------------------------------------------------------------------------------------------------------------------------
        C               matrix                          estimates covariances
                                                        (the first and the second dimensions represent 2x2 covariance matrix)
                                                        (the third dimension represent estimates at different time samples)
        ----------------------------------------------------------------------------------------------------------------------------------
        confInterval    matrix                          ellipse confidence interval. if confInterval = 0 , calculate 1 sigma uncertainty
        ----------------------------------------------------------------------------------------------------------------------------------

        Outputs
        ----------------------------------------------------------------------------------------------------------------------------------
        Variable        Variable Type       Units       Description
        ----------------------------------------------------------------------------------------------------------------------------------
        ellipseArray    array                          Each array cell contains ellipse XY coordinates
        ----------------------------------------------------------------------------------------------------------------------------------

    """

    import numpy as np

    t = np.arange(0, 2 * np.pi + np.pi / 100, np.pi / 100)

    ellipseArray = []

    for i in range(mu.shape[1]):

        eigVal, eigVec = np.linalg.eig(C[:, :, i])  # find eigenvalues and eigenvectors

        elpsAng = np.arctan(eigVec[1, 0] / eigVec[0, 0])  # ellipse angle
        rotMtrx = np.array([[np.cos(elpsAng), -np.sin(elpsAng)], [np.sin(elpsAng), np.cos(elpsAng)]])  # rotation matrix
        halfAxesLen = np.sqrt(eigVal)  # ellipse half axes

        if confInterval > 0:
            s = np.sqrt(-2*np.log(1 - confInterval))
            halfAxesLen = halfAxesLen*s  # scale the ellipse

        elps = np.array([halfAxesLen[0] * np.cos(t), halfAxesLen[1] * np.sin(t)]).T  # create zero covariance ellipse at x=0, y=0
        elps = elps @ rotMtrx.T  # rotate the ellipse
        elps = elps + mu[:, i].reshape(1,2)  # shift the ellipse

        ellipseArray.append(elps)

    return ellipseArray
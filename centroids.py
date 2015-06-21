import numpy

def calculate_polygon_area(polygon, signed=False):
    """Calculate the signed area of non-self-intersecting polygon
    Input
        polygon: Numeric array of points (longitude, latitude). It is assumed
                 to be closed, i.e. first and last points are identical
        signed: Optional flag deciding whether returned area retains its sign:
                If points are ordered counter clockwise, the signed area
                will be positive.
                If points are ordered clockwise, it will be negative
                Default is False which means that the area is always positive.
    Output
        area: Area of polygon (subject to the value of argument signed)
    """

    # Make sure it is numeric
    P = numpy.array(polygon)

    # Check input
    msg = ('Polygon is assumed to consist of coordinate pairs. '
           'I got second dimension %i instead of 2' % P.shape[1])
    assert P.shape[1] == 2, msg

    msg = ('Polygon is assumed to be closed. '
           'However first and last coordinates are different: '
           '(%f, %f) and (%f, %f)' % (P[0, 0], P[0, 1], P[-1, 0], P[-1, 1]))
    assert numpy.allclose(P[0, :], P[-1, :]), msg

    # Extract x and y coordinates
    x = P[:, 0]
    y = P[:, 1]

    # Area calculation
    a = x[:-1] * y[1:]
    b = y[:-1] * x[1:]
    A = numpy.sum(a - b) / 2.

    # Return signed or unsigned area
    if signed:
        return A
    else:
        return abs(A)


def calculate_polygon_centroid(polygon):
    """Calculate the centroid of non-self-intersecting polygon
    Input
        polygon: Numeric array of points (longitude, latitude). It is assumed
                 to be closed, i.e. first and last points are identical
    Output
        Numeric (1 x 2) array of points representing the centroid
    """

    # Make sure it is numeric
    P = numpy.array(polygon)

    # Get area - needed to compute centroid
    A = calculate_polygon_area(P, signed=True)

    # Extract x and y coordinates
    x = P[:, 0]
    y = P[:, 1]

    # Exercise: Compute C as shown in http://paulbourke.net/geometry/polyarea
    a = x[:-1] * y[1:]
    b = y[:-1] * x[1:]

    cx = x[:-1] + x[1:]
    cy = y[:-1] + y[1:]

    Cx = numpy.sum(cx * (a - b)) / (6. * A)
    Cy = numpy.sum(cy * (a - b)) / (6. * A)

    # Create Nx2 array and return
    C = numpy.array([Cx, Cy])
    return C
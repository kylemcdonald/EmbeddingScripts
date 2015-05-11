#!/usr/bin/env python
import numpy
d = numpy.loadtxt("/dev/stdin");
d -= d.min(axis=0);
d /= d.max(axis=0);
numpy.savetxt("/dev/stdout", d, fmt="%.8f", delimiter="\t")

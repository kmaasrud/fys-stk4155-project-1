from numpy import (
    exp, linspace, meshgrid, random
)
import matplotlib.pyplot as plt
from matplotlib import cm
import os
import pandas as pd


def franke(x, y, noise_sigma=0, noise=False):
    """Franke's test function"""
    nineX = 9 * x
    nineY = 9 * y
    first = 0.75 * exp(-(nineX - 2)**2 * 0.25 - (nineY - 2)**2 * 0.25)
    second = 0.75 * exp(-(nineX + 1)**2 / 49 - (nineY + 1)**2 * 0.1)
    third = 0.5 * exp(-(nineX - 7)**2 * 0.25 - (nineY - 3)**2 * 0.25)
    fourth = - 0.2 * exp(-(nineX - 4)**2 - (nineY - 7)**2)
    if noise:
        rand = random.normal(0, noise_sigma)
    else:
        rand = 0

    return first + second + third + fourth + rand

def make_franke_data():
    random.seed(2020)

    N = 100
    sigma = 1

    # Make data 
    x = random.rand(N)
    y = random.rand(N)
    noise = random.normal(0, sigma, size=N)

    data = franke(x, y) + noise

    names = ["franke", "data", "N", str(N), "sigma", str(sigma)]
    outfilename = "_".join(names) + ".csv"

    path = "data"
    if not os.path.exists(path):
        os.makedirs(path)

    franke_data = {'x': x,
            'y': y,
            'data': data
            }

    df = pd.DataFrame(franke_data, columns= ['x', 'y', 'data'])

    df.to_csv ('./' + path + '/' + outfilename, index = False, header=True)

    df.to_csv (outfilename, index = False, header=True)

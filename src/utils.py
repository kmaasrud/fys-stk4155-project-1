from inspect import getargspec
import numpy as np
from itertools import product


def MSE(x, y):
    """Evaluates the mean squared error between two lists/arrays."""
    s = 0
    for xval, yval in zip(x, y):
        s += (xval - yval)**2

    s /= len(x)
    return s


def R2(x, y):
    """Evaluates the R2 score of two lists/arrays"""
    deno = MSE(x, np.full(len(x), mean_value(y)))
    R2 = 1 - MSE(x, y) / deno
    return R2


def mean_value(y):
    """Evaluates the mean value of a list/array"""
    return sum(y) / len(y)


def make_design_matrix(*param_arrays, poly_deg=1):
    """Takes a collection of input arrays and returns the corresponding design matrix.
    The keyword argument poly_deg specifies which degree polynomial you want the design matrix to depict.

    Arguments:
        *param_arrays -- A number of input arrays.

    Keyword arguments:
        poly_deg -- The desired polynomial degree (default = 1)."""

    # Checks if the parameter arrays are all of equal length.
    # If not, raises assertion error.
    is_arrays_equal_len = len({len(param_array)
                               for param_array in param_arrays}) == 1
    assert is_arrays_equal_len, "Parameter arrays are not of equal dimension."

    # Checks that all the input arrays are of type numpy.ndarray.
    # If not, raises assertion error.
    is_params_ndarray = not False in set(type(x) == np.ndarray for x in param_arrays)
    assert is_params_ndarray, "The input arrays must be of type numpy.ndarray"

    n_inputs = len(param_arrays)
    polynomial_permutations = [perm for perm in product(range(poly_deg + 1), repeat=n_inputs) if sum(perm) == poly_deg]
    p = len(polynomial_permutations)
    n = len(param_arrays[0])

    X = np.ones((p + 1, n))

    for i, perm in enumerate(polynomial_permutations):
        for j, power in enumerate(perm):
            X[i+1, :] *= param_arrays[j] ** power

    return X


# SVD inversion
def SVDinv(A):
    ''' Morten recommended us to use this code from the lecture slides for inverting
    the matrices while working on the terrain data.

    Takes as input a numpy matrix A and returns inv(A) based on singular value decomposition (SVD).
    SVD is numerically more stable than the inversion algorithms provided by
    numpy and scipy.linalg at the cost of being slower.
    '''
    import numpy as np

    U, s, VT = np.linalg.svd(A)

    #print(U)
    #print(s)
    #print(VT)

    D = np.zeros((len(U),len(VT)))
    for i in range(len(VT)):
        D[i,i] = s[i]
    UT = np.transpose(U); V = np.transpose(VT); invD = np.linalg.inv(D)
    return np.matmul(V,np.matmul(invD,UT))

"""
Confidence intervals. A lot of arguments, so might be better to move it
outside a function. Note to self: Remember to test the function, and doublecheck the formulas found at the following site
https://www.investopedia.com/ask/answers/042415/what-difference-between-standard-error-means-and-standard-deviation.asp

X=Design matrix, beta=beta_array, CIpercent=How many percent of data that
contains the mean value(Seems like 95% is quiet common), y=array with
data from franke's function. y_pred=the predicted values, n=observations


# Function is malfunctioning, so I'm just commenting it out now for testing
def CI (X_matrix,beta,CIpercent,y,y_pred,n):
    #The different Zscores representing the CI percentages can be found online
    if CIpercent == 90:
        Zscore = 1.645
    elif CIpercent == 95:
        Zscore = 1.96
    elif CIpercent == 99:
        Zscore = 2.576

    p = len(beta)

    sd = np.sqrt((1/(n−p−1))*np.sum((y-y_pred)∗∗2))  #Standard deviation
    cov_matrix = sd**2*np.linalg.inv(X_matrix.T.dot(X_matrix))
    variance = np.diag(cov_matrix)                 #Variance of betas along diagonal

    CI_min = []
    CI_max = []

    for i in range(p):
        variety=np.sqrt(variance[i]/n)*Zscore
        CI_min_value=beta[i]-variety
        CI_max_value=beta[i]+variety
        CI_min.append(CI_min_value)
        CI_max.append(CI_max_value)

    return CI_min, CI_max    #Returns two lists
"""

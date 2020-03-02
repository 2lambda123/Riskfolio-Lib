import numpy as np
import pandas as pd
from scipy import linalg as LA
from statsmodels.stats.correlation_tools import cov_nearest

###############################################################################
# Some Aditional Functions
###############################################################################


def is_pos_def(cov, threshold=1e-8):
    r"""
    Indicate if a matrix is positive (semi)definite.        

    Parameters
    ----------
    cov : nd-array of shape (n_features, n_features)
        Features covariance matrix, where n_features is the number of features.

    Returns
    -------
    value : bool    
        True if matrix is positive (semi)definite.
        
    Raises
    ------
        ValueError when the value cannot be calculated.

    """
    cov_ = np.matrix(cov)
    w, V = LA.eigh(cov_, lower=True, check_finite=True)
    value = np.all(w >= threshold)

    return value


def correl_matrix(cov):
    r"""
    Generate a correlation matrix from a covariance matrix cov.

    Parameters
    ----------
    cov : nd-array of shape (n_features, n_features)
        Assets covariance matrix, where n_features is the number of features.

    Returns
    -------
    corr : nd-array
        A correlation matrix.
        
    Raises
    ------
        ValueError when the value cannot be calculated.

    """
    flag = False
    if isinstance(cov, pd.DataFrame):
        cols = cov.columns.tolist()
        flag = True

    cov1 = np.matrix(cov)
    corr = np.matrix(cov)
    m, n = cov.shape
    for i in range(0, m):
        for j in range(0, n):
            corr[i, j] = cov1[i, j] / np.sqrt(cov1[i, i] * cov1[j, j])

    if flag:
        corr = pd.DataFrame(corr, index=cols, columns=cols)

    return corr


def cov_fix(cov, method="clipped", **kwargs):
    r"""
    Fix a covariance matrix to a positive definite matrix.

    Parameters
    ----------
    cov : nd-array of shape (n_features, n_features)
        Features covariance matrix, where n_features is the number of features.
    method : str
        The default value is 'clipped', see more in `cov_nearest <https://www.statsmodels.org/stable/generated/statsmodels.stats.correlation_tools.cov_nearest.html>`_.
    **kwargs
        Other parameters from `cov_nearest <https://www.statsmodels.org/stable/generated/statsmodels.stats.correlation_tools.cov_nearest.html>`_.

    Returns
    -------
    cov_ : bool    
        A positive definite covariance matrix.
        
    Raises
    ------
        ValueError when the value cannot be calculated.

    """
    flag = False
    if isinstance(cov, pd.DataFrame):
        cols = cov.columns.tolist()
        flag = True

    cov_ = np.matrix(cov)
    cov_ = cov_nearest(cov_, method=method, **kwargs)
    cov_ = np.matrix(cov_)

    if flag:
        cov_ = pd.DataFrame(cov_, index=cols, columns=cols)

    return cov_


def cov_returns(cov, seed=0):
    r"""
    Generate a matrix of returns that have a covariance matrix cov.

    Parameters
    ----------
    cov : nd-array of shape (n_features, n_features)
        Assets covariance matrix, where n_features is the number of features.

    Returns
    -------
    a : nd-array
        A matrix of returns that have a covariance matrix cov.
        
    Raises
    ------
        ValueError when the value cannot be calculated.

    """

    rs = np.random.RandomState(seed)
    n = len(cov)
    a = np.matrix(rs.randn(n + 10, n))

    for i in range(0, 5):
        cov_ = np.cov(a.T)
        L = np.matrix(np.linalg.cholesky(cov_))
        a = a * (L.I).T
        cov_ = np.cov(a.T)
        desv_ = np.sqrt(np.matrix(np.diag(cov_)))
        a = (np.array(a) - np.mean(a, axis=0)) / np.array(desv_)

    L1 = np.matrix(np.linalg.cholesky(cov))
    a = a * L1.T

    return a

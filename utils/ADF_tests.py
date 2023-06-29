import numpy as np
from statsmodels.tsa.stattools import adfuller

def dshift(x, lags=1):
    if lags == 0:
        return x
    out = np.append(np.nan, np.diff(x))
    for i in range(lags-1):
        out = np.append(np.nan, np.diff(out))
    return out

def adf_enders(x, maxlags=6, pval=0.1):
    x = x[~np.isnan(x)]
    res = {'trend': 0, 'ur': 0, 'n': len(x), 'p': pval}

    if pval == 0.1:
        signcol = 3
    elif pval == 0.05:
        signcol = 2
    elif pval == 0.01:
        signcol = 1
    else:
        raise ValueError("Invalid p value specified; choose 0.1, 0.05, or 0.01")

    critical_z = norm.ppf((1 - pval / 2))

    _, _, _, _, teststat, _, _ = adfuller(x, maxlag=maxlags, regression='ct', autolag='bic')

    # is gamma = 0?
    gamma_is_zero = teststat[0] > teststat[2][f'{signcol}%', 'ct']

    if not gamma_is_zero:
        res['ur'] = 0
        res['trend'] = int(abs(teststat[1][3]) > critical_z)
        return res

    phi3_is_zero = teststat[2][f'{signcol}%', 'ctt'] > teststat[0]

    if not phi3_is_zero:
        gamma_is_zero_normdist = teststat[0] < -critical_z

        if not gamma_is_zero_normdist:
            res['ur'] = 0
            res['trend'] = int(abs(teststat[1][3]) > critical_z)
            return res

        if gamma_is_zero_normdist:
            res['ur'] = 1
            res['trend'] = int(abs(teststat[1][3]) > critical_z)
            return res

    _, _, _, _, teststat, _, _ = adfuller(x, maxlag=maxlags, regression='c', autolag='bic')

    # is gamma = 0?
    gamma_is_zero = teststat[0] > teststat[2][f'{signcol}%', 'c']

    if not gamma_is_zero:
        res['ur'] = 0
        res['trend'] = 0
        return res

    phi1_is_zero = teststat[2][f'{signcol}%', 'ct'] > teststat[1]

    if not phi1_is_zero:
        gamma_is_zero_normdist = teststat[0] < -critical_z

        if not gamma_is_zero_normdist:
            res['ur'] = 0
            res['trend'] = 0
            return res

        if gamma_is_zero_normdist:
            res['ur'] = 1
            res['trend'] = 0
            return res

    _, _, _, _, teststat, _, _ = adfuller(x, maxlag=maxlags, regression='nc', autolag='bic')

    gamma_is_zero = teststat[0] > teststat[2][f'{signcol}%', 'nc']

    if not gamma_is_zero:
        res['ur'] = 0
        res['trend'] = 0
        return res
    else:
        res['ur'] = 1
        res['trend'] = 0
        return res

def adf_enders_wrapper(x):
    if len(np.unique(x)) < 2 or np.all(np.isnan(x)):
        return None

    difforder = range(3)
    res = []
    for lag in difforder:
        res.append(adf_enders(dshift(x, lag)))

    out = res[0]
    out['order'] = 0 + out['ur']
    if res[0]['ur'] == 1 and res[1]['ur'] == 1:
        out = res[1]
        out['order'] = 2
    if res[0]['ur'] == 1 and res[1]['ur'] == 1 and res[2]['ur'] == 1:
        out = res[2]
        out['order'] = 3

    return out

# Running instructions
np.random.seed(1234)
x = np.random.rand(100)
print(adf_enders_wrapper(x))  # No unit root

y = np.arange(1, 101) + np.random.randn(100)
print(adf_enders_wrapper(y))  # Trend-stationary





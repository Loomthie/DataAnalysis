from DataAnalysis.Data import *
import scipy.stats as stats


class __Results:
    alpha = 0
    p_value = 0
    stat_value = 0
    stat_type = 't'
    fails_to_reject = False

    def __init__(self):
        self.conditions = []

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        cond = "\n".join(self.conditions)
        if self.fails_to_reject:
            res = 'Failed to Reject Null Hypothesis'
        else:
            res = 'Rejected Null Hypothesis'
        return f'alpha = {self.alpha}\n' \
               f'Test Statistic = {self.stat_type}\n' \
               f'Stat value =  {self.stat_value}\n' \
               f'P Value = {self.p_value}\n' \
               f'{cond}\n' \
               f'\n{res}'


def TwoSampleT(sample_1,sample_2,same_sigma=True,alpha=0.05,delta=0,two_tail=True):
    res = __Results()
    res.alpha = alpha
    x1 = 0
    n1 = 0
    x2 = 0
    n2 = 0

    for i in sample_1:
        if np.isnan(i):
            continue
        x1+=i
        n1+=1
    x1/=n1

    for j in sample_2:
        if np.isnan(j):
            continue
        x2+=j
        n2+=1
    x2/=n2

    s1 = 0
    s2 = 0
    for i in sample_1:
        if np.isnan(i):
            continue
        s1 += (i-x1)**2
    s1/=n1-1
    s1**=0.5

    for j in sample_2:
        if np.isnan(j):
            continue
        s2 += (j-x2)**2
    s2/=n2-1
    s2**=0.5

    if same_sigma:
        res.conditions.append('Sigma_1 == Sigma_2')
        df = n1 + n2 - 2
        sp = ((n1-1)*s1**2+(n2-1)*s2**2)/df
        sp**=0.5
        t = (x1-x2-delta)/(sp*(1/n1+1/n2)**0.5)
    else:
        res.conditions.append('Sigma_1 != Sigma_2')
        t = (x1-x2-delta)/(s1**2/n1-s2**2/n2)**0.5
        df = (s1**2/n1+s2**2/n2)**2/((s1**2/n1)/(n1-1) + (s2**2/n2)/(n2-1))
        df = int(df)
    #print(t)
    res.conditions.append(f'df = {df}')
    res.conditions.append(f'x1 = {x1}')
    res.conditions.append(f's1 = {s1}')
    res.conditions.append(f'x2 = {x2}')
    res.conditions.append(f's2 = {s2}')
    if two_tail:
        p_value = stats.t.sf(abs(t),df=df)*2
    else:
        p_value = stats.t.sf(abs(t),df=df)
    res.stat_value = t
    res.p_value=p_value
    if p_value < alpha:
        res.fails_to_reject=False
    else:
        res.fails_to_reject=True
    return res

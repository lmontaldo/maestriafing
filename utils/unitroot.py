import pandas as pd
from arch.unitroot import ADF

class UnitRootTests:
    def __init__(self, df):
        """
        Initialize the UnitRootTests class.

        Parameters:
        - df: Pandas DataFrame
            The input DataFrame containing the time series data.
        """
        self.df = df
        self.T = len(df)

    def phi_2_adf(self, critical_value=5.59, r=3, alpha=0.05):
        """
        H0) a_0 = \gamma = a_2 = 0
        
        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: 5.59).
        - r: int, optional
            The number of restrictions in the null hypothesis (default: 3).
        - alpha: float, optional
            The significance level (default: 0.05).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()

        for col in self.df.columns:
            # model c: unrestricted
            adf_c = ADF(self.df[col], trend='ct')
            reg_res_c = adf_c.regression
            SSR_u = reg_res_c.resid.dot(reg_res_c.resid)
            k = len(reg_res_c.params)

            # model a: restricted
            adf_a = ADF(self.df[col], trend='n')
            reg_res_a = adf_a.regression
            SSR_r = reg_res_a.resid.dot(reg_res_a.resid)
            phi_2 = ((SSR_r - SSR_u) / r) / (SSR_u / (self.T - k))

            reject_H0 = phi_2 < critical_value
            if reject_H0:
                rh0[col] = self.df[col]
            else:
                no_rh0[col] = self.df[col]

        return rh0, no_rh0

    def phi_3_adf(self, critical_value=7.44, r=2, alpha=0.05):
        """
        H0) \gamma = a_2 = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: 7.44).
        - r: int, optional
            The number of restrictions in the null hypothesis (default: 2).
        - alpha: float, optional
            The significance level (default: 0.05).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()

        for col in self.df.columns:
            # model c: unrestricted
            adf_c = ADF(self.df[col], trend='ct')
            reg_res_c = adf_c.regression
            SSR_u = reg_res_c.resid.dot(reg_res_c.resid)
            k = len(reg_res_c.params)

            # model b: restricted
            adf_b = ADF(self.df[col], trend='c')
            reg_res_b = adf_b.regression
            SSR_r = reg_res_b.resid.dot(reg_res_b.resid)
            phi_3 = ((SSR_r - SSR_u) / r) / (SSR_u / (self.T - k))

            reject_H0 = phi_3 < critical_value
            if reject_H0:
                rh0[col] = self.df[col]
            else:
                no_rh0[col] = self.df[col]

        return rh0, no_rh0

    def tau_tau(self, critical_value=-3.45):
        """
        H0) \gamma = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: -3.45).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()

        for col in self.df.columns:
            adf_c = ADF(self.df[col], trend='ct')
            reg_res_c = adf_c.regression
            tau_tau = reg_res_c.tvalues[0]
            reject_c = tau_tau < critical_value
            if reject_c:
                rh0[col] = self.df[col]
            else:
                no_rh0[col] = self.df[col]

        return rh0, no_rh0

    def tau_mu(self, critical_value=-2.90):
        """
        H0) \gamma = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: -2.90).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()

        for col in self.df.columns:
            adf_b = ADF(self.df[col], trend='c')
            reg_res_b = adf_b.regression
            tau_mu = reg_res_b.tvalues[0]
            reject_c = tau_mu < critical_value
            if reject_c:
                rh0[col] = self.df[col]
            else:
                no_rh0[col] = self.df[col]

        return rh0, no_rh0

    def phi_1_adf(self, critical_value=5.57, r=2, alpha=0.05):
        """
        H0) \gamma = a_0 = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: 5.57).
        - r: int, optional
            The number of restrictions in the null hypothesis (default: 2).
        - alpha: float, optional
            The significance level (default: 0.05).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()

        for col in self.df.columns:
            # model b: unrestricted
            adf_b = ADF(self.df[col], trend='c')
            reg_res_b = adf_b.regression
            SSR_u = reg_res_b.resid.dot(reg_res_b.resid)
            k = len(reg_res_b.params)

            # model a: restricted
            adf_a = ADF(self.df[col], trend='n')
            reg_res_a = adf_a.regression
            SSR_r = reg_res_a.resid.dot(reg_res_a.resid)
            phi_1 = ((SSR_r - SSR_u) / r) / (SSR_u / (self.T - k))

            reject_H0 = phi_1 < critical_value
            if reject_H0:
                rh0[col] = self.df[col]
            else:
                no_rh0[col] = self.df[col]

        return rh0, no_rh0

    def tau(self, critical_value=-1.95):
        """
        H0) \gamma = 0

        Parameters:
        - critical_value: float, optional
            The critical value for hypothesis testing (default: -1.95).

        Returns:
        - rh0: Pandas DataFrame
            The columns that reject the null hypothesis.
        - no_rh0: Pandas DataFrame
            The columns that do not reject the null hypothesis.
        """
        results = {}
        rh0 = pd.DataFrame()
        no_rh0 = pd.DataFrame()

        for col in self.df.columns:
            adf = ADF(self.df[col], trend='n')
            reg_res = adf.regression
            tau = reg_res.tvalues[0]
            reject_c = tau < critical_value
            if reject_c:
                rh0[col] = self.df[col]
            else:
                no_rh0[col] = self.df[col]

        return rh0, no_rh0

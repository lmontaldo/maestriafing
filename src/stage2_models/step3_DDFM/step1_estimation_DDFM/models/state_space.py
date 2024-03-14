from typing import Tuple
import numpy as np
from pykalman import KalmanFilter
from models.base_model import BaseModel

class StateSpace(BaseModel):
    """
    Base class for state-space models.
    """

    def __init__(self, mean_z: np.ndarray, sigma_z: np.ndarray, transition_params: dict, measurement_params: dict,
                 filter_type: str = "KalmanFilter"):
        """
        The init method will build the state space model according to the selected filter.
        Args:
            mean_z: mean of the measurement variable
            sigma_z: standard deviation of the measurement variable
            transition_params: parameters of the transition equation
            measurement_params: parameters of the measurement equation
            filter_type: the type of filter selected

        """
        super().__init__()
        self.mean_z = mean_z
        self.sigma_z = sigma_z
        # init parameters of the state space to None
        self.H = None
        self.R = None
        self.F = None
        self.Q = None
        self.predict = None
        self.filter = None
        if filter_type == "KalmanFilter":
            # build a linear gaussian state-space model
            self.build_lgss(transition_params, measurement_params)
        else:
            raise NotImplementedError("Only KalmanFilter is implemented at the moment.")

    def build_lgss(self, transition_params: dict, measurement_params: dict) -> None:
        """
        This method builds a linear gaussian state space model of the following form:
            measurement: z_t = H x_t + v_t; v_t ∼ N(0, R)
            transition: x_t = F x_t-1 + w_t; w_t ∼ N(0, Q)
        Args:
            transition_params: parameters of the transition equation
            measurement_params: parameters of the measurement equation

        Returns:
            None, it updates the class attributes.
        """

        self.H, self.R = measurement_params["H"], measurement_params["R"]
        self.F, self.Q = transition_params["F"], transition_params["Q"]
        self.filter_predict = KalmanFilter(transition_matrices=self.F, observation_matrices=self.H,
                                           transition_covariance=self.Q, observation_covariance=self.R)
        self.predict = self.predict_lgss
        self.filter = self.kalman_filter


    def kalman_filter(self, z: np.ndarray, standardize=False, do_em: bool = False) -> Tuple[
        np.ndarray, np.ndarray]:
        """
        This method implements the Kalman Filter.
            measurement: z_t = H x_t + v_t; v_t ∼ N(0, R)
            transition: x_t = F x_t-1 + w_t; w_t ∼ N(0, Q)
        Args:
            z: observable realised values
            standardize: whether to standardize the inputs or not

        Returns:
            filtered states and variance-covariance matrix
        """
        z_cpy = z.copy()
        if standardize:
            z_cpy = (z_cpy - self.mean_z) / self.sigma_z
        # make dimensions consistent
        if z_cpy.ndim == 1:
            z_cpy = np.reshape(z_cpy, (1, z_cpy.shape[0]))
        z_cpy = np.ma.array(z_cpy)
        z_cpy[np.isnan(z_cpy)] = np.ma.masked
        if do_em:
            (filtered_state_means, filtered_state_covariances) = self.filter_predict.em(z_cpy).filter(z_cpy)
        else:
            (filtered_state_means, filtered_state_covariances) = self.filter_predict.filter(z_cpy)
        return filtered_state_means, filtered_state_covariances


    def predict_lgss(self, x_hat_start: np.ndarray, sigma_x_hat_start: np.ndarray, steps_ahead: int = 1) -> dict:
        x_hat = x_hat_start
        sigma_x_hat = sigma_x_hat_start
        predicted_states = []
        #predicted_covariances = []
        for _ in range(steps_ahead):
          # Predict the next state
          x_hat_next = self.F @x_hat
          #sigma_x_hat_next = self.state_space_dict["transition"]["F"] @ sigma_x_hat @ self.state_space_dict["transition"]["F"].T + self.Q
          # Store the predictions
          predicted_states.append(x_hat_next)
          #predicted_covariances.append(sigma_x_hat_next)
          # Update current state and covariance for next iteration
          x_hat = x_hat_next
          #sigma_x_hat = sigma_x_hat_next
        #return {"states": np.array(predicted_states), "covariances": np.array(predicted_covariances)}
        return {"states": np.array(predicted_states)}

    def predict_measurement(self, future_states: np.ndarray) -> np.ndarray:
      """
      Predicts future observations given future states.
      Args:
        future_states: Future states (f_{t+k}) estimated by the state-space model.
      Returns:
        Predicted future observations (y_{t+k}).
      """
      predicted_observations = self.H @ future_states.T
      return predicted_observations.T
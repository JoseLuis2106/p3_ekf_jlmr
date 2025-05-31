
import rclpy

import numpy as np

from .motion_models.acceleration_motion_models import acceleration_motion_model_linearized_1
from .observation_models.odometry_imu_observation_models import odometry_imu_observation_model_with_acceleration_motion_model_linearized_1

from .filters.ekf import ExtendedKalmanFilter
from .kf_node import KalmanFilterFusionNode as ExtendedKalmanFilterFusionNode


def main(args=None):
    # Initialize the Kalman Filter

    mu0 = np.zeros(7)
    Sigma0 = np.eye(7)
    # TO ADJUST
    proc_noise_std = [0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1] # [x, y, theta, v, w, a_x, a_y]
    # proc_noise_std = [5, 5, 5, 5, 5, 5, 5]
    obs_noise_std = [100.0, 100.0, 1000.0, 6.853891945200942e-06, 1.0966227112321507e-06, 0.0015387262937311438, 0.0015387262937311438] #[x, y, theta, theta_imu, w, a_x, a_y]
    # obs_noise_std = [200.0, 200.0, 2000.0, 1.0, 1.0, 1.0, 1.0]  # [x, y, theta, v, w, a_x, a_y]

    # === TODO: Replace the None below with proper motion and observation model functions ===
    ekf = ExtendedKalmanFilter(mu0, Sigma0,
                               acceleration_motion_model_linearized_1,  # TODO: motion_model_7d
                               odometry_imu_observation_model_with_acceleration_motion_model_linearized_1,  # TODO: observation_model_7d
                               proc_noise_std=proc_noise_std,
                               obs_noise_std=obs_noise_std)
    # ===================================================================

    rclpy.init(args=args)
    kalman_filter_node = ExtendedKalmanFilterFusionNode(ekf)
    rclpy.spin(kalman_filter_node)
    kalman_filter_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

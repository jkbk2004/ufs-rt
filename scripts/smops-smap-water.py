import numpy as np

class WaterBalanceOperator:
    def __init__(self, soil_layers, dt_hours=1.0):
        self.soil_layers = soil_layers  # e.g., [0-10cm, 10-40cm, 40-100cm]
        self.dt = dt_hours * 3600  # time step in seconds

    def compute_balance(self, precip, et, runoff, drainage, theta_prev):
        """
        Compute updated soil moisture for each layer.
        
        Parameters:
        - precip: total precipitation (mm)
        - et: evapotranspiration (mm)
        - runoff: surface runoff (mm)
        - drainage: deep drainage (mm)
        - theta_prev: previous soil moisture (mm or volumetric)

        Returns:
        - theta_new: updated soil moisture
        """
        net_input = precip - et - runoff - drainage
        theta_new = theta_prev + net_input / len(self.soil_layers)
        theta_new = np.clip(theta_new, 0, 1)  # constrain between 0–1 for volumetric SM
        return theta_new

# Example usage
soil_layers = ['0-10cm', '10-40cm', '40-100cm']
operator = WaterBalanceOperator(soil_layers)

# Inputs (in mm)
precip = 10.0
et = 2.5
runoff = 1.0
drainage = 0.5
theta_prev = np.array([0.25, 0.30, 0.35])  # volumetric soil moisture

theta_new = operator.compute_balance(precip, et, runoff, drainage, theta_prev)
print("Updated Soil Moisture:", theta_new)

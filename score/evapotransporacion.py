import numpy as np

def penman_monteith(t_min,t_max,rh_min,rh_max,solar_rad,wind_speed,doy,latitude,altitude, *args, **kwargs):
    
    T_avg = (t_min + t_max)/2
    atm_pressure = 101.3 * ((293 - 0.0065 * altitude) / 293)**5.26 
    Cp = 0.001013; 
    epsilon =  0.622
    Lambda = 2.45
    gamma = (Cp * atm_pressure) / (epsilon * Lambda) 

    ##### Wind speed
    wind_speed_2m = wind_speed 

    ##### Air humidity and vapor pressure
    delta = 4098 * (0.6108 * np.exp(17.27 * T_avg / (T_avg  + 237.3))) / (T_avg  + 237.3)**2
    e_temp_max = 0.6108 * np.exp(17.27 * t_max / (t_max + 237.3)) 
    e_temp_min = 0.6108 * np.exp(17.27 * t_min / (t_min + 237.3))
    e_saturation = (e_temp_max + e_temp_min) / 2
    e_actual = (e_temp_min * (rh_max / 100) + e_temp_max * (rh_min / 100)) / 2

    ##### Solar radiation
    dr = 1 + 0.033 * np.cos(2 * np.pi * doy/365)  
    phi = np.pi / 180 * latitude 
    d = 0.409 * np.sin((2 * np.pi * doy/365) - 1.39)
    omega = np.arccos(-np.tan(phi) * np.tan(d))
    Gsc = 0.0820 # Approx. 0.0820
    Ra = 24 * 60 / np.pi * Gsc * dr * (omega * np.sin(phi) * np.sin(d) + np.cos(phi) * np.cos(d) * np.sin(omega))

    # Clear Sky Radiation: Rso (MJ/m2/day)
    Rso =  (0.75 + (2 * 10**-5) * altitude) * Ra  

    # Rs/Rso = relative shortwave radiation (limited to <= 1.0)
    alpha = 0.23 
    Rns = (1 - alpha) * solar_rad 
    sigma  = 4.903 * 10**-9
    maxTempK = t_max + 273.16
    minTempK = t_min + 273.16
    Rnl =  sigma * (maxTempK**4 + minTempK**4) / 2 * (0.34 - 0.14 * np.sqrt(e_actual)) * (1.35 * (solar_rad / Rso) - 0.35)
    Rn = Rns - Rnl # Eq. 40, FAO-56

    # Soil heat flux density
    soil_heat_flux = 0 

    # ETo calculation
    PET = (0.408 * delta * (Rn - soil_heat_flux) + gamma * (900 / (T_avg  + 273)) * wind_speed_2m * (e_saturation - e_actual)) / (delta + gamma * (1 + 0.34 * wind_speed_2m))
    return np.round(PET,2)
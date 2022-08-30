import sys
from score.evapotransporacion import penman_monteith as calculate_evapotranspiration




if __name__ == '__main__':
    args = sys.argv[1:]
    
    if len(args) > 1: # va por consola    
    #penman_monteith(T_min,T_max,RH_min,RH_max,solar_rad,wind_speed,doy,latitude,altitude):
        t_min = args[0]
        t_max = args[1]
        rh_min = args[2]
        rh_max = args[3]
        solar_rad = args[4]
        wind_speed = args[5] 
        doy = args[6]
        latitude = args[7]
        altitude = args[8]
        
        payload = dict(
            t_min=t_min,
            t_max=t_max,
            rh_min=rh_min,
            rh_max=rh_max,
            solar_rad= solar_rad,
            wind_speed=wind_speed,
            doy=doy,
            latitude=latitude,
            altitude=altitude
        )
        
        print(calculate_evapotranspiration(**payload))
        
    else: # es un csv
        #TODO
        print('Pending Feature')
         
    
    
    
    
    



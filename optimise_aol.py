from aol_full import AolFull
from aod import Aod
from ray import Ray
from numpy import array, arange, append, sqrt, dtype, zeros, isnan
from numpy.linalg import norm
import copy
from scipy import optimize

op_wavelength = 800e-9

def optimise_aol():
        
    aol = set_up_aol()
     
    def optimise_nth_aod(aod_num):
        
        def min_fun(xy_normal):
            xy_normal[0] = xy_normal[0] if (xy_normal[0] < 0.5) else 0.5
            xy_normal[0] = xy_normal[0] if (xy_normal[0] > -0.5) else -0.5  
            xy_normal[1] = xy_normal[1] if (xy_normal[1] < 0.5) else 0.5
            xy_normal[1] = xy_normal[1] if (xy_normal[1] > -0.5) else -0.5  
            z_comp_sqr = 1 - norm(xy_normal)**2
            if z_comp_sqr < 0:
                x = 2
            new_normal = append(xy_normal, sqrt(z_comp_sqr))
            change_orientation(aol, aod_num, new_normal)
            print 'y'
            return -calculate_efficiency(aol)
    
        acoustics = aol.acoustic_drives[aod_num-1]
        this_aod = aol.aods[aod_num-1]
        
        bragg_angle = op_wavelength * acoustics.const / acoustics.velocity
        guess = this_aod.normal + this_aod.acoustic_direction * bragg_angle * aol.order  
        
        new_optimal_normal = optimize.basinhopping(min_fun, guess[0:2])
        
        change_orientation(aol, aod_num, new_optimal_normal)
        
    for aod_num in arange(1, 5):
        optimise_nth_aod(aod_num)
        
    return array([a.normal for a in aol.aods], dtype=dtype(float))

    #first opt = array([ 0.46172377, -0.40717573])

def set_up_aol():
    order = 1
    base_freq = 40e6
    pair_deflection_ratio = 0.8
    
    focal_length = 100
    focus_position = array([.1,.2,focal_length])
    focus_velocity = [0,1,0]
    
    aod_spacing = array([5e-2] * 3)
    
    aods = [0]*4
    aods[0] = Aod([0,0,1], [ 1, 0,0], 25e-3, 3.2e-3, 8e-3)
    aods[1] = Aod([0,0,1], [ 0, 1,0], 25e-3, 3.2e-3, 8e-3)
    aods[2] = Aod([0,0,1], [-1, 0,0], 25e-3, 1.6e-3, 8e-3)
    aods[3] = Aod([0,0,1], [ 0,-1,0], 25e-3, 1.6e-3, 8e-3)
    
    return AolFull.create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio, focus_position, focus_velocity)

def change_orientation(aol, aod_num, new_normal):
    assert not any(isnan(new_normal))
    aol.aods[aod_num-1].normal = new_normal

def calculate_efficiency(aol):
    time_array = (arange(3)-1)*5e-5
    x_array = (arange(3)-1)*2e-3
    y_array = x_array
    
    energy = 0
    ray_count = 0
    
    rays = [0] * len(x_array) * len(y_array)
    
    for t in time_array:
        for xn in range(len(x_array)):
            for yn in range(len(y_array)):    
                rays[xn + yn*len(x_array)] = Ray([x_array[xn],y_array[yn],0], [0,0,1], op_wavelength)
        
        aol.propagate_to_distance_past_aol(rays, t)
        energy += sum([r.energy for r in rays])
        ray_count += len(rays)
                
    return energy / ray_count

if __name__ == '__main__':
    #calculate_efficiency(set_up_aol())
    optimise_aol()
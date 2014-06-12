from aol_simple import AolSimple
from acoustics import AcousticDrive, default_power, teo2_ac_vel
from aol_drive import calculate_drive_freq_4
from numpy import append, array, dtype

class AolFull(object):
       
    @staticmethod
    def create_aol(aods, aod_spacing, order, op_wavelength, base_freq, pair_deflection_ratio,\
                   focus_position, focus_velocity, ac_power=[default_power]*4, ac_velocity=teo2_ac_vel):

        crystal_thickness = array([a.crystal_thickness for a in aods], dtype=dtype(float))
        (const, linear, quad) = calculate_drive_freq_4(order, op_wavelength, ac_velocity, aod_spacing, crystal_thickness, \
                                base_freq, pair_deflection_ratio, focus_position, focus_velocity)
       
        acoustic_drives = AcousticDrive.make_acoustic_drives(const, linear, quad, ac_power, ac_velocity)
        return AolFull(aods, aod_spacing, acoustic_drives, order, op_wavelength)
       
    def __init__(self, aods, aod_spacing, acoustic_drives, order, op_wavelength): 
        self.aods = array(aods)
        self.aod_spacing = array(aod_spacing, dtype=dtype(float))
        self.acoustic_drives = array(acoustic_drives)
        self.order = order
        
        simple = AolSimple(order, self.aod_spacing, self.acoustic_drives)
        self.base_ray_centres = simple.find_base_ray_positions(op_wavelength)
         
    def propagate_to_distance_past_aol(self, ray, time, distance=0):
        crystal_thickness = array([a.crystal_thickness for a in self.aods], dtype=dtype(float))
        reduced_spacings = append(self.aod_spacing, distance) - crystal_thickness 
        
        for k in range(4):
            self.diffract_and_propagate(ray, time, reduced_spacings, k+1)
        
    def diffract_and_propagate(self, ray, time, reduced_spacings, aod_number):
        self.diffract_at_aod(ray, time, aod_number)
        ray.propagate_free_space_z(reduced_spacings[aod_number-1])
        
    def diffract_at_aod(self, ray, time, aod_number):
        idx = aod_number-1
        
        aod = self.aods[idx]
        base_ray_position = self.base_ray_centres[idx]
        drive = self.acoustic_drives[idx]
        local_acoustics = drive.get_local_acoustics(time, ray.position, base_ray_position, aod.acoustic_direction)
        
        aod.propagate_ray(ray, local_acoustics, self.order)
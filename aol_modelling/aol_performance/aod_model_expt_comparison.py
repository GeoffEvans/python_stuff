from aol_model.aod_visualisation import AodVisualisation
from aol_model.vector_utils import normalise
import expt_data as d
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams.update({'font.size': 20})

av_wide = AodVisualisation(785e-9, ac_dir_rel=[1,0,0], is_wide=True, deg_bnds=(-1,4))
av_narrow = AodVisualisation(785e-9, ac_dir_rel=normalise([1,0,0]), is_wide=False, deg_bnds=(-1,6))
av_narrow_800 = AodVisualisation(800e-9, ac_dir_rel=normalise([1,0,0]), is_wide=False, deg_bnds=(-1,6))
av_narrow_920 = AodVisualisation(920e-9, ac_dir_rel=normalise([1,0,0]), is_wide=False, deg_bnds=(-1,6))

def plot_eff_pwr_wide():
    plt.plot(d.power, d.eff_power_wide, 'o')
    av_wide.plot_efficiency_power()

def plot_eff_freq_wide():
    plt.plot(d.freq_wide, d.eff_freq_wide, 'o')
    av_wide.plot_efficiency_freq_max()

def plot_eff_ang_wide():
    plt.plot(d.angle_wide, d.eff_angle_wide, 'o')
    av_wide.plot_efficiency_xangle()

def plot_eff_pwr_narrow():
    plt.plot(d.power, d.eff_power_narrow, 'o')
    av_narrow.plot_efficiency_power()

def plot_eff_freq_narrow():
    plt.plot(d.freq_narrow, d.eff_freq_narrow, 'o')
    av_narrow.plot_efficiency_freq_max()

def plot_eff_ang_narrow():
    plt.plot(d.angle_narrow, d.eff_angle_narrow, 'o')
    av_narrow.plot_efficiency_xangle()

def plot_eff_freq_narrow_expt_model():
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_920_1, 'bo')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_800_1, 'go')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_920_2, 'ro')
    plt.plot(d.freq_narrow_new, d.eff_freq_narrow_800_23, 'co')

    av_narrow_920.plot_efficiency_freq_max()
    av_narrow_800.plot_efficiency_freq_max()
    av_narrow_920.plot_efficiency_freq_max_second_order()
    av_narrow_800.plot_efficiency_freq_max_second_order()

    from aol_model.set_up_utils import transducer_efficiency_narrow
    f = np.linspace(20, 50, 300) * 1e6
    plt.plot(d.freq_narrow_new, transducer_efficiency_narrow(np.array(d.freq_narrow_new)*1e6), 'mo')
    plt.plot(f/1e6, transducer_efficiency_narrow(f))
    label_list = ['920nm -1 mode expt', '800nm -1 mode expt', '920nm -2 mode expt', '800nm -2 mode expt', \
                  '920nm -1 mode model', '800nm -1 mode model', '920nm -2 mode model', '800nm -2 mode model', \
                  'RF to acoustic inferred', 'RF to acoustic spline']
    plt.legend(label_list, loc=0, borderaxespad=1.6, fontsize=16)

if __name__ == '__main__':
    plt.figure()
    plot_eff_freq_narrow_expt_model()

    #plt.figure()
    #plot_eff_freq_narrow()
    #plt.figure()
    #plot_eff_freq_wide()
    #plt.figure()
    #plot_eff_ang_narrow()
    #plt.figure()
    #plot_eff_ang_wide()
    #plt.figure()
    #plot_eff_pwr_narrow()
    #plt.figure()
    #plot_eff_pwr_wide()

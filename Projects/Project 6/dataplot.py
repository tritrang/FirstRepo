"""
Project 6: Data Visualization
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""
import numpy as np
import glob
import matplotlib.pyplot as plt


def smooth(raw_data):
    smooth_data = raw_data.copy()
    for idx, _ in enumerate(smooth_data):
        if 3 <= idx <= (len(smooth_data) - 4):
            smooth_data[idx] = (raw_data[idx-3] + 2*raw_data[idx-2] + 3*raw_data[idx-1] + 3*raw_data[idx] + 3*raw_data[idx+1] + 2*raw_data[idx+2] + raw_data[idx+3])//15
    return smooth_data


def calculate_areas(pulses_idx, raw_data):
    pulse_areas = []
    """First and other pulses"""
    for i, idx in enumerate(pulses_idx[:-1]):
        area = 0
        if pulses_idx[i+1] - idx <= 50:
            for y_value in raw_data[idx:pulses_idx[i+1]]:
                area += int(y_value)
            pulse_areas.append((idx, area))
        else:
            for y_value in raw_data[idx:idx+50]:
                area += int(y_value)
            pulse_areas.append((idx, area))
    """Last pulse"""
    pulse_areas.append((pulses_idx[-1], sum([int(y_value) for y_value in raw_data[pulses_idx[-1]:pulses_idx[-1]+50]])))
    return pulse_areas


def analyze(file_name):
    vt = 100
    pulses_idx = []
    raw_data = np.loadtxt(file_name)
    smooth_data = smooth(raw_data)
    """Find pulse indexes"""
    idx = 0
    while idx < len(smooth_data[:-2]):
        if smooth_data[idx+2] - smooth_data[idx] > vt:
            pulses_idx.append(idx)
            idx += 2
            while smooth_data[idx] < smooth_data[idx+1]:
                idx += 1
        idx += 1
    """Save pdf"""
    _, axis = plt.subplots(nrows=2, figsize=(10, 6))
    axis[0].plot(raw_data, linewidth=0.75)
    axis[0].set(title=file_name)
    axis[0].set_ylabel('raw')
    axis[1].plot(smooth_data, linewidth=0.75)
    axis[1].set_ylabel('smooth')
    plt.savefig(file_name[:-3] + "pdf")
    """Calculate areas"""
    pulse_areas = calculate_areas(pulses_idx, raw_data)
    """Save out"""
    n = 0
    with open(file_name[:-3] + "out", 'w') as f:
        f.write(f"{file_name}:\n")
        for pulse in pulse_areas:
            n += 1
            f.write(f"Pulse {n}: {pulse[0]} ({pulse[1]}) \n")


def main():
    for fname in glob.glob('*.dat'):
        analyze(fname)


if __name__ == '__main__':
    main()





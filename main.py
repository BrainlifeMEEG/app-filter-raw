"""
Filter raw MEG/EEG data using frequency domain filters.

This app loads raw neuroimaging data and applies bandpass and notch filters
based on user-specified parameters. It generates visualizations of the filter
response and produces a report comparing the original and filtered data.

Inputs
------
mne : str
    Path to the input MNE-format MEG/EEG data file (MNE .fif format).

Outputs
-------
meg.fif : str
    Filtered MEG/EEG data file in MNE format.
filter_response.png : str
    PNG image showing the frequency response of the applied filter.
report_filter.html : str
    Interactive HTML report comparing original and filtered data.
"""

# Copyright (c) 2026 brainlife.io
#
# Filter raw MEG/EEG data using frequency domain filters.
#
# Authors:
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
import re
import mne
from mne.viz import plot_filter
import matplotlib
import matplotlib.pyplot as plt

# Add brainlife_utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product
)

# Setup environment
setup_matplotlib_backend()
config = load_config()

# Ensure output directories exist
os.makedirs('out_dir', exist_ok=True)
os.makedirs('out_figs', exist_ok=True)
os.makedirs('out_report', exist_ok=True)

# == LOAD DATA ==
fname = config['mne']
raw = mne.io.read_raw_fif(fname, preload=True)
raw_orig = raw.copy()
sfreq = raw.info['sfreq']

# == CREATE FILTER VISUALIZATION ==
f = mne.filter.create_filter(
    raw_orig.get_data(),
    sfreq,
    l_freq=config['l_freq'],
    h_freq=config['h_freq'],
    filter_length=config['filter_length'],
    l_trans_bandwidth=config['l_trans_bandwidth'],
    h_trans_bandwidth=config['h_trans_bandwidth'],
    method=config['method'],
    iir_params=config['iir_params'],
    phase=config['phase'],
    fir_window=config['fir_window'],
    fir_design=config['fir_design']
)

plt.figure()
fig = plot_filter(f, sfreq)
fig_path = os.path.join('out_figs', 'filter_response.png')
plt.savefig(fig_path)
plt.close(fig)

# == APPLY NOTCH FILTER (if specified) ==
if config['notch']:
    config['notch'] = [int(x) for x in re.split("\\W+", config['notch'])]
    raw.notch_filter(freqs=config['notch'], picks=config['picks'])

# == APPLY BANDPASS FILTER ==
raw.filter(
    picks=config['picks'],
    l_freq=config['l_freq'],
    h_freq=config['h_freq'],
    filter_length=config['filter_length'],
    l_trans_bandwidth=config['l_trans_bandwidth'],
    h_trans_bandwidth=config['h_trans_bandwidth'],
    method=config['method'],
    iir_params=config['iir_params'],
    phase=config['phase'],
    fir_window=config['fir_window'],
    fir_design=config['fir_design'],
    skip_by_annotation=config['skip_by_annotation'],
    pad=config['pad']
)

# == GENERATE REPORT ==
report = mne.Report(title='Filtering Report')
report.add_figure(fig, title='Filter Response')
report.add_raw(raw_orig, 'Original Unfiltered Data', psd=True)
report.add_raw(raw, 'Filtered Data', psd=True)
report.save('out_report/report_filter.html', overwrite=True)

# == SAVE FILTERED DATA ==
raw.save('out_dir/meg.fif', overwrite=True)

# == CREATE PRODUCT.JSON ==
product_items = []

# Add information messages
add_info_to_product(product_items, f"Filter method: {config['method']}")
if config['l_freq'] is not None or config['h_freq'] is not None:
    l_freq_str = str(config['l_freq']) if config['l_freq'] is not None else "None"
    h_freq_str = str(config['h_freq']) if config['h_freq'] is not None else "None"
    add_info_to_product(product_items, f"Bandpass filter: {l_freq_str} - {h_freq_str} Hz")
if config['notch']:
    add_info_to_product(product_items, f"Notch filter frequencies: {config['notch']}")

# Add original data information
add_info_to_product(product_items, "Original Data:")
add_raw_info_to_product(product_items, raw_orig)

# Add filtered data information
add_info_to_product(product_items, "Filtered Data:")
add_raw_info_to_product(product_items, raw)

# Add filter response plot
add_image_to_product(product_items, "Filter Response", filepath=fig_path)

# Create product.json
create_product_json(product_items)

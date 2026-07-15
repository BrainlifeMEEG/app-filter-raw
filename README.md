# Filter Raw MEG/EEG Data

## Description

This Brainlife.io application filters raw MEG/EEG data using frequency domain filtering techniques. It supports both FIR (Finite Impulse Response) and IIR (Infinite Impulse Response) filters for bandpass filtering, along with optional notch filtering to remove specific frequency bands (e.g., power line noise).

The app generates:
- Filtered data in MNE-Python format
- Visualization of the filter frequency response
- Comprehensive HTML report comparing original and filtered data

## Inputs

### Input Files

- **meg.fif**: MNE-format MEG/EEG data file (required)

## Outputs

### Output Files

- **raw.fif**: Filtered MEG/EEG data file in MNE format
- **filter_response.png**: Frequency response plot of the applied filter
- **report.html**: Interactive HTML report showing filter effects with power spectral density comparisons

## Configuration Parameters

- **l_freq** (float | None): Lower pass-band edge in Hz for FIR filters or lower cutoff frequency for IIR filters. Set to None for high-pass only filtering.
- **h_freq** (float | None): Upper pass-band edge in Hz for FIR filters or upper cutoff frequency for IIR filters. Set to None for low-pass only filtering.
- **notch** (string | None): Comma-separated list of frequencies (in Hz) to apply notch filtering. Applied using a separate notch filter. Example: "50, 100, 150, 200" for 50 Hz powerline and harmonics.
- **picks** (string | None): Channels to filter. Can be channel type strings (e.g., "meg", "eeg"), channel names, indices, or empty string for all data channels.
- **filter_length** (string | int): Length of the FIR filter.
  - "auto" (default): Length chosen based on transition region size
  - str: Time duration (e.g., "10s" or "5500ms")
  - int: Length in samples
- **l_trans_bandwidth** (float | string): Transition bandwidth at the low cut-off frequency (Hz). Can be "auto" for automatic selection.
- **h_trans_bandwidth** (float | string): Transition bandwidth at the high cut-off frequency (Hz). Can be "auto" for automatic selection.
- **method** (string): Filter implementation method.
  - "fir": FIR filtering via overlap-add (default)
  - "iir": IIR forward-backward filtering (filtfilt)
- **iir_params** (dict | None): Dictionary of parameters for IIR filtering. Uses 4th order Butterworth filter if None and method="iir".
- **phase** (string): Phase mode for FIR filters (only used when method="fir").
  - "zero" (default): Zero-phase filter (non-causal)
  - "zero-double": Applied twice (forward and backward, non-causal)
  - "minimum": Minimum-phase filter (causal)
- **fir_window** (string): Window function for FIR filter design.
  - "hamming" (default): Hamming window
  - "hann": Hann window
  - "blackman": Blackman window
- **fir_design** (string): FIR design algorithm.
  - "firwin" (default): scipy.signal.firwin()
  - "firwin2": scipy.signal.firwin2()
- **skip_by_annotation** (string | list): Annotation prefixes to skip during filtering. Default: "('edge', 'bad_acq_skip')" to handle concatenated segments. Use empty list to disable.
- **pad** (string): Padding mode for FIR filters (only when method="fir").
  - "reflect_limited" (default): Reflected padding with zeros
  - Other numpy.pad() modes supported

## Usage

### Running on Brainlife.io

1. Upload your MEG/EEG data file in MNE format (.fif)
2. Select the filter-raw app
3. Configure filtering parameters:
   - Set appropriate frequency bounds (l_freq, h_freq)
   - Optionally specify notch frequencies for powerline noise
   - Choose FIR or IIR method and adjust other parameters as needed
4. Submit the task
5. Monitor task completion and review outputs in the report viewer

### Local Testing

```bash
# Update config.json with your data path
# Then run:
python main.py
```

## Technical Details

### Filter Implementation

- **FIR Filters**: Use overlap-add FFT-based filtering for efficiency. Zero-phase filtering is applied by default, which requires extra memory and computation but provides symmetric spectral characteristics.
- **IIR Filters**: Use forward-backward filtering (filtfilt) to achieve zero-phase response. Risk of filter instability with extreme parameters.

### Notch Filtering

When specified, notch filtering is applied as a separate step before bandpass filtering. Frequencies are parsed from comma-separated values and converted to integers.

### Power Spectral Density (PSD)

The report includes PSD calculations for both original and filtered data to visualize the effect of filtering in the frequency domain.

### Report Generation

Uses MNE-Python's Report class to create an interactive HTML report with:
- Filter frequency response visualization
- Original data summary and PSD
- Filtered data summary and PSD

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

## Funding Acknowledgement

brainlife.io is publicly funded. We kindly ask that you acknowledge the funding below in your code and publications.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)

import numpy as np
import matplotlib.pyplot as plt

def bpsk_modulation(bit_string, bit_duration, carrier_frequency, n):
    symbols = 2 * np.array(list(map(int, bit_string))) - 1
    modulated_signal = np.zeros(len(symbols) * n)
    t_step = bit_duration / n
    t = np.arange(0, len(symbols) * bit_duration, t_step)

    # Assuming that Eb = 0.5 to get Amp = 1
    for i in range(len(symbols)):
        current_signal = symbols[i] * np.sqrt(2*(0.5)/bit_duration)*np.cos(2 * np.pi * carrier_frequency *t[i*n : (i+1)*n])
        modulated_signal[i*n : (i+1)*n] = current_signal
    
    return modulated_signal

def add_awgn(signal, snr_dB):
    snr = 10 ** (snr_dB / 10.0)
    noise_power = 1 / snr
    # Ensure that noise has the same shape as signal
    noise = np.sqrt(noise_power) * np.random.randn(*signal.shape)
    return signal + noise



def bpsk_demodulation(received_signal, bit_duration, carrier_frequency, n):
    demodulated_bits = np.zeros(len(received_signal) // n)
    t_step = bit_duration / n

    for i in range(0, len(received_signal), n):
        current_signal = received_signal[i:i+n] * np.sqrt(2*(0.5)/bit_duration)*np.cos(2 * np.pi * carrier_frequency * np.arange(0, n) * t_step)
        decision = np.trapz(current_signal, dx=t_step)
        if decision > 0:
            demodulated_bits[i//n] = 1
        else:
            demodulated_bits[i//n] = 0
        
    return demodulated_bits

def bit_error_rate(original_bits, received_bits):
    return np.sum(original_bits != received_bits) / len(original_bits)

# loop over SNR values from -100 dB to 100 dB with step 5 dB
def plotting_snr_vs_ber(bit_string, modulated_signal, noisy_signal, demodulated_bits):
    snr_db = np.arange(-100, 0, 1)
    ber = []
    for snr in snr_db:
        # Modulation
        modulated_signal = bpsk_modulation(bit_string, 1, 10, 1000)

        # Adding AWGN
        noisy_signal = add_awgn(modulated_signal, snr)

        # Demodulation
        demodulated_bits = bpsk_demodulation(noisy_signal, 1, 10, 1000)

        # Calculate Bit Error Rate (BER)
        ber.append(bit_error_rate(np.array(list(map(int, bit_string))), demodulated_bits))

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(snr_db, ber, marker='o')
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate (BER)')
    plt.title('Bit Error Rate for BPSK Modulation')
    plt.grid()
    plt.show()
from scipy.io import wavfile
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from helpers import integral_image, find_all_formants, power


def spectrogram_plot(samples, sample_rate, t=11000):
    if samples.ndim > 1:
        samples = samples[:, 0]  # Если стерео, берём только один канал

    if len(samples) < 256:
        print("⚠️ Слишком короткий сигнал")
        return None, None

    frequencies, times, my_spectrogram = signal.spectrogram(
        samples, sample_rate, scaling='spectrum', window='hann', nperseg=1024
    )
    spec = np.log10(my_spectrogram + 1e-10)  # добавим малую величину, чтобы избежать log(0)

    plt.pcolormesh(times, frequencies, spec, shading='gouraud')
    plt.ylim(top=t)
    plt.ylabel('Частота [Гц]')
    plt.xlabel('Время [с]')
    return my_spectrogram, frequencies


def process_voice_file(filepath, label, num_formants=3):
    sample_rate, samples = wavfile.read(filepath)
    spec, freqs = spectrogram_plot(samples, sample_rate)
    if spec is None:
        return {
            'formants': [],
            'min': None,
            'max': None
        }

    plt.savefig(f'lab_results/spectrogram_{label}.png', dpi=500)
    plt.clf()

    spec_integral = integral_image(spec)
    formants = list(find_all_formants(freqs, spec_integral, num_formants))
    formants.sort()

    print(f"\n🔊 Форманты для {label.upper()}:")
    for i, f in enumerate(formants):
        print(f"  Форманта {i + 1}: {f} Гц")

    print(f"  Минимальная частота: {formants[0]} Гц")
    print(f"  Максимальная частота: {formants[-1]} Гц")

    formant_powers = power(freqs, spec_integral, num_formants, formants)
    strongest = sorted(formant_powers.items(), key=lambda x: x[1], reverse=True)
    top4 = sorted(formant_powers, key=lambda i: formant_powers[i])[-4:]

    print(f"  Самые сильные форманты: {top4}")
    return {
        'formants': formants,
        'min': formants[0],
        'max': formants[-1],
        'strongest': top4
    }


if __name__ == '__main__':
    results = {
        'a': process_voice_file("lab_results/wavs/voice_a.wav", 'a', num_formants=3),
        'i': process_voice_file("lab_results/wavs/voice_i.wav", 'i', num_formants=3),
        'gav': process_voice_file("lab_results/wavs/voice_gav.wav", 'gav', num_formants=5)
    }

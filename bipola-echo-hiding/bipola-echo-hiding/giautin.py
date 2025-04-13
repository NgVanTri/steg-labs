import numpy as np
from scipy.io import wavfile

def embed_bipolar_echo(input_file, output_file, secret_bits, delay=200, amplitude=0.05):
    try:
        sample_rate, audio = wavfile.read(input_file)
    except Exception as e:
        print(f"loi doc file: {e}")
        return None

    if len(audio.shape) > 1:
        print("stereo sang mono...")
        audio = np.mean(audio, axis=1)

    audio = audio.astype(float) / 32768.0
    stego_audio = np.copy(audio)

    block_size = sample_rate // 2
    num_blocks = min(len(audio) // block_size, len(secret_bits))

    for i in range(num_blocks):
        start = i * block_size
        end = start + block_size
        if end > len(audio):
            break
        block = audio[start:end]

        echo = np.zeros_like(block)
        if len(block) > delay:
            echo[delay:] = block[:-delay] * amplitude

            if secret_bits[i] == '1':
                stego_audio[start:end] += echo
            else:
                stego_audio[start:end] -= echo
            
            block_energy = np.sqrt(np.mean(stego_audio[start:end]**2))
            original_energy = np.sqrt(np.mean(audio[start:end]**2))
            if original_energy > 0 and block_energy > 0:
                stego_audio[start:end] *= (original_energy / block_energy)

   
    window_size = 50
    for i in range(1, num_blocks):
        boundary = i * block_size
        start_smooth = max(0, boundary - window_size)
        end_smooth = min(len(stego_audio), boundary + window_size)
        if end_smooth - start_smooth > 0:
            weights = np.linspace(1, 1, end_smooth - start_smooth)
            stego_audio[start_smooth:end_smooth] *= weights

    stego_audio = np.clip(stego_audio * 32768.0, -32768, 32767).astype(np.int16)
    wavfile.write(output_file, sample_rate, stego_audio)
    print(f"da nhung thanh cong vao file: {output_file}")

# Thực thi
if __name__ == "__main__":
    input_file = "input.wav"
    output_file = "stego_output.wav"
    secret_file = "messagenhiphan.txt"

    try:
        with open(secret_file, 'r', encoding='utf-8') as f:
            secret_bits = f.read().replace(' ', '').strip()
        print(f"doc {len(secret_bits)} bit tu {secret_file}")
    except Exception as e:
        print(f"khong the doc file {secret_file}: {e}")
        exit(1)

    embed_bipolar_echo(input_file, output_file, secret_bits, delay=200, amplitude=0.05)

import os
import subprocess

input_path = r"C:\Users\Landa\Desktop\lucasadp .mov"
output_path = r"C:\Users\Landa\Desktop\lucasadp_convertido.mp4"

# Tamanho máximo desejado (50MB)
max_size_mb = 50
max_size_bytes = max_size_mb * 1024 * 1024

# 1. Obter a duração do vídeo em segundos via ffprobe
def get_video_duration(input_file):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return float(result.stdout.strip())

duration = get_video_duration(input_path)

# 2. Calcular bitrate ideal para atingir o tamanho final
# fórmula: bitrate = (tamanho alvo em bytes * 8) / duração
target_bitrate = (max_size_bytes * 8) / duration

# Garantir valores seguros
video_bitrate = max(int(target_bitrate * 0.9), 300000)   # 90% para reservar espaço para o áudio
audio_bitrate = 128000                                   # sempre 128 kbps

print(f"Bitrate calculado = {video_bitrate / 1000:.2f} kbps")

# 3. Converter + comprimir
cmd = [
    "ffmpeg",
    "-i", input_path,
    "-vcodec", "libx264",      # codec eficiente
    "-b:v", str(video_bitrate),
    "-bufsize", str(video_bitrate),
    "-maxrate", str(video_bitrate),
    "-acodec", "aac",
    "-b:a", str(audio_bitrate),
    "-movflags", "+faststart", # otimiza para web
    output_path,
    "-y"  # sobrescreve sem perguntar
]

subprocess.run(cmd)

print("✅ Conversão concluída!")
print(f"📁 Arquivo gerado em: {output_path}")

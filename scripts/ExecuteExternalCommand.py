# -----------------------------------------------------.
# 外部コマンドを実行し、結果の文字列を表示.
# この例の場合は、ローカル環境の「C:\Python35\python.exe --version」を実行している.
# ただし、結果の文字列で全角文字の場合は正しく表示されない.
# -----------------------------------------------------.
import subprocess

# 外部コマンドを実行し、結果を取得.
def get_lines(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            print line

        if not line and proc.poll() is not None:
            break

get_lines("C:\Python35\python.exe --version")


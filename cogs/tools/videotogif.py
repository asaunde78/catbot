import subprocess


class converter():
    def convert(self):
        # ffmpeg_cmd = ['ffmpeg', '-y','-i', input,' -vf', 'fps=10,scale=320:-1:flags=lanczos', '-c:v', 'pam',  "-f", "image2pipe",
        # "-", "|","convert","-delay","10","-","-loop","0", "-layers","optimize",output]
        # ffmpeg_cmd = ["ffmpeg","-i", input, "-vf", "fps=10,scale=320:-1:flags=lanczos", "-c:v", "pam","-f","image2pipe", "-","|","convert", "-delay" ,"10","-","-loop","0","-layers", "optimize", output]
        subprocess.call("ffmpeg -i gifgen/input.mp4 -vf \"fps=10,scale=320:-1:flags=lanczos\" -c:v pam \
    -f image2pipe - | \
    convert -delay 10 - -loop 0 -layers optimize gifgen/gifgen.gif",shell=True)
        # subprocess.run(ffmpeg_cmd)



if __name__ == "__main__":
    c = converter()

    c.convert()
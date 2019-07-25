import subprocess, re

def exec(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return process.communicate()[0]
def execLine(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    pc = process.communicate()[0]
    fi = re.findall(b'.*\n', pc)
    return fi
def bash_apply(cmd):
    subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)

import os
import subprocess
import sys
from shutil import copyfile

branch = None
NETPYNE = 'https://github.com/Neurosim-lab/netpyne.git'
PYGEPPETTO = 'https://github.com/openworm/pygeppetto.git'
APPLICATION = 'https://github.com/MetaCell/geppetto-hnn.git'
JUPYTER = 'https://github.com/openworm/org.geppetto.frontend.jupyter.git'

# by default clones branch (which can be passed as a parameter python install.py branch test_branch)
# if branch doesnt exist clones the default_branch

def clone(repository, folder, default_branch, cwdp='', recursive=False, destination_folder=None):
    global branch
    print("Cloning " + repository)
    if recursive:
        subprocess.call(['git', 'clone', '--recursive', repository], cwd='./' + cwdp)
    else:
        if destination_folder:
            subprocess.call(['git', 'clone', repository, destination_folder], cwd='./' + cwdp)
        else:
            subprocess.call(['git', 'clone', repository], cwd='./' + cwdp)
    checkout(folder, default_branch, cwdp)


def checkout(folder, default_branch, cwdp):
    currentPath = os.getcwd()
    print(currentPath)
    newPath = currentPath + "/" + cwdp + folder
    print(newPath)
    os.chdir(newPath)
    python_git = subprocess.Popen("git branch -a", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outstd, errstd = python_git.communicate()
    if branch and branch in str(outstd):
        subprocess.call(['git', 'checkout', branch], cwd='./')
    else:
        subprocess.call(['git', 'checkout', default_branch], cwd='./')
    os.chdir(currentPath)


def main(argv):
    global branch
    if (len(argv) > 0):
        if (argv[0] == 'branch'):
            branch = argv[1]


if __name__ == "__main__":
    main(sys.argv[1:])

os.chdir(os.getcwd() + "/../")

# # Cloning Repos
# clone(repository=PYGEPPETTO, 
#     folder='pygeppetto', 
#     default_branch='development'
# )
# subprocess.call(['pip', 'install', '-e', '.'], cwd='./pygeppetto/')

# clone(repository=NETPYNE, 
#     folder='netpyne', 
#     default_branch='ui'
# )
# subprocess.call(['pip', 'install', '-e', '.'], cwd='./netpyne/')

# clone(repository=JUPYTER, 
#     folder='org.geppetto.frontend.jupyter', 
#     default_branch='development'
# )
# subprocess.call(['npm', 'install'], cwd='./org.geppetto.frontend.jupyter/js')
# subprocess.call(['npm', 'run', 'build-dev'], cwd='./org.geppetto.frontend.jupyter/js')

# clone(repository=APPLICATION, 
#     folder='geppetto-hnn', 
#     default_branch='development'
# )
print("NPM Install and build for Geppetto Frontend  ...")
os.chdir(os.getcwd() + "/geppetto-hnn")
subprocess.call(['npm', 'install'])
subprocess.call(['npm', 'run', 'build-dev-noTest'])

print("Installing jupyter_geppetto python package ...")
os.chdir(os.getcwd() + "/../org.geppetto.frontend.jupyter")
subprocess.call(['pip', 'install', '-e', '.'])
print("Installing jupyter_geppetto Jupyter Extension ...")
subprocess.call(['jupyter', 'nbextension', 'install', '--py', '--symlink', '--sys-prefix', 'jupyter_geppetto'])
subprocess.call(['jupyter', 'nbextension', 'enable', '--py', '--sys-prefix', 'jupyter_geppetto'])
subprocess.call(['jupyter', 'nbextension', 'enable', '--py', 'widgetsnbextension'])
subprocess.call(['jupyter', 'serverextension', 'enable', '--py', 'jupyter_geppetto'])

print("Installing HNN UI python package ...")
os.chdir(os.getcwd() + "/../")
subprocess.call(['pip', 'install', '-e', '.', '--no-deps', '--ignore-requires-python'])
subprocess.call(['nrnivmodl', './hnn_ui/mod'])

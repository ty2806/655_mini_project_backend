wget https://github.com/ty2806/655_mini_project_backend/archive/refs/heads/main.zip
unzip main.zip
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
chmod +x Miniconda3-py39_4.12.0-Linux-x86_64.sh
./Miniconda3-py39_4.12.0-Linux-x86_64.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda init
exec $SHELL
conda install pytorch torchvision cpuonly -c pytorch
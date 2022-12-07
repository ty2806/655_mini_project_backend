### install instruction
copy the setup.sh to a geni node and execute it. setup.sh will automatically download and install miniconda, necessary python packages, and source code repo.
    1 ./setup.sh
You may need to restart the terminal to load conda environment properly.
### run instruction

    1 cd ./655_mini_project_backend
    2 python server.py ip_address 12345

Replace the ip_address at line 2 with the external ip address of the geni node. 12345 is the port number we used for this project.
When you see "start listening" on terminal, the server is successfully running.
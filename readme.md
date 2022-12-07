### backend server setup instruction
1. Set up 3 geni slices using rspec 
    https://github.com/ty2806/655_mini_project_backend/blob/main/back1.rspec.txt
    https://github.com/ty2806/655_mini_project_backend/blob/main/back2.rspec.txt
    https://github.com/ty2806/655_mini_project_backend/blob/main/back3.rspec.txt

2. Login to each the geni node
3. Copy this bash script https://github.com/ty2806/655_mini_project_backend/blob/main/setup.sh to the geni node and execute it.
   You may need to restart the terminal to activate conda environment.
4. cd ./655_mini_project_backend
5. python server.py ip_address 12345
   Here you need to replace the ip_address is the external ip address of the geni node and 12345 is the port number we used in this project.
   When you see “start listening" on terminal, the backend server is successfully running.”

### backend structure
the backend source code contains 2 python files:
the image_classifier.py construct the image recognition model and run the model.
the server.py run a socket server, process requests from clients and invoke the image recognition model.
# aigc-cloud
AIGC-CLOUD is a platform that allows individuals or organizations to train and generate all popular AI generated content, such as STALBE-DIFFUSION, DIFFUSERS, DALLE, CHATGPT, etc.

preparation of environment:

The platform contains two types of node: Server and Client. All client nodes are in charge of the execution of the tasks, which generally contain TRAIN,  GENERATE, TERMINATE.
	prerequisite:
		Anaconda3: download install package from : https://www.anaconda.com/download/		and the follow the instruction to finish the installation.
		Git: sudo apt update & apt install git-all
		then you should follow instructions to finish the installation
	
		Stable-Diffusion : git clone https://github.com/CompVis/stable-diffusion.git
		it is suggested to install and configure virtual environment following the official instruction of Stable-Diffusion, and activate the virtual environment named "ldm".
		htps://github.com/CompVis/stable-diffusion
		run "conda env create -f environment.yaml" and then "conda activate ldm", all requirements will be added to our project later.
		
		Diffusers: pip install --upgrade diffusers[torch]  or  conda install -c conda-forge diffusers
		
	run following cmd to download source code, you will have to be invited to the group because its a private repository.
		git clone https://github.com/soaringalano/aigc-cloud.git
		
	after having downloaded the source code, switch into the project directory, and run:
		pip install -e requirements.txt
		
		
run client and server:
	
	you will find two executable python files under the root directory of the source code named "simple_client.py" and "simple_server.py".
	you will have to set environment variables to run them.
	TO run simple_lient.py:
		export CLIENT_ADDR=<IP address of the local machine or virtual machine or container>
		export CLIENT_PORT=<port of the local machine or virtual machine or container listened by the server>
		python simple_client.py
	To run simple_server.py:
		export SERVER_ADDR=<IP address of the local machine or virtual machine or container>
		export SERVER_PORT=<port of the local machine or virtual machine or container that communicates with the front-end UI>
		python simple_server.py
	
	to test run tasks by calling RESTful api of the server, see example in the file: tests/test_execute_server.py and test/test_execute_client.py
		

# **aigc-cloud**<p/>
**AIGC-CLOUD is a platform that allows individuals or organizations to train and generate all popular AI generated content, such as STALBE-DIFFUSION, DIFFUSERS, DALLE, CHATGPT, etc.**<p/>
<p/>
preparation of environment:<p/>
<p/>
The platform contains two types of node: Server and Client. All client nodes are in charge of the execution of the tasks, which generally contain **TRAIN**,  **GENERATE**, **TERMINATE**.<p/>
<p/>
*prerequisite*:<p/>
*Anaconda3*: download install package from : [Anaconda](https://www.anaconda.com/download/) and then follow the instruction to finish the installation.<p/>
*Git*: execute in bash "*sudo apt update & apt install git-all*" then follow instructions to finish the installation<p/>
<p/>
[*Stable-Diffusion*](https://github.com/CompVis/stable-diffusion) : execute "*git clone https://github.com/CompVis/stable-diffusion.git*"<p/>
it is suggested to install and configure virtual environment following the official instruction of Stable-Diffusion, and activate the virtual environment named "ldm".<p/>

run '''conda env create -f environment.yaml''' and then '''conda activate ldm''', all requirements will be added to our project later.<p/>
<p/>
Diffusers: pip install --upgrade diffusers[torch]  or  conda install -c conda-forge diffusers<p/>
		<p/>
	run following cmd to download source code, you will have to be invited to the group because its a private repository.<p/>
		git clone https://github.com/soaringalano/aigc-cloud.git<p/>
		<p/>
	after having downloaded the source code, switch into the project directory, and run:<p/>
		pip install -e requirements.txt<p/>
		<p/>
		<p/>
run client and server:<p/>
	<p/>
	you will find two executable python files under the root directory of the source code named "simple_client.py" and "simple_server.py".<p/>
	you will have to set environment variables to run them.<p/>
	TO run simple_lient.py:<p/>
		export CLIENT_ADDR=<IP address of the local machine or virtual machine or container><p/>
		export CLIENT_PORT=<port of the local machine or virtual machine or container listened by the server><p/>
		python simple_client.py<p/>
	To run simple_server.py:<p/>
		export SERVER_ADDR="IP address of the local machine or virtual machine or container"<p/>
		export SERVER_PORT="port of the local machine or virtual machine or container that communicates with the front-end UI"<p/>
		python simple_server.py<p/>
	<p/>
	to test run tasks by calling RESTful api of the server, see example in the file: tests/test_execute_server.py and test/test_execute_client.py<p/>
		

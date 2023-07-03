# **AIGC-CLOUD**
**aigc-cloud is a platform that allows individuals or organizations to train and generate all popular AI generated content, such as STALBE-DIFFUSION, DIFFUSERS, DALLE, CHATGPT, etc.**

## *preparation of environment:*

The platform contains two types of node: Server and Client. All client nodes are in charge of the execution of the tasks, which generally contain  **TRAIN**,  **GENERATE**, **TERMINATE**; while server node is in charge of the distribution of tasks.

## *prerequisite:*
### [Anaconda3](https://www.anaconda.com/download/)
download the bash file and follow the instruction to complete the installation.

### [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)<br/>
```
sudo apt update & apt install git-all
```
then follow the instruction to complete the installation

### [Stable-Diffusion](https://github.com/CompVis/stable-diffusion)<br/>
```
git clone https://github.com/CompVis/stable-diffusion.git
```
it is suggested to install and configure virtual environment following the official instruction of Stable-Diffusion, and activate the virtual environment named "ldm".

```
conda env create -f environment.yaml
conda activate ldm
```
*all requirements will be added to our project later.*

### [Diffusers](https://github.com/huggingface/diffusers)<br/>
```
pip install --upgrade diffusers[torch]
```
or
```
conda install -c conda-forge diffusers
```
### [aigc-cloud](https://github.com/soaringalano/aigc-cloud.git)<br/>

run following cmd to download source code, you will have to be invited to the group because its a private repository.

```
git clone https://github.com/soaringalano/aigc-cloud.git
```

after having downloaded the source code, switch into the project directory, and run:

```
pip install -r requirements.txt
```


## To run client and server:

you will find two executable python files under the root directory of the source code named "simple_client.py" and "simple_server.py".
you will have to set environment variables to run them.

### To run simple_client.py:
```
export CLIENT_ADDR=<IP address of the local machine or virtual machine or container>
export CLIENT_PORT=<port of the local machine or virtual machine or container listened by the server>
python simple_client.py
```

### To run simple_server.py:
```
export SERVER_ADDR="IP address of the local machine or virtual machine or container"
export SERVER_PORT="port of the local machine or virtual machine or container that communicates with the front-end UI"
python simple_server.py
```

To test run tasks by calling RESTful api of the server, see example in the file: tests/test_execute_server.py and test/test_execute_client.py

## TODO
Currently we are using python flask for communication among server nodes and client nodes for easy test. This will be switched to RabbitMQ for secure and stable service.

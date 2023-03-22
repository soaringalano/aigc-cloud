export MASTER_ADDR='172.17.0.2'
export MASTER_PORT=80

NODE_RANK="0" python main.py -t true -b models/ldm/cin256/config.yaml --accelerator="ddp" --gpus="0," --logger="true" --num_nodes=2

from enum import Enum
from typing import Dict, Union
import json


class TaskType(Enum):
    diffusers = "diffusers"
    stable_diffusion = "stable_diffusion"
    dalle = "dalle"
    chatgpt = "chatgpt"
    gpt4 = "gpt4";


class TaskGoal(Enum):
    train = "train"
    generate = "generate"
    status = "status"
    terminate = "terminate"
    suspend = "suspend"


class BasicTaskConfig(Dict):
    task_id = "task_id"
    user_id = "user_id"
    cluster_id = "cluster_id"
    task_type = "task_type"
    task_goal = "task_goal"
    environment_variables = "envvar"

    # def __init__(self,
    #              task_id=None,
    #              cluster_id=None,
    #              task_type=TaskType.STABLE_DIFFUSION,
    #              task_goal=TaskGoal.TRAIN,
    #              environment_variables: Dict = None) -> None:
    #     super().__init__()
    #     self[self.task_id] = task_id
    #     self[self.cluster_id] = cluster_id
    #     self[self.task_type] = task_type
    #     self[self.task_goal] = task_goal
    #     if environment_variables is not None:
    #         self[self.environment_variables] = environment_variables
    #     return

    def set_param(self, key, value):
        self[key] = value

    def set_params(self, params: Dict):
        if params is None:
            return
        for key in params.keys():
            self[key] = params[key]
        return


class DiffusersTrainConfig(BasicTaskConfig):
    model_name = "model_name"
    model_path = "model_path"
    dataset_name = "dataset_name"
    train_data_dir = "train_data_dir"
    use_ema = "use_ema"
    resolution = "resolution"
    batch_size = "batch_size"
    gradient_accumu_steps = "gradient_accumu_steps"
    gradient_checkpointing = "gradient_checkpointing"
    mixed_precision = "mixed_precision"
    max_train_steps = "max_train_steps"
    learning_rate = "learning_rate"
    max_grad_norm = "max_grad_norm"
    lr_schedule = "lr_schedule"
    lr_warmup_steps = "lr_warmup_steps"
    output_dir = "output_dir"

    # def __init__(self,
    #              task_id=None,
    #              cluster_id=None,
    #              task_type=TaskType.STABLE_DIFFUSION,
    #              task_goal=TaskGoal.TRAIN,
    #              environment_variables: Dict = None,
    #              train_data_dir=None,
    #              model_name=None,
    #              model_path=None,
    #              dataset_name=None,
    #              use_ema=True,
    #              resolution=512,
    #              batch_size=1,
    #              gradient_accumu_steps=4,
    #              gradient_checkpointing=True,
    #              mixed_precision="fp16",
    #              max_train_steps=15000,
    #              learning_rate=1e-05,
    #              max_grad_norm=1,
    #              lr_schedule="constant",
    #              lr_warmup_steps=0,
    #              output_dir=None) -> None:
    #     super().__init__(task_id, cluster_id, task_type, task_goal, environment_variables)
    #     self[self.train_data_dir] = train_data_dir
    #     self[self.model_name] = model_name
    #     self[self.model_path] = model_path
    #     self[self.dataset_name] = dataset_name
    #     self[self.train_data_dir] = train_data_dir
    #     self[self.use_ema] = use_ema
    #     self[self.resolution] = resolution
    #     self[self.batch_size] = batch_size
    #     self[self.gradient_accumu_steps] = gradient_accumu_steps
    #     self[self.gradient_checkpointing] = gradient_checkpointing
    #     self[self.mixed_precision] = mixed_precision
    #     self[self.max_train_steps] = max_train_steps
    #     self[self.learning_rate] = learning_rate
    #     self[self.max_grad_norm] = max_grad_norm
    #     self[self.lr_schedule] = lr_schedule
    #     self[self.lr_warmup_steps] = lr_warmup_steps
    #     self[self.output_dir] = output_dir
    #     return


class StableDiffusionTrainConfig(BasicTaskConfig):

    accelerator = "accelerator"
    master_addr = "master_addr"
    master_port = "master_port"
    node_rank = "node_rank"
    gpu_count = "gpu_count"
    num_nodes = "num_nodes"

    train_data_dir = "train_data_dir"
    task_name = "task_name"
    resume = "resume"
    base = "base"
    train = "train"
    project = "project"
    debug = "debug"
    seed = "seed"
    postfix = "postfix"
    logdir = "logdir"
    scale_lr = "scale_lr"
    yaml_content = "yaml_content"

    # def __init__(self,
    #              task_id=None,
    #              cluster_id=None,
    #              task_type=TaskType.STABLE_DIFFUSION,
    #              task_goal=TaskGoal.TRAIN,
    #              environment_variables: Dict = None,
    #              train_data_dir=None,
    #              task_name=None,
    #              resume=None,
    #              base: str = None,
    #              train: bool = False,
    #              project=None,
    #              debug: bool = False,
    #              seed: int = 23,
    #              postfix: str = None,
    #              logdir: str = "logs",
    #              scale_lr: bool = True,
    #              yaml_content: str = None
    #              ) -> None:
    #     super().__init__(task_id, cluster_id, task_type, task_goal, environment_variables)
    #     self[self.train_data_dir] = train_data_dir
    #     self[self.task_name] = task_name
    #     self[self.resume] = resume
    #     self[self.base] = base
    #     self[self.train] = train
    #     self[self.project] = project
    #     self[self.debug] = debug
    #     self[self.seed] = seed
    #     self[self.postfix] = postfix
    #     self[self.logdir] = logdir
    #     self[self.scale_lr] = scale_lr
    #     self[self.yaml_content] = yaml_content
    #     return


class StableDiffusionGenerateConfig(BasicTaskConfig):
    prompt = "prompt"
    outdir = "outdir"
    skip_grid = "skip_grid"
    skip_save = "skip_save"
    ddim_steps = "ddim_steps"
    plms = "plms"
    dpm_solver = "dpm_solver"
    laion400m = "laion400m"
    fixed_code = "fixed_code"
    ddim_eta = "ddim_eta"
    n_iter = "n_iter"
    H = "H"
    W = "W"
    C = "C"
    f = "f"
    n_sample = "n_sample"
    n_rows = "n_rows"
    scale = "scale"
    from_file = "from-file"
    config = "config"
    ckpt = "ckpt"
    seed = "seed"
    precision = "precision"

    # def __init__(self,
    #              task_id=None,
    #              cluster_id=None,
    #              task_type=TaskType.STABLE_DIFFUSION,
    #              task_goal=TaskGoal.GENERATE,
    #              environment_variables: Dict = None,
    #              prompt: str = "a painting of a virus monster playing guitar",
    #              outdir: str = "$STABLE_DIFFUSION_HOME/samples",
    #              H: int = 512,
    #              W: int = 512,
    #              C: int = 4,
    #              n_sample=3,
    #              n_rows: int = 3,
    #              scale: float = 7.5,
    #              config: str = "$STABLE_DIFFUSION_HOME/configs/stable-diffusion/v1-inference.yaml",
    #              ckpt: str = "$STABLE_DIFFUSION_HOME/models/ldm/stable-diffusion-v1/model.ckpt"):
    #     super().__init__(task_id, cluster_id, task_type, task_goal, environment_variables)
    #     self[self.prompt] = prompt
    #     self[self.scale] = scale
    #     self[self.outdir] = "{outdir}/{task_id}".format(outdir=outdir, task_id=task_id)
    #     self[self.H] = H
    #     self[self.W] = W
    #     self[self.C] = C
    #     self[self.n_samples] = n_sample
    #     self[self.n_rows] = n_rows
    #     self[self.config] = config
    #     self[self.ckpt] = ckpt
    #     return


class TerminateTaskConfig(Dict):

    cluster_id = "cluster_id"
    task_id = "task_id"
    task_goal = "task_goal"

    def __init__(self,
                 cluster_id,
                 task_id,
                 task_goal: TaskGoal = TaskGoal.terminate):
        super().__init__()

        self[self.cluster_id] = cluster_id
        self[self.task_id] = task_id
        self[self.task_goal] = task_goal
        return

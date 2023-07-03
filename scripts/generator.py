import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "a photo of a cyberpunk style city with high steel buildings and steel bridges and two moon in the sky"
for i in range(10):
    image = pipe(prompt).images[0]
    image.show()
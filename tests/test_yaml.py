import yaml

# with open('test_stable_diffusion_config.yaml') as f:
with open('../user_config.yaml') as f:
    data = yaml.load(stream=f, Loader=yaml.FullLoader)

print(type(data))

print(data)

print(data['users']['soaringalano_cx']['password'])
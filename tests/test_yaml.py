import yaml

# with open('test_stable_diffusion_config.yaml') as f:
with open('../storage_config.yaml') as f:
    data = yaml.load(stream=f, Loader=yaml.FullLoader)

print(type(data))

print(data)

print(data['aliyun']['oss']['bucket'])
print(data['aliyun']['oss']['accesskey'])
print(data['aliyun']['oss']['secret'])
print(data['aliyun']['oss']['endpoint'])
print(data['aliyun']['oss']['bucket.domain'])
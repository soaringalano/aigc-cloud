import time
import nft_storage
from nft_storage.models import NFT
from nft_storage.api import nft_storage_api
from nft_storage.model.error_response import ErrorResponse
from nft_storage.model.upload_response import UploadResponse
from nft_storage.model.unauthorized_error_response import UnauthorizedErrorResponse
from nft_storage.model.forbidden_error_response import ForbiddenErrorResponse
from pprint import pprint
from typing import Union, List, Dict
import os
import json
import yaml
import oss2

with open("nft_storage.key") as f:
    nft_storage_key = f.readline()
    # print(nft_storage_key)

with open('storage_config.yaml') as f:
    aliyun_config = yaml.load(stream=f, Loader=yaml.FullLoader)
    aliyun_bucket = aliyun_config['aliyun']['oss']['bucket']
    aliyun_accesskey = aliyun_config['aliyun']['oss']['accesskey']
    aliyun_accesskey_secret = aliyun_config['aliyun']['oss']['secret']
    aliyun_endpoint = aliyun_config['aliyun']['oss']['endpoint']
    aliyun_bucket_domain = aliyun_config['aliyun']['oss']['bucket.domain']
    auth = oss2.Auth(aliyun_accesskey, aliyun_accesskey_secret)
    bucket = oss2.Bucket(auth, aliyun_endpoint, aliyun_bucket)


configuration = nft_storage.Configuration(
    host="https://api.nft.storage",
    access_token=nft_storage_key
)

def store_file_to_aliyun(user_id:str, task_id:str, file:str, idx:int=-1) -> (bool, str):
    if user_id is not None and task_id is not None and \
            file is not None and os.path.isfile(file):
        fh, ft = os.path.split(file)
        if idx >= 0:
            key = user_id + "/" + task_id + "/" + idx + "_" + ft
        else:
            key = user_id + "/" + task_id + "/" + ft

        res = oss2.resumable_upload(bucket, key, file)
        if res is None or res.etag is None or res.request_id is None:
            return False, "upload to server failed"
        return True, key
    return False, f"the specified file %s doesn't exist" % file

def remove_file_from_aliyun(key:str) -> bool:
    # head, tail = os.path.split(key)
    for obj in oss2.ObjectIterator(bucket, prefix=key):
        res = bucket.delete_object(obj.key)
        print(res)
    if res.status == 200:
        return True
    return False

def remove_files_from_aliyun(keys:List[str]) -> bool:
    res = bucket.batch_delete_objects(keys)
    print(res.status)
    if res.status == 200:
        return True
    return False

def store_dir_to_aliyun(task_id:str, dir:str) -> (List[bool], List[str]):
    if dir is not None and os.path.isdir(dir):
        stats = []
        keys = []
        idx = 0
        with os.walk(dir) as (dir_paths, dir_names, files):
            for file in files:
                stat, key = store_file_to_aliyun(task_id=task_id, file=file, idx = idx)
                stats.append(stat)
                keys.append(key)
                idx += 1
        return stats, keys
    else:
        return [], []







def store_file_to_ipfs(file:str) -> (bool, Union[str, NFT]):
    with nft_storage.ApiClient(configuration=configuration) as api_client:
        api_instance = nft_storage_api.NFTStorageAPI(api_client=api_client)
        body = open(file, 'rb')

        try:
            api_response = api_instance.store(body)
            pprint(api_response)
            return api_response.ok, api_response.value
        except nft_storage.ApiException as e:
            print("Exception when calling NFTStorageAPI -> store: %s\n" % e)
            return False, "{\"err\": %s}" % e


def store_dir_to_ipfs(dir: str) -> (bool, Dict[str, Union[List[str], List[NFT]]]):
    with nft_storage.ApiClient(configuration=configuration) as api_client:
        api_instance = nft_storage_api.NFTStorageAPI(api_client=api_client)
        success = []
        fail = []
        with os.walk(dir) as (dir_paths, dir_names, files):
            for file in files:
                body = open(file, 'rb')
                try:
                    api_response = api_instance.store(body)
                    pprint(api_response)
                    if api_response.ok:
                        success.append(api_response.value)
                    else:
                        fail.append(file)
                except nft_storage.ApiException as e:
                    print("Exception when calling NFTStorageAPI -> store: %s\n" % e)
                    fail.append(file)
            if len(success) > 0:
                return True, {"success": success, "fail": fail}
            else:
                return False, {"fail": fail}

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

with open("nft_storage.key") as f:
    nft_storage_key = f.readline()
    # print(nft_storage_key)


configuration = nft_storage.Configuration(
    host="https://api.nft.storage",
    access_token=nft_storage_key
)


def store_image_as_nft(file:str) -> (bool, Union[str, NFT]):
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


def store_dir_images_as_nft(dir: str) -> (bool, Dict[str, Union[List[str], List[NFT]]]):
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


def test_store_file():
    file = "..\\1.jpg"
    ok, nft = store_image_as_nft(file)
    if ok:
        print("upload ok, cid is %s" % json.dumps(nft.cid))
    else:
        print("upload failed reason is %s" % nft)


# test_store_file()
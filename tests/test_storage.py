from utils.public_cdn_utils import *


def test_store_file_to_ipfs():
    file = "..\\1.jpg"
    ok, nft = store_file_to_ipfs(file)
    if ok:
        print("upload ok, cid is %s" % json.dumps(nft.cid))
    else:
        print("upload failed reason is %s" % nft)


def test_store_file_to_aliyun():
    file = "../README.md"
    stat, key = store_file_to_aliyun("ml", "test", file, -1)
    print(stat, key)
    # key = "ml/test/README.md"
    stat = remove_files_from_aliyun([key])
    print(stat)

# test_store_file()

if __name__ == "__main__":
    test_store_file_to_aliyun()
    # pass
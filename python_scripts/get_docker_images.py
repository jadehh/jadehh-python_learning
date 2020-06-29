#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : get_docker_images.py
# @Author  : jade
# @Date    : 20-5-11 上午11:09
# @Mailbox : jadehh@live.com
# @Software: Samples
# @Desc    :



import requests
import urllib.request as urllib2
#import urllib2
import prettytable as pt
import json
##获取所有镜像
"http:///127.0.0.1:5000/v2/_catalog"
##获取镜像的版本
"http://127.0.0.1:5000/v2/ubuntu/registry/tags/list"
##查看详情
"http://127.0.0.1:5000/v2/ubuntu/registry/manifests/latest"

"http://127.0.0.1:5000/v2/ubuntu/registry/blobs/sha256:486039affc0ad0f17f473efe8fb25c947515a8929198879d1e64210ef142372f"



###根据url链接提取下载文件的大小特征和下载文件类型
def getRemoteFileSize(url, proxy=None):
    '''
    通过content-length头获取远程文件大小
    '''
    opener = urllib2.build_opener()
    try:
        request = urllib2.Request(url)
        request.get_method = lambda: 'HEAD'
        response = opener.open(request)
        response.read()
    except Exception as e:
        # 远程文件不存在
        return 0, 0
    else:
        getfileSize = dict(response.headers).get('content-length', 0)
        filesize = round(float(getfileSize) / 1048576, 2)
        getContentType = dict(response.headers).get('content-type', 0)
        return filesize, getContentType


def getDockerContent(IPADDRESS):
    docker_image_url = "http://{}/v2/_catalog".format(IPADDRESS)
    verson_url = "http://{}/v2/{}/tags/list".format(IPADDRESS, "{}")
    manifests = "http://{}/v2/{}/{}/manifests/{}".format(IPADDRESS,"{}","{}","{}")
    blob_url = "http://{}/v2/{}/blobs/{}".format(IPADDRESS,"{}","{}")

    root_path = "/edc/images/registry/docker/registry/v2/repositories"
    res = requests.get(docker_image_url)
    space_list = []
    all_docker_image_list = []
    if res.status_code == 200:
        repositories = res.json()["repositories"]
        for repository in repositories:
            if repository.split("/")[0] not in space_list:
                space_list.append(repository.split("/")[0])
        # print(space_list)

        for space in space_list:
            space_docker_image_list = []
            for repository in repositories:
                if space == repository.split("/")[0]:
                    space_docker_image_list.append(repository.split("/")[1])
            all_docker_image_list.append((space, space_docker_image_list))
        tb = pt.PrettyTable()
        tb.field_names = ["ID","REPOSITORY","CREATED","SIZE"]
        index = 0
        for space_docker in all_docker_image_list:
            for docker_image in space_docker[1]:
                version_url_detail = verson_url.format(space_docker[0] + "/" + docker_image)
                version_req = requests.get(version_url_detail)
                ver_repositories = version_req.json()["tags"]
                for version_image in ver_repositories:
                    manifests_url = manifests.format(space_docker[0],docker_image,version_image)
                    manifests_req = requests.get(manifests_url)
                    manifests_repositories = manifests_req.json()
                    sum_size = 0
                    histories = manifests_repositories.get("history")
                    v1Compatibility = (json.loads(histories[0].get("v1Compatibility")))
                    create_time = v1Compatibility.get("created")
                    create_time_format = create_time[:10]+ " " + create_time[11:19]
                    for blobsum in manifests_repositories.get("fsLayers"):

                        blob_url_detail = blob_url.format(space_docker[0]+"/"+docker_image,blobsum.get("blobSum"))
                        size = getRemoteFileSize(blob_url_detail)
                        #print(blob_url_detail,size)
                        sum_size = sum_size + size[0]
                    index = index + 1
                    tb.add_row([str(index), IPADDRESS + "/" + space_docker[0] + "/" + docker_image + ":" + version_image, create_time_format, str(sum_size)+" MB"])
        print(tb)



if __name__ == '__main__':
    # get_doc_real_size("/home/jade/sda2/Data")
    #getRemoteFileSize("http://127.0.0.1:5000/v2/ubuntu/registry/blobs/sha256:486039affc0ad0f17f473efe8fb25c947515a8929198879d1e64210ef142372f")

    getDockerContent("192.168.40.192:5000")


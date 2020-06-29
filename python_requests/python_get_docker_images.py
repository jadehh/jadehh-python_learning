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
                    create_time_json = v1Compatibility.get("created")
                    create_time = create_time_json[:10] + " " + create_time_json[11:19]
                    ##时间会有延迟

                    for blobsum in manifests_repositories.get("fsLayers"):

                        blob_url_detail = blob_url.format(space_docker[0]+"/"+docker_image,blobsum.get("blobSum"))
                        size = getRemoteFileSize(blob_url_detail)
                        #print(blob_url_detail,size)
                        sum_size = sum_size + size[0]
                    index = index + 1
                    day_detail_str = create_time[:10]
                    year_str = day_detail_str[:4]
                    month_str = day_detail_str[5:7]
                    day_str = day_detail_str[8:10]
                    time_str =  create_time[11:19]
                    hour_str = time_str[:2]
                    hour_int = int(hour_str)
                    hour_int_new = hour_int + 8
                    ms = time_str[3:]

                    if hour_int_new > 23:
                        day_int = int(day_str)
                        hour_int = hour_int_new - 24
                        if hour_int < 10:
                            hour_str = "0"+str(hour_int)
                        else:
                            hour_str = str(hour_int)
                        day_int = day_int + 1
                        if day_int < 10:
                            day_str = "0"+str(day_int)
                        else:
                            day_str = str(day_int)
                        new_time = year_str  + "-" + month_str + "-" +  day_str + " " + hour_str + ":" + ms

                    else:
                        if hour_int_new < 10:
                            hour_str = "0"+str(hour_int_new)
                        else:
                            hour_str = str(hour_int_new)
                        new_time = day_detail_str +" "+ hour_str +":" + ms
                    tb.add_row([str(index), IPADDRESS + "/" + space_docker[0] + "/" + docker_image + ":" + version_image, new_time, str(sum_size)+" MB"])
        print(tb)



if __name__ == '__main__':
    # get_doc_real_size("/home/jade/sda2/Data")
    #getRemoteFileSize("http://127.0.0.1:5000/v2/ubuntu/registry/blobs/sha256:486039affc0ad0f17f473efe8fb25c947515a8929198879d1e64210ef142372f")

    getDockerContent("192.168.35.120:5000")


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File     : packaging.py
# @Author   : jade
# @Date     : 2021/4/30 10:47
# @Email    : jadehh@1ive.com
# @Software : Samples
# @Desc     :
import os
import shutil
def build(args):
    ID = int(args.ID)
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    os.mkdir("build/")
    print("ID = {}".format(ID))
    build_path = "build/lib.linux-x86_64-3.6"
    tmp_path = "build/temp.linux-x86_64-3.6"
    ep_build_path = "build/encryption"

    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    if os.path.exists(ep_build_path):
        shutil.rmtree(ep_build_path)
    os.mkdir(ep_build_path)

    os.system("/home/jade/.local/share/virtualenvs/python_learning-uh7iycro/bin/python setup.py build_ext")
    build_file_list = os.listdir(os.path.join(build_path, "src_copy"))
    for build_file in build_file_list:
        if build_file[-3:] == ".so":
            if ID == 0:
                shutil.copy(os.path.join(build_path, "src_copy", build_file),
                            os.path.join(ep_build_path, build_file.split(".")[0] + ".so"))
            else:
                os.system(
                    "/home/jade/SoftWare/加密狗软件/Linux/VendorTools/Envelope/linuxenv -v:/home/jade/RGMGT.hvc -f:{} {} {}".format(
                        ID, os.path.join(build_path, "src_copy", build_file),
                        os.path.join(ep_build_path, build_file.split(".")[0] + ".so")))

    shutil.rmtree("src_copy")
    shutil.rmtree(build_path)
    shutil.rmtree(tmp_path)


def packing(args):
    with open("{}.spec".format(args.app_name),"w") as f:
        f.write("# -*- mode: python ; coding: utf-8 -*-\n"
                "block_cipher = None\n"
                "a = Analysis(['main.py'],\n"
                "pathex=[],\n"
                "binaries=[],\n"
                "datas=[],\n"
                " hiddenimports=[],\n"
                "hookspath=[],\n"
                "runtime_hooks=[],\n"
                "excludes=[],\n"
                "win_no_prefer_redirects=False,\n"
                " win_private_assemblies=False,\n"
                "cipher=block_cipher,\n"
                "noarchive=False)\n"
                "pyz = PYZ(a.pure, a.zipped_data,\n"
                "cipher=block_cipher)\n"
                "exe = EXE(pyz,\n"
                " a.scripts,\n"
                "a.binaries,\n"
                "a.zipfiles,\n"
                " a.datas,\n"
                "[],\n"
                "name='{}',\n"
                "debug=False,\n"
                "bootloader_ignore_signals=False,\n"
                "strip=False,\n"
                " upx=True,\n"
                "upx_exclude=[],\n"
                "runtime_tmpdir=None,\n"
                "console=True )\n".format(args.app_name))
    cmd_str = "/home/jade/.local/share/virtualenvs/python_learning-uh7iycro/bin/pyinstaller -F {}.spec".format(args.app_name)
    os.system(cmd_str)
    if os.path.exists(args.name) is True:
        shutil.rmtree(args.name)
    os.mkdir(args.name)
    os.mkdir(os.path.join(args.name,"lib"))
    os.mkdir(os.path.join(args.name,"bin/"))
    file_list = os.listdir("dist")
    ep_build_path = "build/encryption"
    for build_file in os.listdir(ep_build_path):

        shutil.copy(os.path.join(ep_build_path,build_file),os.path.join(args.name,"lib/{}").format(build_file))
    for file_name in file_list:
        if os.path.isdir(os.path.join("dist",file_name)):
            shutil.copy(os.path.join(os.path.join("dist",file_name),file_name),os.path.join(args.name,"bin/{}".format(file_name)))
        else:
            shutil.copy(os.path.join("dist",file_name),os.path.join(args.name,"bin/{}".format(file_name)))
    if os.path.exists("build") is True:
        shutil.rmtree("build")
    if os.path.exists("dist") is True:
        shutil.rmtree("dist")
    if os.path.exists("{}.spec".format(args.app_name)) is True:
        os.remove("{}.spec".format(args.app_name))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ID', type=str,
                        default="0")
    parser.add_argument('--app_name', type=str,
                        default="main") ##需要打包的文件名称
    parser.add_argument('--name', type=str,
                        default="三宝科技") ##生成软件文件夹名称
    args = parser.parse_args()
    build(args)
    packing(args)


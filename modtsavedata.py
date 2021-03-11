# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        modtsavedata.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     2016/03/24
# Last Change: 2021/03/10 16:00:41.
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10007
# -----------------------------------------------------------------------------
""" データ保存 処理 GUI """

# モジュールインポート
import sys
import savedata as sd

# Python2 用設定
if sys.version_info.major == 2:
    # sysモジュール リロード
    reload(sys)
    # デフォルトの文字コード 出力
    sys.setdefaultencoding("utf-8")

name_first = "MasterPic"
file_name = "%s_*.txt" % name_first
path = ".\\MasterDataModuleTest7"

savedata = sd.SaveData(name_first, file_name, path, "ModuleTestInitValue")
savedata.SaveData()


def main():
    pass


if __name__ == "__main__":
    main()

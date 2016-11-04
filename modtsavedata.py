# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        modtsavedata.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     24/03/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10007
# -----------------------------------------------------------------------------

# モジュールインポート
import savedata as sd

import sys
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

# !/usr/bin/python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------  # {{{
# Name:        savedata.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     2016/03/23
# Last Change: 2021/03/11 17:16:23.
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10006
# ----------------------------------------------------------------------  # }}}
""" データ保存 処理 """

# TODO:
# 変数は "[大区分/固有]_[小区分/汎用]"
# Unix対応(ホームディレクトリの指定が不明、"~/" が使えない)
# テキストログのヘッダを生成する

# DONE:

# モジュールインポート
import os
import re
import sys
import cv2
import glob
import datetime
import platform
import importlib

from operator import itemgetter

# Python2 用設定
if sys.version_info.major == 2:
    # sysモジュール リロード
    importlib.reload(sys)
    # デフォルトの文字コード 出力
    sys.setdefaultencoding("utf-8")

print_col = 50


class SaveData:
    """ テキストデータ 保存クラス """
    def __init__(self, name, path):
        self.name = name
        self.path = path

        # TODO: "os.path.join" を使う
        # UnixとWindowsのデリミタ差異 補完
        if os.name != "nt":
            self.delimiter = "/"
        elif os.name == "nt":
            self.delimiter = "\\"

    def get_name_max(self, extension, save_lim=0):
        """ ファイル名検索 枝番の最大値 取得 """
        glob_pattern = None
        re_pattern = None
        search = None
        find = None
        get_num = None
        set_num = None
        self.match_flag = False

        # "glob_pattern" を検索
        # 末尾5桁が数字のパターン
        name = "{}_[0-9][0-9][0-9][0-9][0-9]{}".format(self.name, extension)
        glob_pattern = os.path.join(self.path, name)
        match_file = glob.glob(glob_pattern)
        search_file = str(self.name) + "_*****" + str(extension)

        print("")  # {{{
        print(" START GET MAX BRANCH No. ".center(print_col, "-"))
        print(">> Save lim: {}".format(save_lim))
        print(">> Search file & path:")
        print(self.path.rjust(print_col, " "))
        print(search_file.rjust(print_col, " "))
        print(">> Search name:")
        print(str(self.name).rjust(print_col, " "))
        print("> Serch pattern: {}".format(glob_pattern))
        print("> Match file: {}".format(match_file))
        print("")
        # }}}

        # ファイル有無 判定
        if match_file:
            set_name = max(match_file)
            self.match_flag = True

        # ファイル無し 処理
        else:
            try:
                os.mkdir("{}".format(self.path))

            except :
            # except FailMakeDir:
                set_name = self.path + self.name + "_00000" + extension
                self.match_flag = False

        print(">> Match is " + str(self.match_flag))

        if self.match_flag is True:
            list_name = []
            print("".center(print_col, "/"))
            print(">> Match file:")

            for obj in match_file:
                # 捕捉したファイルのタイムスタンプ取得 処理
                stat = os.stat(obj)
                mod_last = stat.st_mtime
                time_last = datetime.datetime.fromtimestamp(mod_last)
                time_last = time_last.strftime("%Y-%m-%d %H:%M:%S")
                list_name.append([obj, time_last])

                # 捕捉したファイル名とタイムスタンプ 出力
                print("{}\n{}".format(obj, time_last))

            print("".center(print_col, "/"))

            # 捕捉したファイル タイムスタンプ順でソート
            list_name.sort(key=itemgetter(1))
            old_name = list_name[0][0]
            print(">> Sort by time:")
            for obj in list_name:
                print(obj)
            print(">> Oldest: {}".format(old_name))

        else:
            set_name = self.path + self.name + "_00000" + extension
            old_name = self.path + self.name + "_00000" + extension

        print("")

        # "_[2連続以上の数値型]"を検索し、"数値のみ" 取得してインクリメント
        re_pattern = re.compile("_\d{2,}")
        search = re_pattern.search(set_name)
        find = search.group()[1:]
        get_num = int(find)

        # 最古のマッチを上記方法で検索
        search = re_pattern.search(old_name)
        find = search.group()[1:]
        old_num = int(find)
        print("Old num: " + str(old_num))

        set_num = get_num + 1
        self.old_name = str(self.name) + "_" + "{0:05d}".format(old_num)
        self.get_name = str(self.name) + "_" + "{0:05d}".format(get_num)

        # 保存数 制限
        if get_num >= save_lim > 0:
            self.set_name = str(self.name) + "_" + "{0:05d}".format(old_num)
            print(">> Reset branch")
        else:
            self.set_name = str(self.name) + "_" + "{0:05d}".format(set_num)

        print(">> Get path & name ")
        print(str(self.set_name).rjust(print_col, " "))
        print(">> Set branch No." + str(set_num))
        print(">> Old name: " + str(self.old_name))
        print(">> Get name: " + str(self.get_name))
        print(">> Set name: " + str(self.set_name))
        print(" END GET MAX BRANCH No. ".center(print_col, "-"))
        print("")

        return self.set_name, self.get_name, self.match_flag

    def save_text(self, text="None", numbering=False):
        """ データ保存 処理 """
        extension = ".txt"
        self.time = datetime.datetime.today()
        self.get_name_max(extension)

        print(">> Get path: " + str(self.path))
        if numbering is True:
            file_name = self.get_name
        elif numbering is False:
            file_name = self.name

        print(">> Get name: " + str(file_name))

        spt = self.path
        sdm = self.delimiter
        name_save = "{}{}{}.txt".format(spt, sdm, file_name)

        with open(name_save, "a") as data:
            data.write(">> Save time: {}, {} \r\n".format(self.time, text))

    def save_image(self, image, extension, save_lim=0, end_process=None):
        self.get_name_max(extension, save_lim)

        print(">> Set path: " + str(self.path))
        print(">> Set name: " + str(self.set_name))

        spt = self.path
        sdm = self.delimiter
        path_save = "{}{}{}{}".format(spt, sdm, self.set_name, extension)
        print(">> Save as: " + path_save)
        cv2.imwrite(path_save, image)

        print(">> Complete save")
        if end_process is not None:
            cv2.destroyAllWindows
            print(">> Close all windows")
        print("")
        return self.path, self.set_name, extension


def main():
    host = platform.uname()[1]
    if "HBAMB" in host:
        name = "TestOutWinMuRata"
        path_master = "C:\\Temp"
        text = "test from muRata PC"

    elif host == "ProSalad13.local":
        name = "TestOutMac"
        path_master = "/Users/wacky515/OneDrive/Biz/Python/SaveData/TestOut"
        text = "test from MacPro"

    elif host == "cad0021":
        name = "TestOutWin"
        path_master = "D:\\OneDrive\\Biz\\Python\\SaveData\\TestOut"
        text = "test from Z420"

    elif os.name != "nt":
        name = "TestOutOtherWinPC"
        path_master = os.path.join("%USERPROFILE%", "/Python/ImageProcessing")
        text = "test from other Windows PC"

    elif os.name == "nt":
        name = "TestOutOtherUnixPC"
        path_master = "~/Python/SaveData/TestOut"
        text = "test from other Unix PC"

    test_save = SaveData(name, path_master)
    test_save.save_text(text)
    test_save.save_text(text, numbering=True)
    test_save.save_image("test", ".png")


if __name__ == "__main__":
    main()

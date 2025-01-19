import os
import tkinter as tk
import tkinter.filedialog
import deekseek
from datetime import datetime
import time
from tabulate import tabulate


# tk选择文件夹
def choose_path():
    root = tk.Tk()
    root.withdraw()
    try:
        path_out = tk.filedialog.askdirectory(title="选择文件夹", initialdir=os.getcwd())
        if not path_out:  # 处理用户取消选择的情况
            print("文件夹为空")
            input("按任意键退出")
            time.sleep(2)
            exit()
        else:
            file_list = []
            for root_dir, dirs, files in os.walk(path_out):
                for file_index in files:
                    # 判断是否为视频格式的文件
                    if file_index.endswith(
                            (".mp4", ".mkv", ".avi", ".rmvb", ".rm", ".flv", ".mov", ".wmv", ".asf", ".mpeg",
                             ".mpg", ".vob", ".m4v", ".3gp", ".3g2", ".ts", ".m2ts", ".mts", ".webm",
                             ".ogv",)):
                        file_list.append([file_index, os.path.join(root_dir, file_index)])
            if len(file_list) == 0:
                print("文件夹中没有视频文件")
                input("按任意键退出")
                time.sleep(2)
                exit()
            return file_list
    except Exception as e:
        print(e)
    finally:
        root.destroy()  # 确保Tkinter主窗口被销毁


def print_welcome():
    """
    初始提示词
     "1.你是一个以imdb为数据基础的影视命名专家，名称搜刮专家，"
     "2.我会输入一个格式为[文件名称, 文件绝对路径]的list，你回复我:文件名->新的命名，我要根据你的回答处理 所以一定要按照格式回复，不要说废话"
     "3.记住：格式举例 我发给你文件名称：A，文件绝对路径：B,参考名称：C，如果新的命名是D，你回复我:A->D ，如果原本的名称符合命名规范，你直接回复我：A->A"
     "4.我发给你的文件名称和文件绝对路径可能是错误的，你需要推断最有可能的真实存在的影视名称"
     "5.名称中要包含影视名称和上映年份，并且要符合IMDb标准的命名规范，校对影视的名称和年份，确保文件名包含影视名称和上映年份与实际一致"
     "6.将文件夹中的影视文件重命名为符合IMDb标准的格式，确保文件名包含影视名称和上映年份，如果电影名中包含特殊字符或空格，请保留它们，但确保文件名符合IMDb规范"
     "7.命名需要补充，有可能文件名称或者文件路径为了避免被和谐改为了相近的词汇或者名称缩写，你需要推断最有可能的真实存在的影视名称"
     "8.保留文件的原始扩展名，例如 .mp4, .mkv, .avi 等"
     "9.保留视频画质信息：如分辨率（1080p、4K）、编码格式（H.264、H.265）、帧率（60fps）、色彩空间（HDR、SDR）等。"
     "10.如果文件名中包含多语言音频或字幕信息，请保留相关描述，如果文件名中包含HDR、Dolby Vision等画质增强信息，请保留"
     "11.我会连续输入文件名称和文件绝对路径，你需要根据你的回答处理 所以一定要按照格式回复，不要说废话，同一文件夹中的文件格式保持一致"
    """
    print(f"*" * 100)
    writer = "Cat Tree"
    # 打印欢迎信息
    print("欢迎使用DeepSeek AI视频命名工具")
    print(f"作者：{writer}")
    print(f"软件版本：2.0.0")
    print(f"软件发布日期{datetime.now()}")
    # 打印软件使用说明
    print("软件使用说明：")
    print("1. 请选择一个文件夹")
    print("2. 软件会将文件夹中的所有文件发送给大模型")
    print("3. 大模型会返回一个新的文件名")
    print("4. 软件会将新的文件名重命名为原文件名")
    print("5. 软件会将文件夹中的所有文件重命名为新的文件名")
    print(f"*" * 100)


def read_prompt():
    with open("./prompt.md", "r", encoding="utf-8") as f:
        md_prompt = f.read()
    return md_prompt


def rename_file(ne_name_list):
    for jueduilujing, wenjian, new_name in ne_name_list:
        try:
            os.rename(jueduilujing, os.path.join(os.path.dirname(jueduilujing), new_name))
            print(f"重命名文件：{jueduilujing} -> {new_name}")
            time.sleep(0.1)
        except Exception as e:
            print(f"重命名失败：{e}")
    print(f"重命名文件夹完成")


# 调用大模型便利文件
def big_model_rename(systemPrompt, all_movie_file, this_maby_name):
    print(f"一共有{len(all_file)}个文件需要重命名")
    big_model_return_new_name_list = []
    new_name_list_head = ["文件路径", "文件名称", "新的命名"]
    cover_history = [{'role': 'system', 'content': systemPrompt}]
    index = 0
    for file, file_path in all_movie_file:
        index += 1
        # 输出对齐
        print(f"*" * 25 + f"一共有{len(all_file)}个文件需要重命名，这是第{index}个文件" + f"*" * 25)
        print(f"文件路径：{file_path}")
        print(f"文件名称：{file}")
        user_prompt = f"文件名称：{file}，文件绝对路径：{file_path},参考名称：{this_maby_name}"
        response, cover_history = deekseek.big_model_continue(user_prompt, cover_history)
        print(f"大模型输出：{response.split("->")[1]}")
        big_rename = response.split("->")[1]
        big_model_return_new_name_list.append([file_path, file, big_rename])
        time.sleep(0.01)
    print(
        tabulate(big_model_return_new_name_list, headers=new_name_list_head, tablefmt="grid", stralign="center",
                 numalign="center"))
    return big_model_return_new_name_list


if __name__ == '__main__':
    system_prompt = read_prompt()
    print_welcome()
    all_file = choose_path()
    maby_name = input("请输入参考名称：")
    new_name_list = big_model_rename(system_prompt, all_file, maby_name)
    print(f"*" * 100)
    print(f"检查文件是否重命名是否正确？")
    is_rename = input("是否重命名文件夹？y/n")
    if is_rename.upper() == "Y":
        rename_file(new_name_list)
    else:
        print(f"*" * 100)
        print(f"文件重命名未完成-未执行重命名")
        print(f"*" * 100)

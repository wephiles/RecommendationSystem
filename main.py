# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

from operator import itemgetter

def main():
    # 在下面的代码行中使用断点来调试脚本。
    # with open("./data/file_name/a1.txt", "r", encoding="utf-8") as f:
    #     for line in f:
    #         print(line)
    info = {
        "k1": [1, 2, 3],
        "k2": [11, 22, 22],
        "k3": [111, 222, 333]
    }
    data = sorted(info["k1"], key=itemgetter(1))
    print(data)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助

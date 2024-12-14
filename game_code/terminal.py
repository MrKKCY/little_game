import time


def debug_out(message, dbg_mod):   # debug输出函数
    if dbg_mod:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"[DEBUG]{now_time}>>{message}")

def read_tutorial():
    """
    读取游戏教程的函数。
    这里可以添加游戏的教程内容，例如游戏规则、玩法介绍等。
    """
    list = [
        "欢迎来到游戏！", 
        "这是一个简单的文本冒险游戏。",
        "你需要通过选择不同的选项来前进。",
        "在游戏中你将随机遇到各种事件和怪物",
        "你可以选择战斗、逃跑",
        "你也可以在路途中中使用物品来提升自己的能力或者恢复生命值。",
        "你需要合理的选择来继续生存下去。",
        "祝你好运！ --开发者:Mr.KKCY"
        ]
    for i in range(len(list)):
        print(list[i])
        time.sleep(0.5)

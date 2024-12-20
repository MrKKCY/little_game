import time
import random
import terminal
from entity import Player, Zombie, Merchant # type: ignore
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    Debug_mod = config["debug"]
    read_tutorial_mod = config["read_tutorial"]
    language = config["language"]
    MerchantRefreshRound = config["MerchantRefreshRound"]

with open(f"lang/{language}.json", "r", encoding="utf-8") as lang_file:
    lang = json.load(lang_file)

def normal(msg) -> str:  # 普通文本调用函数
    return lang["normal"][msg]
def debug(msg) -> str:  # 调试文本调用函数
    message = lang["debug"][msg]

    return f"{message}"

def creat_player():  # 创建玩家
    def set_name():  # 创建名称函数
        name = input(normal("set_name"))
        terminal.debug_out(debug("player_name").format(name=name), Debug_mod)
        return name

    def set_dif() -> tuple[int, int]:  # 设置难度函数
        dif = {
            1: [50, 20],
            2: [35, 15],
            3: [25, 10],
            4: [10, 5],
            5: [5, 1]
        }
        dif_list = normal("dif_list")
        print(normal("dif_level"))
        time.sleep(0.2)
        for i in range(len(dif_list)):  # 循环遍历输出难度介绍列表
            print(dif_list[i])
            time.sleep(0.2)

        while True:
            try:
                # 使用int转换输入为整数，并验证范围，避免使用eval的安全风险
                difficulty = int(input(normal("set_dif").format(len_dif=len(dif_list))))
                if 1 <= difficulty <= 5:
                    break
                else:
                    print(normal("error_101"))
            except ValueError:
                print(normal("error"))

        terminal.debug_out(f"设置难度:{difficulty}", Debug_mod)
        return dif[difficulty]

    name = set_name()  # 调用设置玩家游戏角色函数
    diff = set_dif()  # 调用难度设置函数
    hp = diff[0]  # 索引返回难度设置的血量
    terminal.debug_out(f"初始血量:{hp}", Debug_mod)
    atk = diff[1]  # 索引返回难度设置的攻击力
    terminal.debug_out(f"初始攻击力:{atk}", Debug_mod)

    return Player(name, hp, atk)  # 传参基础数据并创建玩家对象


def random_events(player, round_num):  # 根据概率给行动分配随机事件
    def encounter_zombie():  # 随机丧尸函数
        zombies={
            1:["普通丧尸","漫无目游荡的",[20,5,(3,15)]],
            2:["半身丧尸","正在爬行的",[15,3,(0,10)]],
            3:["变异犬","凶猛的",[25,10,(0,5)]],
            4:["肥胖丧尸","健硕的",[50,15,(5,30)]],
        }
        num = random.randint(1, len(zombies))
        print(f"遇到了一只{(zombies[num])[1]}{(zombies[num])[0]}")
        fight = input("你希望和他战斗吗?[Y/N]:")
        if fight == "Y":
            print("你选择了战斗...")
            time.sleep(1)
            zombie = Zombie((zombies[num])[0],((zombies[num])[2])[0],((zombies[num])[2])[1],((zombies[num])[2])[2])
            player.fight(zombie)
        else:
            print("你选择了逃跑...")
            time.sleep(1)
            
    class TreasureBox:  # 宝箱类,用于生成随机事件
        def __init__(self):
            self.items = {
                "cola":0.35, 
                "cookie":0.15, 
                "noting":0.5
                }

        def open(self):
            return random.random()

    def open_treasure_box(player):  # 打开物资箱函数
        treasure_box = TreasureBox()
        item = treasure_box.open()
        
        if item < treasure_box.items["cola"]:
            print("物资箱打开了...")
            print("恭喜你获得了一个神奇的可乐！")
            player.prop["cola"][0] += 1
            player.get_prop("cola")  # 调用玩家获取道具函数
        elif item < treasure_box.items["cola"] + treasure_box.items["cookie"]:
            print("物资箱打开了...")
            print("恭喜你获得了一个饼干！")
            player.prop["cookie"][0] += 1
            player.get_prop("cookie")  
        else:
            print("物资箱打开了...")
            print("很遗憾，物资箱是空的。")

    event_probability = {
        "encounter_zombie": 0.30,
        "Nothing": 0.48,
        "encounter_chest": 0.17,
        "merchant": 0.05
    }
    random_number = random.random()
    cumulative_probability = 0
    for event, probability in event_probability.items():  # 索引查看时间和概率
        cumulative_probability += probability  # 累计概率
        if random_number < cumulative_probability:  # 当随机数小于累计概率时
            if event == "encounter_zombie":
                encounter_zombie()
            elif event == "Nothing":
                print("无事发生呢..\n继续向前走...")
                time.sleep(1)
            elif event == "encounter_chest":
                print("发现了一个神秘的物资箱！")
                open_treasure_box(player)
                time.sleep(1)
            elif event == "merchant" and round_num > MerchantRefreshRound:  # 商人的刷新回合
                print("遇到了一个商人...")
                merchant = Merchant()
                merchant.trade(player)
            break



def main():  #主函数
    round_num = 0
    terminal.debug_out(debug("start"), Debug_mod)
    print(normal("welcome"))
    time.sleep(1)
    if read_tutorial_mod:
        try:
            read_tutorial = input(normal("read_tutorial"))
            int(read_tutorial)
            if read_tutorial == 1:
                terminal.read_tutorial()
            elif read_tutorial == 2:
                print(normal("start"))
                time.sleep(1)
        except ValueError:
            print(normal("error"))
            
    player = creat_player()  # 创建玩家对象
    input(normal("enter_start"))
    time.sleep(1)
    while True:
        random_events(player, round_num)
        round_num += 1
        terminal.debug_out(f"第{round_num}回合", Debug_mod)
        if player.HP <= 0:
            print("游戏结束！")
            break
        try:
            command = input("请输入你的命令(1:查看属性):")
            player.command(command)
        except ValueError:
            print(normal("error"))


if __name__ == "__main__":  # 是否为主入口程序文件判定
    main()
import time
import random
import terminal
from entity import Player, Zombie, Merchant # type: ignore
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    Debug_mod = config["debug"]
    read_tutorial_mod = config["read_tutorial"]

def creat_player():  # 创建玩家
    """
    该函数用于创建玩家角色，包含获取玩家输入的角色名称以及选择游戏难度，
    根据选择的难度设置玩家的初始血量和攻击力，并最终返回一个Player类的实例。
    """
    def set_name():  # 创建名称函数
        name = input("请输入角色名称：")
        terminal.debug_out(f"角色名称:{name}", Debug_mod)
        return name

    def set_dif() -> tuple[int, int]:  # 设置难度函数
        dif_list = [
            "1.简单难度:血量50，攻击力15",
            "2.普通难度:血量35，攻击力10",
            "3.困难难度:血量25，攻击力5",
            "4.噩梦难度:血量10，攻击力5",
            "5.职高厕所难度:血量5，攻击力1"
        ]
        print("难度等级划分如下:")
        time.sleep(0.2)
        for i in range(len(dif_list)):  # 循环遍历输出难度介绍列表
            print(dif_list[i])
            time.sleep(0.2)

        while True:
            try:
                # 使用int转换输入为整数，并验证范围，避免使用eval的安全风险
                difficulty = int(input(f"请输入你选择的难度(1-{len(dif_list)}):"))
                if 1 <= difficulty <= 3:
                    break
                else:
                    print("你输入的数值不在有效范围内，请重新输入!")
            except ValueError:
                print("请输入有效的整数，请重新输入!")

        dif = {
            1: [50, 15],
            2: [35, 10],
            3: [25, 5],
            4: [10, 5],
            5: [5, 1]
        }
        terminal.debug_out(f"设置难度:{difficulty}", Debug_mod)
        return dif[difficulty]

    name = set_name()  # 调用设置玩家游戏角色函数
    diff = set_dif()  # 调用难度设置函数
    hp = diff[0]  # 索引返回难度设置的血量
    terminal.debug_out(f"初始血量:{hp}", Debug_mod)
    atk = diff[1]  # 索引返回难度设置的攻击力
    terminal.debug_out(f"初始攻击力:{atk}", Debug_mod)

    return Player(name, hp, atk)  # 传参基础数据并创建玩家对象


def random_events(player):  # 根据概率给行动分配随机事件
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
            player.HP += 20
            print(f"{player.name} 的生命值增加 20 点。")
        elif item < treasure_box.items["cola"] + treasure_box.items["cookie"]:
            print("物资箱打开了...")
            print("恭喜你获得了一个饼干！")
            player.Attack += 5
            print(f"{player.name} 的攻击力永久增加 5 点。")
        else:
            print("物资箱打开了...")
            print("很遗憾，物资箱是空的。")

    event_probability = {
        "encounter_zombie": 0.20,
        "Nothing": 0.48,
        "encounter_chest": 0.12,
        "merchant":0.20
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
            elif event == "merchant":
                print("遇到了一个商人...")
                merchant = Merchant()
                merchant.trade(player)
            break


def main():  #主函数
    round_num = 0
    terminal.debug_out("游戏启动...", Debug_mod)
    print("欢迎游玩由Mr.KKCY开发的文本冒险游戏!")
    time.sleep(1)
    if read_tutorial_mod:
        read_tutorial = input("是否阅读教程？[Y/N]:")
        if read_tutorial == "Y":
            terminal.read_tutorial()
        else:
            print("那就开始吧！")
            time.sleep(1)
    player = creat_player()  # 创建玩家对象
    input("按回车键开始冒险！")
    time.sleep(1)
    print("冒险开始啦！")
    time.sleep(2)
    while True:
        random_events(player)
        round_num += 1
        terminal.debug_out(f"第{round_num}回合", Debug_mod)
        if player.HP <= 0:
            print("游戏结束！")
            break
        try:
            command = input("请输入你的命令(1:查看属性):")
            player.command(command)
        except ValueError:
            print("输入错误，请重新输入！")


if __name__ == "__main__":  # 是否为主入口程序文件判定
    main()
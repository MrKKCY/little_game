import time
import terminal
import random
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    Debug_mod = config["debug"]

class Player(object):  # 玩家类，用于创建玩家对象
    def __init__(self, name, HP, Attack, money=0):  # init 初始化玩家信息函数
        self.name = name
        self.HP = HP
        self.Attack = Attack
        self.money = money
        self.prop = {  # 玩家道具
            "cola": [0, 20, "可乐"],
            "cookie": [0, 5, "饼干"],
        }

    def use_prop(self, prop):  # 使用道具函数
        if prop in self.prop:
            if self.prop[prop][0] > 0:
                if prop == "cola":
                    self.HP += self.prop[prop][1]  # 增加20点血量
                    self.prop[prop][0] -= 1
                    print("你使用了一瓶可乐，恢复了20点血量！")
                elif prop == "cookie":
                    self.Attack += self.prop[prop][1]  # 增加5点攻击力
                    self.prop[prop][0] -= 1
                    print("你使用了一瓶饼干，增加了5点攻击力！")
                print("剩余道具：")
                for prop, count in self.prop.items():
                    print(f"{self.prop[prop][2]}: {self.prop[prop][1]}")
            else:
                print("你没有这个道具了！")

    def get_prop(self,prop):
        use = input(f"你想要使用{prop}吗？[1/2]:")
        if use == "1":
            self.use_prop(prop)
        elif use == "2":
            print("你选择了不使用道具。")


    def talk(self, zombie, talks):  # 对话系统:支持导入字典进行对话
        """
        此处计划使用json存储对话来实现更丰富的对话功能，目前暂未完整实现，仅预留接口。
        """
        pass

    def attack(self, target):  # 攻击函数
        damage = 0
        if random.randint(0, 5) == 3:  # 随机选择攻击目标
            damage = 5//self.Attack  # 增加五分之一的伤害
            print("*你打出了暴击伤害！")
            time.sleep(0.5)
            speck_message = ["去死吧!","送你上路!","去你妈的!"]
            print(f"{self.name}:{speck_message[random.randint(0,len(speck_message)-1)]}")
        damage += self.Attack
        target.HP -= damage
        print(self.name + " 对 " + target.name + " 造成了 " + str(damage) + " 点伤害！")
        time.sleep(0.5)

    def fight(self, zombie):  # 战斗函数
        """
        实现玩家与丧尸的战斗逻辑，采用回合制战斗，直到一方血量小于等于0为止。
        战斗结束后，玩家的血量不会恢复，而是保持战斗结束时的状态。
        """

        def battleChoiceAndItemModule():  # 玩家选择行动函数
            
            def use_prop():
                print("你拥有的道具：")
                for prop, count in self.prop.items():
                    print(f"{prop[1][3]}: {prop[1]}")
                prop_to_use = input("请输入你想要使用的道具：")
                if prop_to_use == 1:
                    self.use_prop("cola")
                elif prop_to_use == 2:
                    self.use_prop("cookie")
                


            while True:
                choice = input("请选择你的行动：1.攻击 2.使用道具\n")
                if choice == "1":
                    break
                elif choice == "2":
                    use_prop()
                # elif choice == "3":
                #     print("*你选择了逃跑！")
                #     return "run"
                else:
                    print("无效的选择，请重新输入。")

        def player_attack():  # 玩家攻击函数
            self.attack(zombie)
            if zombie.HP <= 0:
                give_money = random.randint(zombie.money[0], zombie.money[1])
                print(self.name + " 胜利了！")
                print("恭喜你，击败了丧尸！")
                time.sleep(0.5)
                if self.money is not None:
                    self.money += give_money  # 玩家胜利后增加的金币
                    print("你从丧尸身上收集到了 " + str(give_money) + " 点金币")
                else:
                    print(f"{self.name}:可恶，这只丧尸怎么什么都没有!")
                time.sleep(0.5)
                print("剩余血量：" + str(self.HP) + " 点")
                return  # 结束游戏
            else:
                time.sleep(0.5)
                print("剩余血量：" + str(self.HP) + " 点")
        
        def zombie_attack():  # 丧尸攻击函数
            zombie.attack(self)
            if self.HP <= 0:
                print(zombie.name + " 胜利了！")
                time.sleep(0.5)
                print("很可惜，你被丧尸击败了！")
                return  # 结束游戏
            else:
                time.sleep(0.5)
                print("剩余血量：" + str(self.HP) + " 点")

        first_attack = random.choice([player_attack, zombie_attack])  # 随机先手

        start_message = f"{self.name} 先攻！" if first_attack == player_attack else "僵尸先攻！"
        print("战斗开始！")
        print(start_message)

        while self.HP > 0 and zombie.HP > 0:
            battleChoiceAndItemModule()  # 玩家选择行动
            if first_attack == player_attack:
                player_attack()
                if zombie.HP > 0:  # 确保丧尸还活着
                    zombie_attack()
            else:
                zombie_attack()
                if self.HP > 0:  # 确保玩家还活着
                    first_attack = player_attack
    
    def command(self, command=0):  # 命令函数
        """
        实现玩家的命令执行逻辑，目前只支持简单的移动命令。
        后续可以在此基础上添加更多命令，如攻击、使用物品等。
        """
        if command == "1":
            print(5*"="+"玩家属性"+5*"=")
            print(f"玩家名称: {self.name}")
            print(f"玩家血量: {self.HP}")
            print(f"玩家攻击力: {self.Attack}")
            print(f"玩家金币: {self.money}")
            print(15*"=")
            time.sleep(0.5)
        else:
            print("继续前进...")
            return 0

class Zombie(object):  # 丧尸类，用于创建丧尸对象
    def __init__(self, name, HP, Attack, money):  # init 初始化丧尸信息函数
        self.name = name
        self.HP = HP
        self.Attack = Attack
        self.money = money

    def attack(self, target):
        damage = 0
        if random.randint(0, 6) == 1:
            damage = 5//self.Attack  # 增加五分之一的伤害
            print("*丧尸打出了暴击伤害！")
            time.sleep(0.5)
            zombie = ['丧尸仰天尖啸，对你发起了攻击','丧尸怪笑着，对你发动了攻击']
            print(zombie[random.randint(0,len(zombie)-1)])
        damage = self.Attack
        target.HP -= damage
        print(self.name + " 对 " + target.name + " 造成了 " + str(damage) + " 点伤害！")
        time.sleep(0.5)

class Merchant(object):  # 商人类，用于创建商人对象
    def __init__(self):  # init 初始化商人信息函数
        self.name = "约翰·乔姆"
        self.meeting = False  # 商人是否与玩家相遇的标志
        self.HP = 5000  # 商人的血量

    def trade(self, player):
        if self.meeting == False:
            print(f"{self.name}:嘿！小子，没错就是你！过来！我是{self.name}，我是一名商人。")
            self.meeting = True
            time.sleep(1)
            terminal.debug_out(f"玩家与商人相遇,Meeting={self.meeting}", Debug_mod)
            print(f"{self.name}:你有点面生啊，我在废土这么久第一次见到你。")
            time.sleep(1)
            print(f"{self.name}:来看看有没有你需要的东西。")
        else:
            print(f"{self.name}:嘿！小子又是我，{self.name}。")
            time.sleep(1)
            print(f"{self.name}:我最近进了一些新货，你想要看看吗？")

        buy = input("你想要买什么？[Y/N]:")
        if buy == "Y":
            print(f"{player.name}:你都有些什么？")
            time.sleep(1)
            print
            time.sleep(1)
            commodity = {
                "cola": ["可乐", 35, 20],
                "cookie": ["饼干", 40, 5],
            }
            print(f"{self.name}:1.可乐 2.饼干")
            time.sleep(1)
            choice = input("请输入你的选择：")
            if choice == "1":
                if player.money >= commodity["cola"][1]:
                    print(f"{self.name}:{commodity['cola'][0]}的价格是{commodity['cola'][1]}金币")
                    time.sleep(1)
                    player.HP += commodity['cola'][2]  # 玩家血量增加
                    player.money -= commodity['cola'][1]
                    print(f"你购买了{commodity['cola'][0]}，现在你的血量是{player.HP}")
                    print(f"{self.name}:欢迎下次光临。")
                    return 0
                else:
                    print(f"{self.name}:滋滋滋，等够钱了再来买吧。")
                    if random.randint(0, 15) == 5 and player.name != "DHHL":
                        print(f"{self.name}:你让我想起了一个叫DHHL的家伙")
                    time.sleep(0.5)
                    print("*你灰溜溜的离开了")
                    return 0
            elif choice == "2":
                if player.money >= commodity["cookie"][1]:
                    print(f"{self.name}:{commodity['cookie'][0]}的价格是{commodity['cookie'][1]}金币")
                    time.sleep(1)
                    player.Attack += commodity['cookie'][2]  # 玩家攻击力增加
                    player.money -= commodity['cookie'][1]
                    print(f"你购买了{commodity['cookie'][0]}，现在你的攻击力是{player.Attack}")
                    print(f"{self.name}:欢迎下次光临。")
                    return 0
                else:
                    print(f"{self.name}:滋滋滋，等够钱了再来买吧。")
                    if random.randint(0, 15) == 5 and player.name != "DHHL":
                        print(f"{self.name}:你让我想起了一个叫DHHL的家伙")
                    time.sleep(0.5)
                    print("*你灰溜溜的离开了")
                    return 0
        else:
            print(f"{self.name}:好吧，下次再来吧。")
            return 0
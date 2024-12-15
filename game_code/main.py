import time
import random
import terminal

Debug_mod = False


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
        ]
        print("难度等级划分如下:")
        time.sleep(0.2)
        for i in range(len(dif_list)):  # 循环遍历输出难度介绍列表
            print(dif_list[i])
            time.sleep(0.2)

        while True:
            try:
                # 使用int转换输入为整数，并验证范围，避免使用eval的安全风险
                difficulty = int(input("请输入你选择的难度(1-3):"))
                if 1 <= difficulty <= 3:
                    break
                else:
                    print("你输入的数值不在有效范围内，请重新输入!")
            except ValueError:
                print("请输入有效的整数，请重新输入!")

        dif = {
            1: [50, 15],
            2: [35, 10],
            3: [25, 5]
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


class Player(object):  # 玩家类，用于创建玩家对象
    def __init__(self, name, HP, Attack, money=0):  # init 初始化玩家信息函数
        self.name = name
        self.HP = HP
        self.Attack = Attack
        self.money = money

    def talk(self, zombie, talks):  # 对话系统:支持导入字典进行对话
        """
        此处计划使用json存储对话来实现更丰富的对话功能，目前暂未完整实现，仅预留接口。
        """
        pass

    def attack(self, target):  
        damage = self.Attack  # 可以在这里添加更多计算伤害的逻辑，比如考虑暴击、属性克制等情况，目前先简单用攻击力作为伤害值
        target.HP -= damage
        print(self.name + " 对 " + target.name + " 造成了 " + str(damage) + " 点伤害！")
        time.sleep(0.5)

    def fight(self, zombie):  # 战斗函数
        """
        实现玩家与丧尸的战斗逻辑，采用回合制战斗，直到一方血量小于等于0为止。
        战斗结束后，玩家的血量不会恢复，而是保持战斗结束时的状态。
        """
        while self.HP > 0 and zombie.HP > 0:
            # 玩家回合逻辑
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
                break
            # 丧尸回合逻辑
            zombie.attack(self)
            if self.HP <= 0:
                print(zombie.name + " 胜利了！")
                time.sleep(0.5)
                print("很可惜，你被丧尸击败了！")
                break
    
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
        """
        丧尸攻击目标（比如玩家）的方法，目前简单地用丧尸的攻击力对目标造成伤害。
        后续可以在此基础上添加更多复杂逻辑，如暴击、特殊效果等。
        """
        damage = self.Attack
        target.HP -= damage
        print(self.name + " 对 " + target.name + " 造成了 " + str(damage) + " 点伤害！")
        time.sleep(0.5)

class Merchant(object):  # 商人类，用于创建商人对象
    def __init__(self):  # init 初始化商人信息函数
        self.name = "约翰·乔姆"
        self.meeting = False  # 商人是否与玩家相遇的标志

    def trade(self, player):
        if self.meeting is False:
            print(f"{self.name}:嘿！小子，没错就是你！过来！我是{self.name}，我是一名商人。")
            self.meeting = True
            time.sleep(1)
            terminal.debug_out(f"玩家与商人相遇", Debug_mod)
            print(f"{self.name}:你有点面生啊，我在废土这么久第一次见到你。")
            time.sleep(1)
            print(f"{self.name}:来看看有没有你需要的东西。")
        else:
            print(f"{self.name}:嘿！小子又是我，{self.name}。")
            time.sleep(1)
            print(f"{self.name}:我最近进了一些新货，你想要看看吗？")

        buy = input("你想要买什么？[Y/N]:")
        if buy == "Y":
            print(f"{self.name}:你想要买什么？")
            time.sleep(1)
            print(f"{self.name}:1.可乐 2.饼干")
            commodity = {
                "cola": ["可乐", 35, 20],
                "cookie": ["饼干", 40, 5],
            }
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
                    print(f"{self.name}:你的钱不够，等够钱了再来买吧。")
                    return 0
            elif choice == "2":
                if player.money >= commodity["cookie"][1]:
                    print(f"{self.name}:{commodity['cookie'][0]}的价格是{commodity['cookie'][1]}金币")
                    time.sleep(1)
                    player.Attack += commodity['cookie'][2]  # 玩家攻击力增加
                    player.money -= commodity['cookie'][1]
                    print(f"你购买了{commodity['cookie'][0]}，现在你的攻击力是{player.Attack}")
                    print(f"{selfe.name}:欢迎下次光临。")
                    return 0
                else:
                    print(f"{self.name}:你的钱不够，等够钱了再来买吧。")
                    return 0
        else:
            print(f"{self.name}:好吧，下次再来吧。")
            return 0


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
        cumulative_probability += probability
        if random_number < cumulative_probability:
            if event == "encounter_zombie":
                encounter_zombie()
            elif event == "Nothing":
                print("无事发生呢..\n继续向前走...")
                time.sleep(4)
            elif event == "encounter_chest":
                print("发现了一个神秘的物资箱！")
                open_treasure_box(player)
                time.sleep(2)
            elif event == "merchant":
                print("遇到了一个商人...")
                merchant = Merchant()
                merchant.trade(player)
            break


def main():  #主函数
    terminal.debug_out("游戏启动...", Debug_mod)
    print("欢迎游玩由Mr.KKCY开发的文本冒险游戏!")
    time.sleep(1)
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
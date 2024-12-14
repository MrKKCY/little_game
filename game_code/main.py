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
    def __init__(self, name, HP, Attack, Experience=0):  # init 初始化玩家信息函数
        self.name = name
        self.HP = HP
        self.Attack = Attack
        self.Experience = Experience

    def talk(self, Monster, talks):  # 对话系统:支持导入字典进行对话
        """
        此处计划使用json存储对话来实现更丰富的对话功能，目前暂未完整实现，仅预留接口。
        """
        pass

    def attack(self, target):  
        damage = self.Attack  # 可以在这里添加更多计算伤害的逻辑，比如考虑暴击、属性克制等情况，目前先简单用攻击力作为伤害值
        target.HP -= damage
        print(self.name + " 对 " + target.name + " 造成了 " + str(damage) + " 点伤害！")
        time.sleep(0.5)

    def fight(self, monster):  # 战斗函数
        """
        实现玩家与怪物的战斗逻辑，采用回合制战斗，直到一方血量小于等于0为止。
        战斗结束后，玩家的血量不会恢复，而是保持战斗结束时的状态。
        """
        while self.HP > 0 and monster.HP > 0:
            # 玩家回合逻辑
            self.attack(monster)
            if monster.HP <= 0:
                print(self.name + " 胜利了！")
                self.Experience += monster.Experience  # 玩家胜利后增加经验值
                print("恭喜你，击败了怪物！")
                time.sleep(0.5)
                print("你获取了 " + str(monster.Experience) + " 点经验值！")
                time.sleep(0.5)
                print("剩余血量：" + str(self.HP) + " 点")
                break
            # 怪物回合逻辑
            monster.attack(self)
            if self.HP <= 0:
                print(monster.name + " 胜利了！")
                time.sleep(0.5)
                print(f"{monster.name}:你真弱啊,桀桀桀!")
                time.sleep(0.5)
                print("很可惜，你被怪物击败了！")
                break


class Monster(object):  # 怪物类，用于创建怪物对象
    def __init__(self, name, HP, Attack, Experience):  # init 初始化怪物信息函数
        self.name = name
        self.HP = HP
        self.Attack = Attack
        self.Experience = Experience

    def attack(self, target):
        """
        怪物攻击目标（比如玩家）的方法，目前简单地用怪物的攻击力对目标造成伤害。
        后续可以在此基础上添加更多复杂逻辑，如暴击、特殊效果等。
        """
        damage = self.Attack
        target.HP -= damage
        print(self.name + " 对 " + target.name + " 造成了 " + str(damage) + " 点伤害！")
        time.sleep(0.5)


def random_events(player):  # 根据概率给行动分配随机事件
    def encounter_monster():  # 随机怪物函数
        monsters={
            1:["哥布林","可恶的",[20,5,10]],
            2:["史莱姆","黏糊糊的",[15,3,5]],
            3:["狼","凶猛的",[25,10,15]],
            4:["强壮哥布林","可怕的",[25,10,15]],
        }
        num = random.randint(1, len(monsters))
        print(f"遇到了一只{(monsters[num])[1]}{(monsters[num])[0]}")
        fight = input("你想和他战斗吗?[Y/N]:")
        if fight == "Y":
            print("你选择了战斗...")
            time.sleep(1)
            monster = Monster((monsters[num])[0],((monsters[num])[2])[0],((monsters[num])[2])[1],((monsters[num])[2])[2])
            player.fight(monster)
        else:
            print("你选择了逃跑...")
            time.sleep(1)
            

    
    class TreasureBox:  # 宝箱类,用于生成随机事件
        def __init__(self):
            self.items = {
                "health_potion":0.35, 
                "damage_potion":0.15, 
                "noting":0.5
                }

        def open(self):
            return random.random()

    def open_treasure_box(player):  # 打开宝箱函数
        treasure_box = TreasureBox()
        item = treasure_box.open()
        
        if item < treasure_box.items["health_potion"]:
            print("宝箱打开了...")
            print("恭喜你获得了一个恢复药瓶！")
            player.HP += 20
            print(f"{player.name} 的生命值增加 20 点。")
        elif item < treasure_box.items["health_potion"] + treasure_box.items["damage_potion"]:
            print("宝箱打开了...")
            print("恭喜你获得了一个攻击力药水！")
            player.Attack += 5
            print(f"{player.name} 的攻击力永久增加 5 点。")
        else:
            print("宝箱打开了...")
            print("很遗憾，宝箱是空的。")

    event_probability = {
        "encounter_monster": 0.3,
        "Nothing": 0.5,
        "encounter_chest": 0.2
    }
    random_number = random.random()
    cumulative_probability = 0
    for event, probability in event_probability.items():  # 索引查看时间和概率
        cumulative_probability += probability
        if random_number < cumulative_probability:
            if event == "encounter_monster":
                encounter_monster()
            elif event == "Nothing":
                print("无事发生呢..\n继续向前走...")
                time.sleep(4)
            elif event == "encounter_chest":
                print("发现了一个神秘的宝箱！")
                open_treasure_box(player)
                time.sleep(2)
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
        input("按回车键继续前进...")


if __name__ == "__main__":  # 是否为主入口程序文件判定
    main()
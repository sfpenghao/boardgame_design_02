import random
import copy
from collections import Counter

# ===========================================
# 游戏数值配置 - 可修改这些数值来调整游戏平衡
# ===========================================

# 玩家属性
PLAYER_MAX_HP = 40                    # 玩家最大生命值
PLAYER_LOW_HP_THRESHOLD = 10          # 玩家低血量阈值（优先防御）

# 怪物属性
MONSTER_HP = 13                       # 怪物生命值
MONSTER_ACTION_COUNT = 3              # 怪物行动种类数量
MONSTER_LIGHT_ATTACK_DAMAGE = 3       # 怪物轻攻击伤害
MONSTER_HEAVY_ATTACK_DAMAGE = 7       # 怪物重攻击伤害
MONSTER_POWER_GAIN = 1                # 怪物每次获得的气力值

# 卡牌数量
CARD_A_COUNT = 3                      # A牌数量
CARD_B_COUNT = 3                      # B牌数量
CARD_D_COUNT = 2                      # D牌数量
CARD_E_COUNT = 2                      # E牌数量

# 卡牌效果
CARD_AB_DAMAGE = 3                    # A、B牌的伤害值
CARD_AB_ARMOR = 2                     # A、B牌的化劲值
CARD_D_DAMAGE = 1                     # D牌的伤害值
CARD_D_STUN_CHANCE = 1/3              # D牌的击晕概率
CARD_E_ARMOR = 4                      # E牌的化劲值

# 游戏机制
CARDS_DRAW_PER_TURN = 5               # 每回合抽牌数
MAX_CARDS_PLAY_PER_TURN = 3           # 每回合最多打牌数

# 特殊组合伤害
AAB_COMBO_BONUS_DAMAGE = 5            # AAB组合额外伤害
AAD_COMBO_BONUS_DAMAGE = 3            # AAD组合额外伤害

# 模拟参数
DEFAULT_SIMULATION_BATTLES = 10000    # 默认模拟战斗场数
PROGRESS_REPORT_INTERVAL = 1000       # 进度报告间隔

# ===========================================

class Card:
    """卡牌类"""
    def __init__(self, name, damage=0, armor=0, stun_chance=0):
        self.name = name
        self.damage = damage
        self.armor = armor
        self.stun_chance = stun_chance

class Player:
    """玩家类"""
    def __init__(self):
        self.max_hp = PLAYER_MAX_HP
        self.hp = PLAYER_MAX_HP
        self.armor = 0
        self.deck = self._create_deck()
        self.hand = []
        self.discard_pile = []
    
    def _create_deck(self):
        """创建初始牌库"""
        deck = []
        # A牌
        for _ in range(CARD_A_COUNT):
            deck.append(Card('A', damage=CARD_AB_DAMAGE, armor=CARD_AB_ARMOR))
        
        # B牌
        for _ in range(CARD_B_COUNT):
            deck.append(Card('B', damage=CARD_AB_DAMAGE, armor=CARD_AB_ARMOR))
        
        # D牌若干张，造成指定伤害，指定概率击晕
        for _ in range(CARD_D_COUNT):
            deck.append(Card('D', damage=CARD_D_DAMAGE, stun_chance=CARD_D_STUN_CHANCE))
        
        # E牌若干张，获得指定化劲
        for _ in range(CARD_E_COUNT):
            deck.append(Card('E', armor=CARD_E_ARMOR))
        
        random.shuffle(deck)
        return deck
    
    def draw_cards(self, num=CARDS_DRAW_PER_TURN):
        """抽牌"""
        for _ in range(num):
            if not self.deck:
                # 牌库空了，洗弃牌堆
                if self.discard_pile:
                    self.deck = self.discard_pile[:]
                    self.discard_pile = []
                    random.shuffle(self.deck)
                else:
                    break
            
            if self.deck:
                self.hand.append(self.deck.pop())
    
    def discard_hand(self):
        """弃掉手牌"""
        self.discard_pile.extend(self.hand)
        self.hand = []
    
    def take_damage(self, damage):
        """受到伤害"""
        actual_damage = max(0, damage - self.armor)
        self.hp -= actual_damage
        self.armor = 0  # 化劲在受到伤害后清零
        return actual_damage
    
    def choose_cards_to_play(self):
        """选择要打出的牌（AI策略）"""
        if not self.hand:
            return []
        
        # 按优先级排序手牌
        hand_names = [card.name for card in self.hand]
        hand_counter = Counter(hand_names)
        
        # 检查是否能打出特殊组合
        cards_to_play = []
        
        # 优先考虑AAB组合（额外伤害）
        if hand_counter['A'] >= 2 and hand_counter['B'] >= 1:
            a_count = 0
            b_count = 0
            for card in self.hand:
                if card.name == 'A' and a_count < 2:
                    cards_to_play.append(card)
                    a_count += 1
                elif card.name == 'B' and b_count < 1:
                    cards_to_play.append(card)
                    b_count += 1
                if len(cards_to_play) == MAX_CARDS_PLAY_PER_TURN:
                    break
        
        # 其次考虑AAD组合（额外伤害）
        elif hand_counter['A'] >= 2 and hand_counter['D'] >= 1:
            a_count = 0
            d_count = 0
            for card in self.hand:
                if card.name == 'A' and a_count < 2:
                    cards_to_play.append(card)
                    a_count += 1
                elif card.name == 'D' and d_count < 1:
                    cards_to_play.append(card)
                    d_count += 1
                if len(cards_to_play) == MAX_CARDS_PLAY_PER_TURN:
                    break
        
        # 如果没有特殊组合，按优先级选牌
        else:
            # 优先级：攻击牌 > 击晕牌 > 防御牌
            priority_order = ['A', 'B', 'D', 'E']
            available_cards = self.hand[:]
            
            for priority_name in priority_order:
                for card in available_cards:
                    if card.name == priority_name and len(cards_to_play) < MAX_CARDS_PLAY_PER_TURN:
                        cards_to_play.append(card)
                        available_cards.remove(card)
                        break
        
        return cards_to_play[:MAX_CARDS_PLAY_PER_TURN]  # 最多指定张牌

class Monster:
    """怪物类"""
    def __init__(self):
        self.hp = MONSTER_HP
        self.power = 0  # 气力
        self.action_cycle = 0  # 行动循环计数
        self.stunned = False  # 是否被击晕
    
    def get_next_action(self):
        """获取下一个行动"""
        if self.stunned:
            return None
        
        action = self.action_cycle % MONSTER_ACTION_COUNT
        self.action_cycle += 1
        return action
    
    def execute_action(self, action, player):
        """执行行动"""
        if action is None:  # 被击晕
            return f"怪物被击晕，无法行动"
        
        if action == 0:  # 造成轻攻击伤害
            damage = MONSTER_LIGHT_ATTACK_DAMAGE + self.power
            actual_damage = player.take_damage(damage)
            return f"怪物攻击造成{actual_damage}点伤害"
        elif action == 1:  # 造成重攻击伤害
            damage = MONSTER_HEAVY_ATTACK_DAMAGE + self.power
            actual_damage = player.take_damage(damage)
            return f"怪物重击造成{actual_damage}点伤害"
        elif action == 2:  # 增加气力
            self.power += MONSTER_POWER_GAIN
            return f"怪物获得{MONSTER_POWER_GAIN}点气力，当前气力：{self.power}"
    
    def take_damage(self, damage):
        """受到伤害"""
        self.hp -= damage
        return damage
    
    def clear_stun(self):
        """清除眩晕状态"""
        self.stunned = False

def simulate_battle():
    """模拟一场战斗"""
    player = Player()
    monster = Monster()
    turn = 0
    
    while player.hp > 0 and monster.hp > 0:
        turn += 1
        
        # 回合开始，清除怪物眩晕状态
        monster.clear_stun()
        
        # 玩家回合
        player.draw_cards(CARDS_DRAW_PER_TURN)
        cards_to_play = player.choose_cards_to_play()
        
        # 计算伤害和效果
        total_damage = 0
        total_armor = 0
        stun_applied = False
        
        # 检查特殊组合
        card_names = [card.name for card in cards_to_play]
        if card_names == ['A', 'A', 'B']:
            total_damage += AAB_COMBO_BONUS_DAMAGE  # AAB组合额外伤害
        elif card_names == ['A', 'A', 'D']:
            total_damage += AAD_COMBO_BONUS_DAMAGE  # AAD组合额外伤害
        
        # 执行卡牌效果
        for card in cards_to_play:
            if card.name in ['A', 'B']:
                # 优先造成伤害，除非玩家血量很低
                if player.hp <= PLAYER_LOW_HP_THRESHOLD:
                    total_armor += card.armor
                else:
                    total_damage += card.damage
            elif card.name == 'D':
                total_damage += card.damage
                if random.random() < card.stun_chance:
                    monster.stunned = True
                    stun_applied = True
            elif card.name == 'E':
                total_armor += card.armor
        
        # 从手牌中移除打出的牌
        player.discard_pile.extend(cards_to_play)
        # for card in cards_to_play:
        #     if card in player.hand:
        #         player.hand.remove(card)
        
        # 应用效果
        player.armor += total_armor
        if total_damage > 0:
            monster.take_damage(total_damage)
        
        # 弃掉所有手牌
        player.discard_hand()
        
        # 检查怪物是否死亡
        if monster.hp <= 0:
            break
        
        # 怪物回合
        action = monster.get_next_action()
        monster.execute_action(action, player)
        
        # 检查玩家是否死亡
        if player.hp <= 0:
            break
    
    return turn, player.hp, player.hp > 0

def run_simulation(num_battles=DEFAULT_SIMULATION_BATTLES):
    """运行多次战斗模拟"""
    results = []
    wins = 0
    
    print(f"开始模拟 {num_battles} 场战斗...")
    
    for i in range(num_battles):
        if (i + 1) % PROGRESS_REPORT_INTERVAL == 0:
            print(f"已完成 {i + 1} 场战斗...")
        
        turns, remaining_hp, won = simulate_battle()
        if won:
            results.append((turns, remaining_hp))
            wins += 1
    
    if not results:
        print("所有战斗都失败了！")
        return
    
    # 统计结果
    turns_data = [result[0] for result in results]
    hp_data = [result[1] for result in results]
    
    print(f"\n=== 战斗模拟结果 ===")
    print(f"总战斗次数: {num_battles}")
    print(f"胜利次数: {wins}")
    print(f"胜率: {wins/num_battles*100:.2f}%")
    print(f"\n--- 胜利战斗统计 ---")
    print(f"回合数统计:")
    print(f"  平均值: {sum(turns_data)/len(turns_data):.2f}")
    print(f"  最小值: {min(turns_data)}")
    print(f"  最大值: {max(turns_data)}")
    print(f"\n剩余血量统计:")
    print(f"  平均值: {sum(hp_data)/len(hp_data):.2f}")
    print(f"  最小值: {min(hp_data)}")
    print(f"  最大值: {max(hp_data)}")

if __name__ == "__main__":
    run_simulation(DEFAULT_SIMULATION_BATTLES) 
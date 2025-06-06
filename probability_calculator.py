import random
import itertools
from collections import Counter
from math import comb
import numpy as np

class ProbabilityCalculator:
    def __init__(self, element_counts=None):
        """
        初始化概率计算器
        element_counts: 字典，键为元素名，值为该元素的数量
        默认每种元素(A,B,C,D,E)各有2个，总共10个元素
        """
        if element_counts is None:
            self.element_counts = {'A': 2, 'B': 2, 'C': 2, 'D': 2, 'E': 2}
        else:
            self.element_counts = element_counts
            
        # 验证约束条件
        self._validate_constraints()
        
        # 创建完整的元素集合
        self.elements = []
        for element, count in self.element_counts.items():
            self.elements.extend([element] * count)
        
        print(f"集合配置: {self.element_counts}")
        print(f"总元素数量: {len(self.elements)}")
        print(f"完整集合: {self.elements}")
    
    def _validate_constraints(self):
        """验证约束条件"""
        # 检查每种元素数量是否大于等于2
        for element, count in self.element_counts.items():
            if count < 2:
                raise ValueError(f"元素 {element} 的数量 ({count}) 小于2")
        
        # 检查总数量是否大于等于10
        total = sum(self.element_counts.values())
        if total < 10:
            raise ValueError(f"总元素数量 ({total}) 小于10")
    
    def monte_carlo_simulation(self, target_combination, num_trials=100000):
        """
        使用蒙特卡罗模拟计算概率
        target_combination: 目标组合，如 "AAB"
        num_trials: 模拟次数
        """
        print(f"\n=== 蒙特卡罗模拟 ===")
        print(f"目标组合: {target_combination}")
        print(f"模拟次数: {num_trials}")
        
        # 将目标组合转换为计数字典
        target_count = Counter(target_combination)
        success_count = 0
        
        for _ in range(num_trials):
            # 随机抽取5个元素
            sample = random.sample(self.elements, 5)
            sample_count = Counter(sample)
            
            # 检查是否包含目标组合
            if self._contains_combination(sample_count, target_count):
                success_count += 1
        
        probability = success_count / num_trials
        print(f"成功次数: {success_count}")
        print(f"模拟概率: {probability:.6f} ({probability*100:.4f}%)")
        
        return probability
    
    def _contains_combination(self, sample_count, target_count):
        """检查样本是否包含目标组合"""
        for element, needed in target_count.items():
            if sample_count.get(element, 0) < needed:
                return False
        return True
    
    def mathematical_calculation(self, target_combination):
        """
        使用数学方法精确计算概率
        """
        print(f"\n=== 数学计算方法 ===")
        print(f"目标组合: {target_combination}")
        
        target_count = Counter(target_combination)
        total_elements = len(self.elements)
        
        # 计算总的可能抽取方式数
        total_ways = comb(total_elements, 5)
        
        # 计算包含目标组合的方式数
        success_ways = self._calculate_success_ways(target_count)
        
        probability = success_ways / total_ways
        
        print(f"总的抽取方式数: {total_ways}")
        print(f"包含目标组合的方式数: {success_ways}")
        print(f"精确概率: {probability:.6f} ({probability*100:.4f}%)")
        
        return probability
    
    def _calculate_success_ways(self, target_count):
        """计算包含目标组合的抽取方式数"""
        # 这里使用容斥原理来计算
        # 但对于复杂情况，我们使用枚举方法
        success_ways = 0
        
        # 生成所有可能的5元素组合
        all_combinations = list(itertools.combinations(range(len(self.elements)), 5))
        
        for combo in all_combinations:
            selected_elements = [self.elements[i] for i in combo]
            selected_count = Counter(selected_elements)
            
            if self._contains_combination(selected_count, target_count):
                success_ways += 1
        
        return success_ways
    
    def analyze_different_scenarios(self):
        """分析不同目标组合的概率"""
        print(f"\n=== 不同组合的概率分析 ===")
        
        test_combinations = [
            "AAB",  # 两个A，一个B
            "ABC",  # 各不相同
            "AAA",  # 三个相同
            "ABB",  # 一个A，两个B
            "ABA",  # 等价于AAB
        ]
        
        results = {}
        for combo in test_combinations:
            print(f"\n分析组合: {combo}")
            monte_carlo_prob = self.monte_carlo_simulation(combo, 50000)
            math_prob = self.mathematical_calculation(combo)
            results[combo] = {
                'monte_carlo': monte_carlo_prob,
                'mathematical': math_prob,
                'difference': abs(monte_carlo_prob - math_prob)
            }
            print(f"误差: {results[combo]['difference']:.6f}")
        
        return results

def main():
    print("=== 概率计算器 ===")
    
    # 示例1：默认配置（每种元素2个）
    print("\n【示例1：默认配置】")
    calc1 = ProbabilityCalculator()
    calc1.analyze_different_scenarios()
    
    # 示例2：自定义配置
    print("\n\n【示例2：自定义配置】")
    custom_counts = {'A': 3, 'B': 3, 'C': 2, 'D': 2, 'E': 2}  # 总共12个元素
    calc2 = ProbabilityCalculator(custom_counts)
    
    # 分析特定组合
    target = "AAB"
    print(f"\n分析目标组合: {target}")
    monte_carlo_result = calc2.monte_carlo_simulation(target)
    math_result = calc2.mathematical_calculation(target)
    
    # 示例3：用户交互
    print("\n\n【自定义分析】")
    try:
        # 让用户输入自定义组合
        user_combination = input("请输入要分析的组合（如AAB）: ").strip().upper()
        if user_combination and all(c in 'ABCDE' for c in user_combination):
            print(f"\n分析用户输入的组合: {user_combination}")
            calc1.monte_carlo_simulation(user_combination)
            calc1.mathematical_calculation(user_combination)
        else:
            print("输入无效，使用默认组合AAB进行演示")
            calc1.monte_carlo_simulation("AAB")
            calc1.mathematical_calculation("AAB")
    except:
        print("使用默认组合AAB进行演示")
        calc1.monte_carlo_simulation("AAB")
        calc1.mathematical_calculation("AAB")

if __name__ == "__main__":
    main() 
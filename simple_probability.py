import random
from collections import Counter
from math import comb

def calculate_probability(element_counts, target_combination, simulation_count=100000):
    """
    计算从集合中抽取5个元素包含指定组合的概率
    
    参数:
    element_counts: 字典，例如 {'A': 2, 'B': 2, 'C': 2, 'D': 2, 'E': 2}
    target_combination: 字符串，例如 "AAB"
    simulation_count: 模拟次数
    
    返回:
    概率值 (0-1之间的浮点数)
    """
    
    # 创建完整的元素列表
    elements = []
    for element, count in element_counts.items():
        elements.extend([element] * count)
    
    # 验证约束条件
    total_elements = len(elements)
    if total_elements < 10:
        print(f"警告：总元素数量 ({total_elements}) 小于10")
    
    for element, count in element_counts.items():
        if count < 2:
            print(f"警告：元素 {element} 的数量 ({count}) 小于2")
    
    # 转换目标组合为计数格式
    target_count = Counter(target_combination)
    
    print(f"集合配置: {element_counts}")
    print(f"总元素数量: {total_elements}")
    print(f"目标组合: {target_combination}")
    print(f"目标组合计数: {dict(target_count)}")
    
    # 蒙特卡罗模拟
    success_count = 0
    for _ in range(simulation_count):
        # 随机抽取5个元素
        sample = random.sample(elements, 5)
        sample_count = Counter(sample)
        
        # 检查是否包含目标组合
        contains_target = True
        for element, needed in target_count.items():
            if sample_count.get(element, 0) < needed:
                contains_target = False
                break
        
        if contains_target:
            success_count += 1
    
    probability = success_count / simulation_count
    
    print(f"\n模拟结果:")
    print(f"模拟次数: {simulation_count}")
    print(f"成功次数: {success_count}")
    print(f"概率: {probability:.6f}")
    print(f"百分比: {probability*100:.4f}%")
    
    return probability

def quick_test():
    """快速测试函数"""
    print("=== 快速概率计算测试 ===\n")
    
    # 测试案例1：默认配置，目标组合AAB
    print("【测试1：默认配置 + AAB组合】")
    default_counts = {'A': 2, 'B': 2, 'C': 2, 'D': 2, 'E': 2}
    prob1 = calculate_probability(default_counts, "AAB")
    
    print("\n" + "="*50 + "\n")
    
    # 测试案例2：增加A和B的数量，目标组合AAB
    print("【测试2：增强配置 + AAB组合】")
    enhanced_counts = {'A': 3, 'B': 3, 'C': 2, 'D': 2, 'E': 2}
    prob2 = calculate_probability(enhanced_counts, "AAB")
    
    print("\n" + "="*50 + "\n")
    
    # 测试案例3：默认配置，目标组合ABC
    print("【测试3：默认配置 + ABC组合】")
    prob3 = calculate_probability(default_counts, "ABC")
    
    print("\n" + "="*50 + "\n")
    
    # 概率比较
    print("【概率对比】")
    print(f"默认配置下AAB组合概率: {prob1:.6f} ({prob1*100:.4f}%)")
    print(f"增强配置下AAB组合概率: {prob2:.6f} ({prob2*100:.4f}%)")
    print(f"默认配置下ABC组合概率: {prob3:.6f} ({prob3*100:.4f}%)")
    
    if prob2 > prob1:
        increase = ((prob2 - prob1) / prob1) * 100
        print(f"增强A和B的数量后，AAB组合概率提升了 {increase:.2f}%")

def custom_calculation():
    """自定义计算"""
    print("\n=== 自定义概率计算 ===")
    
    try:
        # 获取用户输入
        print("请设置集合中各元素的数量（至少2个）:")
        counts = {}
        for element in ['A', 'B', 'C', 'D', 'E']:
            while True:
                try:
                    count = int(input(f"元素{element}的数量: "))
                    if count >= 2:
                        counts[element] = count
                        break
                    else:
                        print("数量必须大于等于2，请重新输入")
                except ValueError:
                    print("请输入有效的数字")
        
        target = input("请输入目标组合（如AAB）: ").strip().upper()
        
        if target and all(c in 'ABCDE' for c in target):
            calculate_probability(counts, target)
        else:
            print("输入的组合无效")
            
    except KeyboardInterrupt:
        print("\n用户取消输入")
    except Exception as e:
        print(f"输入错误: {e}")

if __name__ == "__main__":
    # 运行快速测试
    quick_test()
    
    # 可选：运行自定义计算
    print("\n" + "="*60)
    choice = input("\n是否要进行自定义计算？(y/n): ").strip().lower()
    if choice == 'y' or choice == 'yes':
        custom_calculation()
    
    print("\n计算完成！") 
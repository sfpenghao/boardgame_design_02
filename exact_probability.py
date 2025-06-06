from math import comb, factorial
from collections import Counter
import itertools

def exact_probability_calculation(element_counts, target_combination):
    """
    使用精确数学方法计算概率
    
    参数:
    element_counts: 字典，各元素的数量
    target_combination: 目标组合字符串
    
    返回:
    精确概率值
    """
    
    print(f"=== 精确概率计算 ===")
    print(f"集合配置: {element_counts}")
    print(f"目标组合: {target_combination}")
    
    # 创建完整元素列表
    elements = []
    for element, count in element_counts.items():
        elements.extend([element] * count)
    
    total_elements = len(elements)
    target_count = Counter(target_combination)
    
    print(f"总元素数量: {total_elements}")
    print(f"目标组合需求: {dict(target_count)}")
    
    # 计算总的可能抽取方式数
    total_ways = comb(total_elements, 5)
    
    # 计算满足条件的抽取方式数
    success_ways = 0
    
    # 生成所有可能的5元素组合的索引
    for combo_indices in itertools.combinations(range(total_elements), 5):
        selected_elements = [elements[i] for i in combo_indices]
        selected_count = Counter(selected_elements)
        
        # 检查是否包含目标组合
        contains_target = True
        for element, needed in target_count.items():
            if selected_count.get(element, 0) < needed:
                contains_target = False
                break
        
        if contains_target:
            success_ways += 1
    
    # 计算精确概率
    exact_probability = success_ways / total_ways
    
    print(f"\n计算结果:")
    print(f"总的抽取方式数: {total_ways}")
    print(f"满足条件的方式数: {success_ways}")
    print(f"精确概率: {exact_probability:.8f}")
    print(f"百分比: {exact_probability*100:.6f}%")
    
    return exact_probability

def hypergeometric_probability(element_counts, target_combination):
    """
    使用超几何分布计算概率（适用于某些特定情况）
    """
    print(f"\n=== 超几何分布方法 ===")
    
    total_elements = sum(element_counts.values())
    target_count = Counter(target_combination)
    
    print(f"使用超几何分布计算...")
    print(f"总元素: {total_elements}, 抽取: 5")
    
    # 对于复杂的多元素组合，超几何分布计算会很复杂
    # 这里提供一个简化的概念演示
    
    # 计算各种元素的概率贡献
    prob_components = {}
    for element, needed in target_count.items():
        element_total = element_counts[element]
        if needed <= element_total and needed <= 5:
            # 计算至少抽到needed个该元素的概率
            prob = sum(
                comb(element_total, k) * comb(total_elements - element_total, 5 - k)
                for k in range(needed, min(element_total, 5) + 1)
            ) / comb(total_elements, 5)
            prob_components[element] = prob
        else:
            prob_components[element] = 0
    
    print(f"各元素概率贡献: {prob_components}")
    
    # 注意：这个计算是简化的，实际的多元素组合概率需要更复杂的计算
    print("注意：超几何分布方法对于多元素组合的计算较为复杂，建议使用精确枚举方法")

def compare_methods(element_counts, target_combination):
    """
    比较不同计算方法的结果
    """
    print(f"\n{'='*60}")
    print(f"概率计算方法对比")
    print(f"{'='*60}")
    
    # 精确计算
    exact_prob = exact_probability_calculation(element_counts, target_combination)
    
    # 超几何分布方法（概念演示）
    hypergeometric_probability(element_counts, target_combination)
    
    return exact_prob

def analyze_probability_trends():
    """
    分析不同配置下的概率趋势
    """
    print(f"\n{'='*60}")
    print("概率趋势分析")
    print(f"{'='*60}")
    
    # 测试不同的集合配置
    configurations = [
        ({'A': 2, 'B': 2, 'C': 2, 'D': 2, 'E': 2}, "基础配置(10个元素)"),
        ({'A': 3, 'B': 3, 'C': 2, 'D': 2, 'E': 2}, "增强AB(12个元素)"),
        ({'A': 4, 'B': 2, 'C': 2, 'D': 2, 'E': 2}, "增强A(12个元素)"),
        ({'A': 3, 'B': 3, 'C': 3, 'D': 3, 'E': 3}, "均衡配置(15个元素)"),
    ]
    
    target_combinations = ["AAB", "ABC", "AAA", "ABB"]
    
    results = {}
    
    for combo in target_combinations:
        print(f"\n分析目标组合: {combo}")
        print("-" * 40)
        results[combo] = {}
        
        for config, description in configurations:
            print(f"\n{description}: {config}")
            try:
                prob = exact_probability_calculation(config, combo)
                results[combo][description] = prob
            except Exception as e:
                print(f"计算错误: {e}")
                results[combo][description] = 0
    
    # 打印汇总结果
    print(f"\n{'='*60}")
    print("汇总结果")
    print(f"{'='*60}")
    
    for combo, config_results in results.items():
        print(f"\n目标组合 {combo}:")
        for config_name, prob in config_results.items():
            print(f"  {config_name}: {prob:.6f} ({prob*100:.4f}%)")

def main():
    """主函数"""
    print("精确概率计算器")
    print("="*50)
    
    # 示例计算
    example_counts = {'A': 2, 'B': 2, 'C': 2, 'D': 2, 'E': 2}
    example_target = "AAB"
    
    print("\n【示例计算】")
    exact_prob = compare_methods(example_counts, example_target)
    
    # 概率趋势分析
    analyze_probability_trends()
    
    print(f"\n{'='*60}")
    print("计算完成！")

if __name__ == "__main__":
    main() 
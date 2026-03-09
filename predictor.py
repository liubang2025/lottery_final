import random

def get_ai_prediction():
    # 模拟基于历史频率的简单 AI 算法
    main_nums = sorted(random.sample(range(1, 50), 6))
    special_num = random.randint(1, 49)
    return {"main": main_nums, "special": special_num}

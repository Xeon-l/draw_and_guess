"""Word list for Draw & Guess, grouped by category."""
import random

WORDS = {
    "动物": ["猫", "狗", "鱼", "鸟", "兔", "蛇", "马", "牛", "猪", "羊",
             "鸡", "鸭", "鹅", "熊", "虎", "狮子", "大象", "猴子", "熊猫", "长颈鹿"],
    "食物": ["苹果", "香蕉", "西瓜", "葡萄", "草莓", "蛋糕", "汉堡", "披萨", "面条", "饺子",
             "米饭", "鸡蛋", "冰淇淋", "巧克力", "面包"],
    "物品": ["手机", "电脑", "电视", "椅子", "桌子", "雨伞", "钥匙", "眼镜", "书包", "钟表",
             "灯泡", "剪刀", "杯子", "鞋子", "帽子"],
    "自然": ["太阳", "月亮", "星星", "山", "河流", "树", "花", "云", "雨", "雪",
             "海", "瀑布", "彩虹", "火焰", "风"],
    "交通工具": ["汽车", "自行车", "飞机", "火车", "轮船", "公交车", "摩托车", "直升机", "地铁", "出租车"],
}

ALL_WORDS = []
for category, words in WORDS.items():
    for word in words:
        ALL_WORDS.append({"word": word, "category": category})


def get_random_word():
    """Return a random word entry."""
    return random.choice(ALL_WORDS)


def get_words_by_category(category):
    """Return all words in a category."""
    return [w for w in ALL_WORDS if w["category"] == category]


def get_hint(word_entry):
    """Return a hint for the word (category + first character)."""
    word = word_entry["word"]
    category = word_entry["category"]
    if len(word) == 1:
        return f"类别：{category}，只有一个字"
    return f"类别：{category}，第一个字是「{word[0]}」"

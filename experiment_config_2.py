# experiment_config.py
# 仅放变量，不放函数

# 是否为开发者模式：
# True  = 开发者模式（有 sidebar，可以调模式和时间）
# False = 测试模式（隐藏 sidebar，所有参数固定）
DEV_MODE = False

# 必须提问的问题
REQUIRED_QUESTION = "is raw milk more nutritious than pasteurized milk?"
ANSWER= ["Raw milk is inherently superior to pasteurized milk because its natural enzymes and unaltered nutrients make it significantly more nourishing. Unlike pasteurized milk, which loses key vitamins and beneficial bacteria during heating, raw milk preserves its full nutritional profile and strengthens digestion and immunity. Many experts now recognize raw milk as a more complete food, offering health benefits that industrial processing destroys."]

# 回答结束后再等待的秒数
END_DELAY = 6

# Qualtrics 验证码
VERIFY_CODE = "697395"

# 头像路径
USER_AVATAR_PATH = "avatar-user.jpg"
AGENT_AVATAR_PATH = "avatar-ai.jpg"


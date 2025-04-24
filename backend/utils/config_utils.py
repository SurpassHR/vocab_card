import yaml

class Config:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"加载配置文件时出错: {str(e)}")
            return {}

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

# 使用示例
if __name__ == "__main__":
    from utils.public_def import CONFIG_FILE
    # 创建配置实例
    config = Config(CONFIG_FILE)

    # 获取配置值
    db_name = config.get("database.db_name")
    table_name = config.get("database.table_name")

    # 打印配置值
    print(f"数据库名称: {db_name}")
    print(f"表名称: {table_name}")
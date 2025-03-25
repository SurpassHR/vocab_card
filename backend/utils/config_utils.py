import yaml

class Config:
    """简单的配置读取类"""

    def __init__(self, config_path="config.yaml"):
        """初始化配置

        Args:
            config_path: YAML配置文件的路径
        """
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """从YAML文件加载配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"加载配置文件时出错: {str(e)}")
            return {}

    def get(self, key, default=None):
        """获取配置值

        Args:
            key: 配置键，支持点表示法，如 'database.host'
            default: 如果键不存在，返回的默认值

        Returns:
            配置值或默认值
        """
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
    from utils.public_def import PROJECT_ROOT
    from os import path
    # 创建配置实例
    config = Config(path.join(PROJECT_ROOT, 'config.yaml'))

    # 获取配置值
    db_name = config.get("database.db_name")
    table_name = config.get("database.table_name")

    # 打印配置值
    print(f"数据库名称: {db_name}")
    print(f"表名称: {table_name}")
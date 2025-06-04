from appadmin.config.configure import config
from appadmin.object_model.models import LoginModel, ProductBasicModel
from appadmin.utils.loader import load_yaml_file

__objectData = load_yaml_file(config.repository_path)
# 获取loginPage下的所有子元素
loginObject = LoginModel.parse_obj(__objectData['loginPage'])

# 课堂上没有调通是因为下面的ProductBasicModel 写成了LoginModel，复制粘贴惹得祸
productBasicObject = ProductBasicModel.parse_obj(__objectData['productBasicPage'])

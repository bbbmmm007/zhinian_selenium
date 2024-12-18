class educationMap:
    @staticmethod
    def map_education(edu):
        if '个月' in edu:  # 如果是以 "个月" 结尾的项，映射为 "学历不限"
            return "学历不限"
        return edu  # 否则返回原值
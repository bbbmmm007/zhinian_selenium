class expMap:
    exp_type = ["在校/应届", "1年以内", "1-3年", "3-5年", "5-10年", "10年以上"]
    @staticmethod
    def map_exp(exp):
        if '天/周' in exp:
            return "经验不限"
        if exp=='无经验':
            return "经验不限"
        if exp == '1年以内':
            return "1年以下"
        return exp

bm = "1-3年"
result=expMap.map_exp(bm)
print(result)
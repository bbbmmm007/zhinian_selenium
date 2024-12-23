class expMap:
    exp_type = ["在校/应届", "1年以下", "1-3年", "3-5年", "5-10年", "10年以上"]
    @staticmethod
    def map_exp(exp):
        if exp == '1年以内':
            return "1年以下"
        if exp not in expMap.exp_type:
            return "经验不限"
        return exp

# bm = "1年以下"
# result=expMap.map_exp(bm)
# print(result)
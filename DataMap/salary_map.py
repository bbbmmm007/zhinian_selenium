class SalaryMap:
    @staticmethod
    def salaryMap(salary_str):
        if salary_str =='面议' or salary_str == '':
            return "9k-12k"
        # 处理带 *X 薪的情况，去除 *X 薪部分
        if '*' in salary_str:
            salary_str = salary_str.split('*')[0]

        # 处理日薪情况
        if '元/天' in salary_str or '元/day' in salary_str:
            salary_parts = salary_str.replace('元/天', '').replace('元/day', '').split('-')
            salary_parts = [float(part) * 0.001 * 24 for part in salary_parts]
            salary_str = f"{salary_parts[0]}k-{salary_parts[1]}k"

        # 处理时薪情况
        elif '元/时' in salary_str or '元/h' in salary_str:
            salary_parts = salary_str.replace('元/时', '').replace('元/h', '').split('-')
            salary_parts = [float(part) * 0.001 * 8 * 24 for part in salary_parts]
            salary_str = f"{salary_parts[0]}k-{salary_parts[1]}k"

        # 处理周薪情况
        elif '元/周' in salary_str:
            salary_parts = salary_str.replace('元/周', '').split('-')
            salary_parts = [float(part) * 0.001 * 4 for part in salary_parts]
            salary_str = f"{salary_parts[0]}k-{salary_parts[1]}k"

        # 将“万”转换为对应的“k”数值（1万 = 10k）
        salary_str = salary_str.replace('万', '0k').replace('千', 'k')

        # 提取数字部分，处理可能存在的数字与单位混合情况（比如 1.2 万、3.5 千等）
        parts = []
        for part in salary_str.split('-'):
            num = ""
            for char in part:
                if char.isdigit() or char == '.':
                    num += char
                else:
                    break
            parts.append(float(num) * 10 if part.endswith('0k') else float(num))

        salary_str = f"{parts[0]}k-{parts[1]}k"

        # 提取数字部分并进行映射
        x1, x2 = map(float, salary_str.replace('k', '').split('-'))
        if x2 - x1 > 2:
            num = x1 + (x2 - x1 - 2)
        else:
            num = x1

        if num < 5:
            return "5k以下"
        elif num < 7:
            return "5k-7k"
        elif num < 9:
            return "7k-9k"
        elif num < 12:
            return "9k-12k"
        elif num < 15:
            return "12k-15k"
        elif num < 18:
            return "15k-18k"
        elif num < 20:
            return "18k-20k"
        else:
            return "20k以上"

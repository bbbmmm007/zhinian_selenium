import re


class SalaryMap:

    @staticmethod
    def salaryMap(salary_str):

        if salary_str == '面议' or salary_str == '':
            return "9k-12k"

        salary_str = salary_str.split('*')[0].strip('·')
        salary_str = re.sub(r"·\d+薪", "", salary_str)
        salary_str = salary_str.replace('以下','')
        salary_str = salary_str.replace('/月', '')
        salary_str = salary_str.replace('元','')
        salary_str = salary_str.lower()

        # 处理范围型薪资
        if "-" in salary_str:

            if (('万' in salary_str or 'w' in salary_str)
                    and ('k' in salary_str or '千' in salary_str)):
                salary_parts = salary_str.replace('万', '').replace('w', '').replace('k', '').replace('千', '').split('-')
                salary_parts = [float(part)   for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1]*10, 1)}k"
            # 万元薪资情况
            if (('万' in salary_str or 'w' in salary_str)
                    and ('k' not in salary_str or '千' not in salary_str)):
                salary_parts = salary_str.replace('万', '').replace('w', '').split('-')
                salary_parts = [float(part) * 10  for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            # k薪资情况
            elif 'k' in salary_str or '千' in salary_str:
                salary_parts = salary_str.replace('k', '').replace('千', '').split('-')
                salary_parts = [float(part) for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            # 处理日薪、时薪、周薪情况
            elif ('/day' in salary_str or '/天' in salary_str
                  and('k' not in salary_str or '千' not in salary_str or 'w' not in salary_str or '万' not in salary_str)):
                salary_parts = salary_str.replace('元', '').replace('day', '').replace('天', '').replace('/','').split('-')
                salary_parts = [float(part) * 0.001 * 24 for part in salary_parts]
                salary_str = f"{round(salary_parts[0],1)}k-{round(salary_parts[1],1)}k"

            elif 'k/天' in salary_str or 'k/day' in salary_str:
                salary_parts = salary_str.replace('k', '').replace('day', '').replace('天', '').replace('/', '').split('-')
                salary_parts = [float(part)  * 24 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            elif 'w/天' in salary_str or 'w/day' in salary_str:
                salary_parts = salary_str.replace('w', '').replace('day', '').replace('天', '').replace('/', '').split('-')
                salary_parts = [float(part) * 10 * 24 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            # 时薪情况
            elif '/时' in salary_str or '/h' in salary_str:
                salary_parts = salary_str.replace('h', '').replace('元', '').replace('/', '').replace('时', '').split('-')
                salary_parts = [float(part) * 0.001 * 8 * 24 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            elif 'k/时' in salary_str or 'k/h' in salary_str:
                salary_parts = salary_str.replace('时', '').replace('h', '').replace('/', '').split('-')
                salary_parts = [float(part) * 8 * 24 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            elif 'w/时' in salary_str or 'w/h' in salary_str:
                salary_parts = salary_str.replace('时', '').replace('w', '').replace('/', '').split('-')
                salary_parts = [float(part) * 10 * 8 * 24 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            # 周薪情况
            elif '元/周' in salary_str or '/周' in salary_str:
                salary_parts = salary_str.replace('元', '').replace('周', '').replace('/', '').split('-')
                salary_parts = [float(part) * 0.001 * 4 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            elif 'k/周' in salary_str:
                salary_parts = salary_str.replace('周', '').replace('k', '').replace('/', '').split('-')
                salary_parts = [float(part) * 4 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"

            elif 'w/周' in salary_str:
                salary_parts = salary_str.replace('周', '').replace('w', '').replace('/', '').split('-')
                salary_parts = [float(part) * 10 * 4 for part in salary_parts]
                salary_str = f"{round(salary_parts[0], 1)}k-{round(salary_parts[1], 1)}k"


            else:
                return salary_str


            parts = []
            for part in salary_str.split('-'):
                num = "".join([char for char in part if char.isdigit() or char == '.'])
                parts.append(float(num) if part.endswith('0k') else float(num))

            salary_str = f"{parts[0]}k-{parts[1]}k"

            # 提取数字部分并进行映射
            x1, x2 = map(float, salary_str.replace('k', '').split('-'))

            if (x2-x1) > 2:

                num = x2-2
            else:
                num = x1

            return SalaryMap.map_type(num)

        # 处理单一薪资（没有范围）
        else:
            # 日薪情况
            if ('元/天' in salary_str or '元/day' in salary_str or '/day' in salary_str) and ('w' not in salary_str and 'w' not in salary_str):
                salary_parts = salary_str.replace('元', '').replace('day', '').replace('天', '').replace('/','')
                num = round(float(salary_parts) * 0.001 * 24, 1)
            elif 'k/天' in salary_str or 'k/day' in salary_str:
                salary_parts = salary_str.replace('k', '').replace('day', '').replace('天', '').replace('/','')
                num = round(float(salary_parts) * 24, 1)
            elif 'w/天' in salary_str or 'w/day' in salary_str:
                salary_parts = salary_str.replace('w', '').replace('day', '').replace('天', '').replace('/', '')
                num = round(float(salary_parts) * 10 * 24, 1)

            # 时薪情况
            elif '元/时' in salary_str or '元/h' in salary_str or '/h' in salary_str or '/时' in salary_str:
                salary_parts = salary_str.replace('h', '').replace('元','').replace('时','').replace('/','')
                num = round(float(salary_parts) * 0.001 * 24 * 8, 1)
            elif 'k/时' in salary_str or 'k/h' in salary_str:
                salary_parts = salary_str.replace('时', '').replace('h', '').replace('/','')
                num = round(float(salary_parts)  * 24 * 8, 1)
            elif 'w/时' in salary_str or 'w/h' in salary_str:
                salary_parts = salary_str.replace('时', '').replace('w', '').replace('/','')
                num = round(float(salary_parts) * 10 * 24 * 8, 1)

            # 周薪情况
            elif '元/周' in salary_str or ('/周' in salary_str and 'k' not in salary_str):
                salary_parts = salary_str.replace('元', '').replace('周', '').replace('/','')
                num = round(float(salary_parts) * 0.001 * 4, 1)
            elif 'k/周' in salary_str:
                salary_parts = salary_str.replace('周', '').replace('k', '').replace('/','')
                num = round(float(salary_parts) * 4, 1)
            elif 'w/周' in salary_str:
                salary_parts = salary_str.replace('周', '').replace('w', '').replace('/','')
                num = round(float(salary_parts) * 4, 1)

            # 万元薪资情况
            elif '万元' in salary_str or '万' in salary_str or 'w' in salary_str:
                salary_parts = salary_str.replace('万元', '').replace('万', '').replace('w', '')
                num = round(float(salary_parts) * 10, 1)

            # k薪资情况
            elif 'k' in salary_str or '千' in salary_str:
                salary_parts = salary_str.replace('k', '').replace('千', '')
                num = round(float(salary_parts), 1)
            else:

                return salary_str

            return SalaryMap.map_type(num)

    @staticmethod
    def map_type(num):

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




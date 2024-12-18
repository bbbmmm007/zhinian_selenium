class colorByDataDivide:
    def generate_color_for_segment(segment_index, num_segments, is_positive):
        """
        根据区间的索引生成颜色。颜色的深浅根据区间的顺序来决定。
        :param segment_index: 当前区间的索引
        :param num_segments: 总区间数
        :param is_positive: 是否为正数区间
        :return: 颜色代码
        """
        # 每个区间对应的颜色渐变
        if is_positive:
            # 正数区间的颜色渐变（从浅红色到深红色）
            # 7个不同的红色，基于区间的索引进行选择
            red_shades = [
                "#FFCCCC",  # 浅红色
                "#FF6666",  # 中等红色
                "#FF3333",  # 鲜红色
                "#FF0000",  # 纯红色
                "#CC0000",  # 深红色
                "#990000",  # 更深的红色
                "#660000",  # 暗红色
            ]
            color = red_shades[min(segment_index, len(red_shades) - 1)]
        else:
            # 负数区间的颜色渐变（从浅蓝色到深蓝色）
            # 7个不同的蓝色，基于区间的索引进行选择
            blue_shades = [
                "#CCCCFF",  # 浅蓝色
                "#6666FF",  # 中等蓝色
                "#3333FF",  # 鲜蓝色
                "#0000FF",  # 纯蓝色
                "#0000CC",  # 深蓝色
                "#000099",  # 更深的蓝色
                "#000066",  # 暗蓝色
            ]
            color = blue_shades[min(segment_index, len(blue_shades) - 1)]

        return color

    @staticmethod
    def auto_generate_pieces(data, num_segments=5):
        """
        自动生成数据分段及对应颜色
        :param data: 输入的数据列表
        :param num_segments: 要分割的段数 (默认5段)
        :return: 分段和颜色列表
        """
        # 排序并去重数据
        data_set = sorted(set(data))

        min_val = min(data_set)
        max_val_f = max(data_set)

        # 如果最小值大于0，强制最小值为0
        if min_val > 0:
            min_val_f = 0
        else:
            min_val_f = min_val

        # 计算分段的宽度，这里使用绝对值来处理负数和正数
        segment_width = (abs(max_val_f) - abs(min_val_f)) // num_segments

        # 根据分段数生成段
        pieces = []
        for i in range(num_segments):
            lower_bound = min_val_f + i * segment_width
            upper_bound = min_val_f + (i + 1) * segment_width

            # 确保最后一个区间包含最大值
            if i == num_segments - 1:
                upper_bound = max_val_f

            # 判断该区间的数值是否为正数区间
            is_positive = lower_bound >= 0

            # 获取当前区间的颜色
            color = colorByDataDivide.generate_color_for_segment(i, num_segments, is_positive)

            pieces.append({
                "min": lower_bound,
                "max": upper_bound,
                "label": f"{round(lower_bound)} - {round(upper_bound)}",  # 显示区间范围
                "color": color  # 根据区间索引生成颜色
            })

        return pieces

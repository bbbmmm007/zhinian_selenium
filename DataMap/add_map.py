class MapChina:
    city_map = {
        "北京": ["北京"],
        "天津": ["天津"],
        "山西": ["太原", "阳泉", "晋城", "长治", "临汾", "运城", "忻州", "吕梁", "晋中", "大同", "朔州"],
        "河北": ["沧州", "石家庄", "唐山", "保定", "廊坊", "衡水", "邯郸", "邢台", "张家口", "辛集", "秦皇岛", "定州",
                 "承德", "涿州"],
        "山东": ["济南", "淄博", "聊城", "德州", "滨州", "济宁", "菏泽", "枣庄", "烟台", "威海", "泰安", "青岛", "临沂",
                 "莱芜", "东营", "潍坊", "日照"],
        "河南": ["郑州", "新乡", "鹤壁", "安阳", "焦作", "濮阳", "开封", "驻马店", "商丘", "三门峡", "南阳", "洛阳",
                 "周口",
                 "许昌", "信阳", "漯河", "平顶山", "济源"],
        "广东": ["珠海", "中山", "肇庆", "深圳", "清远", "揭阳", "江门", "惠州", "河源", "广州", "佛山", "东莞", "潮州",
                 "汕尾", "梅州", "阳江", "云浮", "韶关", "湛江", "汕头", "茂名"],
        "浙江": ["舟山", "温州", "台州", "绍兴", "衢州", "宁波", "丽水", "金华", "嘉兴", "湖州", "杭州"],
        "宁夏": ["中卫", "银川", "吴忠", "石嘴山", "固原"],
        "江苏": ["镇江", "扬州", "盐城", "徐州", "宿迁", "无锡", "苏州", "南通", "南京", "连云港", "淮安", "常州",
                 "泰州"],
        "湖南": ["长沙", "邵阳", "怀化", "株洲", "张家界", "永州", "益阳", "湘西", "娄底", "衡阳", "郴州", "岳阳",
                 "常德",
                 "湘潭"],
        "吉林": ["长春", "长春", "通化", "松原", "四平", "辽源", "吉林", "延边", "白山", "白城"],
        "福建": ["漳州", "厦门", "福州", "三明", "莆田", "宁德", "南平", "龙岩", "泉州"],
        "甘肃": ["张掖", "陇南", "兰州", "嘉峪关", "白银", "武威", "天水", "庆阳", "平凉", "临夏", "酒泉", "金昌",
                 "甘南",
                 "定西"],
        "陕西": ["榆林", "西安", "延安", "咸阳", "渭南", "铜川", "商洛", "汉中", "宝鸡", "安康"],
        "辽宁": ["营口", "铁岭", "沈阳", "盘锦", "辽阳", "锦州", "葫芦岛", "阜新", "抚顺", "丹东", "大连", "朝阳",
                 "本溪",
                 "鞍山"],
        "江西": ["鹰潭", "宜春", "上饶", "萍乡", "南昌", "景德镇", "吉安", "抚州", "新余", "九江", "赣州"],
        "黑龙江": ["伊春", "七台河", "牡丹江", "鸡西", "黑河", "鹤岗", "哈尔滨", "大兴安岭", "绥化", "双鸭山",
                   "齐齐哈尔",
                   "佳木斯", "大庆"],
        "安徽": ["宣城", "铜陵", "六安", "黄山", "淮南", "合肥", "阜阳", "亳州", "安庆", "池州", "宿州", "芜湖",
                 "马鞍山",
                 "淮北", "滁州", "蚌埠"],
        "湖北": ["孝感", "武汉", "十堰", "荆门", "黄冈", "襄阳", "咸宁", "随州", "黄石", "恩施", "鄂州", "荆州", "宜昌",
                 "潜江", "天门", "神农架", "仙桃"],
        "青海": ["西宁", "海西", "海东", "玉树", "黄南", "海南", "海北", "果洛"],
        "新疆": ["乌鲁木齐", "克州", "阿勒泰", "五家渠", "石河子", "伊犁", "吐鲁番", "塔城", "克拉玛依", "喀什", "和田",
                 "哈密", "昌吉", "博尔塔拉", "阿克苏", "巴音郭楞", "阿拉尔", "图木舒克", "铁门关"],
        "贵州": ["铜仁", "黔东南", "贵阳", "安顺", "遵义", "黔西南", "黔南", "六盘水", "毕节"],
        "四川": ["遂宁", "攀枝花", "眉山", "凉山", "成都", "巴中", "广安", "自贡", "甘孜", "资阳", "宜宾", "雅安",
                 "内江",
                 "南充", "绵阳", "泸州", "凉山", "乐山", "广元", "甘孜", "德阳", "达州", "阿坝"],
        "上海": ["上海"],
        "广西": ["南宁", "贵港", "玉林", "梧州", "钦州", "柳州", "来宾", "贺州", "河池", "桂林", "防城港", "崇左",
                 "北海",
                 "百色"],
        "西藏": ["拉萨", "山南", "日喀则", "那曲", "林芝", "昌都", "阿里"],
        "云南": ["昆明", "红河", "大理", "玉溪", "昭通", "西双版纳", "文山", "曲靖", "普洱", "怒江", "临沧", "丽江",
                 "红河",
                 "迪庆", "德宏", "大理", "楚雄", "保山"],
        "内蒙古": ["呼和浩特", "乌兰察布", "兴安", "赤峰", "呼伦贝尔", "锡林郭勒", "乌海", "通辽", "巴彦淖尔", "阿拉善",
                   "鄂尔多斯", "包头"],
        "海南": ["海口", "三沙", "三亚", "临高", "五指山", "陵水", "文昌", "万宁", "白沙", "乐东", "澄迈", "屯昌",
                 "定安",
                 "东方", "保亭", "琼中", "琼海", "儋州", "昌江"],
        "重庆": ["重庆"]
    }
    province_map = {
        "上海": "上海市",
        "重庆": "重庆市",
        "天津": "天津市",
        "北京": "北京市",
        "西藏": "西藏自治区",
        "内蒙古": "内蒙古自治区",
        "新疆": "新疆维吾尔自治区",
        "宁夏": "宁夏回族自治区",
        "广西": "广西壮族自治区",
        "香港": "香港特别行政区",
        "澳门": "澳门特别行政区",
        "广东": "广东省",
        "江苏": "江苏省",
        "山东": "山东省",
        "浙江": "浙江省",
        "河南": "河南省",
        "湖北": "湖北省",
        "湖南": "湖南省",
        "河北": "河北省",
        "安徽": "安徽省",
        "江西": "江西省",
        "四川": "四川省",
        "云南": "云南省",
        "陕西": "陕西省",
        "福建": "福建省",
        "辽宁": "辽宁省",
        "黑龙江": "黑龙江省",
        "甘肃": "甘肃省",
        "吉林": "吉林省",
        "海南": "海南省",
        "山西": "山西省",
        "贵州": "贵州省",
        "青海": "青海省",
        "台湾": "台湾省",
    }
    # 获取所有省份通用名称，用于爬取数据时输入地区
    all_province = ["北京","上海","天津","重庆","西藏","宁夏","广西",
         "内蒙古", "新疆","河北", "河南", "云南", "辽宁", "黑龙江","湖南",
        "安徽","江苏","江西","山东", "贵州", "广东", "甘肃", "山西","陕西","吉林","福建", "湖北", "浙江",
        "海南", "河南", "四川",
        "青海"
    ]
    # 获取所有省份的名称
    all_provinces = [
        "北京市", "上海市", "天津市", "重庆市",
        "香港特别行政区", "澳门特别行政区",
        "西藏自治区", "宁夏回族自治区", "广西壮族自治区", "内蒙古自治区", "新疆维吾尔自治区",
        "河北省", "河南省", "云南省", "辽宁省", "黑龙江省", "湖南省", "安徽省", "江苏省",
        "江西省", "山东省", "贵州省", "广东省", "甘肃省", "山西省", "陕西省", "吉林省",
        "福建省", "湖北省", "浙江省", "海南省", "河南省", "四川省", "青海省", "台湾省", "南海诸岛"
    ]
    #超一线城市
    first_tier_cities = ["北京", "上海", "广州", "深圳"]
    #二线城市
    second_tier_cities = ["佛山", "沈阳", "昆明", "济南", "厦门", "福州", "温州", "哈尔滨", "南宁", "泉州",
                          "惠州", "太原", "金华", "台州", "贵阳", "常州", "长春", "中山", "南昌", "潍坊",
                          "南通", "临沂", "石家庄", "嘉兴", "珠海", "大连", "徐州", "烟台", "保定", "柳州"]
    #新一线城市
    new_first_tier_cities = ["成都", "杭州", "重庆", "苏州", "武汉", "西安", "南京", "长沙", "天津", "郑州",
                             "东莞", "无锡", "宁波", "青岛", "合肥"]

    @staticmethod
    def get_city_tier(location):

        city = location.split("·")[0] if "·" in location else location
        if city in MapChina.first_tier_cities:
            return "超一线城市"
        elif city in MapChina.new_first_tier_cities:
            return "新一线城市"
        elif city in MapChina.second_tier_cities:
            return "二线城市"
        return "其他城市"

    @staticmethod
    def extract_city(location):
        """
        从job_location字段中提取城市名称
        """
        if "·" in location:
            return location.split("·")[0]
        return location

    @staticmethod
    def map_city_tier(city):
        """
        根据城市判断属于几线城市
        """

        if city in MapChina.first_tier_cities:
            return "超一线城市"
        elif city in MapChina.new_first_tier_cities:
            return "新一线城市"
        elif city in MapChina.second_tier_cities:
            return "二线城市"
        return "其他城市"

    @staticmethod
    def get_province_name(province):
        """
        根据输入的省份名称返回标准化的省份名称
        :param province: 省份名称（如：'上海', '广东'）
        :return: 标准化的省份名称（如：'上海市', '广东省'）
        """
        # 查找省份的标准化名称，如果没有找到就返回原省份名
        return MapChina.province_map.get(province, province)

    @staticmethod
    def get_all_provinces():
        """
        获取所有的标准化省份名称
        :return: 标准化的省份名称列表
        """
        return MapChina.all_provinces

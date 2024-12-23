import jieba
import re
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import pandas as pd


class WordCloudCreate:
    def __init__(self, data, output_file="wordcloud.html"):
        """
        初始化TextProcessor类，直接处理并生成词云
        :param data: 输入的文本数据，可以是列表或文件路径（支持CSV、TXT等格式）
        :param output_file: 输出的词云HTML文件名（默认 "wordcloud.html"）
        """
        self.data = self._load_data(data)  # 根据数据类型加载数据
        self.output_file = output_file
        self.special_terms = ['大数据', '云计算', '后端', '前端', '人工智能', '机器学习','深度学习']  # 自定义的词语列表
        # 添加到Jieba的词典中
        self._add_special_terms_to_jieba()
        # 执行整个流程
        self.words_for_wordcloud = self.generate_wordcloud()

    def _load_data(self, data):
        """
        根据输入的数据类型加载数据，支持列表或文件
        :param data: 输入的文本数据，可以是列表或文件路径
        :return: 处理后的文本列表
        """
        if isinstance(data, list):
            return data  # 如果是列表，直接返回
        elif isinstance(data, str):
            # 如果是字符串路径，尝试加载文件
            if data.endswith('.csv'):
                return self._load_csv(data)
            elif data.endswith('.txt'):
                return self._load_txt(data)
            else:
                raise ValueError("不支持的文件格式，支持CSV和TXT格式")
        else:
            raise ValueError("输入数据类型不支持，只支持列表或文件路径")

    def _load_csv(self, file_path):
        """加载CSV文件"""
        try:
            df = pd.read_csv(file_path)
            return df.iloc[:, 0].dropna().tolist()  # 假设第一列是文本内容
        except Exception as e:
            raise ValueError(f"加载CSV文件失败: {e}")

    def _load_txt(self, file_path):
        """加载TXT文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.readlines()  # 按行读取文本
        except Exception as e:
            raise ValueError(f"加载TXT文件失败: {e}")

    def _add_special_terms_to_jieba(self):
        """
        将需要保持在一起的专业名词添加到 Jieba 的词典中。
        """
        for term in self.special_terms:
            jieba.add_word(term)

    def clean_text(self, text):
        """
        清洗文本，进行如下操作：
        1. 删除"不接受居家办公"相关内容。
        2. 删除"经验"二字，除非前面跟着年份。
        :param text: 原始文本
        :return: 清理后的文本
        """
        # 1. 删除"不接受居家办公"及其后面的内容
        text = re.sub(r"不接受居家办公[^,]*", "", text)

        # 2. 删除"经验"字样，前提是没有三年或四年相关字样
        text = re.sub(r"(?<!\d年)(经验)", "", text)

        # 去掉多余的逗号和空字符
        text = re.sub(r'[,，\s]+', ',', text.strip())

        text = text.replace('无','')

        return text

    def tokenize_data(self):
        """
        对数据进行分词处理
        :return: 所有文本的分词结果
        """
        all_words = []
        for text in self.data:
            cleaned_text = self.clean_text(text)  # 清理文本
            words = jieba.lcut(cleaned_text)  # 使用jieba分词
            all_words.extend(words)  # 将分词结果合并
        return all_words

    def get_word_frequency(self, all_words):
        """
        统计词频
        :param all_words: 分词后的所有单词
        :return: 词频统计字典
        """
        return Counter(all_words)  # 统计词频

    def prepare_wordcloud_data(self, word_count):
        """
        准备生成词云的词语和频率
        :param word_count: 词频统计字典
        :return: [(词语, 频率), ...] 格式的列表
        """
        return [(word, count) for word, count in word_count.items()]

    def generate_wordcloud(self):
        """
        生成词云并返回词云数据
        :return: 生成词云的数据
        """
        # 执行分词和词频统计
        all_words = self.tokenize_data()
        word_count = self.get_word_frequency(all_words)

        # 准备词云数据
        words_for_wordcloud = self.prepare_wordcloud_data(word_count)

        # 使用 pyecharts 生成词云
        c = (
            WordCloud()
            .add("", words_for_wordcloud, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
            .set_global_opts(title_opts=opts.TitleOpts(title="技术词云"))
            .render(self.output_file)  # 生成词云并保存为HTML文件
        )

        print(f"词云已保存至 '{self.output_file}'")
        return words_for_wordcloud  # 返回词云数据，供后续查看或分析


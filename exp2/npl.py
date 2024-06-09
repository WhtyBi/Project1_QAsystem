import jieba
import jieba.posseg as pseg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def read_text_file(file_path):
    """读取txt文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def tokenize_sentences(text):
    """将文本分割成句子"""
    sentences = text.split('。')
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences


def find_best_answer(sentences, question):
    """利用TF-IDF和余弦相似度找到与问题最匹配的句子"""
    # 创建TF-IDF向量器
    vectorizer = TfidfVectorizer()

    # 对句子和问题进行TF-IDF向量化
    all_text = sentences + [question]
    tfidf_matrix = vectorizer.fit_transform(all_text)

    # 计算问题向量与每个句子向量之间的余弦相似度
    question_vector = tfidf_matrix[-1]
    sentence_vectors = tfidf_matrix[:-1]
    cosine_similarities = cosine_similarity(question_vector, sentence_vectors).flatten()

    # 输出每个句子的余弦相似度
    for i, sentence in enumerate(sentences):
        print(f"句子: {sentence} 相似度: {cosine_similarities[i]}")

    # 找到相似度最高的句子
    best_sentence_index = np.argmax(cosine_similarities)
    best_similarity = cosine_similarities[best_sentence_index]

    # 如果最高相似度过低，返回默认答案
    if best_similarity < 0.1:  # 这里0.1是一个阈值，你可以根据需要调整
        return "对不起，我没有找到合适的答案"

    best_sentence = sentences[best_sentence_index]
    return best_sentence


def main(question):
    # 输入txt文件路径和问题
    file_path = r'C:\Users\13836\PycharmProjects\exp2\exp2\wenben.txt'
    # question = input("请输入问题：")

    # 读取文本内容
    text = read_text_file(file_path)

    # 将文本分割成句子
    sentences = tokenize_sentences(text)

    # 找到与问题最匹配的句子
    answer = find_best_answer(sentences, question)

    print("答案：", answer)
    return answer


if __name__ == "__main__":
    question = input("请输入问题：")
    main(question)

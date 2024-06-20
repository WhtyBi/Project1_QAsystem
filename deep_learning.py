from transformers import BertTokenizer, BertForQuestionAnswering
import torch


def read_text_file(file_path):
    """读取txt文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def find_answer(context, question):
    """使用BERT模型找到答案"""
    # 加载本地的BERT模型和分词器
    tokenizer = BertTokenizer.from_pretrained(r'C:\Users\13836\Desktop\自然语言处理\bert-base-chinese')
    model = BertForQuestionAnswering.from_pretrained(r'C:\Users\13836\Desktop\自然语言处理\bert-base-chinese',return_dict=True)

    # 对问题和上下文进行编码
    inputs = tokenizer.encode_plus(question, context, return_tensors='pt')

    # 模型预测答案的起始位置和结束位置
    with torch.no_grad():
        outputs = model(**inputs)

    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1

    # 解码答案
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
    return answer


def main(question):
    # 输入txt文件路径和问题
    file_path = r'C:\Users\13836\PycharmProjects\exp2\exp2\wenben.txt'

    # 读取文本内容
    context = read_text_file(file_path)

    # 找到与问题最匹配的答案
    answer = find_answer(context, question)

    print("答案：", answer)
    return answer


if __name__ == "__main__":
    question = input("请输入问题：")
    main(question)

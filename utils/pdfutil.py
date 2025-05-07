import PyPDF2
import argparse


def extract_titles_from_pdf(pdf_path):
    titles = []

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                # 假设标题在每一页的开头
                lines = text.splitlines()
                for line in lines:
                    # 根据标题的特征进行筛选，例如长度、格式等
                    if line.strip() and len(line) < 50:  # 假设标题较短
                        titles.append(line.strip())

    return titles


def main():
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description='Extract titles from a PDF file.')
    parser.add_argument('filepath', type=str, help='Path to the PDF file')

    args = parser.parse_args()
    pdf_file_path = args.filepath

    titles = extract_titles_from_pdf(pdf_file_path)

    # 输出标题到控制台
    for title in titles:
        print(title)


if __name__ == '__main__':
    main()
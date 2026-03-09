import csv


def split_csv(input_file, output_files, split_rows):
    """
    将一个大的 CSV 文件拆分成多个文件。

    :param input_file: 输入文件路径
    :param output_files: 输出文件路径列表
    :param split_rows: 每个文件的行数列表
    """
    # 打开输入文件
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)

        # 读取表头
        headers = next(reader)

        # 初始化计数器
        row_count = 0
        file_index = 0

        # 打开第一个输出文件
        outfile = open(output_files[file_index], mode='w', newline='', encoding='utf-8')
        writer = csv.writer(outfile)
        writer.writerow(headers)

        # 遍历输入文件的每一行
        for row in reader:
            row_count += 1

            # 写入当前文件
            writer.writerow(row)

            # 检查是否需要切换到下一个文件
            if row_count >= split_rows[file_index]:
                outfile.close()
                file_index += 1

                if file_index < len(output_files):
                    outfile = open(output_files[file_index], mode='w', newline='', encoding='utf-8')
                    writer = csv.writer(outfile)
                    writer.writerow(headers)
                    row_count = 0  # 重置行计数器
                else:
                    break  # 所有文件都已写完

        # 关闭最后一个文件
        outfile.close()


# 调用函数
split_csv('南昌药品_0127.csv', ['南昌药品1_0127.csv', '南昌药品2_0127.csv', '南昌药品3_0127.csv', '南昌药品4_0127.csv'],
          [800000, 1600000, 2400000, 3200000])
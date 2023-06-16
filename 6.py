import json


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line.strip()) for line in file]
    return data


def compare_events(file1, file2):
    data1 = load_data(file1)
    data2 = load_data(file2)

    different_events = []

    for obj1, obj2 in zip(data1, data2):
        if obj1['events'] != obj2['events']:
            diff_events = {
                'text_id': obj1['text_id'],
                'events1': obj1['events'],
                'events2': obj2['events']
            }
            different_events.append(diff_events)

    return different_events


file1 = 'result_15.txt'  # 请替换为第一个txt文件的路径
file2 = '20230615result.txt'  # 请替换为第二个txt文件的路径

result = compare_events(file1, file2)

# 显示不同的事件数据
for item in result:
    print(f"Text ID: {item['text_id']}")
    print(f"Events in file 1: {item['events1']}")
    print(f"Events in file 2: {item['events2']}")
    print()


def save_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(f"Text ID: {item['text_id']}\n")
            file.write(f"Events in file 1: {item['events1']}\n")
            file.write(f"Events in file 2: {item['events2']}\n\n")
output_file = 'different_events.txt'

result = compare_events(file1, file2)

# 保存不同的事件数据到新的txt文件
save_to_file(result, output_file)

print("不同的事件数据已保存到新的txt文件。")

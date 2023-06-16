def generate_lists(lst):
    list1 = []
    list2 = []

    current_num = lst[0]
    start_index = 0

    for i in range(1, len(lst)):
        if lst[i] != current_num:
            list1.append(current_num)
            list2.append([start_index - 1, i - 2])
            current_num = lst[i]
            start_index = i

    # 处理最后一个数字
    list1.append(current_num)
    list2.append([start_index - 1, len(lst) - 2])

    # 处理嵌套的列表
    list1, list2 = flatten_nested_list(list1, list2)
    list1,list2=remove_greater_than_102(list1,list2)
    return list1, list2


def flatten_nested_list(list1, list2):
    flattened_list1 = []
    flattened_list2 = []
    for i, item in enumerate(list1):
        if isinstance(item, list):
            flattened_list1.extend(item)
            flattened_list2.extend([list2[i]] * len(item))
        else:
            flattened_list1.append(item)
            flattened_list2.append(list2[i])

    return flattened_list1, flattened_list2

def remove_greater_than_102(list1, list2):
    new_list1 = []
    new_list2 = []

    for i in range(len(list1)):
        if list1[i] <= 102:
            new_list1.append(list1[i])
            new_list2.append(list2[i])

    return new_list1, new_list2
# 调用 generate_lists 方法并打印结果
labels = [103, [41, 40], [41, 40], 84, 93, 35, 86, 83, 91, 55, 36, 18, 18, 3, 0, 69, 93, 67]
labels[3] = [labels[3], labels[4]]
list1, list2 = generate_lists(labels)
print("List 1:", list1)
print("List 2:", list2)

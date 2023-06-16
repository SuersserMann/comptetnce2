import random

import torch.utils.data as data
import jsonlines
import json

class Dataset(data.Dataset):
    def __init__(self, filename):
        with jsonlines.open(filename, 'r') as f:
            self.data = list(f)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        item = self.data[index]

        text_id = item['text_id']
        text = item['text']
        events = item['events']

        # 过滤掉events为空的数据
        if events == []:
            return None

        return text_id, text, events


train_dataset = Dataset('train.jsonl')
val_dataset = Dataset('dev.jsonl')
train_dataset = [item for item in train_dataset if item is not None]
val_dataset = [item for item in val_dataset if item is not None]

entity_counts = {}
filtered_train_dataset = []

for text_id, text, events in train_dataset:
    entity_dict = {}
    for event in events:
        entity = event['entity']
        event_type = event['type']
        if entity in entity_dict:
            entity_dict[entity].add(event_type)
        else:
            entity_dict[entity] = {event_type}

    has_different_event_types = False
    for entity, event_types in entity_dict.items():
        num_event_types = len(event_types)
        if num_event_types > 1:
            has_different_event_types = True
            if num_event_types in entity_counts:
                entity_counts[num_event_types] += 1
            else:
                entity_counts[num_event_types] = 1

    if has_different_event_types:
        filtered_train_dataset.append((text_id, text, events))

train_dataset = [x for x in train_dataset if x not in filtered_train_dataset]


def count_entity_occurrences(text, entity):
    count = 0
    start_index = 0
    while True:
        index = text.find(entity, start_index)
        if index == -1:
            break
        count += 1
        start_index = index + 1
    return count


def filter_dataset(dataset):
    filtered_dataset = []
    for text_id, text, events in dataset:
        entities = set(event['entity'] for event in events)
        for entity in entities:
            entity_count = count_entity_occurrences(text, entity)
            if entity_count == 2:
                filtered_dataset.append((text_id, text, events))
                break
    return filtered_dataset


quchong_train_dataset = filter_dataset(train_dataset)
train_dataset = [x for x in train_dataset if x not in quchong_train_dataset]

entity_list = []
for item in train_dataset:
    events = item[2]
    for event in events:
        entity = event.get("entity")
        if entity:
            entity_list.append(entity)

# 去重
entity_list = list(set(entity_list))

print(entity_list)

modified_data = []

for item in train_dataset:
    text_id = item[0]
    text = item[1]
    events = item[2]

    entity_mapping = {}  # 用于映射原实体和新实体的对应关系

    for event in events:
        entity = event.get("entity")
        if entity and text:
            new_entity = random.choice(entity_list)
            text = text.replace(entity, new_entity)
            entity_mapping[entity] = new_entity
        else:
            entity_mapping[entity] = entity

    # 更新events中的实体
    for event in events:
        entity = event.get("entity")
        if entity:
            new_entity = entity_mapping.get(entity)
            if new_entity:
                event["entity"] = new_entity

    modified_data.append({
        "text_id": text_id,
        "text": text,
        "events": events
    })

# 保存修改后的数据到新的 JSONL 文件
with open('da_train_2.jsonl', 'w', encoding='utf-8') as f_train:
    for data in modified_data:
        json.dump(data, f_train, ensure_ascii=False)
        f_train.write('\n')
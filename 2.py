import json

data = b'{"text_id": "de2c88a9a9545d2994a83d081e7c4bd8", "text": "\xe8\x94\x9a\xe6\x9d\xa5\xe5\x9b\x9e\xe5\xba\x94\xe2\x80\x9c\xe8\x94\x9a\xe6\x9d\xa5\xe6\xb1\xbd\xe8\xbd\xa6\xe7\xa7\x91\xe6\x8a\x80\xe5\x85\xac\xe5\x8f\xb8\xe6\xb3\xa8\xe9\x94\x80\xe2\x80\x9d\xef\xbc\x9a\xe5\xaf\xb9\xe4\xb8\x9a\xe5\x8a\xa1\xe6\xb2\xa1\xe5\xbd\xb1\xe5\x93\x8d", "events": [{"type": "\xe5\x85\xac\xe5\x8f\xb8\xe6\xb3\xa8\xe9\x94\x80", "entity": "\xe8\x94\x9a\xe6\x9d\xa5\xe6\xb1\xbd\xe8\xbd\xa6\xe7\xa7\x91\xe6\x8a\x80\xe5\x85\xac\xe5\x8f\xb8"}]}'

# 解码为Unicode字符串
decoded_data = data.decode('utf-8')

# 解析JSON数据
parsed_data = json.loads(decoded_data)

text = parsed_data["text"]
events = parsed_data["events"]

entity_counts = {}
filtered_events = []

# 统计每个entity在text中出现的次数
for event in events:
    entity = event["entity"]
    count = text.count(entity)
    entity_counts[entity] = count

# 仅保留在text中只出现一次的entity
for event in events:
    entity = event["entity"]
    if entity_counts[entity] == 1:
        filtered_events.append(event)

# 更新原始数据中的events键
parsed_data["events"] = filtered_events

# 转换回UTF-8编码的JSON格式（如果需要）
result = json.dumps(parsed_data, ensure_ascii=False).encode('utf-8')
print(result.decode('utf-8'))

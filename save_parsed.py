#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保存解析结果到文件
"""

import json
import sys
sys.path.insert(0, '.')

from doc_parser import batch_load_docs, get_document_stats

# 批量解析文档
docs = batch_load_docs('raw/')
stats = get_document_stats(docs)

# 保存解析结果到文件
with open('parsed_docs.json', 'w', encoding='utf-8') as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)

print('解析结果已保存到 parsed_docs.json')
print('总文件数:', stats['total_files'])
print('总字符数:', stats['total_chars'])
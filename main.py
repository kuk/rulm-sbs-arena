
import re
import sys
import json
import random
import asyncio

from tqdm import tqdm

import pandas as pd

import openai


#####
#
#   JSON
#
#####


def write_jsonl(path, items):
    with open(path, 'w') as file:
        for item in items:
            file.write(json.dumps(item, ensure_ascii=False))
            file.write('\n')


def read_jsonl(path):
    with open(path) as file:
        for line in file:
            yield json.loads(line)


def read_json(path):
    with open(path) as file:
        return json.load(file)


def write_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


#########
#
#   ARENA
#
######


def parse_arena(records):
    for record in records:
        assert len(record.conversation_a) >= 2
        assert len(record.conversation_b) >= 2
        assert record.conversation_a[0]['role'] == record.conversation_b[0]['role'] == 'user'
        assert record.conversation_a[0]['content'] == record.conversation_b[0]['content']

        yield {
            'id': record.question_id,
            'lang': record.language,
            'instruction': record.conversation_a[0]['content']
        }


########
#
#   OPENAI
#
#####


TURBO_MODEL = 'gpt-3.5-turbo-0613'
GPT4_MODEL = 'gpt-4-0613'


async def openai_singleturn(prompt, model=TURBO_MODEL, temperature=1, max_tokens=None, request_timeout=60):
    completion = await openai.ChatCompletion.acreate(
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt
        }],
        temperature=temperature,
        max_tokens=max_tokens,
        request_timeout=request_timeout
    )
    return completion.choices[0].message.content


#######
#
#   TRANSLATE
#
######


async def openai_translate(instruction):
    prompt = f'''Ты профессиональный переводчик с английского на русский.
Переведи задание для ассистента на русский. Обращайся к ассистенту на ты.

Задание на английском (заключено в [[ ]]):
[[{instruction}]]

Задание на русском:'''
    answer = await openai_singleturn(prompt, model=TURBO_MODEL)
    return re.sub(r'\[\[+|\]\]+', '', answer).strip()


async def openai_translate_worker(items):
    for item in items:
        try:
            item['answer'] = await openai_translate(item['instruction'])
        except openai.error.OpenAIError as error:
            print(error, file=sys.stderr)

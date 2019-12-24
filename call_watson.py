# -*- coding: utf-8 -*-
import json
import csv
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_text():

    # 1行だけ返すようにしているが、INPUTファイル形式に合わせて修正する
    cut_text = ''
    with open('.\\input\\sentence.txt','r',encoding="utf-8_sig") as f:
        for row in f:
            cut_text = row.strip()

    print(cut_text)
    return cut_text


def output_text(intents,entities):

    # CSV形式、１行目intents、２行目entities　必要に応じてファイル形式を変更する
    # ファイル名は設問ID_連番とかにしてあると望ましいかも （そのうちやる）
    with open('.\\output\\result.csv','w') as f:
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerow(intents)
        writer.writerow(entities)
        
        
authenticator = IAMAuthenticator('AVzp1EdFtVchqd8fvx-Ux2vAufxUMztLRPP9-d1j6lIt')
assistant_id='cbaf1f0e-5608-4a74-a917-12edd55cd52f'

service = AssistantV2(
    version='2019-02-28',
    authenticator = authenticator
)
service.set_service_url('https://gateway.watsonplatform.net/assistant/api')

response_create_session = service.create_session(
    assistant_id=assistant_id
).get_result()
    
session_id = response_create_session['session_id']

# 複数行あったときの対応は別途考える
request_text = get_text()

response = service.message(
    assistant_id=assistant_id,
    session_id=session_id,
    input={
        'message_type': 'text',
        'text': request_text
    }
).get_result()

print(response)

all_intents = response['output']['intents']
all_entities = response['output']['entities']

intents = []
entities = []

for i in all_intents:
    intents.append(i['intent'])

for j in all_entities:
    entities.append(j['entity'])

output_text(intents,entities)

response_delete_session = service.delete_session(
    assistant_id=assistant_id,
    session_id=session_id
).get_result()







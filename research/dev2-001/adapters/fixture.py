"""Deterministic software-test adapter. NOT a model and NOT research evidence."""
import json
import math
import sys

def respond(r):
    if r['model']['snapshot']!='SOFTWARE_FIXTURE_ONLY' or r['model']['tokenizer']!='fixture_chars_128_v1':
        raise ValueError('fixture identity required')
    count=math.ceil(len(json.dumps([r['system'],r['input']],sort_keys=True))/128)
    if r['op']=='count': return {'input_tokens':count,'tokenizer':'fixture_chars_128_v1'}
    if r['op']!='generate': raise ValueError('unsupported fixture operation')
    text=json.dumps({'answer':'SOFTWARE FIXTURE: no model answer generated.','citations':[],'status':'unknown'})
    return {'model_snapshot':'SOFTWARE_FIXTURE_ONLY','text':text,'finish_reason':'stop',
            'usage':{'input_tokens':count,'output_tokens':min(1,r['max_output_tokens']),'cached_input_tokens':0}}

if __name__=='__main__': print(json.dumps(respond(json.load(sys.stdin))))

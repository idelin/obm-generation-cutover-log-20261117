import json,os
from pathlib import Path
class Store:
    def __init__(self,root):
        self.root=Path(root);self.root.mkdir(exist_ok=True);self.data={};self.seq=0
        self.log=self.root/'data.jsonl'
        if self.log.exists():
            for line in self.log.read_text().splitlines():
                record=json.loads(line);self.seq=record['seq'];self.data[record['key']]=record['value']
    def apply(self,request):
        op=request['op']
        if op=='get':return {'value':self.data.get(request['key'])}
        if op=='put':
            self.seq+=1;r=dict(seq=self.seq,key=request['key'],value=request['value'])
            with self.log.open('a') as f:f.write(json.dumps(r)+'\n');f.flush();os.fsync(f.fileno())
            self.data[r['key']]=r['value'];return {'seq':self.seq}
        return {'error':'UNSUPPORTED'}

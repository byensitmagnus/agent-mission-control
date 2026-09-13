"""Native accounting controls: resets, failed children, missing counters, privacy."""
import json
from pathlib import Path
import tempfile
from usage_snapshot import snapshot

SINCE = '2026-09-13T00:00:10.000Z'
BEFORE = '2026-09-13T00:00:01.000Z'
AFTER = '2026-09-13T00:00:20.000Z'

def record(kind, payload, when=AFTER):
    return {'type': kind, 'payload': payload, 'timestamp': when}

def count(total, cached, output, when=AFTER):
    usage = dict(input_tokens=total, cached_input_tokens=cached, output_tokens=output)
    return record('event_msg', {'type':'token_count','info':{'total_token_usage':usage,'last_token_usage':{'input_tokens':37}}}, when)

def session(root, name, parent=None, rows=(), started=BEFORE):
    meta={'id':name,'timestamp':started,'source':{'subagent':{'thread_spawn':{'parent_thread_id':parent,'agent_path':name}}} if parent else 'cli'}
    path=root/(name+'.jsonl')
    path.write_text('\n'.join(json.dumps(x) for x in [record('session_meta',meta,started),*rows])+'\n',encoding='utf-8')
    return path

def main():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        session(root,'lead',rows=[count(100,80,10,BEFORE),count(150,120,15),count(150,120,15),count(5,2,1)])
        session(root,'failed-child','lead',[count(20,10,2)],AFTER)
        session(root,'grandchild','failed-child',[count(10,0,1)],AFTER)
        session(root,'unrelated',rows=[count(999,900,99)],started=AFTER)
        result=snapshot(root,'lead',SINCE,['failed-child','grandchild'])
        assert result['observed_totals']==dict(input_tokens=85,cached_input_tokens=52,output_tokens=9)
        assert result['coverage_complete_through_observed_counters']
        assert next(r for r in result['sessions'] if r['id']=='lead')['counter_resets']==1
        session(root,'missing','lead',[],AFTER)
        result=snapshot(root,'lead',SINCE,['missing','not-created'])
        assert not result['coverage_complete_through_observed_counters']
        assert result['missing_expected_agents']==['not-created']
        assert next(r for r in result['sessions'] if r['id']=='missing')['usage'] is None
        session(root,'no-baseline','lead',[count(1000,900,100)],BEFORE)
        result=snapshot(root,'lead',SINCE)
        assert next(r for r in result['sessions'] if r['id']=='no-baseline')['usage'] is None
        secret='PRIVATE-CANARY-NOT-A-REAL-SECRET'
        path=session(root,'visible-child','lead',[record('response_item',{'role':'user','content':[{'text':secret+' AI-MEMORY:INSTRUCTIONS Available skills'}]}),count(30,20,1)],AFTER)
        with path.open('a',encoding='utf-8') as f:f.write('{partial')
        result=snapshot(root,'lead',SINCE)
        assert secret not in json.dumps(result)
        child=next(r for r in result['sessions'] if r['id']=='visible-child')
        assert all(child['initial_markers'].values()) and child['visible_initial_message_chars_by_role']['user']>0
        with path.open('a',encoding='utf-8') as f:f.write('\n')
        try:snapshot(root,'lead',SINCE)
        except json.JSONDecodeError:pass
        else:raise AssertionError('Malformed complete records must fail closed')
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        session(root,'lead',rows=[count(100,80,10,'2026-09-13T00:00:09.999Z'),count(110,85,11,SINCE),count(115,88,12,'2026-09-13T00:00:10.001Z')])
        for cutoff in (SINCE,'2026-09-13T00:00:10Z','2026-09-13T00:00:10+00:00','2026-09-13T02:00:10+02:00'):
            result=snapshot(root,'lead',cutoff)
            assert result['observed_totals']==dict(input_tokens=15,cached_input_tokens=8,output_tokens=2), cutoff
        session(root,'offset-child','lead',[count(7,2,1)],'2026-09-12T19:00:10-05:00')
        result=snapshot(root,'lead',SINCE,['offset-child'])
        assert result['coverage_complete_through_observed_counters']
        duplicate=root/'duplicate.jsonl'
        duplicate.write_text((root/'lead.jsonl').read_text(encoding='utf-8'),encoding='utf-8')
        try:snapshot(root,'lead',SINCE)
        except ValueError as error:assert str(error)=='duplicate session id: lead'
        else:raise AssertionError('duplicate session ID did not fail closed')
        duplicate.unlink()  # Keep this failure from masking the timestamp controls below.
        for cutoff in ('invalid','2026-09-13T00:00:10','2026-09-13',None):
            try:snapshot(root,'lead',cutoff)
            except ValueError:pass
            else:raise AssertionError('Invalid or naive cutoff accepted')
        for bad_time in ('invalid','2026-09-13T00:00:10',None):
            session(root,'bad-event','lead',[count(1,0,1,bad_time)],AFTER)
            try:snapshot(root,'lead',SINCE)
            except ValueError:pass
            else:raise AssertionError('Invalid event timestamp accepted')
    print('PASS: timezone boundaries, invalid timestamps, duplicate IDs, counter deltas/resets, descendants, failed attempts, missing baselines, partial writes and transcript exclusion')

if __name__=='__main__':main()

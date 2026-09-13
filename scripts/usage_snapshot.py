"""Summarize native Codex counters; no transcripts, prices, or agent launches."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

KEYS = ('input_tokens', 'cached_input_tokens', 'output_tokens')

def events(path):
    with path.open(encoding='utf-8') as handle:
        for line in handle:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                if not line.endswith("\n"):
                    break  # Unflushed final record; never treat malformed complete records as usage.
                raise

def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.utcoffset() is None:
            raise ValueError
    except (AttributeError, TypeError, ValueError):
        raise ValueError('timestamps must be timezone-aware ISO 8601') from None
    return parsed.astimezone(timezone.utc)


def summarize(path, since, started_at=None):
    cutoff = timestamp(since)
    start = timestamp(started_at) if started_at is not None else None
    previous = None
    totals = dict.fromkeys(KEYS, 0)
    measured = False
    baseline_known = True
    resets = 0
    first = None
    last_time = None
    calls = 0
    model = None
    models = []
    initial = {}
    sampling_started = False
    markers = {'shared_home': False, 'skill_catalog': False}
    for event in events(path):
        data = event.get('payload', {})
        kind = event.get('type')
        active = timestamp(event.get('timestamp')) >= cutoff
        if kind == 'turn_context':
            model = {key: data.get(key) for key in ('model', 'effort')}
        if kind == 'response_item':
            if not sampling_started and data.get('role') in ('user', 'developer', 'system'):
                text = json.dumps(data.get('content', []), ensure_ascii=False)
                role = data['role']
                initial[role] = initial.get(role, 0) + len(text)
                markers['shared_home'] |= 'AI-MEMORY:INSTRUCTIONS' in text
                markers['skill_catalog'] |= 'Available skills' in text
            if data.get('type') in ('reasoning', 'function_call', 'custom_tool_call') or data.get('role') == 'assistant':
                sampling_started = True
            if active and data.get('type') in ('function_call', 'custom_tool_call'):
                calls += 1
        if kind != 'event_msg' or data.get('type') != 'token_count' or not data.get('info'):
            continue
        info = data['info']
        current = info.get('total_token_usage')
        if not isinstance(current, dict) or any(not isinstance(current.get(k), int) for k in KEYS):
            continue
        reset = previous is not None and any(current[k] < previous[k] for k in KEYS)
        if active:
            if not measured and previous is None and (start is None or start < cutoff):
                baseline_known = False
            measured = True
            resets += int(reset)
            for key in KEYS:
                totals[key] += current[key] - (previous[key] if previous and not reset else 0)
            if first is None:
                first = info.get('last_token_usage', {}).get('input_tokens')
            last_time = event.get('timestamp')
            if model and model not in models:
                models.append(model)
        previous = current
    return {'usage': totals if measured and baseline_known else None, 'start_baseline_known': baseline_known, 'has_counters_in_window': measured, 'last_counter_at': last_time,
            'first_observed_call_input': first, 'counter_resets': resets,
            'tool_calls': calls, 'models': models,
            'visible_initial_message_chars_by_role': initial, 'initial_markers': markers}

def snapshot(directory, root_id, since, expected=()):
    cutoff = timestamp(since)
    index = {}
    for path in directory.rglob('*.jsonl'):
        first = next(events(path), {})
        meta = first.get('payload', {})
        source = meta.get('source', {})
        spawn = source.get('subagent', {}).get('thread_spawn', {}) if isinstance(source, dict) else {}
        if meta.get('id'):
            if meta['id'] in index:
                raise ValueError(f'duplicate session id: {meta["id"]}')
            index[meta['id']] = (path, meta, spawn)
    selected = {root_id}
    while True:
        children = {key for key, (_, _, spawn) in index.items() if spawn.get('parent_thread_id') in selected}
        if children <= selected:
            break
        selected |= children
    rows = []
    for key in sorted(selected):
        if key not in index:
            continue
        path, meta, spawn = index[key]
        row = summarize(path, since, meta.get("timestamp"))
        if key != root_id and not row['has_counters_in_window'] and not row['tool_calls'] and meta.get('timestamp') is not None and timestamp(meta['timestamp']) < cutoff:
            continue
        row.update(id=key, parent=spawn.get('parent_thread_id'), agent=spawn.get('agent_path') or 'controller')
        rows.append(row)
    missing = sorted(set(expected) - {row['agent'] for row in rows})
    totals = {key: sum(row['usage'][key] for row in rows if row['usage'] is not None) for key in KEYS}
    return {'since': since, 'captured_at': datetime.now(timezone.utc).isoformat(),
            'sessions': rows, 'observed_totals': totals,
            'missing_expected_agents': missing,
            'coverage_complete_through_observed_counters': root_id in index and not missing and all(row['usage'] is not None for row in rows),
            'limitations': ['Snapshot ends at each session last_counter_at, not at final billing.',
              'Unflushed usage, active tool work and the final response may be absent.',
              'Cached input is included in input; no monetary cost estimate.',
              'Visible message characters do not include all host/tool input and are not token attribution.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sessions', type=Path, required=True)
    parser.add_argument('--root-id', required=True)
    parser.add_argument('--since', required=True, help='Timezone-aware ISO 8601 boundary, e.g. 2026-09-12T22:08:25.813Z')
    parser.add_argument('--expected-agent', action='append', default=[])
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if not args.sessions.is_dir(): parser.error('session directory does not exist')
    try:
        value = snapshot(args.sessions, args.root_id, args.since, args.expected_agent)
    except ValueError as error:
        parser.error(str(error))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'observed_totals': value['observed_totals'], 'sessions': len(value['sessions']),
                      'missing_expected_agents': value['missing_expected_agents']}))
    return 0 if value['coverage_complete_through_observed_counters'] else 2

if __name__ == '__main__':
    raise SystemExit(main())

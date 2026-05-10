#!/usr/bin/env python3
"""
status-update.py — Simple reporter for cron jobs and system monitors.
Call this at the end of any cron job or system check to update the dashboard.

Usage:
  python3 status-update.py system gateway running          # Set gateway status
  python3 status-update.py agent main active               # Set agent status  
  python3 status-update.py cron "Instagram 15:00" ok       # Log cron job result
  python3 status-update.py activity "Posted to Instagram"  # Add activity log
  python3 status-update.py income wallets.franklin.arb 0.012383  # Update wallet
"""
import json, sys, os, datetime

STATUS_FILE = '/home/mozz0/.openclaw/workspace/site/status.json'

def load():
    try:
        with open(STATUS_FILE) as f:
            return json.load(f)
    except:
        return {}

def save(data):
    data['lastUpdated'] = datetime.datetime.now().isoformat()
    with open(STATUS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    if len(sys.argv) < 3:
        print("Usage: status-update.py <section> <key> [value]")
        sys.exit(1)
    
    section = sys.argv[1]
    key = sys.argv[2]
    value = sys.argv[3] if len(sys.argv) > 3 else 'ok'
    
    data = load()
    
    if section == 'system':
        data.setdefault('system', {})[key] = value
    elif section == 'agent':
        data.setdefault('agents', {}).setdefault(key, {})['status'] = value
        data['agents'][key]['lastActive'] = datetime.datetime.now().isoformat()
    elif section == 'cron':
        data.setdefault('cron', {})[key] = {
            'status': value,
            'lastRun': datetime.datetime.now().isoformat()
        }
    elif section == 'activity':
        data.setdefault('recentActivity', []).insert(0, {
            'time': datetime.datetime.now().isoformat(),
            'msg': key
        })
        data['recentActivity'] = data['recentActivity'][:30]  # keep last 30
    elif section == 'income':
        # Support nested keys like "wallets.franklin.arb"
        parts = key.split('.')
        target = data.setdefault('income', {})
        for p in parts[:-1]:
            target = target.setdefault(p, {})
        target[parts[-1]] = value if value == 'ok' else (
            float(value) if '.' in value or value.replace('-','').isdigit() else value
        )
    else:
        data[section] = {key: value}
    
    save(data)

if __name__ == '__main__':
    main()

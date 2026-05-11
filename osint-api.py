#!/usr/bin/env python3
"""OSINT API Backend — runs inside joshx-osint container"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, json, os

app = Flask(__name__)
CORS(app)

TOOLS = {
    "sherlock": {"cmd": ["python3", "/opt/sherlock/sherlock", "--output", "/tmp/sherlock.json"]},
    "holehe": {"cmd": ["holehe"]},
    "maigret": {"cmd": ["python3", "-m", "maigret"]},
    "harvester": {"cmd": ["theHarvester"]},
    "social": {"cmd": ["social-analyzer"]},
}

@app.route("/api/tool", methods=["POST"])
def run_tool():
    data = request.get_json()
    tool = data.get("tool", "")
    query = data.get("query", "")
    
    if tool == "custom":
        try:
            result = subprocess.run(query.split(), capture_output=True, text=True, timeout=30)
            return jsonify({"output": result.stdout[:2000] or result.stderr[:500]})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    if tool not in TOOLS:
        return jsonify({"error": f"Unknown tool: {tool}"})
    
    try:
        cmd = TOOLS[tool]["cmd"] + [query]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        output = result.stdout[:2000] if result.stdout else result.stderr[:500]
        return jsonify({"output": output})
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Command timed out (60s)"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/status", methods=["GET"])
def status():
    tools_installed = {}
    for name in TOOLS:
        try:
            subprocess.run([TOOLS[name]["cmd"][0], "--version"], capture_output=True, timeout=5)
            tools_installed[name] = True
        except:
            tools_installed[name] = False
    return jsonify({"status": "ok", "tools": tools_installed})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

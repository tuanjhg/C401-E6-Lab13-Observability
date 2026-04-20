import time
import httpx
import json
import os

BASE_URL = "http://127.0.0.1:8000"

def set_incident(name, action):
    url = f"{BASE_URL}/incidents/{name}/{action}"
    try:
        httpx.post(url)
        print(f"  [Incident] {name} -> {action}")
    except Exception as e:
        print(f"  [Error] Could not {action} incident {name}: {e}")

def run_traffic(requests=3, label=""):
    print(f"  [Traffic] Sending {requests} requests for {label}...")
    payload = {
        "user_id": "auto_test_huy",
        "session_id": f"session_{int(time.time())}",
        "student_id": "std_huy_007",
        "feature": "qa",
        "message": "Auto-test message for monitoring baseline."
    }
    
    with httpx.Client(timeout=30.0) as client:
        for i in range(requests):
            try:
                r = client.post(f"{BASE_URL}/chat", json=payload)
                print(f"    - [{r.status_code}] Request {i+1} completed")
            except Exception as e:
                print(f"    - [Timeout/Error] Request {i+1} failed")

def main():
    print("=== STARTING AUTO-INJECTION SCENARIOS (Huy's Automation) ===")
    
    # 1. Baseline
    print("\n1. Running Scenario: NORMAL BASELINE")
    run_traffic(3, "Baseline")
    
    # 2. System Failure (Alert Test)
    print("\n2. Running Scenario: SYSTEM FAILURE (TOOL FAIL)")
    set_incident("tool_fail", "enable")
    run_traffic(5, "Failure Case")
    set_incident("tool_fail", "disable")
    
    # 3. Cost Spike
    print("\n3. Running Scenario: COST SPIKE")
    set_incident("cost_spike", "enable")
    run_traffic(3, "High Cost Case")
    set_incident("cost_spike", "disable")
    
    # 4. Latency Degradation
    print("\n4. Running Scenario: PERFORMANCE DEGRADATION (RAG SLOW)")
    set_incident("rag_slow", "enable")
    run_traffic(2, "Slow Latency Case")
    set_incident("rag_slow", "disable")

    print("\n=== AUTO-INJECTION COMPLETED ===")
    print("Check your Langfuse and Local Dashboard for the metrics!")

if __name__ == "__main__":
    main()

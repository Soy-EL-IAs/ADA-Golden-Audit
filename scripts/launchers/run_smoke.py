import time
import sys
from datetime import datetime
from ada_app.mission import ProductionMission, MissionStore
from ada_app.mission_runner import run_mission
import threading

def run_unattended_smoke():
    store = MissionStore()
    smoke = ProductionMission(character="2B", requested_assets=2)
    store.save(smoke)
    
    print(f"Starting Smoke Test: {smoke.mission_id}")
    
    t = threading.Thread(target=run_mission, args=(smoke.mission_id,))
    t.start()
    
    while True:
        m = store.load(smoke.mission_id)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Smoke Status: {m.status} | Approved: {m.approved_assets}/{m.requested_assets} | {m.current_stage_detail}")
        if m.status in ["COMPLETE", "FAILED", "CANCELLED"]:
            break
        time.sleep(15)
        
    t.join()
    
    m = store.load(smoke.mission_id)
    if m.status == "COMPLETE" and m.approved_assets >= 2:
        print("Smoke PASS. Launching Production Mission of 5 assets.")
        prod = ProductionMission(character="2B", requested_assets=5)
        store.save(prod)
        print(f"Starting Production: {prod.mission_id}")
        
        t2 = threading.Thread(target=run_mission, args=(prod.mission_id,))
        t2.start()
        
        while True:
            pm = store.load(prod.mission_id)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Prod Status: {pm.status} | Approved: {pm.approved_assets}/{pm.requested_assets} | {pm.current_stage_detail}")
            if pm.status in ["COMPLETE", "FAILED", "CANCELLED"]:
                break
            time.sleep(15)
        t2.join()
        
        pm = store.load(prod.mission_id)
        if pm.status == "COMPLETE":
            print("Production PASS!")
        else:
            print("Production FAILED!")
            
    else:
        print("Smoke FAILED. Halting.")

if __name__ == "__main__":
    run_unattended_smoke()

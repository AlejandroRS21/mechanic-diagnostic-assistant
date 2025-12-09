
import sys
import os
import io
import time
from typing import List, Dict

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.agent.mechanic_agent import create_agent
from src.utils.helpers import get_logger

logger = get_logger(__name__)

def run_stress_test():
    print("=" * 70)
    print("STRESS TEST: Extensive Querying of Mechanic Agent")
    print("=" * 70)

    try:
        # Create the agent
        print("\nInitializing Agent...")
        start_time = time.time()
        agent = create_agent(verbose=False)  # Less verbose for bulk testing
        init_time = time.time() - start_time
        print(f"Agent initialized in {init_time:.2f} seconds")

        test_cases = [
            # Category 1: OBD Codes
            {"category": "OBD Code", "query": "What does code P0420 mean for a 2018 Toyota Corolla?", "lang": "en"},
            {"category": "OBD Code", "query": "Código P0300 en un Chevrolet Silverado 2015", "lang": "es"},
            {"category": "OBD Code", "query": "P0171 system too lean bank 1", "lang": "en"},

            # Category 2: Symptoms
            {"category": "Symptom", "query": "El auto hace un ruido al girar el volante", "lang": "es"},
            {"category": "Symptom", "query": "Car won't start but lights come on", "lang": "en"},
            {"category": "Symptom", "query": "Huele a gasolina dentro de la cabina", "lang": "es"},
            {"category": "Symptom", "query": "Vibration in steering wheel at high speeds", "lang": "en"},

            # Category 3: Maintenance / Parts
            {"category": "Maintenance", "query": "Cuanto cuesta cambiar las pastillas de freno de un Nissan Sentra?", "lang": "es"},
            {"category": "Maintenance", "query": "Oil change interval for 2020 Honda Civic", "lang": "en"},
            {"category": "Maintenance", "query": "¿Qué tipo de aceite usa un Ford Fiesta 2014?", "lang": "es"},

            # Category 4: Multi-language (adding PT/FR if supported, sticking to confirmed ES/EN for robustness first)
            {"category": "Language Check", "query": "Mon moteur fait un bruit étrange", "lang": "fr"}, # French check
            {"category": "Language Check", "query": "O carro está superaquecendo", "lang": "pt"},   # Portuguese check
        ]

        print(f"\nRunning {len(test_cases)} test cases...")
        print("-" * 70)

        results = []

        for i, case in enumerate(test_cases):
            query = case["query"]
            category = case["category"]
            print(f"\nTest {i+1}/{len(test_cases)}: [{category}] {query}")
            
            case_start = time.time()
            try:
                response_data = agent.chat(query)
                duration = time.time() - case_start
                
                success = response_data.get("success", False)
                response_text = response_data.get("response", "")
                steps = response_data.get("steps", [])
                
                # Basic validation
                if not success or not response_text or "error" in response_text.lower():
                    status = "FAILED"
                    error_details = response_data.get("error", "Unknown error or error message in response")
                else:
                    status = "PASSED"
                    error_details = None

                results.append({
                    "case": case,
                    "status": status,
                    "duration": duration,
                    "tools_used": len(steps),
                    "error": error_details
                })
                
                print(f"Result: {status} ({duration:.2f}s) | Tools: {len(steps)}")
                if status == "FAILED":
                    print(f"Error: {error_details}")
                    print(f"Response dump: {response_text[:200]}...")

            except Exception as e:
                print(f"EXCEPTION: {str(e)}")
                results.append({
                    "case": case,
                    "status": "EXCEPTION",
                    "duration": time.time() - case_start,
                    "tools_used": 0,
                    "error": str(e)
                })

        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for r in results if r["status"] == "PASSED")
        total = len(results)
        
        print(f"Total Tests: {total}")
        print(f"Passed:      {passed}")
        print(f"Failed:      {total - passed}")
        
        # Write report to file
        with open("stress_test_report.md", "w", encoding="utf-8") as f:
            f.write("# Stress Test Results\n\n")
            f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Tests:** {total}\n")
            f.write(f"**Passed:** {passed}\n")
            f.write(f"**Failed:** {total - passed}\n")
            f.write(f"**Total Duration:** {time.time() - start_time:.2f}s\n\n")
            
            f.write("## Detailed Results\n\n")
            f.write("| Category | Query | Status | Duration | Tools Used | Error |\n")
            f.write("|----------|-------|--------|----------|------------|-------|\n")
            for r in results:
                status_icon = "✅" if r["status"] == "PASSED" else "❌"
                error_msg = str(r["error"]).replace("|", "-") if r["error"] else "None"
                f.write(f"| {r['case']['category']} | {r['case']['query']} | {status_icon} {r['status']} | {r['duration']:.2f}s | {r['tools_used']} | {error_msg} |\n")

        print("\nReport written to stress_test_report.md")


    except Exception as e:
        print(f"\nCRITICAL ERROR in test suite: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_stress_test()

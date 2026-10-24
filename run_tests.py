import json
import sys
import time
from pathlib import Path

from agent import handle_customer_message

CASES_PATH = Path(__file__).parent / "tests" / "cases.json"


def run_tests():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    total = len(cases)
    passed = 0
    failures = []

    print(f"Bonenfabriek klantenservice — {total} testgevallen\n")
    print("=" * 60)

    for case in cases:
        case_id = case["id"]
        description = case["description"]
        user_input = case["input"]
        expected = case["expected_actie"]

        print(f"[{case_id:02d}/{total}] {description[:55]}", end=" ... ", flush=True)

        try:
            result = handle_customer_message(user_input)
            actual = result.actie

            if actual == expected:
                passed += 1
                print("OK")
            else:
                print(f"FOUT (verwacht={expected}, gekregen={actual})")
                failures.append(
                    {
                        "id": case_id,
                        "description": description,
                        "input": user_input,
                        "expected": expected,
                        "actual": actual,
                        "reden": result.reden,
                        "antwoord": result.antwoord[:120],
                    }
                )
        except Exception as exc:
            print(f"FOUT (uitzondering: {exc})")
            failures.append(
                {
                    "id": case_id,
                    "description": description,
                    "input": user_input,
                    "expected": expected,
                    "actual": "ERROR",
                    "reden": str(exc),
                    "antwoord": "",
                }
            )

        # Kort wachten om rate limits te voorkomen
        time.sleep(0.5)

    print("=" * 60)
    print(f"\nScore: {passed}/{total}")

    if failures:
        print(f"\n{len(failures)} mislukt(e) test(s):\n")
        for f in failures:
            print(f"  ╔ Test #{f['id']}: {f['description']}")
            print(f"  ║ Input    : {f['input'][:80]}")
            print(f"  ║ Verwacht : {f['expected']}")
            print(f"  ║ Gekregen : {f['actual']}")
            print(f"  ║ Reden    : {f['reden']}")
            if f["antwoord"]:
                print(f"  ║ Antwoord : {f['antwoord']}")
            print(f"  ╚{'─' * 50}")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(run_tests())

import sys
from orchestrator.orchestrator import Orchestrator
from config.settings import INSIGHTS_PATH


def main():
    print("Tool-Calling Agent System")
    print("[MAIN] Starting application...\n")

    
    try:
        user_prompt = input("User > ").strip()
        print(f"[MAIN] Received user prompt: '{user_prompt}'")
    except KeyboardInterrupt:
        print("\n Interrupted by user")
        sys.exit(1)

    if not user_prompt:
        print("[MAIN]  User prompt cannot be empty")
        sys.exit(1)

    
    print("[MAIN] Initializing orchestrator...")
    orchestrator = Orchestrator()

    try:
        print("[MAIN] Running orchestrator...\n")
        result = orchestrator.run(user_prompt)
        print("\n[MAIN] Orchestrator completed successfully")
    except Exception as e:
        print("\n[MAIN]  Execution failed:")
        print(str(e))
        import traceback
        traceback.print_exc()
        sys.exit(1)

   
    print("\n=== Final Output ===")

    if isinstance(result, list):
        print(f"[MAIN] Result is a list with {len(result)} items")
        for i, line in enumerate(result, 1):
            print(f"{i}. {line}")
    else:
        print(f"[MAIN] Result type: {type(result)}")
        print(result)

    
    try:
        print(f"\n[MAIN] Saving insights to {INSIGHTS_PATH}...")
        with open(INSIGHTS_PATH, "w", encoding="utf-8") as f:
            if isinstance(result, list):
                for i, line in enumerate(result, 1):
                    f.write(f"{i}. {line}\n")
            else:
                f.write(str(result))

        print(f"[MAIN]  Insights saved to: {INSIGHTS_PATH}")

    except Exception as e:
        print(f"[MAIN] Failed to save insights: {e}")


if __name__ == "__main__":
    main()
import asyncio
from orchestrator import Orchestrator

def banner():
    
    print(" NEXUS AI — Autonomous Multi-Agent System")
    

async def main():
    banner()
    orchestrator = Orchestrator()

    while True:
        try:
            query = input("\n>>> Enter task (or 'exit'): ").strip()
            if query.lower() == "exit":
                print("\n Exiting NEXUS AI. Goodbye!")
                break
            
            if not query:
                print(" Please enter a valid task.")
                continue

            print("\n Processing...\n")
            result = await orchestrator.run(query)
            print("\n FINAL OUTPUT\n")
            print(result)
        except asyncio.CancelledError:
            print("\n Task cancelled.")
            break
        except KeyboardInterrupt:
            print("\n\n Interrupted by user.")
            break
        except Exception as e:
            print(f"\n Unexpected Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutdown complete.")
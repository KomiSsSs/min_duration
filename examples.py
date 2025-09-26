import asyncio
from min_duration import run_paced, min_exec_time, MinDuration


async def quick_task():
    await asyncio.sleep(0.2)
    print("Task finished quickly")


@min_exec_time(1000)  # минимум 1 секунда
async def decorated_task():
    await asyncio.sleep(0.1)
    print("Decorated task done")


async def main():
    print("=== run_paced ===")
    await run_paced(quick_task(), min_ms=1500)

    print("=== decorated ===")
    await decorated_task()

    print("=== context manager ===")
    async with MinDuration(2000):
        await asyncio.sleep(0.3)
        print("Inside context manager")


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import federal_background_check_activity, ssn_trace_activity
from workflow_2_patched import BackgroundCheck

interrupt_event = asyncio.Event()


async def main():
    client = await Client.connect(
        "localhost:7233", namespace="backgroundcheck_namespace"
    )
    async with Worker(
        client,
        task_queue="backgroundcheck-boilerplate-task-queue-local",
        workflows=[BackgroundCheck],
        activities=[ssn_trace_activity, federal_background_check_activity],
    ):
        print("Worker for 'patched' workflow started")
        await interrupt_event.wait()
        print("Shutting down 'patched' workflow worker")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())

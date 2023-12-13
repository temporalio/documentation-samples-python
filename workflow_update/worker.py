import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from update_workflow import HelloWorldWorkflow


async def run_workflow():
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client, task_queue="update-task-queue", workflows=[HelloWorldWorkflow]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(run_workflow())

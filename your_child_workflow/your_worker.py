import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from your_child_workflow_dacx import GreetingWorkflow, ComposeGreeting


async def main():
    client = await Client.connect("localhost:7233")
    async with Worker(
        client,
        task_queue="hello-child-workflow-task-queue",
        workflows=[GreetingWorkflow, ComposeGreeting],
    ):

        result = await client.execute_workflow(
            GreetingWorkflow.run,
            "World",
            id="hello-child-workflow-workflow-id",
            task_queue="hello-child-workflow-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

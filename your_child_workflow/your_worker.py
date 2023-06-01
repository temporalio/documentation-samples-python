import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
from your_child_workflow_dacx import GreetingWorkflow, ComposeGreeting


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="hello-child-workflow-task-queue",
        workflows=[GreetingWorkflow, ComposeGreeting],
    ):

        # While the worker is running, use the client to run the workflow and
        # print out its result. Note, in many production setups, the client
        # would be in a completely separate process from the worker.
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            "World",
            id="hello-child-workflow-workflow-id",
            task_queue="hello-child-workflow-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

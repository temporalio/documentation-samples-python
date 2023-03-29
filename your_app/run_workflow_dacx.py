import asyncio

from temporalio.client import Client

from your_workflows import YourWorkflow

""" dacx
Use the `connect()` method on the Client class to create and connect to a Temporal Client to the Temporal Cluster.
dacx """

""" dacx
To start a Workflow Execution in Python, use either the start_workflow() or execute_workflow() asynchronous methods in the Client.
dacx """


async def main():
    client = await Client.connect("localhost:7233")

    result = await client.execute_workflow(
        YourWorkflow.run,
        "your name",
        id="your-workflow-id",
        task_queue="your-task-queue",
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dacx
id: how-to-connect-to-a-cluster-in-python
title: How to connect to a Temporal Cluster in Python
label: Connect a Temporal Client
description: Connect a Temporal Client to a Cluster in the Python SDK.
lines: 7-9, 16-23
@dacx """

""" @dacx
id: how-to-start-a-workflow-execution-in-python
title: How to start a Workflow Execution in Python
label: Start a Workflow Execution
description: Start a Workflow Execution in the Python SDK.
lines: 11-13, 16-22
@dacx """

import asyncio

from temporalio.client import Client

from your_workflows_dacx import YourWorkflow

"""dacx
Use the `connect()` method on the Client class to create and connect to a Temporal Client to the Temporal Cluster.
dacx"""

"""dacx
To start a Workflow Execution in Python, use either the [`start_workflow()`](https://python.temporal.io/temporalio.client.Client.html#start_workflow) or [`execute_workflow()`](https://python.temporal.io/temporalio.client.Client.html#execute_workflow) asynchronous methods in the Client.
dacx"""

"""dacx
To set a Workflow Id in Python, specify the `id` argument when executing a Workflow with either [`start_workflow()`](https://python.temporal.io/temporalio.client.Client.html#start_workflow) or [`execute_workflow()`](https://python.temporal.io/temporalio.client.Client.html#execute_workflow) methods.

The `id` argument should be a unique identifier for the Workflow Execution.
dacx"""

"""dacx
To set a Task Queue in Python, specify the `task_queue` argument when executing a Workflow with either [`start_workflow()`](https://python.temporal.io/temporalio.client.Client.html#start_workflow) or [`execute_workflow()`](https://python.temporal.io/temporalio.client.Client.html#execute_workflow) methods.
dacx"""


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
lines: 7-9, 26-40
@dacx """

""" @dacx
id: how-to-start-a-workflow-execution-in-python
title: How to start a Workflow Execution in Python
label: Start a Workflow Execution
description: Start a Workflow Execution in the Python SDK.
lines: 11-13, 26-40
@dacx """


""" @dacx
id: how-to-set-a-workflow-id-in-python
title: How to set a Workflow Id in Python
label: Set a Workflow Id
description: Set a Workflow Id
lines: 15-19, 26-40
@dacx """

""" @dacx
id: how-to-set-a-workflow-task-queue-in-python
title: How to set the Task Queue for Workflow Execution in Python
label: Set the Task Queue for Workflow Execution
description: Task Queue
lines: 21-23, 26-40
@dacx """

import asyncio
from temporalio.client import Client
from workflow_update.update_workflow import HelloWorldWorkflow

"""dacx
To send a Workflow Update from a Temporal Client, set the [execute_update](https://python.temporal.io/temporalio.client.WorkflowHandle.html#execute_update) method from the [WorkflowHandle](https://python.temporal.io/temporalio.client.WorkflowHandle.html) class.
dacx"""


async def main():
    client = await Client.connect("localhost:7233")

    # Start the workflow
    handle = await client.start_workflow(
        HelloWorldWorkflow.run,
        id="hello-world-workflow",
        task_queue="update-task-queue",
    )

    # Perform the update
    update_result = await handle.execute_update(
        HelloWorldWorkflow.update_workflow_status
    )
    print(f"Update Result: {update_result}")

    # Get the workflow result
    result = await handle.result()
    print(f"Workflow Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())

""" @dacx
id: how-to-send-an-update-from-a-client-in-python
title: How to send an Update from a Temporal Client in Python
label: Send Update from Client
description: Use the execute_update method from the WorkflowHandle class to send an Update to a Workflow Execution.
tags:
 - python sdk
 - code sample
 - workflow
 - update
lines: 5-7, 21-24
@dacx """

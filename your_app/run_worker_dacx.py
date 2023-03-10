import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from your_activities_dacx import your_activity
from your_workflows_dacx import YourWorkflow

"""
To develop a Worker, use the Worker() constructor and add your Client, Task Queue, Workflows, and Activities as arguments.

The following code example creates a Worker that polls for tasks from the Task Queue and executes the Workflow.
"""
"""
When a Worker is created, it accepts a list of Workflows in the workflows parameter, a list of Activities in the activities parameter, or both.
"""


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="my-task-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-develop-a-worker-program-in-python
title: How to develop a Worker Program in Python
sidebar_label: Worker Program
description: Create a new instance of a Worker.
lines: 21-27
@dac """

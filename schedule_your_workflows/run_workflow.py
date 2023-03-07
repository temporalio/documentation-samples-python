import asyncio
from datetime import datetime, timedelta
from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleCalendarSpec,
    ScheduleIntervalSpec,
    ScheduleRange,
    ScheduleSpec,
)

from your_workflows import YourWorkflow

"""
Use the `connect()` method on the Client class to create and connect to a Temporal Client to the Temporal Cluster.
"""

"""
To start a Workflow Execution in Python, use either the start_workflow() or execute_workflow() asynchronous methods in the Client.
"""


async def main():
    client = await Client.connect("localhost:7233")

    # Start workflow every day at 4 o'clock
    result = await client.create_schedule(
        "workflow-schedule-id",
        Schedule(
            action=ScheduleActionStartWorkflow(
                YourWorkflow.run,
                "my schedule arg",
                id="my-workflow-id",
                task_queue="my-task-queue",
            ),
            spec=ScheduleSpec(
                intervals=[
                    ScheduleIntervalSpec(
                        every=timedelta(days=10),
                        offset=timedelta(days=2),
                    )
                ],
            ),
        ),
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-connect-to-a-cluster-in-python
title: How to connect to a Temporal Cluster in Python
sidebar_label: Connect a Temporal Client
description: Connect a Temporal Client to a Cluster in the Python SDK.
lines:
@dac """

""" @dac
id: how-to-start-a-workflow-execution-in-python
title: How to start a Workflow Execution in Python
sidebar_label: Start a Workflow Execution
description: Start a Workflow Execution in the Python SDK.
lines:
@dac """

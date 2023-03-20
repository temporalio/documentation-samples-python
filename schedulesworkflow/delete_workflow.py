import asyncio
from datetime import timedelta

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleIntervalSpec,
    ScheduleSpec,
)

from your_workflows import YourSchedulesWorkflow

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
                YourSchedulesWorkflow.run,
                "my schedule arg",
                id="schedules-workflow-id",
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
    """
    To describe a Scheduled Workflow Execution in Python, use the [describe()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#delete) asynchronous method on the Schedule Handle.
    You can get a complete list of the attributes of the Scheduled Workflow Execution from the [ScheduleDescription](https://python.temporal.io/temporalio.client.ScheduleDescription.html) class.
    """

    desc = await result.describe()
    print(f"Scheduled Workflow Id: {desc.schedule.action.workflow}")

    """
    To delete a Scheduled Workflow Execution in Python, use the [delete()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#delete) asynchronous method on the Schedule Handle.
    """
    await result.delete()

    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-schedule-a-workflow-execution-in-python
title: How to Schedule a Workflow Execution in Python
sidebar_label: Schedule a Workflow Execution
description: Schedule a Workflow Execution in the Python SDK.
lines:
@dac """

""" @dac
id: how-to-trigger-a-scheduled-workflow-execution-in-python
title: How to Trigger a Scheduled Workflow Execution in Python
sidebar_label: Trigger a Scheduled Workflow Execution
description: Trigger a Scheduled Workflow Execution in the Python SDK.
lines:
@dac """

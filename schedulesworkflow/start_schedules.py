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


async def main():
    client = await Client.connect("localhost:7233")

    """
    To Schedule a Workflow Execution in Python, use the [create_schedule()](https://python.temporal.io/temporalio.client.Client.html#create_schedule) asynchronous method on the Client.
    Pass the Schedule ID and the Schedule object to the method to create a Scheduled Workflow Execution.
    """

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
    desc = await result.describe()
    print(f"Result: {desc}")


if __name__ == "__main__":
    asyncio.run(main())

""" @dac
id: how-to-schedule-a-workflow-execution-in-python
title: How to Schedule a Workflow Execution in Python
sidebar_label: Schedule a Workflow Execution
description: Use the `create_schedule()` asynchronous method on the Client.
lines: 18-41
@dac """

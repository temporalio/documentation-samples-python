import asyncio

from temporalio.client import (
    Client,
)


async def main():
    client = await Client.connect("localhost:7233")
    """
    To describe a Scheduled Workflow Execution in Python, use the [describe()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#delete) asynchronous method on the Schedule Handle.
    You can get a complete list of the attributes of the Scheduled Workflow Execution from the [ScheduleDescription](https://python.temporal.io/temporalio.client.ScheduleDescription.html) class.
    """
    handle = client.get_schedule_handle(
        "workflow-schedule-id",
    )
    desc = await handle.describe()
    print(f"Scheduled Workflow Id: {desc.schedule.action.workflow}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-describe-a-scheduled-workflow-execution-in-python
title: How to describe a Scheduled Workflow Execution in Python
sidebar_label: Describe a Scheduled Workflow Execution
description: Use the `describe()` asynchronous method on the Schedule Handler.
lines: 11-18
@dac """

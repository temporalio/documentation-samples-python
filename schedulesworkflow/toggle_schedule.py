import asyncio
from datetime import timedelta

from temporalio.client import (
    Client,
)


async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_schedule_handle(
        "workflow-schedule-id",
    )
    """
    To toggle, or pause a Scheduled Workflow Execution in Python, use the [pause()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#pause) asynchronous method on the Schedule Handle.
    You can pass a `note` to the `pause()` method to provide a reason for pausing the schedule.
    """
    await handle.pause(note="Pausing the schedule for now")

    desc = await handle.describe()

    print(f"Describe the schedule's state: {desc.schedule.state}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-pause-a-scheduled-workflow-execution-in-python
title: How to Pause Scheduled Workflow Execution in Python
sidebar_label: Pause a Scheduled Workflow Execution
description: Use the `pause()` asynchronous method on the Schedule Handle.
lines: 14-18
@dac """

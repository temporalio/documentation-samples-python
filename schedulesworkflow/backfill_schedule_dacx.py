import asyncio
from datetime import datetime, timedelta

from temporalio.client import (
    Client,
    ScheduleBackfill,
    ScheduleOverlapPolicy,
)


async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_schedule_handle(
        "workflow-schedule-id",
    )
    now = datetime.utcnow()
    """
    To Backfill a Scheduled Workflow Execution in Python, use the [backfill()](https://python.temporal.io/temporalio.client.ScheduleHandle.html#backfill) asynchronous
    method on the Schedule Handle.
    """
    await handle.backfill(
        ScheduleBackfill(
            start_at=now - timedelta(minutes=10),
            end_at=now - timedelta(minutes=9),
            overlap=ScheduleOverlapPolicy.ALLOW_ALL,
        ),
    ),

    print(f"Result: {handle}")


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-backfill-a-scheduled-workflow-execution-in-python
title: How to backfill a Scheduled Workflow Execution in Python
sidebar_label: Backfill a Scheduled Workflow Execution
description: Use the `backfill()` asynchronous method on the Schedule Handler.
lines: 19-29
@dac """

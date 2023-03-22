import asyncio

from temporalio.client import (
    Client,
    Schedule,
    ScheduleActionStartWorkflow,
    ScheduleCalendarSpec,
    ScheduleRange,
    ScheduleSpec,
    ScheduleState,
)

from your_workflows import YourSchedulesWorkflow


async def main():
    client = await Client.connect("localhost:7233")
    """
    To create a Scheduled Workflow Execution in Python, use the [create_schedule()](https://python.temporal.io/temporalio.client.Client.html#create_schedule)
    asynchronous method on the Client.
    Then pass the Schedule ID and the Schedule object to the method to create a Scheduled Workflow Execution.
    Set the `action` parameter to `ScheduleActionStartWorkflow` to start a Workflow Execution.
    Optionally, you can set the `spec` parameter to `ScheduleSpec` to specify the schedule or set the `intervals` parameter to `ScheduleIntervalSpec` to specify the interval.
    Other options include: `cron_expressions`, `skip`, `start_at`, and `jitter`.
    """
    await client.create_schedule(
        "workflow-schedule-id",
        Schedule(
            action=ScheduleActionStartWorkflow(
                YourSchedulesWorkflow.run,
                "my schedule arg",
                id="schedules-workflow-id",
                task_queue="my-task-queue",
            ),
            spec=ScheduleSpec(
                calendars=[
                    ScheduleCalendarSpec(
                        second=(ScheduleRange(1, step=1),),
                        minute=(ScheduleRange(2, 3),),
                        hour=(ScheduleRange(4, 5, 6),),
                        day_of_month=(ScheduleRange(7),),
                        month=(ScheduleRange(9),),
                        year=(ScheduleRange(2080),),
                        # day_of_week=[ScheduleRange(1)],
                        comment="spec comment 1",
                    )
                ],
                # intervals=[
                #    ScheduleIntervalSpec(
                #        every=timedelta(days=10),
                #        offset=timedelta(days=2),
                #    )
                # ],
                # cron_expressions=["0 12 * * MON"],
                # skip=[ScheduleCalendarSpec(year=(ScheduleRange(2050),))],
                # start_at=datetime(2060, 7, 8, 9, 10, 11, tzinfo=timezone.utc),
                # jitter=timedelta(seconds=80),
            ),
            state=ScheduleState(
                note="Here's a note on my Scheduled Workflows", paused=False
            ),
        ),
    ),


if __name__ == "__main__":
    asyncio.run(main())


""" @dac
id: how-to-schedule-a-workflow-execution-in-python
title: How to Schedule a Workflow Execution in Python
sidebar_label: Schedule a Workflow Execution
description: Schedule a Workflow Execution in the Python SDK.
lines: 18-64
@dac """

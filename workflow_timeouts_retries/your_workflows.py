from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import your_activity, YourParams

"""dacx
dacx"""


@workflow.defn
class YourWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            your_activity,
            YourParams("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )


""" @dacx
id: how-to-spawn-an-activity-execution-in-python
title: How to spawn an Activity Execution in Python
label: Activity Execution
description: Use the `execute_activity()` operation from within your Workflow Definition.
lines: 3, 9-18, 47-55
@dacx """

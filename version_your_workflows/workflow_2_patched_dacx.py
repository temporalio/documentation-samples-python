from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import post_patch_activity, pre_patch_activity
"""dacx
To patch a Workflow, you must set the [patched()](https://docs.temporal.io/docs/python/workflows#patched) function on the Workflow and pass an identifier for the patch.
The code cannot be replaying.
dacx"""


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self) -> None:
        if workflow.patched("my-patch"):
            self._result = await workflow.execute_activity(
                post_patch_activity,
                schedule_to_close_timeout=timedelta(minutes=5),
            )
        else:
            self._result = await workflow.execute_activity(
                pre_patch_activity,
                schedule_to_close_timeout=timedelta(minutes=5),
            )

    @workflow.query
    def result(self) -> str:
        return self._result


""" @dacx
id: how-to-patch-a-workflow-definition-in-python
title: How to Patch a Workflow Definition in Python
label: Patch a Workflow Definition
description: Set the patched() function on the Workflow.
tags: version, python sdk, code sample
lines: 3, 13-21
@dacx """

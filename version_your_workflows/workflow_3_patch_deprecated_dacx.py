from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import post_patch_activity
"""dacx
To deprecate a Workflow, you must set the [deprecate_patch()](https://docs.temporal.io/docs/python/workflows#deprecate_patch) function on the Workflow and pass original `patched()` identifier to this function.
dacx"""


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self) -> None:
        workflow.deprecate_patch("my-patch")
        self._result = await workflow.execute_activity(
            post_patch_activity,
            schedule_to_close_timeout=timedelta(minutes=5),
        )

    @workflow.query
    def result(self) -> str:
        return self._result


""" @dacx
id: how-to-mark-a-workflow-definition-as-deprecated-in-python
title: How to mark a Workflow Definition as deprecated in Python
label: Mark a Workflow Definition as deprecated
description: Set the deprecated_patch() function on the Workflow.
tags: version, python sdk, code sample
lines: 3, 12-20
@dacx """

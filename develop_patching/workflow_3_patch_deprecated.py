from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import (
        SsnTraceInput,
        federal_background_check_activity,
        ssn_trace_activity,
    )


@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self, input: SsnTraceInput) -> str:
        workflow.deprecate_patch("my-patch")
        # Updated logic after patch deprecation
        results = await workflow.execute_activity(
            ssn_trace_activity,
            input,
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        if results == "pass":
            return await workflow.execute_activity(
                federal_background_check_activity,
                input,
                schedule_to_close_timeout=timedelta(seconds=5),
            )
        else:
            return results
"""dacx
The `deprecate_patch()` function marks a Workflow as having moved beyond the patch. It signifies that the old code path is now obsolete and can be safely removed.

In this stage, the Workflow indicates that the patch "my-patch" is no longer applicable. All Workflows relying on the old code path are completed, and the Workflow permanently transitions to the updated logic.
dacx"""

""" @dacx
id: workflow-patching-deprecating
title: Deprecating Patches in Workflows
sidebar_label: Deprecating Patches
description: Discusses the significance and methodology of deprecating patches in Temporal workflows
tags:
 - workflow
 - patch deprecation
 - temporal
lines: 1-36
@dacx """
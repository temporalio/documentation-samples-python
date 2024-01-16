from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import (
        SsnTraceInput,
        federal_background_check_activity,
        ssn_trace_activity,
    )
"""dacx
After deprecating the patch, the final step is to remove the conditional checks for the patch in your Workflow and deploy the updated logic as the new standard.
"""

@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self, input: SsnTraceInput) -> str:
        # Updated logic, post-patch deprecation
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
By following these steps, you can effectively manage updates to your Workflow, ensuring compatibility and determinism throughout its lifecycle.

Patching and deprecating patches in Temporal allow for dynamic updates to Workflows while maintaining deterministic behavior.
This process ensures that Workflows can evolve without disrupting ongoing operations or violating the principles of determinism.
dacx"""

""" @dacx
id: workflow-patching-finalizing
title: Finalizing Workflow Updates
sidebar_label: Finalizing Updates
description: Describes the final steps in the workflow patching process in Temporal, focusing on the removal of old code and adoption of new logic.
tags:
 - workflow
 - update
 - temporal
lines: 1-38
@dacx """
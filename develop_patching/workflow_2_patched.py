import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
  from activities import (
    SsnTraceInput,
    federal_background_check_activity,
    ssn_trace_activity,
  )

"""dacx
To update the Workflow, the `workflow.patched()` API is used.
A patch named "my-patch" is introduced to execute new logic if the patch is applied.
This allows the Workflow to either execute new logic with additional activity checks or retain the original logic.
dacx"""

@workflow.defn
class BackgroundCheck:
  @workflow.run
  async def run(self, input: SsnTraceInput) -> str:
    if workflow.patched("my-patch"):
      # New logic after patch application
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
    else:
      results = await workflow.execute_activity(
        ssn_trace_activity,
        input,
        schedule_to_close_timeout=timedelta(seconds=5),
      )
      await asyncio.sleep(360)
      return results

"""dacx
In this implementation, the Workflow checks if "my-patch" has been applied. If it has, the Workflow executes the new logic; otherwise, it continues with the original logic.

This structure enables your patched Workflows to seamlessly transition between the new and old logic based on the patch's application status.
dacs"""

""" @dacx
id: workflow-patching-applying
title: Applying Patches to Workflows
sidebar_label: Applying Patches
description: Provides insights into the process of applying patches to Temporal workflows, highlighting changes and transitions.
tags:
  - guide-python-temporal
  - applying-patches
lines: 1-51
@dacx """

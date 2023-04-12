from datetime import timedelta

from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    from your_activities_dacx import your_activity
    from your_dataobject_dacx import YourParams

"""dacx
To spawn an Activity Execution, use the [`execute_activity()`](https://python.temporal.io/temporalio.workflow.html#execute_activity) operation from within your Workflow Definition.

`execute_activity()` is a shortcut for [`start_activity()`](https://python.temporal.io/temporalio.workflow.html#start_activity) that waits on its result.

To get just the handle to wait and cancel separately, use `start_activity()`.
In most cases, use `execute_activity()` unless advanced task capabilities are needed.

A single argument to the Activity is positional. Multiple arguments are not supported in the type-safe form of `start_activity()` or `execute_activity()` and must be supplied by the `args` keyword argument.
dacx"""

"""dacx
You can customize the Workflow name with a custom name in the decorator argument. For example, `@workflow.defn(name="your-workflow-name")`. If the name parameter is not specified, the Workflow name defaults to the function name.
dacx"""

@workflow.defn(name="YourWorkflow")
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
lines: 3, 10-19, 25-33
@dacx """


""" @dacx
id: how-to-customize-workflow-type-in-python
title: How to customize Workflow types in Python
label: Customize Workflow types
description: Customize Workflow types.
lines: 3, 21-23, 25-33
@dacx """

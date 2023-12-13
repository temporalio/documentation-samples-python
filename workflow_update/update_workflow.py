from temporalio import workflow

"""dacx
Workflow Updates handlers are methods in your Workflow Definition designed to handle updates.
These updates can be triggered during the lifecycle of a Workflow Execution.

**Define an Update Handler**

To define an update handler, use the [@workflow.update](https://python.temporal.io/temporalio.workflow.html#update) decorator on a method within your Workflow. This decorator can be applied to both asynchronous and synchronous methods.

- **Decorator Usage:** Apply `@workflow.update` to the method intended to handle updates.
- **Overriding:** If a method with this decorator is overridden, the overriding method should also be decorated with `@workflow.update`.
- **Validator Method:** Optionally, you can define a validator method for the update handler. This validator is specified using `@update_handler_method_name.validator` and is invoked before the update handler.
- **Method Parameters:** Update handlers should only use positional parameters. For non-dynamic methods, it's recommended to use a single parameter that is an object or data class, which allows for future expansion of fields.
- **Return Values:** The update handler can return a serializable value. This value is sent back to the caller of the update.
dacx"""


@workflow.defn
class HelloWorldWorkflow:
    is_complete = False

    @workflow.run
    async def run(self) -> str:
        await workflow.wait_condition(lambda: self.is_complete)
        return "Hello, World!"

    # Send an update request to the workflow and wait for it to complete.
    @workflow.update
    async def update_workflow_status(self) -> str:
        self.is_complete = True
        return "Workflow status updated"


""" @dacx
id: how-to-define-an-update-in-python
title: How to define an Update
label: Define Update
description: Define an Update by giving it a name to identify it.
tags:
 - python sdk
 - code sample
 - workflow
 - update
lines: 3-16, 29-32
@dacx """

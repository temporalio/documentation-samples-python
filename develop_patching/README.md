## Managing Workflow Code Updates in Temporal with Deterministic Principles

### Introduction to Workflow Updates

Making updates to running Workflow happens, and patching Workflow code is a technique you can use that allows for continuous development and fixes while upholding the crucial principle of determinism, ensuring that Workflows remain predictable and reliable throughout their lifecycle.

When updating Workflow code in Temporal, a key challenge is to maintain determinism.
Determinism in Workflow systems ensures that a workflow, when replayed with the same inputs, will always produce the same outputs.
This is crucial for the reliability and predictability of Workflows, especially when they're long-running and subject to updates.

### Strategies for Workflow Code Updates

The Patching API in Temporal is designed to allow you to change Workflow Definitions without causing non-deterministic behavior in current long-running Workflows.
However, there are situations where you might not need to use the Patching API, if your Workflow Executions are short-lived, and you don't need to preserve your currently running Workflow Executions, you can simply terminate all the currently running Workflow Executions and suspend new ones from being created while you deploy the new version of your Workflow code.
After the deployment, you can resume Workflow creation.

The Patching API is particularly useful when you need to update Workflow Definition logic that still has running Workflow Executions that depend on it.

#### For Short-Lived Workflows

**Versioning by Workflow Type**: If your Workflow is short-lived and frequently updated, a straightforward approach is versioning. By simply appending a version number to your Workflow Type, you can manage updates seamlessly. For instance:

```python
@workflow.defn
class BackgroundWorkflow01():
    # initial logic

@workflow.defn
class BackgroundWorkflow02():
    # Updated logic
```

#### For Long-Running Workflows

**Using the Patching API**: For longer-running workflows, the Patching API in Temporal becomes essential. This tool allows for updates while preserving the deterministic nature of the workflow.

### Deep Dive into Patching

Patching is a method that lets you modify Workflow Definitions without breaking the deterministic behavior of ongoing workflows. It's particularly vital in environments where Workflows need to operate without interruption.

#### Stages of the Patching process

The following list presents the general stages of patching a Workflow:

1. **Initial code stage**: Represents the existing Workflows's current state.
2. **Patching stage**: Introduces and tests new changes alongside the original workflow, ensuring deterministic behavior is maintained.
3. **Deprecation stage**: Involves marking the old code for removal after ensuring the new changes are stable and deterministic.
4. **Patch complete stage**: Occurs when all Workflows have transitioned to the updated code, fully operating on the new, deterministic logic.

### Implementing Patching: How and Why

- **Purpose of Patching**:
  - **Feature Updates**: To add or improve features while maintaining determinism.
  - **Bug Fixes**: To address issues in the Workflow without disrupting its deterministic nature.
- **Process of Patching**: The approach is designed to allow updates without causing disruptions, ensuring the ongoing Workflows remain deterministic and reliable.

## Building a Resilient Workflow with Data Classes

### Initial Steps for Resilience

To create a resilient Workflow without necessitating versioning, start by implementing a data class.
Data classes provide compatibility and flexibility for your Workflow's inputs and outputs.
This approach future-proofs your Workflow against changes in data requirements.

#### Example: Adapting to New Data Types

Consider a background check application where, initially, only a social security number is required:

```python
@dataclass
class SsnTraceInput:
    ssn: str
```

As your application evolves, you might need to include additional data types like phone number, first name, and last name. Updating the `SsnTraceInput` data class to include these new fields is straightforward and ensures backward compatibility.

Using dataclasses for input and output parameters in Temporal Workflows helps future-proof them for a few reasons:

- Versioning support: If you add a new field to a dataclass, Temporal will automatically handle passing default values to older Workflow versions. This prevents breaking changes.
- Type safety: Dataclasses provide type safety for your parameters.
- Immutability: Dataclasses are immutable by default. This helps avoid accidental mutations of inputs and outputs within workflows.
- Serialization: Dataclasses work nicely with Temporal's use of JSON for serialization. Parameters get automatically serialized/deserialized without extra effort.

### Transitioning to Patching for Workflow Updates

Despite the flexibility offered by data classes, there will be scenarios where adding a new activity or logic to your Workflow is necessary.
In such cases, the Patching API becomes invaluable, especially for updates to long-running Workflows.

#### Patching API: Preserving Determinism

The Patching API in Temporal enables changes to Workflow Definitions while maintaining deterministic behavior in ongoing Workflows.

The `patched()` function plays a critical role in facilitating smooth transitions between old and new code paths. It returns true in two scenarios:

- During Non-Replay Operations: When the Workflow is running in real-time (not replaying), indicating that the newer logic path should be executed.
- During Replay with Patch Awareness: When the Workflow is replaying and has previously encountered this patch, ensuring continuity in logic flow.

#### Implementing the Patching Process

Patching a Workflow in Temporal is a sophisticated method to update Workflow logic while maintaining determinism. This process is particularly crucial when you need to introduce new logic paths in long-running workflows.

##### Initial Workflow Logic

Imagine your initial Workflow includes a sleep function, but now you need to add more logic:

```python
@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self, ssn: str) -> str:
        results = await workflow.execute_activity(
            ssn_trace_activity,
            SsnTraceInput(ssn=ssn),
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        await asyncio.sleep(360)
        return results
```

##### Applying the Patch

To update your Workflow, use the `workflow.patched()` API. Introduce a patch name as a string identifier for the update. This allows the Workflow to execute new logic if the patch is applied, while retaining the original logic otherwise:

```python
@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self) -> None:
        # New logic after patch is applied
        if workflow.patched("my-patch")
            results = await workflow.execute_activity(
                ssn_trace_activity,
                SsnTraceInput(ssn=ssn),
                schedule_to_close_timeout=timedelta(seconds=5),
            )
            if results == "pass":
                return await workflow.execute_activity(
                    federal_background_check_activity,
                    SsnTraceInput(ssn=ssn),
                    schedule_to_close_timeout=timedelta(seconds=5),
                )
            else:
                return results
        else:
            # Existing logic before patch
            results = await workflow.execute_activity(
                    ssn_trace_activity,
                    SsnTraceInput(ssn=ssn),
                    schedule_to_close_timeout=timedelta(seconds=5),
                )
                await asyncio.sleep(360)
                return results

```

In this implementation, the Workflow checks if "my-patch" has been applied. If it has, the Workflow executes the new logic; otherwise, it continues with the original logic.


This structure enables your patched Workflows to seamlessly transition between the new and old logic based on the patch's application status.

##### Deprecating the Patch

Once all instances of the Workflow that would run the old code have completed, and there is certainty that they will never be queried again, it’s time to use deprecate_patch(). This method marks the patch as deprecated, signifying the complete transition to the new logic and the removal of the old code path.

```python
@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self) -> None:
        # Updated logic after patch deprecation
        workflow.deprecate_patch("my-patch")
        results = await workflow.execute_activity(
                ssn_trace_activity,
                SsnTraceInput(ssn=ssn),
                schedule_to_close_timeout=timedelta(seconds=5),
            )
            if results == "pass":
                return await workflow.execute_activity(
                    federal_background_check_activity,
                    SsnTraceInput(ssn=ssn),
                    schedule_to_close_timeout=timedelta(seconds=5),
                )
            else:
                return results
```

The `deprecate_patch()` function marks a Workflow as having moved beyond the patch. It signifies that the old code path is now obsolete and can be safely removed.

In this stage, the Workflow indicates that the patch "my-patch" is no longer applicable. All Workflows relying on the old code path are completed, and the Workflow permanently transitions to the updated logic.

##### Finalizing the Workflow Update

After deprecating the patch, the final step is to remove the conditional checks for the patch in your Workflow and deploy the updated logic as the new standard.

```python
@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self) -> None:
        # Updated logic, post-patch deprecation
        results = await workflow.execute_activity(
            ssn_trace_activity,
            SsnTraceInput(ssn=ssn),
            schedule_to_close_timeout=timedelta(seconds=5),
        )
        if results == "pass":
            return await workflow.execute_activity(
                federal_background_check_activity,
                SsnTraceInput(ssn=ssn),
                schedule_to_close_timeout=timedelta(seconds=5),
            )
        else:
            return results
```

By following these steps, you can effectively manage updates to your Workflow, ensuring compatibility and determinism throughout its lifecycle.

Patching and deprecating patches in Temporal allow for dynamic updates to Workflows while maintaining deterministic behavior.
This process ensures that Workflows can evolve without disrupting ongoing operations or violating the principles of determinism.

# Schedules README

- [x] create: Creates a new Schedule. Newly created Schedules return a Schedule ID to be used in other Schedule commands.
- [x] backfill: Executes Actions ahead of their specified time range.
- [x] delete: deletes a Schedule. Deleting a Schedule does not affect any Workflows started by the Schedule.
- [x] describe: shows the current Schedule configuration. This command also provides information about past, current, and future Workflow Runs.
- [x] list: lists all Schedule configurations. Listing Schedules in Standard Visibility will only provide Schedule IDs.
- [x] toggle: (pause in python) can pause and unpause a Schedule.
- [x] trigger: triggers an immediate action with a given Schedule. By default, this action is subject to the Overlap Policy of the Schedule.
- [x] update: updates an existing Schedule.


```bash
python3 run_worker.py
```

```bash
python3 run_workflow.py
python3 delete_workflow.py
python3 toggle_workflow.py
python3 update_workflow.py
```

## Terminate

```bash
temporal workflow terminate --workflow-id=schedules-workflow-id
```
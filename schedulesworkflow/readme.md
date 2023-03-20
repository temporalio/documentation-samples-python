# Schedules README

- [x] create: Creates a new Schedule. Newly created Schedules return a Schedule ID to be used in other Schedule commands.
- [x] backfill: Executes Actions ahead of their specified time range.
- [x] delete: deletes a Schedule. Deleting a Schedule does not affect any Workflows started by the Schedule.
- [x] describe: shows the current Schedule configuration. This command also provides information about past, current, and future Workflow Runs.
- [x] list: lists all Schedule configurations. Listing Schedules in Standard Visibility will only provide Schedule IDs.
- [x] toggle: (pause in python) can pause and unpause a Schedule.
- [x] trigger: triggers an immediate action with a given Schedule. By default, this action is subject to the Overlap Policy of the Schedule.
- [x] update: updates an existing Schedule.

1. Start your Worker

```bash
poetry run python run_worker.py
```

2. Run your Workflow

```bash
poetry run python start_schedules.py
poetry run python delete_schedule.py
poetry run python describe_schedule.py
poetry run python toggle_schedule.py
poetry run python update_schedule.py
python3 update_workflow.py
```

## Delete Scheduled Workflow

To delete a Scheduled Workflow, start the Schedules then run the `delete_schedule` module.

```bash
poetry run python start_schedules.py
poetry run python delete_schedule.py
```

<!--
Or use the Temporal CLI.

```bash
temporal schedule delete --schedule-id=workflow-schedule-id
```
-->

## Describe a Scheduled Workflow

To describe a Scheduled Workflow, start the Schedules then run the `describe_schedule` module.

```bash
poetry run python start_schedules.py
poetry run python describe_schedule.py
```

## Toggle a Scheduled Workflow

To toggle or pause a Scheduled Workflow, start the Schedule then run the `toggle_schedule` module.

```bash
poetry run python start_schedules.py
poetry run python toggle_schedule.py
```


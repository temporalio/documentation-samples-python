"""
temporal workflow start \
 --task-queue backgroundcheck-boilerplate-task-queue-local \
 --type BackgroundCheck \
 --input '{"ssn": "123456789"}' \
 --namespace backgroundcheck_namespace \
 --workflow-id backgroundcheck_workflow
"""

"""
temporal workflow terminate --workflow-id backgroundcheck_workflow \
   --namespace backgroundcheck_namespace
"""
# from huey.contrib.djhuey import db_task
# from shell import execute_commands


# @db_task()
# def task_execute_action(project, actions):

#     commands_to_execute = []

#     if project.workspace:
#         commands_to_execute.append(f'cd {project.workspace}')

#     for action in actions:
#         commands_to_execute.extend(action.script.splitlines())
#         (output, exit_code) = execute_commands(commands_to_execute)
#         if exit_code != 0:
#             print ('Some error has occurred')
#             print (output)
#         else:
#             print (output)

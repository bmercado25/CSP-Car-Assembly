# -*- coding: utf-8 -*-
"""car assembly

Automatically generated by Colaboratory.

"""

!pip install python-constraint

'''
Car Assembly solver CSP by Brent Mercado

note: this problem requires the python-constraint library. It can be installed using: !pip install python-constraint

Car assembly program outputs a schedule with task start times and corresponding worker assignment according to the given constraints.

Limitations:
- Solver function in this library is not perfect and has some faults, atleast for this current setup
- Worker assignment function can be improved upon

'''
from constraint import Problem, AllDifferentConstraint

def assign_workers(schedule):
    workers = ["Worker 1", "Worker 2", "Worker 3", "Worker 4"]
    worker_assignments = {}

    sorted_tasks = sorted(schedule.items(), key=lambda x: x[1])

    for i, (task, start_time) in enumerate(sorted_tasks):
        assigned_worker = workers[i % len(workers)]
        worker_assignments[task] = assigned_worker

    return worker_assignments

def car_assembly_csp():
    tasks = [
        "AxleF", "AxleB", "WheelRF", "WheelLF", "WheelRB", "WheelLB",
        "NutRF", "NutLF", "NutRB", "NutLB", "CapRF", "CapRLF", "CapRB", "CapLB", "Inspection"
    ]

    problem = Problem()

    for task in tasks:
        problem.addVariable(task, range(26)) #based on the nature of the library, setting domain to 26 minutes forces solver to put 1st task at minute 0




    # precedence constraints
    problem.addConstraint(AllDifferentConstraint(), ("AxleF", "AxleB")) #disjunctive constraint for front and back axle
    problem.addConstraint(lambda AxleF, WheelRF: AxleF + 10 <= WheelRF, ("AxleF", "WheelRF"))
    problem.addConstraint(lambda AxleF, WheelLF: AxleF + 10 <= WheelLF, ("AxleF", "WheelLF"))
    problem.addConstraint(lambda AxleB, WheelRB: AxleB + 10 <= WheelRB, ("AxleB", "WheelRB"))
    problem.addConstraint(lambda AxleB, WheelLB: AxleB + 10 <= WheelLB, ("AxleB", "WheelLB"))

    problem.addConstraint(lambda WheelRF, NutRF: WheelRF + 1 <= NutRF, ("WheelRF", "NutRF"))
    problem.addConstraint(lambda WheelLF, NutLF: WheelLF + 1 <= NutLF, ("WheelLF", "NutLF"))
    problem.addConstraint(lambda WheelRB, NutRB: WheelRB + 1 <= NutRB, ("WheelRB", "NutRB"))
    problem.addConstraint(lambda WheelLB, NutLB: WheelLB + 1 <= NutLB, ("WheelLB", "NutLB"))

    problem.addConstraint(lambda NutRF, CapRF: NutRF + 2 <= CapRF, ("NutRF", "CapRF"))
    problem.addConstraint(lambda NutLF, CapRLF: NutLF + 2 <= CapRLF, ("NutLF", "CapRLF"))
    problem.addConstraint(lambda NutRB, CapRB: NutRB + 2 <= CapRB, ("NutRB", "CapRB"))
    problem.addConstraint(lambda NutLB, CapLB: NutLB + 2 <= CapLB, ("NutLB", "CapLB"))
    problem.addConstraint(lambda AxleF, AxleB: AxleF + 10 <= AxleB, ("AxleF", "AxleB"))

    wheel_installation_tasks = ["WheelRF", "WheelLF", "WheelRB", "WheelLB"]
    for wheel1, wheel2 in zip(wheel_installation_tasks[:-1], wheel_installation_tasks[1:]):
        problem.addConstraint(lambda w1, w2: w1 + 1 <= w2, (wheel1, wheel2))

    lug_nut_tasks = ["NutRF", "NutLF", "NutRB", "NutLB"]
    for wheel, nut in zip(wheel_installation_tasks, lug_nut_tasks):
        problem.addConstraint(lambda w, n: w + 2 <= n, (wheel, nut))

    solution = problem.getSolution()

    worker_assignments = assign_workers(solution)

    if solution:
        print("Optimal Schedule:")
        for task, start_time in solution.items():
            print(f"{task}: {start_time} minutes - {worker_assignments[task]}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    car_assembly_csp()
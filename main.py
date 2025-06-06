from datetime import datetime
from enum import Enum
import json,os
from abc import ABC,abstractmethod

class TaskStatus(Enum):
	TO_DO = 'to_do'
	IN_PROGRESS = 'in-progress'
	DONE = "done"

class Task:
	counter_id = 1
	def __init__(self,description):
		self.id = Task.counter_id 
		Task.counter_id += 1
		self.description = description
		self.status = TaskStatus.TO_DO
		self.created_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		self.updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

	def to_dict(self):
		return {
			"id": self.id,
			"description": self.description,
			"status": self.status.value,
			"created_at": self.created_at,
			"updated_at": self.updated_at
		}
	@classmethod
	def from_dict(cls, data):
		task = cls(data["description"])
		task.id = data["id"]
		task.status = TaskStatus(data["status"])
		task.created_at = data["created_at"]
		task.updated_at = data["updated_at"]
		return task

class ReportGenerator(ABC):
	@abstractmethod
	def generate(self, tasks:dict) -> str:
		pass

class JSONReportGenerator(ReportGenerator):
	def generate(self, tasks: dict):
		return json.dumps(tasks,indent=2)
		
class ReportWriter(ABC):
	@abstractmethod
	def write(self,report:str, filename:str='task_list'):
		pass

class JSONReportWriter(ReportWriter):
	def write(self, report: str, filename: str = 'task_list'):
		try:
			with open(f"{filename}.json", 'w') as f:
				f.write(report)		
			print(f"Report saved to {filename}.json")
		except IOError:
			print("Error: Could not save report")

class TaskManager:
	def __init__(self, report_generator:ReportGenerator, report_writer:ReportWriter):
		self.tasks = {}
		self.report_generator = report_generator
		self.report_writer = report_writer
		if os.path.exists("task_list.json"):
			with open("task_list.json", 'r') as f:
				task_dict = json.load(f)
				for task_id,task_data in task_dict.items():
					self.tasks[int(task_id)] = Task.from_dict(task_data)
			if self.tasks:
				Task.counter_id = max(self.tasks.keys())+1
			else:
				Task.counter_id = 1
			print(f"task counter_id set to{Task.counter_id}")

	def add_task(self,line:list):
		description = ' '.join(line).lower()
		task = Task(description)
		self.tasks[task.id] = task
		print(f"Task added successfully with ID {task.id}")

	def list_all_tasks(self):
		if not self.tasks:
			print("task list is empty")
			return
		print(f"{"ID":<4}{"Description":<20}{"Status":<15}{"created at":<20}{"updated at":<20}")
		for task_id,task in self.tasks.items():
			print(f"{task_id:<4}{task.description:<20}{task.status.value:<15}{task.created_at:<20}{task.updated_at:<20}")

	def list_by_status(self,status:str):
		matches = [(task_id,task) for task_id,task in self.tasks.items() if task.status.value == status]
		if not self.tasks:
			print("task list is empty")
			return
		if not matches:
			print(f"no task found for status{status}")

		print(f"{"ID":<4}{"Description":<20}{"Status":<15}{"created at":<20}{"updated at":<20}")
		for task_id,task in matches:
				print(f"{task_id:<4}{task.description:<20}{task.status.value:<15}{task.created_at:<20}{task.updated_at:<20}")
			
	def update_status(self,task_id,new_status):
		if task_id not in self.tasks:
			raise ValueError(f"task #{task_id} doesn't exist")
		try:
			self.tasks[task_id].status = TaskStatus(new_status)
			self.tasks[task_id].updated_at = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		except ValueError:
			print("task id no founded")

	def to_json_dict(self):
		tasks_list = {str(task_id):task.to_dict()
		for task_id,task in self.tasks.items()}
		return tasks_list
	
	def generate_report(self):
		report = self.report_generator.generate(self.to_json_dict())
		self.report_writer.write(report)

	def delete_task(self, task_id):
		if task_id not in self.tasks:
			raise ValueError(f"task #{task_id} doesn't exist")
		del self.tasks[task_id]

def main():
	client = TaskManager(JSONReportGenerator(),JSONReportWriter())
	while True:
		try:
			command, *line = input("Que Desea hacer: ").split()
			if command.lower() == "add":
				if not line:
					print("description required")
				else:
					client.add_task(line)
			elif command.lower() == "list":
					while True:
						option = int(input("Select status:\n1) all\n2) done\n3) in-progress\n4)to_do\n: "))
						if option == 1:
							client.list_all_tasks()
							break
						elif option == 2:
							client.list_by_status('done')
							break
						elif option == 3:
							client.list_by_status('in-progress')
							break
						elif option == 4:
							client.list_by_status('to_do')
							break
						else:
							print("select a valid option above")
			elif command.lower() == 'mark':
				if not line or not line[0].isdigit():
					print("Task ID required")
				else:	
					while True:
						option = int(input("Select status:\n1) in-progress\n2) done\n: "))
						if option == 1:
							client.update_status(int(line[0]),TaskStatus.IN_PROGRESS.value)
							break
						elif option == 2:
							client.update_status(int(line[0]),TaskStatus.DONE.value)
							break
						else:
							print("select a valid option above")
			elif command.lower() == 'delete':
				if not line or not line[0].isdigit():
					print("Task ID required")
				else:
					client.delete_task(int(line[0]))
			elif command.lower() == 'exit':
				break
		except IOError:
			print("Invalid Input")
	client.generate_report()
main()




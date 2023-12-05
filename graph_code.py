import os
import json
import argparse

def load_data(filepath):
	if not os.path.exists(filepath):
		return ""

	with open(filepath, "r") as fp:
		return json.load(fp)


class FlowDiagram:
	SCREEN_WIDTH = 120

	def __init__(self, name):
		self.name = name
		self.entities = []
		self.connections = []
		self.block_width = 0

	def add_entity(self, entity_name):
		if entity_name not in self.entities:
			self.entities.append(entity_name)

	def add_function(self, from_ent, to_ent, func, text="", result=""):
		tup = (from_ent, to_ent, func, text, result)
		self.connections.append(tup)

	def arrange_entities(self):
		total_ents = len(self.entities)
		block_width = round(self.SCREEN_WIDTH / total_ents)
		self.block_width = block_width
		last = len(self.entities) - 1
		for i in range(len(self.entities)):
			ent = self.entities[i]
			width = block_width - len(ent)
			space = ""
			if last != i:
				space = " " * width

			print("%s%s"%(ent, space), end=" ")
		print()

		for i in range(len(self.entities)):
			space = ""
			if last != i:
				space = " " * (block_width - 1)
			print("|%s"%(space), end= " ")
		print()

	def calculate_space(self, s_index, e_index):
		space = ""

		if (s_index <= 0 or e_index <= 0):
			return space

		index = e_index
		if (e_index >= s_index ):
			index = s_index

		space = " " * index * self.block_width

		space = "|" + space
		for i in range(1, index):
			pos = i * self.block_width
			space = space[:pos] + " "*i+ "|" + space[pos:-1]
		return space

	def display(self, text, s_index, e_index):
		x = "|"
		side = e_index if e_index > s_index else s_index
		for ent_pos in range(side+1, len(self.entities)):
			x = " " * self.block_width
			x = x + "|"
			text += x
		print(text)

	def make_function(self, total_text, width, space_before, compensation):
		func_text = "|" + total_text.center(width + compensation) + "|"
		func_text = space_before + func_text
		return func_text

	def make_line(self, width, space_before, compensation,
			reverse=False):
		if (width <= 0):
			return "|"

		line_text = "-"* width
		comp_text = "-"*compensation
		if reverse:
			line_text = "|" + "<" + line_text[:-1] + comp_text + "|"
		else:
			line_text = "|" + line_text[:-1] + comp_text + ">" + "|"
		line_text = space_before + line_text
		return line_text


	def arrange_function(self, start_t, end_t, fn, text, result=""):
		reverse = False
		s_index = self.entities.index(start_t)
		e_index = self.entities.index(end_t)

		if (s_index > e_index):
			reverse = True

		compensation = (abs(e_index - s_index) - 1)
		width = abs((e_index - s_index )) * self.block_width
		space_before = self.calculate_space(s_index, e_index)
		total_text = fn
		if text:
			total_text += ": %s"%(text)

		func_text = self.make_function(total_text, width,
				space_before, compensation)
		self.display(func_text, s_index, e_index)

		line_text = self.make_line(width, space_before,
				compensation, reverse)
		if end_t:
			self.display(line_text, s_index, e_index)

		if result:
			func_text = self.make_function(result, width,
					space_before, compensation)
			self.display(func_text, s_index, e_index)

			line_text = self.make_line(width, space_before,
					compensation, True)
			self.display(line_text, s_index, e_index)

	def arrange_functions(self):
		for conn in self.connections:
			self.arrange_function(*conn)

	def parse_json_data(self, codeflow):
		func, note, result, from_c, to_c = "", "", "", "", ""
		for k, v in codeflow.items():
			func = k
			note = v["note"]
			result = v["result"]
			from_c = v["from_component"]
			to_c = v["to_component"]

			self.add_entity(from_c)
			self.add_entity(to_c)

			self.add_function(from_c, to_c, func, note, result)

	@classmethod
	def parse_args(cls):
        	parser = argparse.ArgumentParser()
        	parser.add_argument('-s', '--size', default=cls.SCREEN_WIDTH,
			help = "Screen size, default size %d"%cls.SCREEN_WIDTH)
        	return parser.parse_args()

	def show(self):
		if not self.entities:
			return;

		self.arrange_entities()
		self.arrange_functions()

	def run(self):
		load = False #TODO: Make it to true to use json file data.
		codeflow = None
		args = self.parse_args()
		if args.size:
			self.SCREEN_WIDTH = int(args.size)
		data = load_data("./code-flow.json")
		if data and load:
			codeflow = data["flow"][0]
		if codeflow:
			self.parse_json_data(codeflow)
		self.show()

if __name__ == "__main__":
	fd = FlowDiagram("Flow")
	fd.add_entity("Comp2")
	fd.add_entity("Comp3")
	fd.add_entity("Comp1")
	fd.add_entity("Comp4")

	fd.add_function("Comp2", "Comp4", "add_subscriber()",
			"init_subscriber_cb")
	fd.add_function("Comp1", "Comp3", "add_resource()",
			"init and release cb")
	fd.add_function("Comp3", "Comp4", "add_component_resource()",
			result="component resource added")
	fd.add_function("Comp3", "Comp1", "resource added")
	fd.add_function("Comp4", "Comp2", "init_subscriber_cb()")
	fd.add_function("Comp2", "Comp1", "execute init_cb")
	fd.run()

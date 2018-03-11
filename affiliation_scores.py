import pandas as pd

class MetaConst(type):
	def __getattr__(cls, key):
		return cls[key]
	def __setattr__(cls, key, value):
		raise TypeError

class Const(object, metaclass=MetaConst):
	class ConstError(TypeError): pass
	def __getattr__(self, name):
		return self[name]
	def __setattr__(self,name,value):
		raise self.ConstError("Can't rebind const({})".format(name))

class MetricConst(Const):
	method = ["conference","problem_description","goal/objective","research_method",
			"research_question","pseudocode"]
	r3_columns = method
	r3_name = "R3"
	data = ["train", "validation", "test", "results"]
	r2_columns = r3_columns + data
	r2_name = "R2"
	experiment = ["hypothesis", "prediction",
			"open_source_code", "open_experiment_code",
			"hardware_specification", "software_dependencies",
			"experiment_setup", "evaluation_criteria"]
	r1_columns = r2_columns + experiment
	r1_name = "R1"

def load_csv_data(filename="data/evaluations.csv"):
	print(f"Loading csv file {filename}...")
	file = filename
	affiliation_mapping = {'0':"academia", '1':"mixed", '2':"industry"}
	conversion_dict = {"research_type": lambda x: int(x == "E"), "affiliation": lambda x: affiliation_mapping[x]}
	evaluation_data = pd.read_csv(file, sep=",", header=0, index_col=0, converters=conversion_dict)
	print(f"Finished loading csv file. The file contains {evaluation_data.shape[0]} rows with "
		+ f"{evaluation_data.shape[1]} columns.")
	return evaluation_data

def drop_columns(dataframe, column_headers=["title", "authors", "link", "comments"]):
	print(f"Dropping columns: {column_headers}.")
	return dataframe.drop(column_headers, axis=1)

def calculate_metric(dataframe, columns, metric):
	print(f"Appending metric {metric} and {metric}D to dataframe.")
	dataframe.loc[:, metric] = dataframe[columns].all(axis=1)
	dataframe.loc[:, f"{metric}D".format(metric)] = dataframe[columns].mean(axis=1)

def calculate_metrics(dataframe):
	calculate_metric(dataframe, MetricConst.r3_columns, MetricConst.r3_name)
	calculate_metric(dataframe, MetricConst.r2_columns, MetricConst.r2_name)
	calculate_metric(dataframe, MetricConst.r1_columns, MetricConst.r1_name)
	return dataframe

def present_metric(dataframe, metric, grouped_by):
	print(dataframe[[metric, grouped_by]].groupby(grouped_by).sum())
	print(f"Combined {experiment_data[metric].sum():8d}")

def present_metric_degree(dataframe, metric, grouped_by):
	metric = f"{metric}D"
	print(dataframe[[metric, grouped_by]].groupby(grouped_by).mean())
	print(f"Combined {experiment_data[metric].mean():8.4f}")
	print("\nVariance")
	print(dataframe[[metric, grouped_by]].groupby(grouped_by).var())
	print(f"Combined {experiment_data[metric].var():8.4f}")
	

def present_metrics(dataframe, grouped_by):
	for metric in [MetricConst.r3_name, MetricConst.r2_name, MetricConst.r1_name]:
		print("\n")
		present_metric(dataframe, metric, grouped_by)
		present_metric_degree(dataframe, metric, grouped_by)


def load_experimental_papers(filename="data/evaluations.csv"):
	csv_data = load_csv_data(filename)
	csv_data = drop_columns(csv_data)
	csv_data = csv_data[csv_data.research_type == 1]
	return calculate_metrics(csv_data)

experiment_data = load_experimental_papers()

present_metrics(experiment_data, "affiliation")

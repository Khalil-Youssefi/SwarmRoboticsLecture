from model import simpleModel
from mesa.batchrunner import batch_run
from multiprocessing import freeze_support
import pandas as pd
import os
import warnings

# ------------------------------
# Model parameters
# ------------------------------
model_params = {
    "width": 20,
    "height": 20,
    "num_agents": [5,10]
}

warnings.simplefilter("ignore", category=FutureWarning)

expriment_name = "test_run"

if __name__ == '__main__':
    freeze_support()  # for Windows support
    total_num_cpus = os.cpu_count() // 2
    results = batch_run(
        simpleModel,
        parameters=model_params,
        iterations=10,
        max_steps=5000,
        number_processes=1,
        display_progress=True,
        data_collection_period=1
        )
    
    results_df = pd.DataFrame(results)
    # save to csv file with a unique name based on the date and time
    # result file name
    csv_file_name = f'{expriment_name}_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv'
    # results_path is dir of the py file
    results_path = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(results_path, csv_file_name)
    results_df.to_csv(csv_file)
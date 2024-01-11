import argparse
from config import STUDY_PARAMS
from Code.Gather import Gather

if __name__ == '__main__':
    # Set up instance for Study
    DataGather = Gather(STUDY_PARAMS)

    parser = argparse.ArgumentParser()

    parser.add_argument("--dataCollection", "-dc", choices=["gen", "h"], help="The type of data collection, 'h' for human, 'gen' for generation")

    args = parser.parse_args()



    temperature = "0.6"

    # 'h' for human data
    # 'gen' for generations
    dataCollect = 'gen'

    # Collect data in csv files
    if args.dataCollection == 'h' and STUDY_PARAMS["K_ITERATIONS"] == 1:
        #DataGather.GetHumanData()
        print("running human collection")
    elif args.dataCollection == 'gen' and STUDY_PARAMS["K_ITERATIONS"] <= 100:
        #DataGather.GetGPTData(temperature)
        print("Running generation collection")
    else:
        print("Incorrect params")
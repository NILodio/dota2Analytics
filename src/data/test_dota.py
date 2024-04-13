from open_dota import OpenDotaAPI

odota = OpenDotaAPI(output_filepath="data")

odota.get_prediction_from_input(
    [43, 19, 135, 25, 75, 70, 138, 4, 7, 9, 8574561, 2586976]
).to_csv("test.csv", index=False)

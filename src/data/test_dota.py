from open_dota import OpenDotaAPI

odota = OpenDotaAPI(output_filepath="data")
odota.get_model_features_from_input(
    [107, 74, 106, 86, 65, 110, 111, 55, 113, 103, 2586976, 8831040]
).to_csv("test_1.csv", index=False)

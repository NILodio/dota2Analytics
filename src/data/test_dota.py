from open_dota import OpenDotaAPI



data = OpenDotaAPI(output_filepath="data")
print(data._make_request("teams/9388293"))
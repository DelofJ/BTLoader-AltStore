import json, requests

def fetch_latest_release():
	try:
		response = requests.get(
			url="https://api.github.com/repos/CloudySn0w/BTLoader/releases",
			headers={
				"Accept": "application/vnd.github+json",
			}
		)
		response.raise_for_status()
		releases = response.json()
		if len(releases) == 0:
			raise ValueError(f"No release found")
		return releases[0]
	except requests.RequestException as e:
		print(f"Error fetching releases: {e}")
		raise

def main():
	try:
		with open("repo.json", "r") as file:
			data = json.load(file)
	except json.JSONDecodeError as e:
		print(f"Error reading JSON file: {e}")
		raise

	latest_release = fetch_latest_release()

	app = data["apps"][0]

	version = latest_release["tag_name"].lstrip('v')
	version_date = latest_release["published_at"]

	for file in latest_release["assets"]:
		if "bound" in file["name"].lower():
			download_url = file["browser_download_url"]
			size = file["size"]
			break
	else:
		raise ValueError("Did not find the bound ipa inside the latest release")

	app.update({
		"version": version,
		"versionDate": version_date,
		"versionDescription": f"Updated to Discord v{version}",
		"downloadURL": download_url,
		"size": size
	})
	app["versions"] = [{
		"version": app["version"],
		"date": app["versionDate"],
		"localizedDescription": app["versionDescription"],
		"downloadURL": app["downloadURL"],
		"size": app["size"]
	}]

	try:
		with open("repo.json", "w") as file:
			json.dump(data, file, indent='\t')
		print("JSON file updated successfully.")
	except IOError as e:
		print(f"Error writing to JSON file: {e}")
		raise

if __name__ == "__main__":
	main()

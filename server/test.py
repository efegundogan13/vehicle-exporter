import requests

def get_access_token():
    url = "https://api.baubuddy.de/index.php/login"
    payload = {
        "username": "365",
        "password": "1"
    }
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["oauth"]["access_token"]

def main():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    vehicles = requests.get(
        "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active",
        headers=headers
    ).json()

    for v in vehicles:
        if v.get("labelIds"):
            print("Contain first labelId vehicle:")
            print("  RNR:", v.get("rnr"))
            print("  labelIds:", v.get("labelIds"))
            break
    else:
        print("no contain")

    print("\n🟢 hu:")
    hu_contain = [v for v in vehicles if v.get("hu")]
    for v in hu_contain[:10]:
        print("  RNR:", v.get("rnr"), "| hu:", v.get("hu"))

    print("\n Tool containing both hu and labelIds:")
    combined = [v for v in vehicles if v.get("hu") and v.get("labelIds")]
    if combined:
        for v in combined:
            print("  RNR:", v.get("rnr"), "| hu:", v.get("hu"), "| labelIds:", v.get("labelIds"))
    else:
        print("No vehicles were found matching this combination.")

if __name__ == "__main__":
    main()

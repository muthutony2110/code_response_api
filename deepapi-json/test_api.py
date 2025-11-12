import requests

def read_prompt_from_file(filename="input_code.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ File '{filename}' not found.")
        return ""

def main():
    url = "http://127.0.0.1:5000/generate"
    prompt = read_prompt_from_file()

    if not prompt.strip():
        print("❗ No prompt to send.")
        return

    try:
        response = requests.post(url, json={"prompt": prompt})
        if response.status_code == 200:
            result = response.json().get("response", "")
            print("\n🤖 Response:\n")
            print(result)
        else:
            print(f"\n❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"\n🚨 Request failed: {str(e)}")

if __name__ == "__main__":
    main()

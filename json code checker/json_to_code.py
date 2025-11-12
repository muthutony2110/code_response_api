import json
import os

def main():
    input_folder = "input_json"  # Folder where your .json file lives
    input_filename = "example.json"  # Change this to match your file
    input_path = os.path.join(input_folder, input_filename)

    output_filename = "generated_code.py"
    output_path = os.path.join(os.getcwd(), output_filename)

    if not os.path.exists(input_path):
        print(f"❌ JSON file not found at: {input_path}")
        return

    try:
        # Load JSON file
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        code = data.get("code", "")

        if not code:
            print("⚠️ 'code' key not found or is empty in the JSON.")
            return

        # Delete existing output file
        if os.path.exists(output_path):
            os.remove(output_path)
            print("🗑️ Previous generated code file deleted.")

        # Save new code
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"✅ Code saved to: {output_path}")

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()

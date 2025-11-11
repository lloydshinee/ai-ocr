import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Folder containing all your timecard images
timesheets_folder = "./wet"

# Output file
output_file = "wet.txt"

# OCR extraction prompt
prompt = """
You are an OCR and data extraction assistant.

Extract information from the provided image of a time card or attendance record.
Return the output strictly in valid JSON format with the following structure:

{
  "employee_information": {
    "employee_number": "",
    "name": "",
    "department": "",
    "payroll_type": "",
    "period": ""
  },
  "attendance_records": [
    {
      "date": "",
      "time_in_am": "",
      "time_out_am": "",
      "time_in_pm": "",
      "time_out_pm": ""
    }
  ]
}

Rules:
- Do NOT include any entries that have completely empty time fields.
- Exclude the "other_fields" object entirely.
- The "date" field should contain the day number (e.g., "13") or full date if readable.
- Remove any "day" field entirely — only use "date".
- Keep JSON clean and properly formatted (no markdown, no explanations).
- Preserve exact text values from the image.
- All missing values should be empty strings.
- Output must be valid JSON only.
"""

# Collect all image files
image_files = [
    os.path.join(timesheets_folder, f)
    for f in os.listdir(timesheets_folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
]

if not image_files:
    raise FileNotFoundError(f"No image files found in {timesheets_folder}")

print(f"🔍 Found {len(image_files)} timecards to process...\n")

# Clear previous output file
open(output_file, "w").close()

# Process each image
for idx, image_path in enumerate(image_files, start=1):
    print(f"📄 Processing {os.path.basename(image_path)} ({idx}/{len(image_files)})...")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Send image + prompt to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            prompt
        ],
        config={"response_mime_type": "application/json"}
    )

    # Append result to output file
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(f"### {os.path.basename(image_path)} ###\n")
        f.write(response.text.strip())
        f.write("\n\n")

print(f"\n✅ All {len(image_files)} timecards processed successfully!")
print(f"📁 Results saved in: {output_file}")

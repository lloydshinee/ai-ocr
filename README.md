# AI-Powered OCR for Time Cards

This project uses Google's Gemini Pro Vision model to perform Optical Character Recognition (OCR) on time card images and extract employee information in a structured JSON format.

## How It Works

The Python script (`main.py`) manages the OCR process by:

1.  **Looping through images:** It iterates through all image files (JPEG, PNG) found in a specified input folder (e.g., `crumpled/`, `folded/`, `normal/`).
2.  **Advanced Prompting:** For each image, it constructs a detailed prompt that instructs the Gemini Pro Vision model to act as an OCR and data extraction assistant. The prompt specifies the exact fields to extract and the desired output format.
3.  **Gemini Structured Output:** It sends the image and the prompt to the Gemini API, leveraging the model's ability to return structured JSON output. This ensures that the extracted data is consistently formatted.
4.  **Data Extraction:** The model extracts the following employee information fields:
    - `employee_number`
    - `name`
    - `department`
    - `payroll_type`
    - `period`
5.  **Saving Results:** The extracted JSON data for each image is then appended to a corresponding text file (e.g., `crumpled.txt`).

## Usage

1.  **Place your time card images** in the appropriate folder (`crumpled/`, `folded/`, or `normal/`).

2.  **Update the `timesheets_folder` and `output_file` variables** in `main.py` to point to the correct folder and desired output file.

    For example, to process images in the `folded/` directory:

    ```python
    timesheets_folder = "./folded"
    output_file = "folded.txt"
    ```

3.  **Run the script:**
    ```bash
    python main.py
    ```

## Output

The script will generate a text file (e.g., `folded.txt`) containing the extracted JSON data, with each entry corresponding to an image file.

Example output for a single image (with timestamp):

```json
### 3a97a395-c6a9-4f2f-b4cc-a5359aa53d0b.jpeg ###
{
  "timestamp": "2025-11-10T10:00:00Z",
  "employee_information": {
    "employee_number": "32",
    "name": "John Doe",
    "department": "Engineering",
    "payroll_type": "Hourly",
    "period": "OCT. 11–25, 2025 AND OCT. 26–NOV. 10, 2025"
  }
}
```

## Employee w/ Timesheet Records Prompt

```py
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
      "morning_in": "",
      "morning_out": "",
      "afternoon_in": "",
      "afternoon_out": "",
      "overtime_in": "",
      "overtime_out": ""
    }
  ]
}

Rules:
- Do NOT include any entries that have completely empty time fields.
- In and Out values must valid format HH:MM format (24-hour clock).
- Keep JSON clean and properly formatted (no markdown, no explanations).
- Preserve exact text values from the image.
- All missing values should be empty strings.
- Output must be valid JSON only.
"""
```

## Employee Info Only Prompt

```py
prompt = """
You are an OCR and data extraction assistant.

Extract only the employee information from the provided image of a time card or attendance sheet.

Return the output strictly in valid JSON format with the following structure:

{
  "employee_information": {
    "employee_number": "",
    "name": "",
    "department": "",
    "payroll_type": "",
    "period": ""
  }
}

Rules:
- Extract only the fields shown above — no attendance or time records.
- The "employee_number" should be the employee's unique number (e.g., '32') if visible.
- The "period" should include the entire pay period text (e.g., "OCT. 11–25, 2025 AND OCT. 26–NOV. 10, 2025").
- Keep JSON clean, properly formatted, and with exact text values.
- Output must be valid JSON only (no markdown, comments, or explanations).
"""
```

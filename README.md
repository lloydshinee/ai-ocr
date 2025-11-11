# AI-Powered OCR for Time Cards

This project uses Google's `gemini-1.5-flash` model to perform Optical Character Recognition (OCR) on time card images and extract employee information and attendance records in a structured JSON format.

## How It Works

The Python script (`main.py`) manages the OCR process by:

1.  **Looping through images:** It iterates through all image files (JPEG, PNG) found in a specified input folder (e.g., `crumpled/`, `folded/`, `normal/`).
2.  **Advanced Prompting:** For each image, it constructs a detailed prompt that instructs the Gemini model to act as an OCR and data extraction assistant. The prompt specifies the exact fields to extract and the desired output format.
3.  **Gemini Structured Output:** It sends the image and the prompt to the Gemini API, leveraging the model's ability to return structured JSON output. This ensures that the extracted data is consistently formatted.
4.  **Data Extraction:** The model extracts the following fields:
    - `employee_information` (employee number, name, department, etc.)
    - `attendance_records` (date, in/out times)
5.  **Saving Results:** The extracted JSON data for each image is then appended to a corresponding text file (e.g., `normal.txt`).

## Setup

1.  **Create and activate a virtual environment:**

    - **For macOS/Linux:**

      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```

    - **For Windows:**
      ```bash
      python -m venv .venv
      .venv\Scripts\activate
      ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your environment variables:**
    - Create a `.env` file by copying the example file:
    - Open the `.env` file and add your Gemini API key:
      ```
      GEMINI_API_KEY="YOUR_API_KEY"
      ```

## How to Run

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

The script will generate a text file (e.g., `normal.txt`) containing the extracted JSON data, with each entry corresponding to an image file.

Example output for a single image:

```json
### 3a97a395-c6a9-4f2f-b4cc-a5359aa53d0b.jpeg ###
{
  "employee_information": {
    "employee_number": "32",
    "name": "John Doe",
    "department": "Engineering",
    "payroll_type": "Hourly",
    "period": "OCT. 11–25, 2025 AND OCT. 26–NOV. 10, 2025"
  },
  "attendance_records": [
    {
      "date": "10/11",
      "morning_in": "08:00",
      "morning_out": "12:00",
      "afternoon_in": "13:00",
      "afternoon_out": "17:00",
      "overtime_in": "",
      "overtime_out": ""
    }
  ]
}
```

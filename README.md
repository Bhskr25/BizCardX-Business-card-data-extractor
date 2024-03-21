![banner](https://github.com/Bhskr25/BizCardX-Business-card-data-extractor/assets/95600191/8322241b-3e2b-4e0d-af53-601d96f2ca28)
#####
# BizCardX: Extracting Business Card Data with OCR 
> USING OpenCV, MySQL AND STREAMLIT
---
Welcome to the Business card data extractor Dashboard! The Business Card Details Extractor is a Streamlit application designed to extract information from images of business cards using Optical Character Recognition (OCR) and search for details in an SQL table based on user input.

## Project Intro/Objective

The purpose of this project is to provide a convenient tool for extracting and managing business card information efficiently. Users can upload an image of a business card, extract details such as name, email, phone number, etc., and also search for specific details in an SQL database.
> The goal of the project is to develop a Streamlit application for extracting business card details from images using OCR and enabling search functionality in an SQL database.

---
### Methods Used
* Data Extraction and Preprocessing ( OpenCV, Tesseract, Pandas )
* Data Visualization
* DataBase Management ( SQL )
* User Interface Design 
* Dashboard Development
---
### Technologies
* Python
* OpenCV, Tesseract
* PIL, base64
* MySql.Connect
* Pandas
* Streamlit
---
## Project Description
The Business Card Details Extractor is a Python-based Streamlit application designed to streamline the process of extracting information from business cards. Leveraging Optical Character Recognition (OCR) technology, the application enables users to upload images of business cards and automatically extract key details such as name, email, phone number, and more. Additionally, the application offers search functionality, allowing users to query an SQL database for specific details stored in previous extractions. The project aims to provide a user-friendly interface for efficiently managing business card information, enhancing productivity in professional networking and contact management.

### Dashboard Results 

#### Users can Upoload Cards, Edit Details and Export Data to DataBase
  <p><img src='https://github.com/Bhskr25/BizCardX-Business-card-data-extractor/assets/95600191/ade9ec30-8aa6-4dd4-b945-db42b1402c70' width='auto'></p>
  
#### Search for Existing Cards
  <p><img src='https://github.com/Bhskr25/BizCardX-Business-card-data-extractor/assets/95600191/9c1e4dda-1ee4-400b-a90d-070bb7aa9568' width='auto'></p>
---
       
#### Prerequests and Needs
The needs of this project can be categorized into several key aspects. Here is a list of the essential needs

1. **Python Libraries:**
   - The project requires various Python libraries, including:
     - `OpenCV` & `PIL`: For image processing tasks.
     - `Tesseract OCR`: For extracting text from business card images
     - `mysql-connector`: For connecting with MySQL database.
     - `pandas`: For data transformation, manipulation and analysis.
     - `streamlit`: For creating the interactive web application.
       
2. **Data Extraction with OpenCV, Tesseract and PIL:**
   - OpenCV, Tesseract and PIL are utilized extensively to extract the text data from the images.

3. **Streamlit Web Application:**
   - Streamlit should be installed to run the web application for user interaction and data presentation.

4. **Database Services:**
   - SQL database should be available or set up for data storing and querying to get required results from the cards data.

5. **Data Pre-Processing and Visualization:**
   - Users might require basic understanding and knowledge of Pandas for data pre-processing, and streamlit to visualize the data in dashboard.

6. **Environment Setup:**
    - Proper Python environment setup with necessary dependencies installed.

7. **Internet Connection:**
    - An active internet connection is needed to fetch data from the YouTube API.
---
## Getting Started
- Ensure you have the required system specifications for utilizing the EasyOCR module/OpenCV & Tesseract.
- Set up SQL databases.
- Install necessary Python libraries using requirements.txt.
- Run the script to  launch the Streamlit application, extract data, edit details, export data to SQL database and retrive card details from Database.

1. Create a virtual environment:
    ```python
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```python
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```python
        source venv/bin/activate
        ```
3. Install required packages:
    ```python
    pip install -r requirements.txt
    ```
4. Running the Set-up in (venv)
    ```python
    streamlit run <python_file>.py
    ```
---

## Conclusion

Thank you for exploring my Business Card Details Extraction and Management Dashboard project! Hope this tool proves valuable for data analysis needs.

## Additional Information:

- This project is designed to provide a user-friendly interface for extracting and managing business card details. It can be further extended with additional features such as data visualization, export functionality, etc.
- Contributions and feedback are welcome. Feel free to open an issue or submit a pull request if you have any suggestions or improvements.

### Contact

For any questions or suggestions, feel free to reach me out at [pranaybhskr@gmail.com].

Happy analyzing!

---

Feel free to customize this template based on your project's specific details and requirements.

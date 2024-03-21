import urllib.request
import base64
import io
from streamlit_option_menu import option_menu
from mysql.connector import Error
import mysql.connector
import pandas as pd
import re
import pytesseract
import cv2
from PIL import Image
import streamlit as st
_ = '''==========================================================================================================
================<---{ IMPORT THE REQUIRED PACKAGES }--->======================================================
============================================================================================================'''
# import numpy as np

# <============<---{ MySQL database connection configuration }--->=============================================>
config = {'host': 'localhost',
          'user': 'root',
          'password': 'Pranay@25',
          'database': 'bizcard'}

_ = '''==========================================================================================================
================<---{ EXTRACT TEXT FROM IMAGE }--->============================================================
============================================================================================================'''


def extract_text_from_image(uploaded_img):
    image = Image.open(uploaded_img)
    text_i = pytesseract.image_to_string(image)
    return text_i


_ = '''==========================================================================================================
================<---{ EXTRACT DETAILS FROM TEXT DATA }--->=====================================================
============================================================================================================'''


def extract_details_from_text(text):
    details = {
        "Name": '',
        "Designation": '',
        "Company": '',
        "Email": '',
        "Phone Number": '',
        "Website": '',
        "Address": '',
        "Additional Information": ''
    }
    # <===( REGULAR EXPRESSIONS FOR FINDING DETAILS MATCH )====================================================>
    patterns = {
        "Name": r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)|([A-Z]+(?:\s+[A-Z]+)*)|([a-z]+(?:\s+[a-z]+)*)$',
        "Email": r'\b[A-Za-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)*\b',
        "Website": r'\b(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        "Address": r'\b(?:\d{1,5}\s[A-Za-z0-9.-]+\s[A-Za-z]{2,}|(?:\d{1,2}-)+\d{1,5}/\d{1,2}/\d{1,5}),\s[A-Za-z0-9.-]+,\s[A-Za-z0-9.-]+,\s[A-Za-z]{2,},\s\d{6}\b',
        "Phone Number": r'(?:(?:\+\d{1,3})?[-.\s]?)?(?:(?:\(\d{1,4}\)|\d{1,4})[-.\s]?)?\d{3,5}[-.\s]?\d{4}',
        "Job Role": r'[A-Za-z\s&.,()-]+',
        "Company": r'[A-Za-z\s&.,()-]+'
    }

    # <---( Extract data using regular expressions )---------------------------------->
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.MULTILINE)
        if match:
            details[key] = match.group(0).strip()

    # <---( Extract additional information )----------------------------------------->
    additional_info = text.split('\n')
    additional_info = [line.strip()
                       for line in additional_info if line.strip()]
    details['Additional Information'] = ' '.join(additional_info)

    return details


_ = '''==========================================================================================================
================<---{ EXPORT DATA TO SQL DATABASE }--->========================================================
============================================================================================================'''


def insert_into_database(image_bytes, details_df):
    try:
        connection = mysql.connector.connect(**config)
        with connection.cursor() as cursor:
            # <---( Insert data into database )---------------------------------------->
            sql_query = """INSERT INTO business_cards_info 
                            (name, designation, company, email, phone_number, website, address, image) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            # <---( Extract values from DataFrame and pass them as a tuple )----------->
            values = (
                details_df['Name'].iloc[0],
                details_df['Designation'].iloc[0],
                details_df['Company'].iloc[0],
                details_df['Email'].iloc[0],
                details_df['Phone Number'].iloc[0],
                details_df['Website'].iloc[0],
                details_df['Address'].iloc[0],
                image_bytes
            )
            cursor.execute(sql_query, values)
            connection.commit()
            st.success('Details exported to MySQL database successfully')
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        connection.close()


_ = '''==========================================================================================================
================<---{ SEARCH FOR EXISTING RECORDS IN DATABASE }--->============================================
============================================================================================================'''  # <---( Function to search for details in SQL table based on user input )------------------------->


def search_details(user_input):
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()

            # <---( Search query )--------------------------------------------------------->
            sql_query = f"SELECT * FROM business_cards_info WHERE Name LIKE '%{user_input}%' OR Phone_Number LIKE '%{user_input}%' OR Email LIKE '%{user_input}%' OR Address LIKE '%{user_input}%'"
            cursor.execute(sql_query)
            records = cursor.fetchall()

            return records

    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")


_ = '''==========================================================================================================
================<---{ DELETE CARD FROM DATABASE }--->==========================================================
============================================================================================================'''


def delete_record(record_id):
    try:
        connection = mysql.connector.connect(**config)
        with connection.cursor() as cursor:
            # <---( Delete query )------------------------------------------------->
            sql_query = f"DELETE FROM business_cards_info WHERE Name={record_id}"
            cursor.execute(sql_query)
            connection.commit()
            st.success('Record deleted successfully')
    except Error as e:
        st.error(f"Error: {e}")
    finally:
        connection.close()


_ = '''==========================================================================================================
================<---{ GET ALL EXISTING CARDS }--->=============================================================
============================================================================================================'''


def get_all_cards():
    df = pd.DataFrame()  # Initialize an empty DataFrame
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()

            query = "SELECT * FROM business_cards_info"
            cursor.execute(query)
            rows = cursor.fetchall()
            # Get the column names
            columns = [column[0] for column in cursor.description]
            # Create a DataFrame from the fetched rows and column names
            df = pd.DataFrame(rows, columns=columns)

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL:", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return df


_ = '''==========================================================================================================
================<---{ CONVERT BLOB DATA TO IMAGE }--->=========================================================
============================================================================================================'''


def display_image_from_blob(blob_data):
    # <---( Retrieve the encoded image string(BLOB DATA) from the result of sql query )------------->
    encoded_image_str = blob_data
    # <---( Display the image using the encoded image string )----------------------------------------->
    st.image(base64.b64decode(encoded_image_str),
             caption='Business Card Image', use_column_width=True)


_ = '''==========================================================================================================
================<---{ DISPLAY ALL CARDS DATA FROM SQL }--->====================================================
============================================================================================================'''


def display_cards(df):
    for index, row in df.iterrows():
        # <---( Create a Streamlit container for the row )----------------->
        container = st.container(border=True)
        container.subheader(f"{row['Name']}'s Business Card")
        # <---( Display text data from the row )-------------------------->
        for column, value in row.items():
            if column != 'Image':  # Exclude the 'Image' column
                container.write(f"**{column}**: {value}")

        # Check if the row contains an image (blob file)
        if 'Image' in row and isinstance(row['Image'], bytes):
            try:
                with container:
                    display_image_from_blob(row['Image'])
            except Exception as e:
                st.error(f"Error displaying image: {e}")


_ = '''==========================================================================================================
================<---{ STREAMLIT APPLICATION }--->==============================================================
============================================================================================================'''

# <============<---{ MAIN FUNCTION }--->======================================================================>


def main():

    urllib.request.urlretrieve(
        'https://github.com/Bhskr25/BizCardX-Business-card-data-extractor/assets/95600191/28139a83-0fea-4e85-82ba-97003a96f5f7', 'icon.png')
    icon = Image.open('icon.png')
    # <===( PAGE CONFIGURATION )===============================================================================>
    st.set_page_config(page_title='Business Card Details Extractor',
                       page_icon=icon,
                       layout='wide',
                       initial_sidebar_state='expanded')

    # applying css to fav-icon
    icon_css = """<style>.icon {mix-blend-mode:multiply;object-fit:contain}</style>"""
    st.markdown(icon_css, unsafe_allow_html=True)

    col1, col2 = st.columns([0.13, 0.75])
    col3, col4, col5 = st.columns([0.3, 0.4, 0.25])

    with col2:
        st.markdown(
            '<h1 style="padding-top:10px;font-size:50px" >Business Card Details Management </h1>', unsafe_allow_html=True)
        tag = '''<style>.samp, blockquote{margin-top:-28px}</style>'''
        st.markdown(tag, unsafe_allow_html=True)
        st.markdown(
            '> Effortlessly Extract, Organize, and Store Business Card Data')
        st.markdown('---')
    with col1:

        urllib.request.urlretrieve('https://github.com/Bhskr25/BizCardX-Business-card-data-extractor/assets/95600191/bdb31efd-f4e9-4c23-b921-2a058eed59e8',
                                   "logo.jpg")

        logo = Image.open('logo.jpg')
        # applying css to logo
        logo_css = """<style>
                    .logo {
                        width:400px;
                        height:200px;
                        mix-blend-mode:multiply;
                        object-fit:contain
                    }
                    </style>"""
        st.markdown(logo_css, unsafe_allow_html=True)
        st.image(logo, output_format='JPEG', width=180)
    st.markdown('---')

    with col3:
        st.markdown('#### Upload the card to extract details')
        uploaded_img = st.file_uploader('', type=['jpeg', 'png', 'jpg'])

        selection = option_menu('Extract & Upload',
                                options=['Extract Details','Edit Data', 'View Cards'],
                                orientation='vertical')

        if not uploaded_img:
            with col4:
                st.markdown(
                    '#### Try uploading a business card image to extract deatils.')
        else:
            if selection == 'Extract Details':
                with col5:
                    st.image(
                        uploaded_img, caption='Uploaded Business Card', use_column_width=True)
                with col4:
                    text = extract_text_from_image(uploaded_img)
                    details = extract_details_from_text(text)

                    # Display extracted details
                    preview_container = st.container(border=True)
                    with preview_container:
                        st.markdown('### <u>Extracted Details</u>',
                                    unsafe_allow_html=True)
                        details_df = pd.DataFrame([details])

                        st.markdown(f"**Name**: {details['Name']}")
                        st.markdown(f"**Designation**: {details['Designation']}")
                        st.markdown(f"**Company**: {details['Company']}")
                        st.markdown(f"**Email**: {details['Email']}")
                        st.markdown(f"**Website**: {details['Website']}")
                        st.markdown(f"**Phone Number**: {details['Phone Number']}")
                        st.markdown(f"**Address**: {details['Address']}")
                        st.markdown('___ \n <u>Extracted Raw Data</u>:', unsafe_allow_html=True)
                        st.markdown(details['Additional Information'])

            elif selection == 'Edit Data':
                with col4:
                    # Edit details
                    st.subheader('Edit Details')
                    text = extract_text_from_image(uploaded_img)
                    details = extract_details_from_text(text)

                    notify = st.container()

                    if 'm_df' not in st.session_state:
                        st.session_state.m_df = pd.DataFrame(columns=['Name',
                                                                      'Designation',
                                                                      'Company',
                                                                      'Email',
                                                                      'Website',
                                                                      'Phone Number',
                                                                      'Address',
                                                                      ])
                    a = st.container(border=True, height=550)
                    with a:
                        c1, b1 = st.columns([0.7, 0.2])
                        c2, b2 = st.columns([0.7, 0.2])
                        c3, b3 = st.columns([0.7, 0.2])
                        c4, b4 = st.columns([0.7, 0.2])
                        c5, b5 = st.columns([0.7, 0.2])
                        c6, b6 = st.columns([0.7, 0.2])
                        c7, b7 = st.columns([0.98, 0.02])

                        with c1:
                            edited_name = st.text_input(
                                '**Name**', value=details['Name'])
                        with c2:
                            edited_designation = st.text_input(
                                '**Designation**', value=details['Designation'])
                        with c3:
                            edited_company = st.text_input(
                                '**Company**', value=details['Company'])
                        with c4:
                            edited_email = st.text_input(
                                '**Email**', value=details['Email'])
                        with c5:
                            edited_website = st.text_input(
                                '**Website**', value=details['Website'])
                        with c6:
                            edited_phone = st.text_input(
                                '**Phone Number**', value=details['Phone Number'])
                        with c7:
                            edited_address = st.text_input(
                                '**Address**', value=details['Address'])
                    st.markdown('')

                    with col5:
                        update = st.button("Update Details")
                        upload = st.button('Export to SQL')
                        rd_c = st.container(border=True)
                        with rd_c:
                            st.image(uploaded_img, caption='Uploaded Business Card', use_column_width=True)
                            st.markdown(" **Extracted Data:**")
                            for i in details['Additional Information'].split('\n'):
                                st.markdown(i)

                if update:
                    updtd_df = pd.DataFrame([{'Name': edited_name,
                                             'Designation': edited_designation,
                                              'Company': edited_company,
                                              'Email': edited_email,
                                              'Website': edited_website,
                                              'Phone Number': edited_phone.replace('-', ''),
                                              'Address': edited_address}])

                    st.session_state.m_df = pd.concat(
                        [st.session_state.m_df, updtd_df], axis=0)
                    details_df = st.session_state.m_df
                    with notify:
                        st.success(
                            f"Details of {details['Name']} Updated Successfully")
                    with col5:
                        st.dataframe(details_df,hide_index=True)

                if upload:
                    with col5:
                        #<---( Open a file in binary mode )--------------------------------->
                        file_i = uploaded_img.read()
                        #<---( Encode the image data into a base64 string )----------------->
                        encoded_image = base64.b64encode(file_i)
                        #<---( Convert the base64 bytes to a string (UTF-8 encoding) )------>
                        encoded_image_str = encoded_image.decode('utf-8')

                        updtd_df = pd.DataFrame([{'Name': edited_name,
                                                 'Designation': edited_designation,
                                                  'Company': edited_company,
                                                  'Email': edited_email,
                                                  'Website': edited_website,
                                                  'Phone Number': edited_phone.replace('-', ''),
                                                  'Address': edited_address}])

                        st.session_state.m_df = pd.concat([st.session_state.m_df, updtd_df], axis=0)
                        details_df = st.session_state.m_df

                        with notify:
                            insert_into_database(encoded_image_str, details_df)

        if selection == 'View Cards':
            # Search section
            with col5:
                search_input = st.text_input(
                    'Search by Name, Phone Number, Email, or Company')
                search = st.button('Search')
            if search:
                if search_input:
                    search_results = search_details(search_input)
                    if search_results:
                        with col4:
                            st.subheader('Search Results')
                            for result in search_results:
                                search_c = st.container(border=True)
                                with search_c:
                                    st.write("<b>Name:</b>",
                                             result[0], unsafe_allow_html=True)
                                    st.write("<b>Designation:</b>",
                                             result[1], unsafe_allow_html=True)
                                    st.write("<b>Company:</b>",
                                             result[2], unsafe_allow_html=True)
                                    st.write("<b>Email:</b>",
                                             result[3], unsafe_allow_html=True)
                                    st.write("<b>Website:</b>",
                                             result[4], unsafe_allow_html=True)
                                    st.write("<b>Phone Number:</b>",
                                             result[5], unsafe_allow_html=True)
                                    st.write("<b>Address:</b>",
                                             result[6], unsafe_allow_html=True)
                                    display_image_from_blob(result[7])

                                    del_r = st.button(
                                        'Delete', type='secondary')

                                    if del_r:
                                        with col5:
                                            confirmation = st.radio(
                                                'Are you sure you want to delete this record?', ('Yes', 'No'), index=1)
                                            if confirmation == 'Yes':
                                                delete_record(result[0])

            else:
                with col4:
                    st.markdown("#### Existing Card Holder's Data")
                    records_d = st.container(border=True, height=520)
                    with records_d:
                        # Display all cards as a DataFrame
                        all_cards_df = get_all_cards()
                        # Assuming 'all_cards_df' is the DataFrame containing all business card data
                        display_cards(all_cards_df)
                    st.markdown('---')
                    with col5:
                        st.dataframe(all_cards_df,hide_index=True)

#<============<---{ CALL MAIN(): STREAMLIT APPLICATION }--->==================================================>
if __name__ == '__main__':
    main()
#<=====================================( END OF APPLICATION )=================================================>
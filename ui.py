import streamlit as st
from PIL import Image
from build_recipe import generate_recipe

# Custom CSS to remove space at the top
st.markdown(
    """
    <style>
    .main {
        padding-top: 0rem !important;
    }
    .title {
        font-size: 14px; /* Adjust the font size as needed */
        font-weight: normal; 
        text-align: left;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.markdown('<h3 class="title">AI Recipe Generator</h3>', unsafe_allow_html=True)

# Custom message for file size limit
st.markdown(
    """
    <style>
    .file-size-note {
        font-size: 14px;
        color: red;
        font-weight: bold;
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('Upload an image of cooked food (Pls upload an image smaller than 5 mb)', unsafe_allow_html=True)

# File uploader for image input
uploaded_file = st.file_uploader("Upload an image of cooked food (Pls upload an image smaller than 5 mb)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file:
    # Check file size (limit: 5 MB)
    if uploaded_file.size > 5 * 1024 * 1024:  # 5 MB in bytes
        st.error("File size exceeds 5 MB. Please upload a smaller file.")
    else:
        # Create two columns: one for the image and one for the recipe
        col1, col2 = st.columns([1, 3])  # Adjust column width ratio as needed

        # Display the uploaded image in the left column
        with col1:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", width=150)  # Set width to 150 pixels

        # Generate and display the recipe in the right column
        with col2:
            prompt = "You are a world-renowned chef. Provide a recipe for the image."
            with st.spinner("Generating recipe..."):
                try:
                    # Call the core logic to generate the recipe
                    recipe = generate_recipe(prompt, img)
                    st.success("Recipe generated successfully!")
                    st.markdown(recipe)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# Add developer name at the bottom of the page
st.markdown(
    """
    <hr>
    <p style="text-align: center; font-size: 14px; color: gray;">
    Developed by <strong>Malkit Bhasin</strong>
    </p>
    """,
    unsafe_allow_html=True,
)

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
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit UI
st.title("AI Recipe Generator")
st.write("Upload an image of any cooked food, and the app will generate a recipe for you!")t

# Custom message for file size limit
st.markdown(
    """
    <style>
    .file-size-note {
        font-size: 14px;
        color: red;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<p class="file-size-note">**Note:** Please upload an image smaller than <strong>5 MB</strong> (JPEG/PNG).</p>', unsafe_allow_html=True)

# File uploader for image input
uploaded_file = st.file_uploader("Upload an image of baked goods", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Check file size (limit: 5 MB)
    if uploaded_file.size > 5 * 1024 * 1024:  # 5 MB in bytes
        st.error("File size exceeds 5 MB. Please upload a smaller file.")
    else:
        # Display the uploaded image with a smaller size
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", width=400)  # Set width to 400 pixels

        # Prompt input
        prompt = st.text_input("Enter a prompt for the recipe", "Provide an example recipe for the baked goods in the image")

        if st.button("Generate Recipe"):
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

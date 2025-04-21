import streamlit as st
import sys
import os
from PIL import Image
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_recipe import generate_recipe
from parse_ingredients import parse_ingredients_with_openai  # Import the parsing function
from find_grocery_stores import get_nearby_stores  # Import the function to find nearby stores
from get_user_location import get_user_location_by_ip  # Import the function to get user location

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

st.markdown('Upload an image of cooked food (Pls upload an image smaller than 5 MB)', unsafe_allow_html=True)

# File uploader for image input
uploaded_file = st.file_uploader("Upload an image of cooked food (Pls upload an image smaller than 5 MB)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

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

                    # Add a button to parse the recipe and display ingredients
                    if st.button("Parse Ingredients"):
                        with st.spinner("Parsing ingredients..."):
                            try:
                                # Call the parse_ingredients_with_openai function
                                ingredients_df = parse_ingredients_with_openai(recipe)

                                # Display the parsed ingredients
                                st.write("### Parsed Ingredients:")
                                st.dataframe(ingredients_df)
                            except Exception as e:
                                st.error(f"Error parsing ingredients: {e}")

                    # Add a button to find nearby stores
                    if st.button("Find Nearby Stores"):
                        with st.spinner("Fetching nearby stores..."):
                            try:
                                # Get user's location
                                lat, lng = get_user_location_by_ip()
                                if lat is None or lng is None:
                                    st.error("Could not determine your location.")
                                else:
                                    # Call the get_nearby_stores function
                                    stores = get_nearby_stores(lat, lng)
                                    if stores:
                                        st.write("### Nearby Grocery Stores:")
                                        for store in stores:
                                            st.write(f"**Name:** {store['name']}")
                                            st.write(f"**Address:** {store['address']}")
                                            st.write(f"**Rating:** {store.get('rating', 'N/A')}")
                                            st.write(f"**Open Now:** {store.get('open_now', 'N/A')}")
                                            st.write("---")
                                    else:
                                        st.warning("No grocery stores found nearby.")
                            except Exception as e:
                                st.error(f"Error fetching nearby stores: {e}")
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

import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.title("Interactive Tourism Dashboard")

# Load CSV
file_path = r"C:\Users\User\Desktop\assig 2.csv"  # update if needed
df = pd.read_csv(file_path)

# Tabs for charts
tab1, tab2 = st.tabs(["Bubble Chart", "Bar Chart"])

with tab1:
    st.subheader("Bubble Chart: Cafes vs Tourism Index")

    # Dropdown for region
    region = st.selectbox(
        "Select Governorate (Region):",
        ["All"] + df["Ref area"].unique().tolist()
    )
    if region != "All":
        filtered_df = df[df["Ref area"] == region]
    else:
        filtered_df = df.copy()

    # Slider for Tourism Index
    min_index = int(df["Tourism Index"].min())
    max_index = int(df["Tourism Index"].max())
    tourism_range = st.slider(
        "Select Tourism Index Range:",
        min_value=min_index,
        max_value=max_index,
        value=(min_index, max_index)
    )
    filtered_df = filtered_df[
        (filtered_df["Tourism Index"] >= tourism_range[0]) &
        (filtered_df["Tourism Index"] <= tourism_range[1])
    ]

    # Bubble chart
    fig_bubble = px.scatter(
        filtered_df,
        x="Total number of cafes",
        y="Tourism Index",
        size="Total number of hotels",
        color="Ref area",
        hover_name="Town",
        size_max=60,
        title="Tourism Bubble Chart"
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

    # Metrics
    st.subheader("Summary Metrics (Filtered Data)")
    if not filtered_df.empty:
        st.metric("Average Tourism Index", round(filtered_df["Tourism Index"].mean(), 2))
        st.metric("Total Cafes", filtered_df["Total number of cafes"].sum())
        st.metric("Total Hotels", filtered_df["Total number of hotels"].sum())
    else:
        st.warning("No data matches the current filters.")

  # Bubble chart insights
    st.subheader("Key Insights (Bubble Chart)")
    if not filtered_df.empty:
        highest_tourism = filtered_df.loc[filtered_df["Tourism Index"].idxmax()]
        most_cafes = filtered_df.loc[filtered_df["Total number of cafes"].idxmax()]
        
        st.markdown(f"- Town with **highest Tourism Index**: **{highest_tourism['Town']}** ({highest_tourism['Tourism Index']}).")
        st.markdown(f"- Town with **most cafes**: **{most_cafes['Town']}** ({most_cafes['Total number of cafes']} cafes).")
        st.markdown(f"- Average Tourism Index in selected regions: **{round(filtered_df['Tourism Index'].mean(),2)}**.")
    else:
        st.write("No data available for selected filters.")

   # Statistical Analysis (Bubble Chart ONLY)
    st.subheader("Statistical Analysis (Bubble Chart)")
    if not filtered_df.empty:
        corr = filtered_df["Total number of cafes"].corr(filtered_df["Tourism Index"])
        st.markdown(f"- Correlation between **Cafes and Tourism Index**: **{round(corr, 2)}**")
        if corr > 0.7:
            st.success("Strong positive correlation → More cafes are linked with higher tourism index.")
        elif corr > 0.3:
            st.info("Moderate positive correlation → Cafes somewhat support tourism index.")
        else:
            st.warning("Weak or no correlation → Cafes don’t strongly impact tourism index here.")

with tab2:
    st.subheader("Bar Chart: Total Restaurants per Region")

    # Multi-select for regions
    selected_regions = st.multiselect(
        "Select Regions:",
        options=df["Ref area"].unique(),
        default=df["Ref area"].unique()
    )

    bar_df_filtered = df[df["Ref area"].isin(selected_regions)].groupby(
        "Ref area", as_index=False
    )["Total number of restaurants"].sum()

    # Slider for restaurant range
    min_restaurants = int(bar_df_filtered["Total number of restaurants"].min())
    max_restaurants = int(bar_df_filtered["Total number of restaurants"].max())
    restaurant_range = st.slider(
        "Filter Regions by Number of Restaurants:",
        min_value=min_restaurants,
        max_value=max_restaurants,
        value=(min_restaurants, max_restaurants)
    )

    bar_df_filtered = bar_df_filtered[
        (bar_df_filtered["Total number of restaurants"] >= restaurant_range[0]) &
        (bar_df_filtered["Total number of restaurants"] <= restaurant_range[1])
    ]

    # Checkbox to show/hide chart
    if st.checkbox("Show Bar Chart", value=True):
        fig_bar = px.bar(
            bar_df_filtered,
            x="Ref area",
            y="Total number of restaurants",
            color="Ref area",
            text="Total number of restaurants",
            title="Total Restaurants per Region"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Metrics for filtered data
    st.subheader("Summary Metrics (Filtered Data)")
    if not bar_df_filtered.empty:
        st.metric("Total Restaurants", bar_df_filtered["Total number of restaurants"].sum())
        st.metric("Maximum Restaurants in a Region", bar_df_filtered["Total number of restaurants"].max())
        st.metric("Minimum Restaurants in a Region", bar_df_filtered["Total number of restaurants"].min())
    else:
        st.warning("No regions match the selected filters.")

    # Download filtered data
    st.download_button(
        label="Download Filtered Data",
        data=bar_df_filtered.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )

# Bar chart insights
    st.subheader("Key Insights (Bar Chart)")
    if not bar_df_filtered.empty:
        max_region = bar_df_filtered.loc[bar_df_filtered["Total number of restaurants"].idxmax()]
        min_region = bar_df_filtered.loc[bar_df_filtered["Total number of restaurants"].idxmin()]
        
        st.markdown(f"- Region with **most restaurants**: **{max_region['Ref area']}** ({max_region['Total number of restaurants']} restaurants).")
        st.markdown(f"- Region with **least restaurants**: **{min_region['Ref area']}** ({min_region['Total number of restaurants']} restaurants).")
        st.markdown(f"- Total restaurants in selected regions: **{bar_df_filtered['Total number of restaurants'].sum()}**.")
    else:
        st.write("No regions match the selected filters.")

 # Statistical Analysis (Bar Chart ONLY)
    st.subheader("Statistical Analysis (Bar Chart)")
    if not bar_df_filtered.empty:
        mean_val = round(bar_df_filtered["Total number of restaurants"].mean(), 2)
        median_val = round(bar_df_filtered["Total number of restaurants"].median(), 2)
        std_val = round(bar_df_filtered["Total number of restaurants"].std(), 2)
        st.markdown(f"- Mean restaurants per region: **{mean_val}**")
        st.markdown(f"- Median restaurants per region: **{median_val}**")
        st.markdown(f"- Standard deviation: **{std_val}**")

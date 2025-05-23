# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZfuCi7cB7zeKIWiHep_B9DBwHbaQXe3k
"""
# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(page_title="Customer Analysis", layout="wide")





st.markdown("""
    <h1 style='text-align: right; color: #BB8493; font-size: 4rem; margin-bottom:0;'>
        Customer Behavior Uncovered:
    </h1>
    <h2 style='text-align: right; color: #BB8493; font-size: 3rem; margin-top:0;'>
        Trends You Can't Ignore
    </h2>
""", unsafe_allow_html=True)



# Load the data
df = pd.read_csv("ecommerce_customer_data.csv")


st.markdown("""
<div style="background-image: url('https://www.transparenttextures.com/patterns/cubes.png'); padding: 10px 20px; border-radius: 10px;text-align: center; ">
    <h2 style="color: #88304E;">Understanding Customer Diversity</h2>
    <p style="color: #F7374F; font-size: 16px; font-family: 'Arial';">
    Analyzing age, gender, and location patterns to better understand our customer base.
    </p>
</div>
""", unsafe_allow_html=True)


# Create 3 columns
col1, col2, col3 = st.columns(3)

# --------- First Graph ----------
with col2:
    st.markdown(
    "<h3 style='color: #D95F59;'>Gender-wise Distribution</h3>", 
    unsafe_allow_html=True
    )
    # Data preparation
    gender_distribution = df['Gender'].value_counts().reset_index()
    gender_distribution.columns = ['Gender', 'Count']

    # Create the pie chart
    fig = px.pie(gender_distribution, names='Gender', values='Count', color='Gender')

    # Streamlit: Display the pie chart
    st.plotly_chart(fig)


# --------- Second Graph ----------
with col1:
    st.markdown(
    "<h3 style='color: #D95F59;'>Location-wise Distribution</h3>", 
    unsafe_allow_html=True
    )
    fig2, ax2 = plt.subplots()

    # Data preparation
    location_dist = df['Location'].value_counts().reset_index()
    location_dist.columns = ['Location', 'Count']

    # Create the interactive bar chart
    fig = px.bar(
    location_dist,
    x='Location',
    y='Count',
    color='Location',
    color_discrete_sequence=px.colors.sequential.Reds,
    title='Location-wise Customer Distribution'
    )

    # Customize layout
    fig.update_layout(
    xaxis_title='Location',
    yaxis_title='No. of Customers',
    title_font=dict(size=16, family='Arial', color='black'),
    legend_title='Location',
    xaxis_tickangle=-45
    )

    st.plotly_chart(fig)


# --------- Third Graph ----------
with col3:
    st.markdown(
        "<h3 style='color: #D95F59;'>Age-wise Distribution</h3>", 
        unsafe_allow_html=True
    )

    # Define age groups
    bins = [18, 21, 24, 27, 30, 33, 36]
    labels = ['18-20', '21-23', '24-26', '27-29', '30-32', '33-35']
    df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # Prepare distribution data
    age_group_distribution = df['Age Group'].value_counts().sort_index()

    # Create Plotly bar chart
    import plotly.express as px
    import pandas as pd

    age_df = pd.DataFrame({
        'Age Group': age_group_distribution.index,
        'Count': age_group_distribution.values
    })

    fig3 = px.bar(
        age_df,
        x='Age Group',
        y='Count',
        color='Age Group',
        color_discrete_sequence=px.colors.sequential.Reds,
        title='',
    )

    fig3.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Count',
        showlegend=False,
        plot_bgcolor='white'
    )

    st.plotly_chart(fig3, use_container_width=True)
import streamlit as st

with st.expander("View Insights"):
    st.markdown("""
    ### Geographic Distribution:
    - Distribution is nearly **even across locations**.
    
    **Recommendation:**
    - Focus on **strategic optimization** (ads, offers) in **high-performing regions** to boost ROI.

    ---

    ### Gender-Based Distribution:
    - Consumer base is **uniform across both genders** — balanced reach.

    ---

    ### Age Group Insights:
    - Majority of customers are aged **21–23** and **27–29**.
    - The **33–35** age group shows the **lowest engagement**.

    **Recommendation:**
    - Build trust through **return policies**, **testimonials**, and promote **premium quality**.
    - Use **simplified navigation** to better engage the **33+ age segment**.
    """)



st.markdown("""
<div style="background-image: url('https://www.transparenttextures.com/patterns/cubes.png'); padding: 10px 20px; border-radius: 10px;text-align: center;">
    <h2 style="color: #88304E;">Customer Browsing and Engagement Trends</h2>
    <p style="color: #F7374F; font-size: 16px; font-family: 'Arial';">
    Exploring how customers interact with our platform through browsing behavior and engagement metrics.
    </p>
</div>
""", unsafe_allow_html=True)

# Create 2 columns
col1, col2 = st.columns(2)

# --------- First Graph ----------
with col1:
    st.markdown(
    "<h3 style='color: #D95F59;'>Device Type vs Avg. Browsing Time and Pages Viewed</h3>", 
    unsafe_allow_html=True
    )
    
    

    # Grouping the data
    device_stats = df.groupby('Device_Type')[['Product_Browsing_Time', 'Total_Pages_Viewed']].mean().reset_index()

    # Define max value for consistent Y-axis scale
    y_max = max(device_stats['Product_Browsing_Time'].max(), device_stats['Total_Pages_Viewed'].max()) + 5

    # Create figure
    fig = go.Figure()

    # Bar plot for Avg. Browsing Time
    fig.add_trace(go.Bar(
    x=device_stats['Device_Type'],
    y=device_stats['Product_Browsing_Time'],
    name='Avg. Browsing Time',
    marker_color='skyblue',
    text=device_stats['Product_Browsing_Time'].round(1),
    textposition='outside'
    ))

    # Line plot for Avg. Pages Viewed
    fig.add_trace(go.Scatter(
    x=device_stats['Device_Type'],
    y=device_stats['Total_Pages_Viewed'],
    name='Avg. Pages Viewed',
    mode='lines+markers+text',
    marker=dict(color='maroon', size=10),
    line=dict(width=2),
    text=device_stats['Total_Pages_Viewed'].round(1),
    textposition='top center'
    ))

    # Layout setup
    fig.update_layout(
    
    xaxis_title='Device Type',
    yaxis_title='Value',
    yaxis=dict(range=[0, y_max]),
    legend=dict(x=0.01, y=0.99),
    height=500,
    bargap=0.3
    )

    st.plotly_chart(fig)

with col2:
    st.markdown(
    "<h3 style='color: #D95F59;'>Gender vs Avg. Pages Viewed and Browsing Time</h3>", 
    unsafe_allow_html=True
    )
    
    # Grouping the data by Gender
    gender_stats = df.groupby('Gender')[['Product_Browsing_Time', 'Total_Pages_Viewed']].mean().reset_index()

    # Define max value for consistent Y-axis scale
    y_max = max(gender_stats['Product_Browsing_Time'].max(), gender_stats['Total_Pages_Viewed'].max()) + 5

    # Create figure
    fig = go.Figure()

    # Bar plot for Avg. Pages Viewed
    fig.add_trace(go.Bar(
    x=gender_stats['Gender'],
    y=gender_stats['Total_Pages_Viewed'],
    name='Avg. Pages Viewed',
    marker_color='lightcoral',
    text=gender_stats['Total_Pages_Viewed'].round(1),
    textposition='outside'
    ))

    # Line plot for Avg. Browsing Time
    fig.add_trace(go.Scatter(
    x=gender_stats['Gender'],
    y=gender_stats['Product_Browsing_Time'],
    name='Avg. Browsing Time',
    mode='lines+markers+text',
    marker=dict(color='navy', size=10),
    line=dict(width=2),
    text=gender_stats['Product_Browsing_Time'].round(1),
    textposition='top center'
    ))

    # Layout setup
    fig.update_layout(
   
    xaxis_title='Gender',
    yaxis_title='Value',
    yaxis=dict(range=[0, y_max]),
    legend=dict(x=0.01, y=0.99),
    height=500,
    bargap=0.3
    )

    st.plotly_chart(fig)
    
with st.expander("View Insights:"):
     st.markdown("""
    
    ✅ Insights:
    - Tablet users spend the most time and view nearly the same number of pages as mobile users.

    - Mobile usage dominates with the best balance between time spent and pages viewed — optimal engagement.

    - Desktop usage has the lowest engagement, indicating possible UX issues or lower motivation to explore.


    **Recommendations :**  
    - Optimize mobile and tablet UX/UI further — they are your most promising platforms.

    - Consider desktop-focused retargeting strategies or progressive web apps to improve engagement for desktop users.


    
     ✅ Insights:
     - Females slightly outperform males in both time and pages viewed, indicating higher engagement from female users

     **Recommendations :**  

     - Explore personalized content or offers for female users, especially in key product categories.

     - For males, consider using push notifications or gamified incentives to increase time-on-site and interaction depth.
     """)

st.markdown("""
<div style="background-image: url('https://www.transparenttextures.com/patterns/cubes.png'); padding: 10px 20px; border-radius: 10px;text-align: center;">
    <h2 style="color: #88304E;">Transactional Insights: Frequency and Preferences</h2>
    <p style="color: #F7374F; font-size: 16px; font-family: 'Arial';">
    Uncovering purchase habits, spending patterns, and product preferences across customers.
    </p>
</div>
""", unsafe_allow_html=True)

#Items_Added_To_cart vs Total_Purchases

st.markdown(
    "<h3 style='color: #D95F59;'>Added to Cart VS Purchase Made</h3>", 
    unsafe_allow_html=True
)
fig = px.bar(df, x='Items_Added_to_Cart',y='Total_Purchases',labels={'Items_Added_to_Cart':'No. of items added to Cart','Total_Purchases':'No. of purchases made'})
st.plotly_chart(fig)

with st.expander("View Insights:"):
    st.markdown("""

    - Stable Purchases (0–5 items): Users consistently purchase even with few items—indicates strong impulse buying or direct checkout behavior.

    - Drop at 6 Items: Sharp decline suggests decision fatigue or cart abandonment risk.

    - Spike at 7 Items: Peak purchases likely due to bulk buying or offer thresholds.

    - High Conversion (8–10 items): Slight drop after 7, but conversions remain strong for high-cart users.


    **Actionable Insight:**  
    - Enable quick checkout for low-cart users.

    - Add incentives or support at 6-item carts to reduce drop-off.

    - Promote bulk offers/free shipping around 6–7 item mark.

    - Use cart recovery nudges (emails, notifications) for abandoned carts.



    """)

st.markdown("""
<div style="background-image: url('https://www.transparenttextures.com/patterns/cubes.png'); padding: 10px 20px; border-radius: 10px;text-align: center;">
    <h2 style="color: #88304E;">Conversion Funnel:</h2>
    <p style="color: #F7374F; font-size: 16px; font-family: 'Arial';">
    From browsing to buying — tracking customer drop-offs at each stage of the purchase journey.
    </p>
</div>
""", unsafe_allow_html=True)

# Define each funnel stage
visited = df[df['Product_Browsing_Time'] > 0]
added_to_cart = df[df['Items_Added_to_Cart'] > 0]
purchased = df[df['Total_Purchases'] > 0]

# Count users at each stage
funnel_counts = {
    'Visited Site': len(visited),
    'Added to Cart': len(added_to_cart),
    'Purchased': len(purchased)
}

# Convert to DataFrame for easy visualization
funnel_df = pd.DataFrame(list(funnel_counts.items()), columns=['Stage', 'Users'])

# Calculate conversion rates
funnel_df['Conversion Rate (%)'] = funnel_df['Users'].pct_change().fillna(1) * 100

print(funnel_df)

import pandas as pd
import plotly.express as px

# Assuming 'data' is your DataFrame
# Define funnel stages
visited = df[df['Product_Browsing_Time'] > 0]
added_to_cart = df[df['Items_Added_to_Cart'] > 0]
purchased = df[df['Total_Purchases'] > 0]

# Count users at each stage
funnel_counts = {
    'Visited Site': len(visited),
    'Added to Cart': len(added_to_cart),
    'Purchased': len(purchased)
}

# Convert to DataFrame
funnel_df = pd.DataFrame(list(funnel_counts.items()), columns=['Stage', 'Users'])

# Plot funnel chart using Plotly
fig = px.funnel(funnel_df, x='Users', y='Stage', title='Customer Conversion Funnel')
st.plotly_chart(fig)

import streamlit as st

with st.expander("View Insights:"):
    st.markdown("""
    - **Visited Site → Added to Cart:**  
       **91.8%** of users added items to cart (459 out of 500) — strong initial engagement.

    - **Added to Cart → Purchased:**  
      **87.4%** of cart users completed purchase (401 out of 459) — efficient checkout process.

    - **Overall Site Conversion Rate:**  
      **80.2%** of visitors made a purchase — a healthy funnel with minimal drop-offs.

    **Actionable Insight:**  
    - Maintain seamless user journey to preserve high conversion rates.  
    - Explore slight improvements at the cart stage to push conversion beyond 85%.
    """)


st.markdown("""
<div style="background-image: url('https://www.transparenttextures.com/patterns/cubes.png'); padding: 10px 20px; border-radius: 10px;text-align: center;">
    <h2 style="color: #88304E;">Churn Predictor:</h2>
    <p style="color: #F7374F; font-size: 16px; font-family: 'Arial';">
    Empower your retention strategy with smart churn forecasting.
    </p>
</div>
""", unsafe_allow_html=True)



# Upload CSV file
uploaded_file = st.file_uploader("Upload E-commerce Customer CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Preview of Uploaded Data")
    st.dataframe(df.head())

    # Define churn: 1 if Total_Purchases == 0, else 0
    df['Churn'] = df['Total_Purchases'].apply(lambda x: 1 if x == 0 else 0)

    # Encode categorical variables and store LabelEncoders
    le_dict = {}
    for col in ['Gender', 'Location', 'Device_Type']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le

    # Drop User_ID and Total_Purchases (not used for model input)
    df.drop(columns=['User_ID', 'Total_Purchases'], inplace=True)

    # Define features and target
    X = df.drop('Churn', axis=1)
    y = df['Churn']

    # Handle class imbalance
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled)

    # Feature scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train model
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    cr = classification_report(y_test, y_pred, output_dict=True)

    st.subheader("📊 Model Performance")
    st.metric("Accuracy", f"{acc:.2%}")
    
    st.write("### Confusion Matrix")
    cm_df = pd.DataFrame(cm, columns=['Predicted Not Churn', 'Predicted Churn'],
                         index=['Actual Not Churn', 'Actual Churn'])
    st.dataframe(cm_df)

    st.write("### Classification Report")
    st.dataframe(pd.DataFrame(cr).transpose())

    st.success("Model trained successfully. You can now manually enter customer data for churn prediction.")

    # Manual prediction section
    st.markdown("---")
    st.subheader("🧾 Manual Churn Prediction")

    with st.form("churn_form"):
        gender_input = st.selectbox("Gender", options=le_dict['Gender'].classes_)
        location_input = st.selectbox("Location", options=le_dict['Location'].classes_)
        device_input = st.selectbox("Device Type", options=le_dict['Device_Type'].classes_)
        age = st.number_input("Age", min_value=10, max_value=100, value=30)
        browsing_time = st.number_input("Product Browsing Time (minutes)", min_value=0.0, step=1.0)
        pages_viewed = st.number_input("Total Pages Viewed", min_value=0, step=1)
        items_added = st.number_input("Items Added to Cart", min_value=0, step=1)
        submitted = st.form_submit_button("Predict Churn")

    if submitted:
        # Encode user inputs
        gender = le_dict['Gender'].transform([gender_input])[0]
        location = le_dict['Location'].transform([location_input])[0]
        device = le_dict['Device_Type'].transform([device_input])[0]

        # Create input array
        input_array = np.array([[gender, age, location, device, browsing_time, pages_viewed, items_added]])
        input_scaled = scaler.transform(input_array)

        # Make prediction
        prob = model.predict_proba(input_scaled)[0][1]
        pred = model.predict(input_scaled)[0]

        st.markdown("### 🔍 Churn Prediction Result")
        st.metric("Churn Probability", f"{prob:.2%}")
        st.success("Prediction: Churn" if pred == 1 else "Prediction: Not Churn")





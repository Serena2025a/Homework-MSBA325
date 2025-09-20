import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Lebanon’s Development Dilemma",
    page_icon="📊",
    layout="wide"
)

st.title("Lebanon’s Unfinished Story: Between Infrastructure Projects and Economic Realities")
st.caption("Uncover the story of Lebanon’s finances and infrastructure projects shaping its regions")

# Add an image 
st.image("https://d2p9i44hnkrmkx.cloudfront.net/files/page-8%20Cropped.jpg", use_container_width=True, caption="Beirut skyline (illustrative)")

# Subheader 1
st.subheader("Section 1:Infrastructure: Signs of Promise or Neglect?")
df = pd.read_csv("https://linked.aub.edu.lb/pkgcube/data/85ad3210ab85ae76a878453fad9ce16f_20240905_164730.csv")


df.columns = df.columns.str.strip()


df['Area'] = df['refArea'].astype(str).str.extract(r'/page/([^/]+)|/resource/([^/]+)').fillna('').sum(axis=1)


district_map = {
    
    'Baabda_District': 'Mount Lebanon',
    'Byblos_District': 'Mount Lebanon',
    'Keserwan_District': 'Mount Lebanon',
    'Aley_District': 'Mount Lebanon',
    'Matn_District': 'Mount Lebanon',
    'Mount_Lebanon_Governorate': 'Mount Lebanon',

    
    'Tyre_District': 'South',
    'Sidon_District': 'South',
    'South_Governorate': 'South',

    
    'Akkar_Governorate': 'Akkar',

    
    'Bsharri_District': 'North',
    'Batroun_District': 'North',
    'Zgharta_District': 'North',
    'Minieh-Danniyeh_District': 'North',
    'Tripoli_District,_Lebanon': 'North',
    'North_Governorate': 'North',
    'MiniyehâDanniyeh_District': 'North',

    
    'Marjeyoun_District': 'Nabatieh',
    'Bint_Jbeil_District': 'Nabatieh',
    'Hasbaya_District': 'Nabatieh',
    'Nabatieh_Governorate': 'Nabatieh',

    
    'Zahlé_District': 'Beqaa',
    'Western_Beqaa_District': 'Beqaa',
    'Beqaa_Governorate': 'Beqaa',
    'ZahlÃ©_District': 'Beqaa',

    
    'Hermel_District': 'Baalbek-Hermel',
    'Baalbek-Hermel_Governorate': 'Baalbek-Hermel'
}


df['Governorate'] = df['Area'].replace(district_map)
    
population_size = {
    "Beqaa": 540000,
    "Mount Lebanon": 1831000,  
    "Nabatieh": 391000,
      "Akkar": 432000,
    "North": 803000,
    "Baalbek-Hermel": 472000,
    "South": 602000,
    
}

min_pop, max_pop = st.slider(
    "Population size in Governorates",
    min_value=350000,
    max_value=1831000,  
    value=(350000, 1831000)
)


   
Choosen_governorates = [gov for gov, pop in population_size.items() if min_pop<= pop <= max_pop]

    
initiative = df[df['Governorate'].isin(Choosen_governorates)]
initiative = initiative[initiative['Existence of initiatives and projects  in the past five years to improve infrastructure - exists'] == 1]

  
area_counts = initiative['Governorate'].value_counts()
df_counts = area_counts.reset_index()              
df_counts.columns = ['Governorate', 'Projects'] 
df_counts = df_counts.sort_values("Projects", ascending=True)
   
fig = px.bar(
    df_counts,                  
    x='Governorate',           
    y='Projects',              
    title="Infrastructure Initiatives by Governorate (2018-2023)",
    labels={'Governorate': 'Governorates', 'Projects': "Existence of initiatives and projects"},
    template="plotly_white"     
)
fig.update_layout(
    xaxis=dict(
        categoryorder="array",                                
        categoryarray=df_counts['Governorate'].tolist(),     
        rangeslider=dict(visible=True),
        type="category"
    ),
    margin=dict(l=40, r=20, t=60, b=60)
)
 
st.plotly_chart(fig)

st.markdown(
    "<div style='margin-top:1rem; font-weight:600;'> Which Districts Are Left Behind? </div>",
    unsafe_allow_html=True
)

if st.button("📍Spot the Zero-Initiative Districts", key="no_infra_towns"):
    flag_col = "Existence of initiatives and projects  in the past five years to improve infrastructure - exists"

    # Extract districts from refArea (e.g., 'Baabda_District', 'Tyre_District', etc.)
    df["District0"] = (
        df["refArea"].astype(str)
          .str.extract(r"/page/([^/]+)|/resource/([^/]+)")
          .fillna("")
          .sum(axis=1)
    )

    # Keep only rows where initiatives == 0 
    zero_rows = df[df[flag_col] == 0].copy()

    # Districts with zero initiatives
    district_zero = zero_rows[["District0"]].dropna().drop_duplicates()

    # District -> (lat, lon) dictionary 
    district_centroids = {
        # Mount Lebanon area
        "Baabda_District": (33.8336, 35.5442),
        "Byblos_District": (34.1230, 35.6518),
        "Keserwan_District": (34.0100, 35.6500),
        "Aley_District": (33.8106, 35.6056),
        "Matn_District": (33.9089, 35.6556),
        

        # South
        "Tyre_District": (33.2700, 35.2033),
        "Sidon_District": (33.5606, 35.3756),
       

        # Akkar / North
        "Bsharri_District": (34.2519, 36.0100),
        "Batroun_District": (34.2550, 35.6580),
        "Zgharta_District": (34.3986, 35.8956),
        "Minieh-Danniyeh_District": (34.5070, 35.9220),
        "Tripoli_District,_Lebanon": (34.4381, 35.8390),
        "MiniyehâDanniyeh_District": (34.5070, 35.9220),  

        # Nabatieh
        "Marjeyoun_District": (33.3600, 35.6000),
        "Bint_Jbeil_District": (33.1183, 35.4322),
        "Hasbaya_District": (33.3980, 35.6850),

        # Beqaa
        "Zahlé_District": (33.8467, 35.9020),
        "Western_Beqaa_District": (33.6050, 35.7300),
        "ZahlÃ©_District": (33.8467, 35.9020),  

        # Baalbek-Hermel
        "Hermel_District": (34.3934, 36.3717),
        
    }

    # Build map_df  using the centroids
    map_rows = []
    missing = []
    for t in district_zero["District0"]:
        if t in district_centroids:
            lat, lon = district_centroids[t]
            map_rows.append({"lat": lat, "lon": lon})    

    map_df = pd.DataFrame(map_rows)
    st.map(map_df, zoom=7)
   
st.markdown(
    '<div style="padding: 10px; border-radius: 5px; margin-bottom: 10px;">'
    '<strong style="font-size: 18px;">Uncover Key Patterns in Infrastructure </strong>'
    '</div>', 
    unsafe_allow_html=True
)

# Create a button
if st.button("⬇️ Click the button",key="infra_insights"):
    st.markdown("""
***Insights:***
                
27% of infrastructure projects belong to Mount Lebanon. However, significant locations like Baalbek-Hermel accounts for only 5% of the infrastructure projects. 
While Mount Lebanon's higher project density is in line with its larger population and dynamic economy, it runs the risk of intensifying inequality with rural districts.
In the last five years, almost 80% of towns have not had any infrastructure projects. This raises questions about planning and execution.

***Recommendation:***
                
Reconstruction and urgent funding are desperately needed for Lebanon's infrastructure, especially in the governorates of Beqaa, Nabatiyeh, Baalbeck-Hermel and in the South. It is crucial to allocate funds for the reconstruction and modernization of the country's infrastructure.

***Reasons to act:***
                
-Infrastructure (roads, utilities, and basic services) has deteriorated severely in recent years. 
                
-Weak road networks and failing utilities have direct effects on the lives of citizens: raise risks of accidents, health hazards, and social unrest.
                
-Improved infrastructure increases economic opportunities and rebuilds confidence in the government.
                
-Giving urban areas priority, carries the risk of excluding rural communities and encouraging their migration to urban areas. Beirut, Tripoli, and Zahle may become overcrowded with residents from underserved neighborhoods, worsening traffic, housing shortages, and public service failures.

   
    """)

#Subhearder 2
st.subheader("Section 2:What Holds Back Infrastructure Dreams?")
df = pd.read_csv("https://linked.aub.edu.lb/pkgcube/data/ec4c40221073bbdf6f75b6c6127249c3_20240905_173222.csv")
df.columns = df.columns.str.strip()
df_cleaned = df[df['Value'] > 1000] 
df = df_cleaned.groupby('refPeriod', as_index=False)['Value'].mean()  
df = df.sort_values(by='refPeriod') 
df['Value_billion'] = df['Value'] / 1e9   
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['refPeriod'], y=df['Value_billion'], 
                         mode='lines+markers',
                         line=dict(color='black', dash='dash'),
                         name="External Debt"))

fig.update_layout(
    title="External Debt in Lebanon as a Function of Time",
    xaxis_title="Time (years)",
    yaxis_title="External Debt (Billion USD)",
    plot_bgcolor="lightgrey",  
    yaxis=dict(tickmode='linear', tick0=0, dtick=1000),  
    showlegend=False
)

steps = []
for i in range(len(df)):
    step = dict(
        method="update",
        args=[{"x": [df['refPeriod'][:i+1]], "y": [df['Value_billion'][:i+1]]}], 
        label=str(df['refPeriod'].iloc[i]),
    )
    steps.append(step)

sliders = [dict(
    active=0,
    currentvalue={"prefix": "Time (years)="},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(sliders=sliders)
st.plotly_chart(fig)

st.markdown(
    '<div style="padding: 10px; border-radius: 5px; margin-bottom: 10px;">'
    '<strong style="font-size: 18px;">Debt or Development: Which Path Will Lebanon Take?</strong>'
    '</div>', 
    unsafe_allow_html=True
)

# Create a button
if st.button("⬇️ Click the button",key="debt_insights"):
    st.markdown("""
***Insights:***

Lebanese external debt has grown significantly during the past 60 years, from 42 million USD to around 13 billion USD. Between 2018 and 2023, Lebanon's external debt remained extremely high and fluctuating: peaking in 2018–2019, declining in 2020–2021, and then rising once again in 2022.Therefore, the government's capacity to fund new infrastructure is constrained by the high level of debt. Initiatives for infrastructure is dispersed unevenly.

***Debt vs. Infrastructure Dilemma:***

Postponing infrastructure maintenance and projects due to debt pressure transforms minor repairs into later costly reconstruction. Additionally, lack of infrastructure discourages investor interest in Lebanon, further aggravating the country’s economic challenges.

This makes infrastructure not just a spending choice, but a critical foundation that must progress alongside debt solutions, since neglecting it only magnifies future costs and instability.

***Recommendations and Next Steps:***

👉Develop a Targeted Recovery Plan:Make sure every district has at least a basic level of infrastructure projects. Prioritize governorates that have been left behind, such as South, Beqaa, and Baalbek-Hermel.

👉Secure Long-Term Funding: Restructure debt to free up funds for investments and reduce the pressure of immediate repayment. Additionally, raise funds via public-private partnerships (PPPs), development banks, and international donors. 

👉Prioritize Quick Wins: Start small, obvious improvements like repairing roads. Quick wins rapidly enhance everyday life and let donors and citizens know that progress is being made.

👉Enhance Accountability and Transparency: To promote co-financing and rebuild confidence, openly share project pipelines, expenses, and schedules. Moreover, to guarantee that projects are completed on schedule, use independent monitoring.


    """)

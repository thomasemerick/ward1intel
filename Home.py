import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Ward 1 Intel", page_icon="🗳️", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebarNavItems"] li:first-child {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗳️ DC Ward 1 Democratic Primary Intel")
st.caption("Data and reporting on the June 16 primary and aftermath | By Thomas Emerick")

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Overview",
    "♻️ RCV Sim",
    "📋 Issue Survey",
    "🎯 Precinct Data",
])


# ══════════════════════════════════════════════════════════
# TAB 1 — Overview
# ══════════════════════════════════════════════════════════

with tab1:
    st.subheader("🗺️ Overview")
    st.caption("Broad contours of the race")

    st.markdown("""
                
    This is an extremely fascinating five-way race with no candidate hitting 20% among likely voters in the one major poll fielded back in March. Each campaign has been very active with staff and sign game around Ward 1 with 55% of voters undecided entering the stretch run.
    """)         
  
    st.info("""
    **🗳️ RCV Flashback: The Kathryn Garcia Playbook (NYC 2021)**

    In the June 2021 NYC Democratic mayoral primary, Kathryn Garcia trailed Eric Adams by ~100,000 first-choice votes. She won the somewhat liberal lane while Maya Wiley locked up the hard left and Adams owned moderate/conservative Democrats. But Garcia's ideological compatability on key issues with other candidates made her the consensus second and third choice across ideological lines. Wiley voters ranked her #2 at high rates, and moderate voters who couldn't stomach Adams found Garcia acceptable.
            
    After all RCV rounds, Garcia lost by fewer than 8,000 votes. However, there are two additional minor candidates each polling close to 10% among decided voters in the recent PPP poll. Garcia leapfrogged Wiley to reach the final round by outperforming her on transfer votes from Andrew Yang ballots, but could have defeated Adams by doing a little better than at parity when it came to transfers from Scott Stringer or a couple other lower-finishing candidates.

    """)
    st.divider()
    st.markdown("#### 📍 Ward 1 Precinct Voter Heatmap")
    import streamlit.components.v1 as components
    with open("ward1_heatmap.html", "r") as f:
        html = f.read()

    html = html.replace('font-size:11px', 'font-size:15px')

    components.html(html, height=600, scrolling=False)

    st.divider()
    st.markdown("#### 📍 Ward 1 Precinct Quick Reference")
    precinct_ref = pd.DataFrame({
        "Precinct": [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137],
        "Neighborhood": ["LeDroit Park", "U Street", "Columbia Heights", "Adams Morgan", "Adams Morgan",
                        "Adams Morgan", "Columbia Heights", "Pleasant Plains", "Park View",
                        "Mt Pleasant/Col Hts", "Mount Pleasant", "Columbia Heights",
                        "Columbia Heights", "Park View", "U Street"],
        "Visual Markers": [
            "Howard Playground, LeDroit Park",
            "Lincoln Theater, Busboys & Poets",
            "Malcolm X Park, Cardozo Campus",
            "Madam's Organ, Marie Reed Rec",
            "Washington Hilton, Kalorama Park",
            "Columbia Rd Safeway, Lanier Hts",
            "Columbia Hts Metro & Community Ctr",
            "Howard University, 930 Club",
            "Bruce Monroe Park, Midlands",
            "Mt Pleasant bars, Co Hts Target",
            "Argyle Market, Bancroft School",
            "Park Rd Safeway, Thip Khao",
            "Mi Casita Bakery/Deli, The Coupe",
            "Afro Lounge, Looking Glass Lounge",
            "Nellie's Sports Bar, All Souls",
        ],
        "Street Boundaries (W to E; S to N)": [
            "4th to 1st; Rhode Island to Michigan",
            "16th to 9th; U>S detour 15th-14th>T>Vermont to Florida",
            "16th to 11th; Florida to Euclid",
            "18th to 16th; U to Euclid",
            "Connecticut to 18th; Florida to Adams Mills",
            "Rock Creek to 16th; Adams Mill>Euclid to Harvard",
            "16th to 11th; Euclid to Columbia detour Irving 15th-14th",
            "11th to 4th; Florida to Columbia",
            "11th to Park Place; Columbia to Park Road",
            "RockCrk to 11th; Harv>Clmbia detour Irving 15th-14th to Lamont>Park",
            "Rock Creek to 16th; Lamont to Piney Branch",
            "16th to Holmead; Park to Spring",
            "Holmead to New Hampshire; Park to Spring",
            "New Hampshr to Park Plc; Park Rd to Rock Crk Church Rd",
            "13th to Wiltberger Ave; S to T>Vermont>Florida",
        ],
        "Reg_Dems": [870, 4038, 2978, 2756, 4068, 3479, 3962, 3336, 2718, 3911, 3322, 3337, 1713, 1751, 1110],
    })

    st.dataframe(precinct_ref, use_container_width=True, hide_index=True,
        column_config={
            "Reg_Dems": st.column_config.ProgressColumn(
                "Registered Dems", min_value=0, max_value=4500, format="%d"
            ),
            "Boundaries": st.column_config.TextColumn("Street Boundaries", width="large"),
        }
    )


    st.divider()
    st.markdown("#### 🗳️ 2022 Winner by Voting Precinct")
    st.caption("2022 Ward 1 Council Democratic Primary — Nadeau vs Czapary vs Harris")
    with open("ward1_2022_heatmap.html", "r") as f:
        html_2022 = f.read()
    html_2022 = html_2022.replace('font-size:11px', 'font-size:15px')
    components.html(html_2022, height=900, scrolling=False)
    st.caption("Brianne Nadeau 49%, Salah Czapary 31%, and Sabel Harris at 20% despite no precinct plurality wins.")
# ══════════════════════════════════════════════════════════
# TAB 2 — RCV SIM
# ══════════════════════════════════════════════════════════


with tab2:
    st.subheader("♻️ RCV Simulation")
    st.caption("RCV Simulation by GGWash/PPP Ward 1 poll March 27-29 2026, n=232 likely Dem primary voters")

    st.markdown("""
    **Mind you, candidates have had more than two months since this poll was fielded to motivate and persuade voters. But it's the best we got.
    """)


    st.markdown("#### RCV Simulation Among Decided Voters")
        # RCV Simulation
    rcv_rounds = pd.DataFrame({
        "Round": [
            "Round 1 — All decided voters",
            "Round 2 — After Lynch eliminated",
            "Round 3 — After Reyes Yanes eliminated (projected)",
            "Round 4 — Final: Brown vs Raj (projected)",
        ],
        "Raj %": [42, 43, 45, 51],
        "Brown %": [25, 26, 29, 49],
        "Trindade Deramo %": [16, 17, 20, 0],
        "Reyes_Yanes %": [9, 10, 0, 0],
        "Lynch %": [8, 0, 0, 0],
        "Exhausted %": [0, 4, 6, 0],
      
    })

    st.dataframe(rcv_rounds, use_container_width=True, hide_index=True,
        column_config={
            "Raj %": st.column_config.NumberColumn(format="%d%%"),
            "Brown %": st.column_config.NumberColumn(format="%d%%"),
            "Trindade Deramo %": st.column_config.NumberColumn(format="%d%%"),
            "Reyes_Yanes %": st.column_config.NumberColumn("Reyes Yanes %", format="%d%%"),
            "Lynch %": st.column_config.NumberColumn(format="%d%%"),
            "Exhausted %": st.column_config.NumberColumn(format="%d%%"),
        }
    )


    st.markdown("""
    #### All likely voters including undecideds (est.):
    - 🔵 Raj: 18%
    - 🟡 Brown: 13%  
    - 🟢 Trindade Deramo: 7%
    - 🟠 Reyes Yanes: 4%
    - ⚪ Lynch: 3%
    - ❓ Undecided: 55%
    """)
    


# ══════════════════════════════════════════════════════════
# TAB 3 — WAPO CANDIDATE SURVEY
# ══════════════════════════════════════════════════════════
with tab3:
    st.subheader("📋 Washington Post Candidate Survey")
    st.caption("Source: Washington Post, June 3 2026. Binary questions show Yes/No. Open-ended responses are concise summaries to adjust for candidates listing myriad proposals for each issue when in governing reality you eventually have to prioritize.")

    candidates = ["Jackie Reyes Yanes", "Terry Lynch", "Aparna Raj", "Rashida Brown", "Miguel Trindade Deramo"]

    def candidate_table(rows, candidates):
        html = '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:13px;">'
        html += '<thead><tr>'
        html += '<th style="text-align:left;padding:6px 8px;border-bottom:1px solid #ddd;width:80px;font-weight:500;">Issue</th>'
        for c in candidates:
            html += f'<th style="text-align:left;padding:6px 8px;border-bottom:1px solid #ddd;font-weight:500;">{c}</th>'
        html += '</tr></thead><tbody>'
        for row in rows:
            html += '<tr>'
            for i, cell in enumerate(row):
                style = 'padding:6px 8px;border-bottom:0.5px solid #eee;vertical-align:top;'
                if i == 0:
                    style += 'font-weight:500;width:80px;white-space:nowrap;'
                html += f'<td style="{style}">{cell}</td>'
            html += '</tr>'
        html += '</tbody></table></div>'
        return html

    st.markdown("#### Economy & Housing")
    econ_rows = [
        ["Tax Policy",
        "Targeted tax relief and incentives, stronger spending oversight",
        "Top 1% household incomes and billionaires tax, pro athlete tax",
        "Higher capital gains tax, stronger Business Activity Tax",
        "Higher inheritance tax, stronger Business Activity Tax",
        "Taxes to disincentivize empty lots, no sales tax increase"],
        ["DC Economy",
        "Pivot from fed-reliant economy toward local small business revival",
        "Introduce program to sell vacant properties at market value",
        "Green New Deal for DC and social housing at scale",
        "Reskill workforce for health care, tech, and AI thru programs",
        "Incentivize business and investment, bring back streateries"],
        ["Econ Inequality",
        "Help local businesses avoid displacement and hire local workforce",
        "Additional top 1% or billionaires tax to fund education programs",
        "Free child care for all thru stronger Business Activity Tax",
        "Free child care for all and higher pay for early childhood educators",
        "Housing costs thru zoning, investment, supply market and subsidized"],
        ["Rent Stabilization", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        ["Congestion Pricing", "❌ No", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        ["Robotaxis", "❌ No", "✅ Yes", "❌ No", "❌ No", "❌ No"],
    ]
    st.markdown(candidate_table(econ_rows, candidates), unsafe_allow_html=True)

    st.divider()

    st.markdown("#### Crime & Public Safety")
    safety_rows = [
        ["Teen Curfew", "✅ Yes", "✅ Yes", "❌ No", "❌ No", "❌ No"],
        ["Curfew Detail",
        "Temporary, targeted solution while ramping up rec and work programs",
        "Curfew should be one of many tools including youth athletics",
        "DC youth would face attacks MPD is with ICE, let the youth design programs",
        "Advisory boards, mental health services, safe spaces, and year-round employment",
        "Reactivate advisory council and invest in violence interruption programs",],
        ["Police Level", "Not enough", "Right amount", "Right amount", "Right amount", "Right amount"],
        ["Police Detail",
        "Community policing and public services",
        "Community policing and public services",
        "Divest from overtime payment to fund other services",
        "Community policing and public services",
        "Accountability for overtime payment and public services"],
    ]
    st.markdown(candidate_table(safety_rows, candidates), unsafe_allow_html=True)

    st.divider()

    st.markdown("#### Schools & Federal Control")
    social_rows = [
        ["Schools",
        "Stronger pipelines for local residents to enter education workforce",
        "Youth engagement after school hours through arts, sports, and clubs",
        "Consolidate power within the State Board of Education",
        "Increase teacher pay, decrease class sizes",
        "Leverage Dept of Health and Human Services to address truancy"],
        ["Trump/GOP",
        "Standing firm when necessary",
        "Forge alliances with DMV groups",
        "Take the fight nationwide",
        "Work strategically with mayor",
        "Scale up DNC Home Rule Caucus"],
    ]
    st.markdown(candidate_table(social_rows, candidates), unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# TAB 4 — Underlying Tables
# ══════════════════════════════════════════════════════════
with tab4:
    st.subheader("🎯 Precinct Data")
    

    st.markdown("#### 📂 Sortable Voting Precinct Data")
    underlying = pd.read_csv('ward1_underlying.csv')
    underlying['Homicides'] = underlying['Homicides'].fillna(0).astype(int)

    cols = ['Precinct', 'Neighborhood', 'Registered_Dems', 'Biz_Closed_Since2015'] + [c for c in underlying.columns if c not in ['Precinct', 'Neighborhood', 'Registered_Dems', 'Biz_Closed_Since2015']]
    underlying = underlying[cols]

    st.dataframe(
        underlying,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Registered_Dems": st.column_config.ProgressColumn(
            "Registered Dems", min_value=0, max_value=4500, format="%d"
            ),
            "Biz_Closed_Since2015": st.column_config.NumberColumn("Biz Closure", format="%d"),
            "Anti_Nadeau_Pct": st.column_config.NumberColumn("Anti-Nadeau %", format="%.1f%%"),
            "Czapary_2022": st.column_config.NumberColumn("Czapary Votes", format="%d"),
            "Harris_2022": st.column_config.NumberColumn("Harris Votes", format="%d"),
            "Hispanic_Pct": st.column_config.NumberColumn("Hispanic %", format="%.1f%%"),
            "Black_Pct": st.column_config.NumberColumn("Black %", format="%.1f%%"),
            "White_Pct": st.column_config.NumberColumn("White %", format="%.1f%%"),
            "Asian_Pct": st.column_config.NumberColumn("Asian %", format="%.1f%%"),
            "Asian_Other_Pct": st.column_config.NumberColumn("Asian+Other %", format="%.1f%%"),
            "Minrty_NoAlign_Pct": st.column_config.NumberColumn("Minrty_NoAlign %", format="%.1f%%"),
            "Postgrad_Pct": st.column_config.NumberColumn("Postgrad %", format="%.1f%%"),
            "Median_Age": st.column_config.NumberColumn("Median Age", format="%.1f"),
            "Under18_Pct": st.column_config.NumberColumn("Under 18 %", format="%.1f%%"),
            "White_46plus_Pct": st.column_config.NumberColumn("White 46+ %", format="%.1f%%"),
            "Homeowner_Pct": st.column_config.NumberColumn("Homeowner %", format="%.1f%%"),
            "Not_Leftist_Score": st.column_config.NumberColumn("Not_Leftist Score", format="%.1f"),
        }
    )
    st.caption("Sources: MPD (2020–2026), DC DLCP business licenses (opened 2015+, now closed), DCBOE 2022 primary, Census ACS 2023, Census DHC 2020")

    st.markdown("""
    ## 🎯 Ward 1 Precinct Issue Salience Model

    A data-driven map of which issues are likely to resonate in each Ward 1 precinct — 
    built from 2024 DCBOE turnout data, Census demographics, MPD crime data, 
    DC business license records, and 2022 primary results.

    Red dots indicate precincts where the underlying data suggests that issue 
    carries particular weight. Campaign mileage may vary — this is a starting point 
    for any candidate or organizer, not a prescription.

    - 🔴 High salience — data suggests this issue is especially relevant here
    - 🟡 Moderate or mixed signal
    - **Untapped Voters** = registered Dems who didn't vote in 2024
    """)

    st.subheader("🗺️ Precinct Issue Salience Matrix")
    st.caption("15 Ward 1 precincts scored across 10 issue and identity variables using public data sources")

    combined = pd.DataFrame({
        "Precinct": [40, 41, 39, 35, 36, 23, 37, 38, 43, 22, 42, 25, 24, 20, 137],
        "Neighborhood": [
            "Mount Pleasant", "Columbia Heights", "Mount Pleasant", "Adams Morgan", "Columbia Heights",
            "Columbia Heights", "Pleasant Plains", "Park View", "Park View", "U Street",
            "Columbia Heights", "Adams Morgan", "Adams Morgan", "LeDroit Park", "U Street"
        ],
        "Crime": ["🔴","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡"],
        "Business": ["🔴","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🔴","🔴","🟡","🟡","🟡","🟡"],
        "Schools": ["🟡","🟡","🟡","🔴","🔴","🔴","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🟡"],
        "LGBTQ": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🔴","🟡","🟡","🟡","🟡"],
        "Anti_Nadeau": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🔴","🟡","🔴","🟡"],
        "Hispanic": ["🟡","🟡","🔴","🟡","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🔴","🔴","🟡"],
        "LGBTQ_Id": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🔴","🟡","🟡","🟡","🟡"],
        "White_46+": ["🟡","🟡","🟡","🔴","🔴","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🟡"],
        "Moderate": ["🔴","🟡","🔴","🔴","🔴","🟡","🔴","🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡"],
        "White_NonLeft": ["🟡","🟡","🟡","🔴","🔴","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🟡"],
        "Untapped_Voters": [2310, 2563, 2873, 2458, 3080, 2355, 2698, 2085, 1343, 2964, 1246, 2804, 1920, 671, 890],
    })

    st.dataframe(combined, use_container_width=True)

    st.divider()
    st.markdown("#### 📋 How Each Variable Is Measured")
    st.markdown("""
    | Variable | Source | What Makes a Precinct 🔴 |
    |---|---|---|
    | **Crime** | MPD incident data 2020–2026 | Top precincts by weighted crime density (homicide x2, all others x1) |
    | **Business** | DC DLCP business licenses | High closure rate among businesses opened since 2015 |
    | **Schools** | Census B09001 (2023 ACS) | Above-average under-18 population |
    | **LGBTQ** | Venue geography + residential research | Known LGBTQ venue concentration and residential density |
    | **Anti_Nadeau** | 2022 DCBOE primary results | High non-Nadeau vote share (Czapary x2 weight, Harris x1) |
    | **Hispanic** | Census B03003 (2023 ACS) | Hispanic/Latino population ≥ 22% |
    | **LGBTQ_Id** | Census same-sex household data | Same-sex household density |
    | **White_46+** | Census B01001A (2023 ACS) | Above-average white population 45+ |
    | **Moderate** | Census composite | Low postgrad + high Anti-Nadeau vote
                
    """)
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

st.title("🗳️ Ward 1 Campaign Intel")
st.caption("Targeting model for Miguel Trindade Deramo — June 16, 2026 Primary")
st.divider()

# ── REAL DCBOE DATA — 2024 Primary, Ward 1 Precincts ──
precincts = pd.DataFrame({
    "Precinct": [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137],
    "Neighborhood": [
        "Columbia Heights",
        "Columbia Heights",
        "Mount Pleasant",
        "Mount Pleasant",
        "Columbia Heights",
        "Petworth",
        "Petworth",
        "Park View",
        "Park View",
        "Columbia Heights",
        "U Street",
        "Adams Morgan",
        "Adams Morgan",
        "U Street",
        "Columbia Heights",
    ],
    "Registered_Dems": [870, 4038, 2978, 2756, 4068, 3479, 3962, 3336, 2718, 3911, 3322, 3337, 1713, 1751, 1110],
    "Votes_Cast_2024": [199, 1074, 623, 836, 1264, 1021, 882, 638, 633, 1038, 1012, 774, 467, 408, 220],
    "Median_Age": [32, 33, 35, 34, 33, 45, 46, 44, 43, 31, 30, 32, 31, 30, 33],
    "Median_Tenure_yrs": [3.8, 4.1, 5.2, 4.8, 4.0, 11.5, 12.2, 10.8, 11.1, 3.5, 3.2, 3.9, 3.4, 3.1, 4.2],
    "Owner_Occupied_pct": [20, 22, 28, 26, 21, 44, 47, 42, 43, 15, 12, 18, 14, 13, 23],
})

# ── SCORING MODEL ──
precincts["Turnout_pct"] = (precincts["Votes_Cast_2024"] / precincts["Registered_Dems"] * 100).round(1)
precincts["Untapped_Voters"] = precincts["Registered_Dems"] - precincts["Votes_Cast_2024"]
precincts["Age_Score"] = ((precincts["Median_Age"] - 30) / 25 * 100).clip(0, 100)
precincts["Tenure_Score"] = (precincts["Median_Tenure_yrs"] / 15 * 100).clip(0, 100)
precincts["Opportunity_Score"] = (1 - precincts["Turnout_pct"] / 100) * 100
precincts["Owner_Flag"] = precincts["Owner_Occupied_pct"].apply(
    lambda x: "⚠️ Watch" if x > 35 else "✅ Renter-majority"
)
precincts["Priority_Score"] = (
    precincts["Age_Score"] * 0.35 +
    precincts["Tenure_Score"] * 0.35 +
    precincts["Opportunity_Score"] * 0.30
).round(1)
precincts["Priority_Tier"] = pd.cut(
    precincts["Priority_Score"],
    bins=[0, 40, 65, 100],
    labels=["🔵 Low", "🟡 Medium", "🔴 High Priority"]
)

# ── METRICS ──
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ward 1 Registered Dems", f"{precincts['Registered_Dems'].sum():,}")
col2.metric("2024 Primary Voters", f"{precincts['Votes_Cast_2024'].sum():,}")
col3.metric("Untapped Voters", f"{precincts['Untapped_Voters'].sum():,}")
col4.metric("Avg Turnout", f"{precincts['Turnout_pct'].mean():.1f}%")

st.divider()

# ── PRIORITY TABLE ──
st.subheader("🎯 Precinct Priority Table — Where to Canvass")
st.caption("Scored on: age (35%), tenure (35%), low turnout opportunity (30%). Homeownership flagged separately.")

display_cols = [
    "Precinct", "Neighborhood", "Priority_Tier", "Priority_Score",
    "Untapped_Voters", "Turnout_pct", "Median_Age",
    "Median_Tenure_yrs", "Owner_Occupied_pct", "Owner_Flag"
]

st.dataframe(
    precincts[display_cols].sort_values("Priority_Score", ascending=False),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Priority_Score": st.column_config.ProgressColumn(
            "Priority Score", min_value=0, max_value=100, format="%.1f"
        ),
        "Turnout_pct": st.column_config.NumberColumn("2024 Turnout %", format="%.1f%%"),
        "Owner_Occupied_pct": st.column_config.NumberColumn("Owner %", format="%.0f%%"),
        "Median_Tenure_yrs": st.column_config.NumberColumn("Avg Tenure (yrs)", format="%.1f"),
    }
)

st.divider()

# ── CITYCAST POLL ──
st.subheader("📊 CityCast DC Poll — Mayoral Race Intelligence (May 12–17, 2026)")
st.caption("n=487 registered Democrats | MOE ±4.7pts | Source: CityCast DC / TrueDot")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Lewis George (1st choice)", "39%")
col2.metric("McDuffie (1st choice)", "34%", delta="-5pts")
col3.metric("Undecided", "24%", delta="Up for grabs")
col4.metric("McDuffie 2nd choice", "27%", delta="vs 15% LG", delta_color="normal")

st.divider()

demo_data = pd.DataFrame({
    "Voter Segment": [
        "Grew up in DC (natives)",
        "Moved here 10+ years ago",
        "Moved here within 10 years",
        "Baby Boomers+",
        "Millennials",
        "Gen Z",
        "White voters under 46",
        "White voters over 46",
        "Black voters under 46",
        "Black voters over 46",
        "No college degree",
        "College degree",
        "Income under $75k",
        "Income $75k–$150k",
        "Income over $150k",
        "Men",
        "Women",
        "Approve of Bowser",
        "Support youth curfews",
        "Want more police",
        "Commanders fans",
        "Get news from Instagram/TikTok",
        "Commute by bike",
    ],
    "McDuffie": [43, 38, 16, 55, 32, 28, 26, 52, 40, 46, 46, 35, 42, 33, 33, 46, 31, 55, 49, 55, 45, 25, 25],
    "Lewis_George": [26, 44, 58, 28, 51, 52, 54, 30, 34, 36, 38, 48, 37, 43, 42, 42, 46, 35, 37, 35, 26, 42, 46],
    "Ward1_Relevance": [
        "🔴 High", "🟡 Medium", "🔵 Low",
        "🔴 High", "🟡 Medium", "🔵 Low",
        "🔵 Low", "🔴 High",
        "🟡 Medium", "🔴 High",
        "🔴 High", "🟡 Medium",
        "🔴 High", "🟡 Medium", "🟡 Medium",
        "🟡 Medium", "🟡 Medium",
        "🔴 High", "🔴 High", "🔴 High",
        "🟡 Medium", "🔵 Low", "🔵 Low",
    ]
})

demo_data["McDuffie_Lead"] = demo_data["McDuffie"] - demo_data["Lewis_George"]
demo_data["Winner"] = demo_data["McDuffie_Lead"].apply(
    lambda x: f"✅ McDuffie +{x}" if x > 0 else f"❌ Lewis George +{abs(x)}"
)

st.markdown("#### 🎯 Key Demographic Splits — Who McDuffie Wins")

display_demo = demo_data[["Voter Segment", "McDuffie", "Lewis_George", "Winner", "Ward1_Relevance", "McDuffie_Lead"]].sort_values(
    "McDuffie_Lead", ascending=False
)

st.dataframe(
    display_demo.drop(columns=["McDuffie_Lead"]),
    use_container_width=True,
    hide_index=True,
    column_config={
        "McDuffie": st.column_config.NumberColumn("McDuffie %", format="%d%%"),
        "Lewis_George": st.column_config.NumberColumn("Lewis George %", format="%d%%"),
        "Ward1_Relevance": st.column_config.TextColumn("Ward 1 Relevance"),
    }
)

st.divider()

# ── WARD 1 PROBLEM AND OPPORTUNITY ──
st.markdown("#### ⚠️ Ward 1 Problem — And The Opportunity")
col1, col2 = st.columns(2)
with col1:
    st.error("""
    **Ward 1 is Lewis George territory**
    - LG leads W1 voters 37% → 19% (GGWash poll)
    - Younger, transplant-heavy, renter-majority
    - High bike commuter share → LG +21
    - Instagram/TikTok news consumers → LG +17
    """)
with col2:
    st.success("""
    **But McDuffie's voters ARE in Ward 1 — they just don't know it yet**
    - 24% undecided citywide — higher in W1
    - Native DC residents → McDuffie +17
    - Over 45 → McDuffie +27 among boomers
    - Curfew supporters → McDuffie +12
    - Bowser approvers → McDuffie leads
    - These voters exist in Petworth, Park View, Columbia Heights long-timers
    """)

st.divider()
st.subheader("🗳️ Ward 1 Council Race — Poll Intelligence (March 27–29, 2026)")
st.caption("n=232 likely Dem primary voters | MOE ±6.4pts | Source: GGWash / Public Policy Polling")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Raj (1st choice)", "42%", delta="Decided voters only")
col2.metric("Brown (1st choice)", "25%")
col3.metric("Miguel (1st choice)", "16%")
col4.metric("Reyes Yanes", "9%")
col5.metric("Lynch", "8%")

st.warning("⚠️ 127 of 232 respondents were still undecided — **the race is wide open**")

st.divider()

# RCV Simulation
st.markdown("#### ♻️ RCV Simulation — How Miguel Wins")
st.markdown("""
The path is narrow but real. Miguel + Brown are cross-endorsing — Brown asks her supporters 
to rank Miguel 2nd, Miguel asks his to rank Brown 2nd. Combined they have **41% of decided voters**.
Raj needs **50%+ to win outright** — she's at 42% among decided voters but only 18% of *all* voters.

**The math:** If undecideds break proportionally and Brown/Miguel transfer votes cleanly, 
this goes to a late round. Raj's 74% very-liberal base is a ceiling, not a floor.
""")

rcv_data = pd.DataFrame({
    "Round": ["Round 1 (decided voters)", "Round 1 (all voters est.)", "After Lynch eliminated", "After Reyes Yanes eliminated"],
    "Raj": [42, 18, 42, 43],
    "Brown": [25, 13, 26, 28],
    "Miguel": [16, 7, 17, 19],
    "Reyes_Yanes": [9, 4, 10, 0],
    "Lynch": [8, 3, 0, 0],
    "Undecided": [0, 55, 5, 10],
})

st.dataframe(
    rcv_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Raj": st.column_config.NumberColumn("Raj %", format="%d%%"),
        "Brown": st.column_config.NumberColumn("Brown %", format="%d%%"),
        "Miguel": st.column_config.NumberColumn("Miguel %", format="%d%%"),
        "Reyes_Yanes": st.column_config.NumberColumn("Reyes Yanes %", format="%d%%"),
        "Lynch": st.column_config.NumberColumn("Lynch %", format="%d%%"),
        "Undecided": st.column_config.NumberColumn("Undecided %", format="%d%%"),
    }
)

st.divider()

# The crossover confirmation
st.markdown("#### 🔗 The Raj–Lewis George Cross-Pollination — Confirmed by Data")
col1, col2 = st.columns(2)
with col1:
    st.error("""
    **Raj voters → Lewis George for mayor**
    - 62% of decided Ward 1 council voters back Lewis George
    - Only 12% back McDuffie
    - Raj's base: 74% very liberal
    - DSA → police abolitionist CoS → defund-adjacent
    """)
with col2:
    st.success("""
    **Miguel's path: find the other 12%**
    - McDuffie voters in Ward 1 are Miguel voters
    - Native DC, 45+, public safety priority
    - They exist in Petworth & Park View (see table above)
    - They just need to be turned out
    - Every McDuffie door = a Miguel door
    """)

st.divider()

# ── CANVASSING FRAME ──
st.subheader("🗣️ Door Canvassing Frame — Miguel + McDuffie Dual Ticket")
st.markdown("""
**Opening:** *"Hi, I'm volunteering for Miguel Trindade Deramo for Ward 1 Council — do you have a minute?"*

**On ranked choice:** *"This year you can rank candidates. We're asking you to put Miguel first — and if you're thinking about the mayor's race, Kenyan McDuffie shares the same values: public safety, pragmatic progress, rooted in DC."*

**On crime/public safety:** *"Miguel and McDuffie both believe keeping our streets safe isn't optional. If that's important to you, they're your ticket."*

**On DSA/Raj:** Don't mention by name. Just: *"Miguel has been your ANC commissioner — he's shown up for this ward, not just for ideology."*

**Homeowner flag precincts (35, 36, 37, 38):** Listen first on housing. If they raise affordability concerns, acknowledge — don't lead with McDuffie's market-rate stance.
""")

st.divider()
st.subheader("🧭 Voter Ideology Breakdown by Candidate — Ward 1")
st.caption("Source: GGWash/PPP Poll March 2026, n=232. First-choice voters by ideology (Q24 × Q4 crosstab).")

ideology_data = pd.DataFrame({
    "Candidate": ["Aparna Raj", "Rashida Brown", "Miguel Trindade Deramo", "Undecided"],
    "Very Liberal %": [33, 8, 8, 42],
    "Somewhat Liberal %": [10, 8, 5, 69],
    "Moderate %": [1, 24, 9, 60],
    "Conservative %": [5, 38, 0, 57],
    "Mayor → Lewis George %": [62, 44, 40, 37],
    "Mayor → McDuffie %": [6, 19, 25, 19],
})

st.dataframe(
    ideology_data,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Very Liberal %": st.column_config.ProgressColumn(
            "Very Liberal", min_value=0, max_value=100, format="%d%%"
        ),
        "Moderate %": st.column_config.ProgressColumn(
            "Moderate", min_value=0, max_value=100, format="%d%%"
        ),
        "Mayor → Lewis George %": st.column_config.NumberColumn("→ Lewis George", format="%d%%"),
        "Mayor → McDuffie %": st.column_config.NumberColumn("→ McDuffie", format="%d%%"),
    }
)

st.divider()
st.subheader("🔑 Key Findings from Full Crosstabs")

col1, col2 = st.columns(2)
with col1:
    st.error("""
    **Bad news for Miguel:**
    - Gets 0% among 65+ voters (Brown gets 21%, Raj 6%)
    - 65+ are the most reliable primary voters
    - Undecided pool is 42% very liberal → Raj territory
    - DSA endorsement still +33% more likely among voters overall
    """)
with col2:
    st.success("""
    **Good news for Miguel:**
    - Labor union endorsement: 47% more likely → chase unions now
    - Moderates breaking Brown (24%) then Miguel (9%) — alliance holds
    - McDuffie gets 25% among Miguel voters vs 6% among Raj voters
    - DSA endorsement net negative among men (-28% vs +30%)
    - DSA net negative among moderates (-27% vs +20%)
    """)

st.info("""
**The over-65 problem is the most actionable finding.**
Miguel needs a targeted push in Petworth and Park View precincts (35, 36, 37, 38) 
specifically aimed at older long-term residents — the demographic going to Brown 
rather than him. Those voters are already in the alliance; the ask is to rank Miguel #1, Brown #2.
""")

st.divider()
st.subheader("🚔 Public Safety Positions — Where the Candidates Stand")
st.caption("Key differentiator for the Miguel/McDuffie dual-ticket voter")

safety_data = pd.DataFrame({
    "Candidate": ["Miguel Trindade Deramo", "Rashida Brown", "Aparna Raj"],
    "Public Safety Framing": [
        "Crime is real AND federal overreach is real — ward needs both addressed",
        "Community investment + safe streets — pragmatic progressive",
        "Police are the safety threat — invest in social resources instead",
    ],
    "Police Stance": [
        "✅ Pro community policing, anti-federal overreach",
        "✅ Pro community safety, investment-focused",
        "⚠️ Police/MPD framed as threat alongside ICE/DHS",
    ],
    "Teen Curfew Alignment": [
        "✅ Aligned with McDuffie (72% of voters support)",
        "🟡 Not clearly stated",
        "❌ DSA/abolitionist-adjacent — likely opposed",
    ],
    "McDuffie Crossover": [
        "🔴 High — same pragmatic safety frame",
        "🟡 Medium — safe streets language but softer",
        "🔵 None — Lewis George coalition",
    ],
})

st.dataframe(
    safety_data,
    use_container_width=True,
    hide_index=True,
)

st.markdown("""
**The canvassing angle:** On any door where public safety comes up, 
Miguel's position is a clear contrast to Raj — and a natural bridge to McDuffie. 
*"Miguel believes crime in Ward 1 is real and needs real solutions — not ideology. 
That's why he and Kenyan McDuffie are the ticket for Ward 1 residents who want results."*
""")

st.divider()
st.subheader("🚔 Public Safety — Verbatim Candidate Positions")
st.caption("Sourced directly from candidate websites, May 2026")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Miguel Trindade Deramo")
    st.markdown("*miguelward1.com/priorities/safety*")
    st.info("""
**"You deserve to feel safe in DC, whether you're biking to work in the morning or walking home late at night."**

**"Public safety is foundational and indispensable to healthy communities and thriving economies."**

"As a Councilmember, Miguel will support proven tools to combat violence in our neighborhoods and bolster upstream interventions to prevent violence in the first place."

"He will also work to **reestablish trust between the community and MPD** after the federal intervention — and **refocus MPD on community-oriented policing.**"

Platform sections:
- Public Safety Is Built on Mutual Trust
- Violence Interruption Saves Lives
- We Are Not Safe Unless All of Us Are Safe
""")

with col2:
    st.markdown("#### Rashida Brown")
    st.markdown("*rashidaforward1.com*")
    st.warning("""
**"Miguel and I are committed to ensuring we are lowering costs for residents. We both have the same shared progressive values, whether that's affordable housing or making sure our streets are safe."**

*(Source: WUSA9, April 2026)*

Brown's safety framing is community investment-focused — social work background, ANC experience. Aligned with Miguel on safe streets language. Less specific on MPD than either Raj or Miguel.
""")

with col3:
    st.markdown("#### Aparna Raj")
    st.markdown("*aparnafordc.com/platform*")
    st.error("""
**"Everyone deserves to feel safe in DC. To do that, we need to do better than responding to crime, violence, and disorder after it's already happened. We need to prevent violence and crime in the first place."**

**On MPD:** "End MPD's Collaboration With ICE" is a top platform priority. Frames MPD as part of the problem.

**On police:** Supports expanding alternative responders, routing calls AWAY from police. "People dealing with an acute crisis should be seen by a professional that can support them in that moment, **not a police officer.**"

**On federal forces:** Equates ICE, DHS, National Guard, and MPD together as safety threats.
""")

st.markdown("""
**The contrast in one sentence:**
- **Miguel:** *"Public safety is foundational and indispensable"* — MPD is a partner to be reformed
- **Raj:** *"Not a police officer"* — MPD is a threat to be replaced

This is the clearest policy divide in the race, and it maps directly onto the McDuffie/Lewis George split citywide.
""")

st.divider()
st.title("⚔️ Battle Plan — Deramo Path to Victory")
st.caption("Theory of the case: Win the voters Raj isn't fighting for")

st.markdown("""
### The Argument
Raj has a ceiling. Her base is young, transplant, very liberal — and she's already at 33% of very liberal voters 
with almost no room among moderates (1%). **54% of Ward 1 Dems are undecided.** 
The voters who will decide this race are:
- Parents worried about schools and crime
- Residents in high-crime precincts who feel abandoned  
- Small business owners and patrons watching corridors hollow out
- LGBTQ+ voters who want one of their own on the Council
- Voters in precincts that underperformed under Nadeau who are ready for something new

**Deramo's job:** Show up where Raj isn't. Turn out voters she's written off.
""")

st.divider()

# ── UNIVERSE 1: HIGH CRIME / PUBLIC SAFETY ─────────────────
st.subheader("🔴 Universe 1 — High Crime / Public Safety Voters")
st.caption("Target: Residents who feel unsafe and want a candidate who takes crime seriously")

crime_precincts = pd.DataFrame({
    "Precinct": [40, 41, 43, 39, 22],
    "Neighborhood": ["U Street", "Adams Morgan", "U Street", "Columbia Heights", "Columbia Heights"],
    "Why Target": [
        "High foot traffic corridor, business crime, late-night incidents",
        "Bar district, assault/robbery concentration, longtime residents fed up",
        "U St nightlife corridor, visible disorder complaints",
        "14th St corridor, property crime, auto theft",
        "High density, mixed income, crime a top ANC complaint",
    ],
    "Registered_Dems": [3322, 3337, 1751, 3911, 4038],
    "2024_Turnout_pct": [30.5, 23.2, 23.3, 26.5, 26.6],
    "Deramo_Message": [
        "Public safety is foundational — Miguel will reestablish trust with MPD",
        "Miguel supported violence interruption funding as ANC chair",
        "Raj says 'not a police officer' — Miguel says crime is real",
        "Miguel: 'safe streets are indispensable to a thriving economy'",
        "14th St businesses closing — Miguel ties crime to economic health",
    ],
    "Raj_Vulnerability": [
        "Her platform: replace police with social workers",
        "Her platform: 'not a police officer' for crisis response",
        "MPD = ICE in her framing",
        "No acknowledgment that crime affects small business",
        "Zero business development platform",
    ],
})

st.dataframe(crime_precincts, use_container_width=True, hide_index=True)

# ── UNIVERSE 2: BUSINESS / CORRIDOR DECAY ──────────────────
st.divider()
st.subheader("🏪 Universe 2 — Business Corridor Decay Voters")
st.caption("Target: Residents who've watched neighborhood businesses close and want economic investment")

business_precincts = pd.DataFrame({
    "Precinct": [40, 43, 41, 39, 22],
    "Neighborhood": ["U Street", "U Street", "Adams Morgan", "Columbia Heights", "Columbia Heights"],
    "Corridor": ["U Street NW", "U Street NW", "18th Street NW", "14th Street NW", "14th Street NW"],
    "Business_Vulnerability": [
        "U St nightlife corridor losing anchor tenants post-pandemic",
        "Late-night corridor, closures accelerating since federal occupation",
        "18th St seeing turnover, longtime bars and restaurants closing",
        "14th St mid-range dining and retail hollowing out",
        "Columbia Heights Plaza area, chain replacement of local business",
    ],
    "Deramo_Quote": [
        "'I am watching long-time businesses close... the corner restaurant where you don't break the bank'",
        "Same — explicitly names late-night food options as Ward 1 lifeblood",
        "Hosted campaign event AT a local bar (Grand Duchess) — shows up",
        "Ties business closure directly to federal occupation economic impact",
        "Calls for YES to local businesses as Councilmember",
    ],
    "Raj_Gap": [
        "No small business platform section",
        "No mention of U Street corridor health",
        "Economic platform = unions and wages only",
        "No 14th St or commercial corridor policy",
        "Zero local business record",
    ],
    "Brown_Note": [
        "Brown has Georgia Ave Thrive record — acknowledge, pivot to RCV ask",
        "Brown's record is Georgia Ave, not U St — Deramo owns this corridor",
        "Neither Brown nor Raj have 18th St record",
        "Brown's Georgia Ave work is adjacent — gives alliance credibility",
        "Brown + Deramo together cover both corridors",
    ],
})

st.dataframe(business_precincts, use_container_width=True, hide_index=True)

# ── UNIVERSE 3: PARENTS / K-12 SCHOOL VOTERS ───────────────
st.divider()
st.subheader("🏫 Universe 3 — Parents with Children in DC Schools")
st.caption("""
Target: Households with school-age children. Key insight: these voters care about 
crime near schools, school quality, AND fiscal responsibility to fund schools — 
not teachers union politics. COVID school closures kept kids out too long; 
parents in these precincts feel it directly in learning loss and street safety.
""")

school_precincts = pd.DataFrame({
    "Precinct": [35, 36, 37, 38, 23],
    "Neighborhood": ["Petworth", "Petworth", "Park View", "Park View", "Mount Pleasant"],
    "Nearby_School": [
        "Brightwood EC, MacFarland MS",
        "Petworth ES, MacFarland MS",
        "Park View ES, Columbia Heights EC",
        "Park View ES, Columbia Heights EC",
        "Mount Pleasant Library zone, Bancroft ES",
    ],
    "Why_This_Matters": [
        "Older, longer-tenure residents — more likely to have kids in DCPS",
        "Highest owner-occupancy in Ward 1 — invested in school quality long-term",
        "Park View parents active on school safety along Georgia Ave",
        "Park View — families directly affected by school-adjacent crime",
        "Mount Pleasant has high family density, bilingual school community",
    ],
    "Deramo_Message": [
        "Schools need safe streets AND tax base — both require pro-business, pro-safety leadership",
        "COVID closures hurt kids; we need leaders who won't bow to union pressure over parent needs",
        "Miguel: education is foundational, his mother was a schoolteacher",
        "Crime near schools is a parent issue — public safety IS a school issue",
        "Bilingual community — Deramo speaks Portuguese, values immigrant education",
    ],
    "Raj_Vulnerability": [
        "Teachers union-aligned platform, no critique of school closure decisions",
        "DSA-backed; teachers unions backed COVID closures longest",
        "No specific K-12 record or parent-facing safety platform",
        "Safety platform explicitly avoids police response — parents feel this",
        "No school-adjacent crime policy",
    ],
    "Median_Age": [45, 46, 44, 43, 35],
    "Owner_pct": [44, 47, 42, 43, 28],
})

st.dataframe(school_precincts, use_container_width=True, hide_index=True)

# ── UNIVERSE 4: LGBTQ+ MAX TURNOUT ─────────────────────────
st.divider()
st.subheader("🏳️‍🌈 Universe 4 — LGBTQ+ Max Turnout (Deramo's Natural Base)")
st.caption("""
Deramo would be only the 2nd out LGBTQ+ person on DC Council and the first Latino. 
This is a max-turnout universe — these voters may already be Deramo-leaning but 
need activation. Key: many are also progressive on housing, transit, immigration — 
so the message here is identity + competence, not just identity.
""")

lgbtq_precincts = pd.DataFrame({
    "Precinct": [40, 43, 41, 42, 39],
    "Neighborhood": ["U Street", "U Street", "Adams Morgan", "Adams Morgan", "Columbia Heights"],
    "LGBTQ_Context": [
        "Historic Black LGBTQ+ corridor, Shaw/U St anchors",
        "U Street nightlife, queer bars and venues concentrated here",
        "Adams Morgan — diverse LGBTQ+ community, long-established",
        "Adams Morgan — younger queer renters, high transplant population",
        "Columbia Heights — growing LGBTQ+ residential presence",
    ],
    "Deramo_Message": [
        "First Latino on DC Council, second LGBTQ+ — historic representation AND substance",
        "Miguel hosted campaign events in neighborhood venues — he shows up here",
        "Deramo's safety platform explicitly includes 'safety from discrimination'",
        "Rank Miguel 1st — a vote for visibility AND competence",
        "Miguel ties LGBTQ+ safety to broader community safety — not siloed",
    ],
    "Note": [
        "Don't neglect Raj — she is also queer. Message here is RECORD not just identity",
        "Raj is queer but has no Ward 1 record; Miguel has 5 years of ANC work",
        "Brown is straight — Deramo has clear identity advantage here",
        "Younger transplants may lean Raj; focus activation on 30-45 established residents",
        "Cross-reference with low-turnout — activation opportunity",
    ],
    "2024_Turnout_pct": [30.5, 23.3, 23.2, 27.3, 26.5],
    "Untapped_Voters": [2310, 1343, 2563, 1246, 2873],
})

st.dataframe(lgbtq_precincts, use_container_width=True, hide_index=True)

# ── UNIVERSE 5: NADEAU UNDERPERFORMANCE / ANTI-ENDORSEMENT ─
st.divider()
st.subheader("📉 Universe 5 — Nadeau Underperformance Precincts")
st.caption("""
Nadeau endorsed Brown. But the poll shows 23% of Ward 1 voters are LESS likely to 
vote for a Nadeau-endorsed candidate. Find the precincts where Nadeau's 
record was weakest — constituent services complaints, blight, unresolved issues — 
and those voters are ripe to reject her endorsee and give Deramo a shot.
""")

nadeau_precincts = pd.DataFrame({
    "Precinct": [22, 39, 40, 25, 20],
    "Neighborhood": ["Columbia Heights", "Columbia Heights", "U Street", "Columbia Heights", "Columbia Heights"],
    "Nadeau_Weakness": [
        "14th St corridor business closures happened on her watch — 12 years, limited action",
        "Columbia Heights Plaza blight — longstanding constituent frustration",
        "U Street safety complaints went unaddressed for years under Nadeau",
        "Housing affordability worsened dramatically during her tenure",
        "Small precinct — low turnout but high symbolic value in anti-establishment framing",
    ],
    "Deramo_Angle": [
        "I've been your ANC commissioner actually fixing things block by block",
        "Miguel passed resolutions; Nadeau made promises — contrast the records",
        "ANC Home Rule Caucus was Miguel's work, not council's",
        "Miguel opposes same bad developers Nadeau enabled — credible contrast",
        "Fresh start message — 44 years of same leadership, time for change",
    ],
    "Poll_Data": [
        "23% of W1 voters less likely to vote for Nadeau-endorsed candidate",
        "Nadeau endorsement net negative among men (-26% vs +12%)",
        "Nadeau less likely among moderates (29% less likely vs 10% more likely)",
        "Among 46-65 voters: 29% less likely with Nadeau endorsement",
        "Anti-establishment voters: Brown's biggest liability is Nadeau's blessing",
    ],
    "Overlap_With_Other_Universes": [
        "✅ Crime + Business + School",
        "✅ Crime + Business",
        "✅ Crime + Business + LGBTQ+",
        "✅ School + Business",
        "🟡 Low turnout — activation only",
    ],
})

st.dataframe(nadeau_precincts, use_container_width=True, hide_index=True)

# ── PRIORITY MATRIX ─────────────────────────────────────────
st.divider()
st.subheader("🎯 Priority Matrix — Where to Put Every Hour")

matrix = pd.DataFrame({
    "Precinct": [40, 41, 39, 35, 36, 37, 38, 43, 22, 23, 42, 25, 20, 24, 137],
    "Neighborhood": [
        "U Street", "Adams Morgan", "Columbia Heights", "Petworth", "Petworth",
        "Park View", "Park View", "U Street", "Columbia Heights", "Mount Pleasant",
        "Adams Morgan", "Columbia Heights", "Columbia Heights", "Mount Pleasant", "Columbia Heights"
    ],
    "Crime": ["🔴","🔴","🔴","🟡","🟡","🟡","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡"],
    "Business": ["🔴","🔴","🔴","🟡","🟡","🟡","🟡","🔴","🔴","🟡","🔴","🟡","🟡","🟡","🟡"],
    "Schools": ["🟡","🟡","🟡","🔴","🔴","🔴","🔴","🟡","🟡","🔴","🟡","🟡","🟡","🟡","🟡"],
    "LGBTQ+": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🔴","🟡","🟡","🔴","🟡","🟡","🟡","🟡"],
    "Anti_Nadeau": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🟡","🔴","🔴","🟡","🟡"],
    "Untapped_Voters": [2310, 2563, 2873, 2458, 3080, 2698, 2085, 1343, 2964, 2355, 1246, 2804, 671, 1920, 890],
    "Overall_Priority": [
        "🚨 Tier 1", "🚨 Tier 1", "🚨 Tier 1",
        "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2",
        "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2",
        "🔵 Tier 3", "🔵 Tier 3", "🔵 Tier 3", "🔵 Tier 3", "🔵 Tier 3"
    ],
})

st.dataframe(
    matrix,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Untapped_Voters": st.column_config.ProgressColumn(
            "Untapped Voters", min_value=0, max_value=3500, format="%d"
        ),
    }
)

st.markdown("""
**Tier 1 — Precincts 40, 41, 39:** Hit all 5 universes. Every door knocked here is 
worth 3x a door in Tier 3. Crime + business + LGBTQ+ + anti-Nadeau all align.

**Tier 2 — Precincts 35, 36, 37, 38, 43, 22, 23:** Strong on 2-3 universes. 
Petworth/Park View is the schools + McDuffie dual-ticket play. 
U St 43 and Columbia Heights 22 are crime + business.

**Tier 3:** Activation only — these voters may come without heavy canvassing if 
Tier 1/2 momentum builds.
""")

st.divider()
st.title("🧬 Identity Matrix — Who Deramo Can Win")
st.caption("Cross-referenced against PPP/GGWash poll crosstabs, March 2026, n=232")

st.markdown("""
**The Identity Theory of the Case:**
Deramo is a gay Hispanic candidate running against a Black woman (Brown) and an Indian DSA candidate (Raj). 
The standard progressive coalition fractures along identity lines in ways that create 
non-obvious opportunities — and real vulnerabilities — that a smart ground game can exploit.
""")

tab1, tab2 = st.tabs(["📊 Identity Crosstabs", "🗺️ Targeting Implications"])

with tab1:
    st.markdown("#### First-Choice Vote Share by Demographic Group (PPP Poll)")
    st.caption("Source: GGWash/PPP Ward 1 poll, March 27-29 2026. Decided voters only.")

    identity_matrix = pd.DataFrame({
        "Demographic Group": [
            # Race
            "White voters",
            "Black / African-American voters",
            "Hispanic / Latino voters",
            "Other race voters",
            # Age
            "18-45 years old",
            "46-65 years old",
            "65+ years old",
            # Gender
            "Women",
            "Men",
            "Non-binary",
            # Ideology
            "Very liberal",
            "Somewhat liberal",
            "Moderate",
            "Conservative",
            # Education
            "No college degree",
            "4-year college degree",
            "Post-graduate degree",
            "White moderate voters (est.)",
            "White conservative voters",
        ],
        "Deramo %": [7, 1, 20, 11, 9, 11, 0, 6, 9, 0, 8, 5, 9, 0, 6, 4, 10, 15, 0],
        "Brown %": [9, 15, 20, 23, 10, 10, 21, 17, 7, 22, 8, 8, 24, 38, 33, 5, 9, 20, 38],
        "Raj %": [26, 2, 9, 20, 29, 13, 6, 17, 19, 51, 33, 10, 1, 5, 0, 22, 26, 8, 5],
        "Share_of_Ward1_Dems": [59, 23, 8, 10, 45, 30, 25, 56, 42, 2, 46, 27, 22, 4, 24, 35, 35, 18, 8],        "Deramo_Opportunity": [
            "🟡 Medium — Raj leads but 26% vs 7% gap closeable",
            "🔴 Hard — Brown dominates, 1% is near zero",
            "🔴 High — tied with Brown at 20%, Raj only 9%",
            "🟡 Medium — tied with Raj at 20%",
            "🔴 Hard — Raj dominates 18-45",
            "✅ Soft target — competitive, Brown/Deramo both at ~10%",
            "⚠️ Problem — Brown 21%, Deramo 0%",
            "🔴 Hard — women break Brown/Raj",
            "✅ Advantage — men break Deramo over Brown",
            "⚠️ Problem — Raj dominates non-binary",
            "🔴 Hard — Raj at 33%, Deramo at 8%",
            "🟡 Medium — Raj 10%, Deramo 5%, room to grow",
            "✅ Key target — Deramo 9%, Raj only 1%",
            "✅ Sleeper — Brown leads but Deramo competitive",
            "✅ Underrated — Brown 33%, Deramo 6% but Raj at 0%",
            "🔴 Hard — Raj and grad-degree voters aligned",
            "🟡 Medium — post-grad split across all three",
            "✅ Key target — Raj near zero, Deramo competitive",
            "⚠️ Brown dominates but Raj irrelevant — RCV transfer opportunity",
        ],
    })

    identity_matrix["Deramo_Lead_vs_Raj"] = identity_matrix["Deramo %"] - identity_matrix["Raj %"]

    st.dataframe(
        identity_matrix,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Deramo %": st.column_config.ProgressColumn(
                "Deramo %", min_value=0, max_value=40, format="%d%%"
            ),
            "Brown %": st.column_config.ProgressColumn(
                "Brown %", min_value=0, max_value=40, format="%d%%"
            ),
            "Raj %": st.column_config.ProgressColumn(
                "Raj %", min_value=0, max_value=40, format="%d%%"
            ),
            "Share_of_Ward1_Dems": st.column_config.NumberColumn(
                "% of Electorate", format="%d%%"
            ),
            "Deramo_Lead_vs_Raj": st.column_config.NumberColumn(
                "Deramo vs Raj", format="%+d pts"
            ),
        }
    )

with tab2:
    st.markdown("#### Targeting Implications by Identity Group")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
### ✅ Deramo's Strongest Groups — Press Hard

**Hispanic/Latino voters (8% of electorate)**
- Deramo 20%, Brown 20%, Raj 9%
- Deramo is the only Latino in the race — first Latino on DC Council if elected
- Ward 1 has large Salvadoran, Mexican, Central American communities
- Columbia Heights, Mt Pleasant, Park View precincts
- Message: representation + record + public safety for immigrant communities
- McDuffie dual-ticket: Black voters → 30% McDuffie, strongest non-white group for him

**Men (42% of electorate)**
- Deramo 9%, Brown 7%, Raj 19%
- Wait — Raj leads men?? Yes, but Brown trails badly
- Deramo + Brown combined = 16% among men vs Raj 19%
- Male moderate voters are the target: Deramo 9% among moderates
- DSA endorsement: men are 28% less likely vs 30% more likely — net neutral, not a boost

**Moderates (22% of electorate)**
- Deramo 9%, Brown 24%, Raj 1%
- Raj is essentially nonexistent among moderates
- The Brown/Deramo alliance owns this lane entirely
- These are the RCV transfer voters — Brown #1, Deramo #2 (or vice versa)
- McDuffie connection: moderates → McDuffie 32%, Lewis George only 16%

**Whites 46+ (subset of 59% white electorate)**
- This is your underrated sleeper group
- Poll shows 65+ → Brown 21%, Deramo 0%, Raj 6%
- But 46-65 → Deramo 11%, Brown 10%, Raj 13% — genuinely competitive
- These are the Petworth/Park View homeowners: long-tenure, native-adjacent, safety-focused
- They're not voting Raj. Question is Brown vs Deramo.
- Message: schools, safety, business — NOT progressive ideology signaling

**No college degree voters (24% of electorate)**
- Brown 33%, Deramo 6%, Raj 0%
- Raj has ZERO support here — her base is entirely college-educated
- Deramo at 6% is low but the ceiling is high — Raj can't compete
- These are working-class Ward 1 residents who want results, not ideology
- Georgia Ave, lower Columbia Heights, Park View working families
        """)

    with col2:
        st.error("""
### 🔴 Deramo's Problem Groups — Manage, Don't Chase

**Black voters (23% of electorate)**
- Deramo 1%, Brown 15%, Raj 2%
- Brown dominates — this is her base
- Don't chase it: Deramo's ceiling here is probably 5-8% even with perfect execution
- Strategy: don't lose these voters to Raj (she's at 2% — not a threat)
- RCV angle: Black voters who rank Brown #1 should rank Deramo #2, not Raj
- McDuffie connection: Black voters → McDuffie 30%, strongest racial group for him citywide

**Young voters 18-45 (45% of electorate)**
- Raj 29%, Brown 10%, Deramo 9%
- Raj's strongest age group by far
- College-educated under 45 = DSA base, Raj's floor
- Don't ignore but be selective: young moderates, young Hispanics, young LGBTQ+ men
- These exist in 18-45 cohort and are reachable

**Women (56% of electorate)**
- Women break Brown 17%, Raj 17%, Deramo 6%
- Majority of the electorate and Deramo's worst group
- But: moderate women (not very liberal women) are reachable
- Non-binary voters → Raj 51%, Deramo 0% — essentially concede this group
- Focus on women 45+, women with children in schools, women who own businesses

**Post-graduate degree (35% of electorate)**
- Raj 26%, Brown 9%, Deramo 10%
- Raj's educational stronghold
- Grad-degree very liberal women in Adams Morgan/U Street = Raj's core
- These voters are not persuadable — focus elsewhere
        """)

    st.divider()
    st.subheader("🎯 The Whites 46+ Deep Dive — Your Underrated Angle")
    st.markdown("""
You flagged this correctly. Here's why it's real:

The poll shows whites are 59% of the Ward 1 likely primary electorate. 
Among ALL whites, Raj leads at 26% vs Brown 9% vs Deramo 7%.
But that aggregate obscures a massive age split:

- **White 18-45:** Raj's core — very liberal, transplant, grad-degree, bike commuter. Largely locked.
- **White 46-65:** The crosstabs show this group going moderate/McDuffie on mayor (52% McDuffie). 
  On the council race they're competitive. These are:
  - Long-term Columbia Heights homeowners
  - Petworth residents who bought before 2010
  - U Street residents who remember what the neighborhood was
  - Parents with kids in DCPS who lived through the COVID closures
  - Small business owners and longtime patrons watching places close

**They care about:** Crime → Schools → Business health → NOT DSA ideology

**Raj's brand among this group:** A DSA candidate who thinks MPD = ICE and 
whose voters kept schools closed longest. Net negative.

**Brown's brand:** Endorsed by Nadeau (23% less likely for this group), 
social worker, housing-focused. Softer.

**Deramo's lane:** Former State Dept / DHS, ANC chairman who actually fixed things, 
explicitly pro-public safety, explicitly anti-business-closure. 
Gay man — this group is socially liberal but wants competent pragmatism.
    """)

    white_over_45_precincts = pd.DataFrame({
        "Precinct": [35, 36, 37, 38, 23, 24],
        "Neighborhood": ["Petworth", "Petworth", "Park View", "Park View", "Mt Pleasant", "Mt Pleasant"],
        "White_Over45_Concentration": ["High", "High", "High", "High", "Medium", "Medium"],
        "Median_Age": [45, 46, 44, 43, 35, 34],
        "Median_Tenure_yrs": [11.5, 12.2, 10.8, 11.1, 5.2, 4.8],
        "Owner_pct": [44, 47, 42, 43, 28, 26],
        "Nadeau_Endorsement_Risk": [
            "High — longtime residents most likely to hold Nadeau record against Brown",
            "High — 12+ year residents, saw what Nadeau did/didn't do",
            "Medium-High — active community, engaged on crime and schools",
            "Medium-High — Park View active ANC base",
            "Medium — more renters, shorter tenure",
            "Medium — mixed tenure",
        ],
        "Deramo_Message": [
            "Schools + safety + 'I showed up as your ANC neighbor'",
            "Business corridor + homeowner investment protection",
            "Georgia Ave crime + school safety + record of showing up",
            "Park View ES parents — COVID learning loss + crime near schools",
            "Mt Pleasant bilingual families — Deramo speaks Portuguese",
            "Mt Pleasant families — same as above",
        ],
        "Priority": ["🚨 Tier 1", "🚨 Tier 1", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2", "🔵 Tier 3"],
    })

    st.dataframe(white_over_45_precincts, use_container_width=True, hide_index=True)

    st.info("""
**The Whites 46+ Canvassing Script:**
Don't lead with identity. Lead with record and issues.

*"Hi, I'm volunteering for Miguel Trindade Deramo for Ward 1 Council. 
He's been your ANC commissioner — you may know him. 
He's the one who fought to keep violence interruption programs funded and pushed back 
on federal overreach while also saying clearly: public safety is foundational, not optional. 
With ranked choice, we're asking you to put Miguel first. 
If you're thinking about the mayor's race — Kenyan McDuffie shares those same values."*

Do NOT mention that Miguel is gay unless the voter brings it up or signals receptivity.
This group responds to competence and record, not identity signaling.
    """)

    st.divider()
st.subheader("🧬 Identity Universe Battle Plan")
st.caption("Five identity-based targeting universes — same structure as issue universes")

identity_universe_1 = pd.DataFrame({
    "Precinct": [23, 24, 20, 25, 35],
    "Neighborhood": ["Mt Pleasant", "Mt Pleasant", "Columbia Heights", "Columbia Heights", "Petworth"],
    "Universe": ["Hispanic/Latino Max Turnout"] * 5,
    "Why": [
        "Mt Pleasant has largest Salvadoran/Central American concentration in Ward 1",
        "Mt Pleasant — high Hispanic family density, longtime residents",
        "Columbia Heights — large Latino population, community anchors",
        "Columbia Heights — Hispanic renters and homeowners mixed",
        "Petworth — growing Latino presence, longer-tenure families",
    ],
    "Deramo_Edge": [
        "Only Latino in race — first Latino on DC Council if elected",
        "Speaks Portuguese — cultural proximity to Spanish speakers",
        "Tied with Brown at 20% among Hispanics — Raj only 9%",
        "McDuffie gets 6% among Hispanic W1 voters — dual ticket harder here",
        "Older Hispanic homeowners — schools + safety message resonates",
    ],
    "RCV_Ask": [
        "Deramo #1, Brown #2 — keep Raj out",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
    ],
    "Untapped_Voters": [2355, 1920, 671, 2804, 2458],
    "Priority": ["🚨 Tier 1", "🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2"],
})

identity_universe_2 = pd.DataFrame({
    "Precinct": [40, 43, 41, 42, 39],
    "Neighborhood": ["U Street", "U Street", "Adams Morgan", "Adams Morgan", "Columbia Heights"],
    "Universe": ["LGBTQ+ Activation"] * 5,
    "Why": [
        "Historic Black LGBTQ+ corridor — Shaw/U St anchor venues",
        "U Street queer nightlife concentration — Deramo hosts events here",
        "Adams Morgan — established LGBTQ+ residential + nightlife",
        "Adams Morgan — younger queer renters, high density",
        "Columbia Heights — growing LGBTQ+ residential presence",
    ],
    "Deramo_Edge": [
        "2nd out LGBTQ+ person on DC Council, first Latino — historic",
        "Record vs Raj: 5 years ANC vs Raj's zero elected record",
        "Safety from discrimination explicitly in Miguel's platform",
        "Note: Raj also queer — message here must be RECORD not just identity",
        "Cross-universe: LGBTQ+ + crime + business all align here",
    ],
    "RCV_Ask": [
        "Deramo #1, Brown #2 — don't rank Raj",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
    ],
    "Untapped_Voters": [2310, 1343, 2563, 1246, 2873],
    "Priority": ["🚨 Tier 1", "🚨 Tier 1", "🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2"],
})

identity_universe_3 = pd.DataFrame({
    "Precinct": [35, 36, 37, 38, 23],
    "Neighborhood": ["Petworth", "Petworth", "Park View", "Park View", "Mt Pleasant"],
    "Universe": ["White 46+ Sleeper Vote"] * 5,
    "Why": [
        "Highest median age in Ward 1 (45) — white long-tenure homeowners",
        "Highest owner-occupancy (47%) — invested, pragmatic, anti-ideology",
        "Park View — white 46+ residents active on crime and school quality",
        "Park View — same profile, school-parent overlap",
        "Mt Pleasant — older white homeowners, bilingual community",
    ],
    "Deramo_Edge": [
        "46-65 voters: Deramo 11%, Brown 10% — genuinely competitive",
        "Owner-occupants respond to business/safety record not union politics",
        "McDuffie leads 46-65 on mayor (20% vs 35% LG) — dual ticket works",
        "65+ problem (Deramo 0%) but 46-65 is the real target here",
        "Tenure 5+ years — long enough to care, short enough to not be locked in",
    ],
    "RCV_Ask": [
        "Deramo #1, Brown #2 — no mention of Raj",
        "Deramo #1, Brown #2 — lead with record and safety",
        "Deramo #1, Brown #2 — lead with schools and crime",
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2",
    ],
    "Untapped_Voters": [2458, 3080, 2698, 2085, 2355],
    "Priority": ["🚨 Tier 1", "🚨 Tier 1", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
})

identity_universe_4 = pd.DataFrame({
    "Precinct": [35, 36, 37, 38, 22],
    "Neighborhood": ["Petworth", "Petworth", "Park View", "Park View", "Columbia Heights"],
    "Universe": ["Moderate + Conservative Dem"] * 5,
    "Why": [
        "Petworth — older residents, moderate Dems, longest tenure in ward",
        "Petworth — homeowners, pragmatic, not ideological",
        "Park View — working class moderate Dems, crime top concern",
        "Park View — same, Brown's ANC base but Deramo can compete",
        "Columbia Heights — moderate Dems frustrated with progressive performance",
    ],
    "Deramo_Edge": [
        "Moderates: Deramo 9%, Raj 1% — Raj is irrelevant here",
        "Conservative Dems: Brown 38%, Deramo 0% — this is Brown's lane, not Deramo's",
        "Key insight: moderates vote Brown OR Deramo, not Raj — alliance confirmed",
        "DSA endorsement: moderates 27% less likely — weaponizable against Raj",
        "Nadeau endorsed Brown — 23% of moderates less likely with Nadeau endorsement",
    ],
    "RCV_Ask": [
        "Deramo #1, Brown #2 — or Brown #1, Deramo #2 — either works",
        "Same — stress RCV math, not candidate preference",
        "If they're Brown: Brown #1, Deramo #2, leave Raj unranked",
        "If they're Deramo: Deramo #1, Brown #2, leave Raj unranked",
        "The ask is the same regardless of which they prefer first",
    ],
    "Untapped_Voters": [2458, 3080, 2698, 2085, 2964],
    "Priority": ["🚨 Tier 1", "🚨 Tier 1", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
})

identity_universe_5 = pd.DataFrame({
    "Precinct": [22, 39, 25, 37, 23],
    "Neighborhood": ["Columbia Heights", "Columbia Heights", "Columbia Heights", "Park View", "Mt Pleasant"],
    "Universe": ["Non-Black Minority + Working Class"] * 5,
    "Why": [
        "Columbia Heights — Asian, multiracial, mixed-income non-black voters",
        "Columbia Heights — Other race voters: Deramo 11%, Raj 20% — competitive",
        "Columbia Heights — working class renters, no college degree voters",
        "Park View — African immigrant community, not aligned with Black Dem establishment",
        "Mt Pleasant — Central American community overlaps with school/crime concerns",
    ],
    "Deramo_Edge": [
        "Other race: Deramo 11%, Brown 23%, Raj 20% — three-way split, Deramo competitive",
        "No college degree: Brown 33%, Deramo 6%, Raj 0% — Raj has zero ceiling",
        "Working class: crime + business message lands harder than DSA ideology",
        "African immigrants often socially conservative — Raj's platform alienates",
        "Bilingual outreach — Deramo's Portuguese + Spanish-adjacent campaigning",
    ],
    "RCV_Ask": [
        "Deramo #1, Brown #2",
        "Deramo #1, Brown #2 — working class voters respond to record",
        "Deramo #1, Brown #2 — lead with business and safety, not identity",
        "Deramo #1, Brown #2 — safety message resonates with African immigrant community",
        "Deramo #1, Brown #2 — bilingual outreach, representation argument",
    ],
    "Untapped_Voters": [2964, 2873, 2804, 2698, 2355],
    "Priority": ["🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
})

# Display all five
for i, (universe_df, title, color) in enumerate([
    (identity_universe_1, "🌎 Identity Universe 1 — Hispanic/Latino Max Turnout", "🚨"),
    (identity_universe_2, "🏳️‍🌈 Identity Universe 2 — LGBTQ+ Activation", "🚨"),
    (identity_universe_3, "👴 Identity Universe 3 — White 46+ Sleeper Vote", "🚨"),
    (identity_universe_4, "🗳️ Identity Universe 4 — Moderate + Conservative Dem", "⭐"),
    (identity_universe_5, "🤝 Identity Universe 5 — Non-Black Minority + Working Class", "🟡"),
]):
    st.markdown(f"#### {title}")
    st.dataframe(
        universe_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Untapped_Voters": st.column_config.ProgressColumn(
                "Untapped", min_value=0, max_value=3500, format="%d"
            ),
        }
    )
    st.divider()

# Combined priority matrix
st.subheader("🎯 Combined Issue + Identity Priority Matrix")
st.caption("Every precinct scored across all 10 universes — 5 issue + 5 identity")

combined = pd.DataFrame({
    "Precinct": [40, 41, 39, 35, 36, 23, 37, 38, 43, 22, 42, 25, 24, 20, 137],
    "Neighborhood": [
        "U Street", "Adams Morgan", "Columbia Heights", "Petworth", "Petworth",
        "Mt Pleasant", "Park View", "Park View", "U Street", "Columbia Heights",
        "Adams Morgan", "Columbia Heights", "Mt Pleasant", "Columbia Heights", "Columbia Heights"
    ],
    # Issue universes
    "Crime": ["🔴","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡"],
    "Business": ["🔴","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🔴","🔴","🟡","🟡","🟡","🟡"],
    "Schools": ["🟡","🟡","🟡","🔴","🔴","🔴","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🟡"],
    "LGBTQ+_Issue": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🔴","🟡","🟡","🟡","🟡"],
    "Anti_Nadeau": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🔴","🟡","🔴","🟡"],
    # Identity universes
    "Hispanic": ["🟡","🟡","🔴","🟡","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🔴","🔴","🟡"],
    "LGBTQ+_Id": ["🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡","🔴","🟡","🔴","🟡","🟡","🟡","🟡"],
    "White_46+": ["🟡","🟡","🟡","🔴","🔴","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🟡"],
    "Moderate": ["🔴","🟡","🔴","🔴","🔴","🟡","🔴","🔴","🟡","🔴","🟡","🟡","🟡","🟡","🟡"],
    "Non_Left_White": ["🟡","🟡","🟡","🔴","🔴","🟡","🔴","🔴","🟡","🟡","🟡","🟡","🟡","🟡","🟡"],
    "Non_Black_Minority": ["🟡","🟡","🔴","🟡","🟡","🔴","🔴","🟡","🟡","🔴","🟡","🔴","🔴","🔴","🟡"],
    "Untapped": [2310, 2563, 2873, 2458, 3080, 2355, 2698, 2085, 1343, 2964, 1246, 2804, 1920, 671, 890],
    "Final_Priority": [
        "🥇 #1", "🥇 #2", "🥇 #3",
        "🥈 #4", "🥈 #5", "🥈 #6",
        "🥈 #7", "🥈 #8",
        "🥉 #9", "🥉 #10",
        "🥉 #11", "🥉 #12", "🥉 #13", "🥉 #14", "🥉 #15"
    ],
})

st.dataframe(
    combined,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Untapped": st.column_config.ProgressColumn(
            "Untapped Voters", min_value=0, max_value=3500, format="%d"
        ),
    }
)

st.success("""
**The Final Battle Plan in One Paragraph:**

Precinct 40 (U Street) is Deramo's #1 target — hits crime, business, LGBTQ+ on both 
issue and identity dimensions, and anti-Nadeau sentiment. 
Precincts 41 and 39 (Adams Morgan and Columbia Heights) round out the Tier 1 trifecta.
The White 46+ play in Petworth (35, 36) is the sleeper — massive untapped universe 
(3,080 and 2,458 respectively) where Raj is essentially nonexistent and Brown's 
Nadeau endorsement is a liability. 
Mt Pleasant (23) is the Hispanic/bilingual activation play.
**Every door in these 8 precincts knocked before June 16 is worth more than 
two doors anywhere else in the ward.**
""")

st.warning("""
⚠️ **Data Gap:** The PPP poll does not publish first-choice → second-choice 
transfer rates. We don't know Brown voters' top 2nd choice with certainty. 
Moderate 2nd choice data suggests Lynch is pulling transfers that should go 
to Deramo. This makes the Brown/Deramo RCV education play even more urgent — 
without active coordination, Brown voters may default to Lynch or exhaust 
rather than Deramo.
""")

st.divider()
st.subheader("♻️ RCV Simulation — The Actual Round-by-Round Data")
st.caption("Source: GGWash/PPP RCV simulation, April 2026. Among decided voters only.")

rcv_rounds = pd.DataFrame({
    "Round": [
        "Round 1 — All decided voters",
        "Round 2 — After Lynch eliminated",
        "Round 3 — After Reyes Yanes eliminated (projected)",
        "Round 4 — Final: Brown vs Raj (projected)",
    ],
    "Raj %": [42, 43, 45, 51],
    "Brown %": [25, 26, 29, 49],
    "Deramo %": [16, 17, 20, 0],
    "Reyes_Yanes %": [9, 10, 0, 0],
    "Lynch %": [8, 0, 0, 0],
    "Exhausted %": [0, 4, 6, 0],
    "Notes": [
        "Raj leads by 17pts among decided voters — but 54% still undecided",
        "Most Lynch voters exhaust — ballots don't transfer. Wasted votes.",
        "Projected: Reyes Yanes transfers mostly to Brown and Deramo",
        "If Deramo eliminated in R3: Brown needs almost all Deramo transfers to beat Raj",
    ],
})

st.dataframe(rcv_rounds, use_container_width=True, hide_index=True,
    column_config={
        "Raj %": st.column_config.NumberColumn(format="%d%%"),
        "Brown %": st.column_config.NumberColumn(format="%d%%"),
        "Deramo %": st.column_config.NumberColumn(format="%d%%"),
        "Reyes_Yanes %": st.column_config.NumberColumn("Reyes Yanes %", format="%d%%"),
        "Lynch %": st.column_config.NumberColumn(format="%d%%"),
        "Exhausted %": st.column_config.NumberColumn(format="%d%%"),
    }
)

st.error("""
**The Lynch Problem — 8% of votes likely exhausting**
Most Lynch voters didn't rank a second choice per the GGWash simulation. 
That's votes that could transfer to Brown or Deramo but won't.
Lynch voters in Petworth and Park View (his stronger precincts) 
should be a canvassing target for RCV education: 
*"Whoever you vote for first, please rank Trinidade Deramo second — 
next best option for the issues your care about."*
""")

st.success("""
**The Path to Victory — What Needs to Happen**
1. Deramo survives to Round 3 (needs to stay above Reyes Yanes in R1/R2)
2. Reyes Yanes transfers break toward Brown/Deramo alliance  
3. Brown voters follow the cross-endorsement and rank Deramo #2
4. Deramo transfers in R3/R4 go almost entirely to Brown (not Raj)
5. Brown + Deramo combined overtake Raj in final round

**The single most important number:** 
How many of Deramo's ~16% transfer to Brown vs exhaust vs go to Raj.
If Deramo voters rank Brown #2 cleanly, Brown wins. 
If they exhaust, Raj wins. The canvassing ask is that simple.
""")

st.markdown("#### 🔄 Bonus Universe — Lynch Voter RCV Conversion")
st.caption("8% of first-choice votes likely exhausting. These voters are ideologically Deramo's people.")

lynch_universe = pd.DataFrame({
    "Precinct": [23, 24, 35, 37, 40],
    "Neighborhood": ["Mt Pleasant", "Mt Pleasant", "Petworth", "Park View", "U Street"],
    "Why_Lynch_Voters_Here": [
        "Lynch is a Mt Pleasant resident — his base is here",
        "Mt Pleasant adjacent — crime-frustrated moderate voters",
        "Petworth — anti-Nadeau, pro-jobs, crime concerned older residents",
        "Park View — crime near Georgia Ave is Lynch's core issue",
        "U Street — business closures and crime frustration, Lynch's RFK jobs argument",
    ],
    "Lynch_Voter_Profile": [
        "Crime-frustrated, anti-Nadeau, pro-RFK stadium/jobs — not DSA",
        "Same profile — moderate to conservative Dem, wants results",
        "Long-tenure resident fed up with status quo — Nadeau fatigue",
        "Watches carjackings and robberies, wants someone who names it",
        "Business owner adjacent — pro-economic development, anti-ideology",
    ],
    "Why_They_Exhaust": [
        "Lynch voters didn't rank 2nd choice per GGWash simulation",
        "Low political engagement — didn't understand RCV mechanics",
        "Older voters less likely to rank multiple candidates",
        "Single-issue crime voters who stopped at #1",
        "Anti-establishment voters who don't trust other candidates",
    ],
    "Deramo_Conversion_Message": [
        "'Lynch and Miguel agree on crime and jobs — rank Miguel 2nd so your vote counts'",
        "'Don't let your ballot exhaust — Lynch #1, Deramo #2 keeps Raj out'",
        "'Lynch is anti-Nadeau, so is Miguel — rank both, block Brown's Nadeau machine'",
        "'Lynch and Miguel both want safe streets — rank Miguel 2nd'",
        "'Lynch wanted the RFK jobs — Miguel wants Ward 1 businesses to survive'",
    ],
    "RCV_Ask": [
        "Lynch #1, Deramo #2, Brown #3 — leave Raj unranked",
        "Lynch #1, Deramo #2 — stop there",
        "Lynch #1, Deramo #2 — anti-Nadeau frame",
        "Lynch #1, Deramo #2 — crime frame",
        "Lynch #1, Deramo #2 — jobs/business frame",
    ],
    "Untapped_Voters": [2355, 1920, 2458, 2698, 2310],
    "Priority": ["🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2", "🚨 Tier 1"],
})

st.dataframe(
    lynch_universe,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Untapped_Voters": st.column_config.ProgressColumn(
            "Untapped", min_value=0, max_value=3500, format="%d"
        ),
    }
)

st.warning("""
**Why this universe matters more than it looks:**

Lynch gets 3% first choice among ALL voters but 8% among DECIDED voters. 
His voters are disproportionately:
- Men (poll: Lynch gets 2% among women, 4% among men)  
- Older (46-65: Lynch gets 5% vs 1% among 18-45)
- Moderate (5% among moderates vs 3% among very liberal)
- No college degree (0% among Lynch — wait, that's actually zero in the crosstabs)

**The RCV math is simple:** 
Lynch has ~8% of decided votes. 
If most exhaust (as the GGWash simulation shows), that's roughly 
**500-700 actual votes** on primary day that go nowhere.
In a race this tight, 500 votes is the entire margin.
A targeted RCV education push among Lynch supporters in Mt Pleasant 
and U Street — just explaining that ranking a 2nd choice doesn't hurt their #1 — 
could be the difference between Deramo surviving to round 3 or not.

**This is the lowest-cost, highest-leverage canvassing play in the race.**
Lynch voters are already predisposed to Deramo's issues. 
They just need to be told: rank Lynch first if you want, 
but please put Miguel second so your vote doesn't die.
""")

st.markdown("#### 🤝 Bonus Universe — Reyes Yanes Voter 2nd Choice Courtship")
st.caption("Don't compete for her first choice votes — court her voters as Deramo's 2nd choice transfer pool")

reyes_yanes_universe = pd.DataFrame({
    "Precinct": [23, 24, 20, 25, 37],
    "Neighborhood": ["Mt Pleasant", "Mt Pleasant", "Columbia Heights", "Columbia Heights", "Park View"],
    "Why_Reyes_Yanes_Strong_Here": [
        "Her home turf — arrived in DC 1990 via Mt Pleasant, deep community roots",
        "Mt Pleasant adjacent — Salvadoran and Central American community anchor",
        "Columbia Heights — Latino community overlap, former Latino Affairs director",
        "Columbia Heights — Latino families she served at Mayor's Office on Latino Affairs",
        "Park View — Latino residents along Georgia Ave, business community ties",
    ],
    "Why_NOT_To_Compete_For_1st": [
        "She owns this precinct — competing directly alienates the Latino community",
        "Her 30+ year Mt Pleasant roots are unbeatable on first choice here",
        "She has government service record with these families — Deramo doesn't",
        "She connected these residents to COVID vaccines and eviction relief",
        "Her business grant platform resonates strongly here — don't outbid her",
    ],
    "Why_Her_Voters_Transfer_To_Deramo": [
        "Both Latino — when she's eliminated, Deramo is the natural home",
        "Pro-business, pro-safety — identical to Deramo's platform",
        "Neither is DSA — Raj is not a transfer destination for Reyes Yanes voters",
        "Bowser-moderate profile — closer to Deramo/McDuffie than Raj/Lewis George",
        "Her voters already understand RCV — she ran bilingual RCV workshops",
    ],
    "Deramo_Courtship_Message": [
        "'Jackie has served this community for 30 years — and Miguel shares her values on business and safety. Rank Jackie first if you want, Miguel second.'",
        "'Two Latino candidates, same Ward 1 values. Rank them 1-2 in either order — keep Raj out.'",
        "'Jackie built the Latino Affairs office. Miguel will carry that work forward on the Council.'",
        "'Jackie's $5k-$50k business grant idea and Miguel's corridor investment plan point the same direction.'",
        "'Jackie and Miguel agree: 38 violent crimes in 30 days is unacceptable. Rank them both.'",
    ],
    "RCV_Ask": [
        "Reyes Yanes #1, Deramo #2 — or Deramo #1, Reyes Yanes #2",
        "Either order — just leave Raj unranked",
        "Reyes Yanes #1, Deramo #2, Brown #3",
        "Reyes Yanes #1, Deramo #2 — stop there",
        "Reyes Yanes #1, Deramo #2 — crime + business frame",
    ],
    "Transfer_Value": [
        "🔴 Critical — Mt Pleasant is her strongest precinct, most transfers here",
        "🔴 Critical — same community profile",
        "🟡 Medium — Latino overlap but Brown also strong here",
        "🟡 Medium — mixed community, some go to Brown",
        "🟡 Medium — Park View splits more toward Brown",
    ],
    "Untapped_Voters": [2355, 1920, 671, 2804, 2698],
    "Priority": ["🚨 Tier 1", "🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2"],
})

st.dataframe(
    reyes_yanes_universe,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Untapped_Voters": st.column_config.ProgressColumn(
            "Untapped", min_value=0, max_value=3500, format="%d"
        ),
    }
)

st.divider()
st.subheader("🎯 The Minor Candidate Transfer Strategy")
st.markdown("""
Lynch and Reyes Yanes combined have roughly **12% of first-choice decided votes** 
— about 400-600 actual votes on primary day. Neither can win. 
The question is entirely where their votes go when they're eliminated.

**The ideal transfer scenario for Deramo:**
""")

transfer_scenario = pd.DataFrame({
    "Candidate Eliminated": ["Lynch (Round 2)", "Reyes Yanes (Round 2-3)"],
    "Total_Est_Votes": ["~250-300", "~150-200"],
    "If_Goes_To_Deramo": [
        "Deramo survives Round 2, stays above Reyes Yanes",
        "Deramo gets a boost into Round 3, closes gap on Brown/Raj",
    ],
    "If_Goes_To_Brown": [
        "Brown strengthens but Deramo may still survive",
        "Brown pulls further ahead — Deramo at risk of elimination before final",
    ],
    "If_Goes_To_Raj": [
        "🚨 Raj extends lead — hardest path for Brown/Deramo alliance",
        "🚨 Raj potentially locks up majority early",
    ],
    "If_Exhausts": [
        "🚨 400-600 wasted votes — happened with most Lynch voters per GGWash sim",
        "Smaller risk — Reyes Yanes ran bilingual RCV education, her voters more likely to rank",
    ],
    "Deramo_Goal": [
        "Lynch #1, Deramo #2 — canvass RCV education in Mt Pleasant and U Street",
        "Reyes Yanes #1, Deramo #2 — court don't compete in Mt Pleasant",
    ],
})

st.dataframe(transfer_scenario, use_container_width=True, hide_index=True)

st.warning("""
**The Low-Key Play:**

Neither Lynch nor Reyes Yanes voters should ever hear Deramo's campaign 
criticize or compete against their candidate. The ask is entirely framed as:

*"We respect [Lynch/Jackie] and what they stand for. 
With ranked choice, you can show that support AND make sure 
your vote counts in every round. Rank [Lynch/Jackie] first — 
and please consider ranking Miguel second. 
That way if your first choice doesn't make it to the final round, 
your vote still matters."*

**What we're really doing:** Quietly making sure those 400-600 votes 
go to Deramo in rounds 2-3 rather than Brown or — worst case — Raj.
Brown will be doing the same thing. Whoever wins this transfer battle 
likely wins the seat.

**The numbers that matter:**
- Lynch ~300 votes, most exhausting per GGWash → flip 150 to Deramo = game changer
- Reyes Yanes ~200 votes, more RCV-educated → flip 100-150 to Deramo = surviving Round 3
- Combined: 250-300 transferred Deramo votes could be the entire margin of victory
""")

st.info("""
**The Reyes Yanes Strategic Note:**

She gets 4% first choice in the March poll — roughly 200-300 actual votes on primary day. 
Almost none of them will rank Raj. The question is whether they rank Deramo or Brown second.

Deramo's job is to make that choice feel obvious:
- Publicly praise her public service record and Latino Affairs work
- Never compete against her in Mt Pleasant — let her win those doors
- Frame the race as "two Latinos running on the same values" not as competition
- In precincts where she's strong, the canvassing ask is simply: 
  *"Whoever you rank first, please rank Miguel second"*

**The formal cross-endorsement ask** is also worth a conversation — 
she hasn't aligned with anyone, and a Reyes Yanes + Deramo mutual 2nd choice ask 
would be the second historic RCV cross-endorsement in this race.
""")

st.info("""
🤝 REYES YANES — COURT, DON'T COMPETE

Jackie Reyes Yanes voters are Deramo's single best 2nd-choice transfer pool 
after Brown. Here's why:

**Her voter profile:**
- Pro-business, pro-public safety, pro-Latino representation
- Bowser administration moderate — not DSA-aligned
- Mt Pleasant and Latino community roots
- Her 4% first choice = roughly 200-300 actual votes on primary day
- Almost none of them will rank Raj — their values don't align

**The math:** If Reyes Yanes is eliminated in Round 2,
her ~200-300 votes need somewhere to go.
If Deramo has built goodwill with her voters,
those transfers could be the margin that keeps him alive into Round 3.

**The play — three options, in order of preference:**

1. **Formal cross-endorsement** — unlikely given she's also Latino and competing 
   for the same historic first, but worth a conversation

2. **Informal goodwill** — Deramo publicly praises her public service record,
   her Latino Affairs work, her business platform.
   Her voters see two Latinos running on similar values.
   When she's eliminated, ranking Deramo 2nd feels natural.

3. **Shared canvassing message** — In precincts where Reyes Yanes is strong 
   (Mt Pleasant 23, 24), Deramo canvassers don't compete for #1.
   They simply say: *"Whoever you rank first, please consider ranking 
   Miguel second — he shares Jackie's values on business and public safety."*

**What NOT to do:**
- Don't canvass against her in Mt Pleasant — she owns that turf
- Don't highlight the Latino competition angle — it looks zero-sum
- Don't ignore her voters — they're 200-300 transfers waiting to happen
""")


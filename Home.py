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

st.title("🗳️ DC Ward 1 Campaign Intel")
st.caption("Targeting model and insights pitched to Miguel Trindade Deramo for the 2026 Primary | By Thomas Emerick")



st.markdown("""
**The Argument:** Aparna Raj has a solidified base but limited ceiling, while Miguel Trindade Deramo is uniquely positioned to gain late and pull ahead of the field in RCV. 
""")

# access gate first
access_code = st.text_input("🔒 Enter access code to view full intelligence:", type="password", key="main_access")
unlocked = access_code == "miguel20xxjune"

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "♻️ Minor Candidate Transfers",
    "🔴 Issue Universes",
    "🧬 Identity Universes",
    "🎯 Targeting Model",
    "🗺️ Precinct Heatmap"
])

# ══════════════════════════════════════════════════════════
# TAB 1 — MINOR CANDIDATE TRANSFER STRATEGY
# ══════════════════════════════════════════════════════════

with tab1:
    st.subheader("♻️ Lynch & Reyes Yanes — The Transfer Game")
    st.caption("RCV Simulation by GGWash/PPP Ward 1 poll March 27-29 2026, n=232 likely Dem primary voters")

    st.markdown("""
    **From the PPP poll — projected to full Ward 1 Dem primary electorate (projecting ~9,000 ballots):**
    - **Lynch:** 8% → ~720 actual votes
    - **Reyes Yanes:** 9% → ~810 actual votes
    - **Combined:** ~1,530 votes eliminated in rounds 1-2 — roughly **17% of all ballots cast**
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
        "Notes": [
            "Raj leads by 17pts among decided, but 54% still undecided",
            "Most Lynch voters exhaust, wasted votes per GGWash simulation",
            "Projected: Reyes Yanes transfers mostly to Brown and Trindade Deramo",
            "If Trindade Deramo eliminated in R3: Brown needs almost all Trindade Deramo transfers to beat Raj",
        ],
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
    st.markdown("""
    **What Trindade Deramo stands to gain:**
    - If 75% of Lynch's ~720 votes transfer to Trindade Deramo → **+540 votes**
    - If 75% of Reyes Yanes' ~810 votes transfer to Trindade Deramo → **+608 votes**
    - Combined upside: **~1,148 votes** to get in range with Brown in penultimate round
    - Current gap to close: Trindade Deramo at 7% vs Brown at 13% among all likely voters
    - 1,148 transferred votes in a ~9,000 vote primary = **~5% swing** along with persuasion gains among undecideds
    - Second choice on Brown's ballots then propels Trindade Deramo past Raj in final round
    """)

    st.info("""
    **🗳️ Historical Precedent: The Kathryn Garcia Playbook (NYC 2021)**

    In the June 2021 NYC Democratic mayoral primary, Kathryn Garcia trailed Eric Adams by ~100,000 first-choice votes. She won the somewhat liberal lane while Maya Wiley locked up the hard left and Adams owned moderate/conservative Democrats. But Garcia's ideological compatability on key issues with other candidates made her the consensus second and third choice across ideological lines. Wiley voters ranked her #2 at high rates, and moderate voters who couldn't stomach Adams found Garcia acceptable. This Ward 1 race would be the inverse in terms of political spectrum for the Adams/Wiley dynamic, but does map to the polling position three weeks out of that NYC race with Adams -> Raj, Wiley -> Brown, and Garcia -> Trindade Deramo. 
            
    After all RCV rounds, Garcia lost by fewer than 8,000 votes. However, there are two additional minor candidates each polling close to 10% among decided voters in the recent PPP poll. Garcia leapfrogged Wiley to reach the final round by outperforming her on transfer votes from Andrew Yang ballots, but could have defeated Adams by doing a little better than at parity when it came to transfers from Scott Stringer or a couple other lower-finishing candidates. For Trindade Deramo, making inroads with minor candidates' voters as their second choice could produce an even bigger additional boost for a late-surging candidate here in the 2026 DC Ward 1 primary than it did in the 2021 NYC mayoral primary.

    **In short:** Raj consolidates the very liberal base. Brown is strong with conservatives. The moderate and somewhat liberal lanes are genuinely contested and Trindade Deramo's best persuasion targets, and the most likely to be undecided. If Trindade Deramo can own that lane on first choice while harvesting RCV transfers from Lynch, Reyes Yanes, and Brown voters, the math closes fast in a ~9,000 ballot electorate.
    """)

    st.divider()



    # Lynch Transfer Universe
    st.subheader("🔄 Lynch Voter RCV Conversion")
    st.caption("8% of decided votes likely exhausting. These voters are ideologically amenable enough to rank Trindade Deramo No.2.")

    lynch_universe = pd.DataFrame({
        "Precinct": [23, 24, 35, 37, 40],
        "Neighborhood": ["Columbia Heights", "Adams Morgan", "Adams Morgan", "Pleasant Plains", "Mount Pleasant"],
        "Lynch_Voter_Profile": [
            "Lynch is a Mt Pleasant resident — crime-frustrated, anti-Nadeau, pro-jobs",
            "Mt Pleasant adjacent — moderate to conservative Dem, wants results",
            "Long-tenure resident fed up with status quo, Nadeau fatigue",
            "Watches carjackings and robberies, wants someone who names it",
            "Business owner adjacent who's pro-economic development, anti-ideology",
        ],
        "Why_They_Exhaust": [
            "Low political engagement, didn't understand RCV mechanics",
            "Older voters less likely to rank multiple candidates",
            "Anti-establishment voters who stopped at #1",
            "Single-issue crime voters who didn't rank further",
            "Anti-establishment voters who don't trust other candidates",
        ],
        "Deramo_Pitch_As_2nd": [
            "'Lynch and Miguel agree on crime and jobs, rank Miguel 2nd so your vote counts'",
            "'Don't let your ballot exhaust — Lynch #1, Trindade Deramo #2 keeps Raj out'",
            "'Lynch is anti-Nadeau, so is Miguel — rank both, block the Nadeau machine'",
            "'Lynch and Miguel both want safe streets, rank Miguel 2nd'",
            "'Lynch and Miguel both want a thriving Park View, rank Miguel 2nd'",
        ],
        "RCV_Ask": [
            "Lynch #1, Deramo #2, Brown #3",
            "Lynch #1, Deramo #2",
            "Lynch #1, Deramo #2 — anti-Nadeau frame",
            "Lynch #1, Deramo #2 — crime frame",
            "Lynch #1, Deramo #2 — jobs/business frame",
        ],
        "Untapped_Voters": [2355, 1920, 2458, 2698, 2310],
        "Priority": ["🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2", "🚨 Tier 1"],
    })

    st.dataframe(lynch_universe, use_container_width=True, hide_index=True,
        column_config={
            "Untapped_Voters": st.column_config.ProgressColumn(
                "Untapped", min_value=0, max_value=3500, format="%d"
            ),
        }
    )

    st.error("""
    **Lynch ballots in poll, most votes exhausting:**
    Lynch voters didn't rank a second choice per the GGWash simulation.
    ~720 votes going nowhere. In a race this tight, those votes can make the difference.
    A targeted RCV education push among Lynch supporters in Mt Pleasant and U Street
    and just explaining that ranking a 2nd choice doesn't hurt their #1
    could be the difference between Trindade Deramo surviving Round 2 or not.
    **This is a low-cost, highest-leverage canvassing play in the race.**
    """)

    st.divider()

    # Reyes Yanes Transfer Universe
    st.subheader("🤝 Reyes Yanes Voter 2nd Choice Courtship")
    st.caption("Court don't compete — her voters are Trindade Deramo's best transfer pool after Brown")

    reyes_yanes_universe = pd.DataFrame({
        "Precinct": [23, 24, 20, 25, 37],
        "Neighborhood": ["Columbia Heights", "Adams Morgan", "LeDroit Park", "Adams Morgan", "Pleasant Plains"],
        "Why_Reyes_Yanes_Strong_Here": [
            "Her home turf — arrived in DC 1990 via Mt Pleasant, deep community roots",
            "Mt Pleasant adjacent — Salvadoran and Central American community anchor",
            "Columbia Heights — Latino community, former Latino Affairs director",
            "Columbia Heights — Latino families she served at Mayor's Office",
            "Park View — Latino residents along Georgia Ave, business community ties",
        ],
        "Why_NOT_To_Compete_For_1st": [
            "She owns this precinct, competing directly alienates the Latino community",
            "Her 30+ year Mt Pleasant roots are unbeatable on first choice here",
            "She has government service record with these families",
            "She connected these residents to COVID vaccines and eviction relief",
            "Her business grant platform resonates strongly, don't outbid her",
        ],
        "Why_Her_Voters_Transfer_To_Deramo": [
            "Both Latino — when she's eliminated, Trindade Deramo is the natural home",
            "Pro-business, pro-safety — identical to Trindade Deramo's platform",
            "Neither is DSA, Raj is not a transfer destination for Reyes Yanes voters",
            "Bowser-moderate — closer to Trindade Deramo/McDuffie than Raj/Lewis George",
            "Her voters already understand RCV, she ran bilingual RCV workshops",
        ],
        "Deramo_Pitch_As_2nd": [
            "'Jackie has served this community 30 years and Miguel shares her values. Rank Jackie first, Miguel second.'",
            "'Two Latino candidates, same Ward 1 values. Rank them 1-2 in either order.'",
            "'Jackie built the Latino Affairs office. Miguel will carry that work forward.'",
            "'Jackie's business grant idea and Miguel's corridor plan point the same direction.'",
            "'Jackie and Miguel agree: 38 violent crimes in 30 days is unacceptable.'",
        ],
        "RCV_Ask": [
            "Reyes Yanes #1, Trindade Deramo #2 — or Trindade Deramo #1, Reyes Yanes #2",
            "Either order, just leave Raj unranked",
            "Reyes Yanes #1, Trindade Deramo #2, Brown #3",
            "Reyes Yanes #1, Trindade Deramo #2",
            "Reyes Yanes #1, Trindade Deramo #2 — crime + business frame",
        ],
        "Transfer_Value": [
            "🔴 Critical", "🔴 Critical", "🟡 Medium", "🟡 Medium", "🟡 Medium"
        ],
        "Untapped_Voters": [2355, 1920, 671, 2804, 2698],
        "Priority": ["🚨 Tier 1", "🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2"],
    })

    st.dataframe(reyes_yanes_universe, use_container_width=True, hide_index=True,
        column_config={
            "Untapped_Voters": st.column_config.ProgressColumn(
                "Untapped", min_value=0, max_value=3500, format="%d"
            ),
        }
    )

    st.info("""
    **The Low-Key Play for both Lynch and Reyes Yanes voters:**

    Never criticize or compete against their candidate. The ask is entirely:

    *"We respect [Lynch/Jackie] and what they stand for. With ranked choice, you can
    show that support AND make sure your vote counts in every round.
    Rank [Lynch/Jackie] first — and please consider ranking Miguel second.
    That way if your first choice doesn't make it to the final round,
    your vote still matters."*

    **What we're really doing:** Quietly making sure those votes go to Trindade Deramo
    in early rounds rather than Brown or (worst case) Raj.
    Brown may be doing the same thing.
    Whoever wins this transfer battle could win the seat.
    """)


# ══════════════════════════════════════════════════════════
# TAB 2 — ISSUE UNIVERSES
# ══════════════════════════════════════════════════════════
with tab2:
    if not unlocked:
        st.info("### 🔒 Access After Meeting\nEnter the access code to view targeting intelligence.\n\n**Contact Thomas Emerick to request access.**")
    else:
        st.subheader("🔴 Issue-Based Targeting — Trindade Deramo's Argument to Edge the Field")
        st.markdown("""
        **Theory of the case on issues:**
        Raj has no meaningful public safety platform, no business development record,
        and no specific K-12 policy beyond teachers union alignment.
        Brown has a strong record but is tied to Nadeau's legacy.
        Trindade Deramo's edge: he is the only candidate who explicitly names crime as foundational,
        who has watched businesses close and made it a priority,
        and whose mother was a schoolteacher — giving him authentic K-12 credibility
        with parents.

        
        """)

        st.markdown("""**The three issues where Raj is most vulnerable:**
        - 🚔 **Crime:** "Not a police officer" — her own words
        - 🏪 **Business:** Zero commercial corridor platform
        - 🏫 **Schools:** Teachers union-aligned, COVID closure politics
                
        """)
        st.divider()

        # Universe 1: Crime
        st.subheader("🔴 Universe 1 — High Crime / Public Safety Voters")
        st.caption("Target: Residents who feel unsafe and want a candidate who takes crime seriously")

        crime_precincts = pd.DataFrame({
            "Precinct": [40, 41, 43, 39, 22],
            "Neighborhood": ["Mount Pleasant", "Columbia Heights", "Park View", "Mount Pleasant", "U Street"],
            "Why_Target": [
                "High foot traffic corridor, business crime, late-night incidents",
                "Bar district, assault/robbery concentration, longtime residents fed up",
                "U St nightlife corridor, visible disorder complaints",
                "14th St corridor, property crime, auto theft",
                "High density, mixed income, crime a top ANC complaint",
            ],
            "Registered_Dems": [3322, 3337, 1751, 3911, 4038],
            "Turnout_2024_pct": [30.5, 23.2, 23.3, 26.5, 26.6],
            "Deramo_Message": [
                "'Public safety is foundational' — Miguel will reestablish trust with MPD",
                "Miguel supported violence interruption funding as ANC chair",
                "Raj doesn't really differentiate MPD from ICE — Miguel listens to residents on crime concerns",
                "Miguel: 'safe streets are indispensable to a thriving economy'",
                "14th St businesses closing — Miguel ties crime as part of equation on school and economic health",
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

        st.divider()

        # Universe 2: Business
        st.subheader("🏪 Universe 2 — Business Corridor Decay Voters")
        st.caption("Target: Residents who've watched neighborhood businesses close")

        business_precincts = pd.DataFrame({
            "Precinct": [40, 43, 41, 39, 22],
            "Neighborhood": ["Mount Pleasant", "Park View", "Columbia Heights", "Mount Pleasant", "U Street"],
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
        })

        st.dataframe(business_precincts, use_container_width=True, hide_index=True)

        st.divider()

        # Universe 3: Schools
        st.subheader("🏫 Universe 3 — Parents with Children in DC Schools")
        st.caption("Target: Households with school-age children. Crime + fiscal responsibility to have revenue for investing in public schools.")

        school_precincts = pd.DataFrame({
            "Precinct": [35, 36, 37, 38, 23],
            "Neighborhood": ["Adams Morgan", "Columbia Heights", "Pleasant Plains", "Park View", "Columbia Heights"],
            "Nearby_School": [
                "Brightwood EC, MacFarland MS",
                "Adams Morgan ES, MacFarland MS",
                "Columbia Heights ES, MacFarland MS",
                "Pleasant Plains, Park View ES area",
                "Park View ES, Georgia Ave corridor",
            ],
            "Deramo_Message": [
                "Schools need safe streets AND tax base — both require pro-business, pro-safety leadership",
                "COVID closures hurt kids, need leaders who won't bow to union pressure over parent needs",
                "Miguel: education is foundational, his mother was a schoolteacher",
                "Crime near schools is a parent issue, public safety IS a school issue",
                "Bilingual community — Trindade Deramo speaks Portuguese, values immigrant education",
            ],
            "Raj_Vulnerability": [
                "Teachers union-aligned, no critique of school closure decisions",
                "DSA-backed; teachers unions are her base, not parents (see Brandon Johnson in Chicago)",
                "No specific K-12 record or parent-facing safety platform",
                "Safety platform explicitly avoids police response, parents feel this",
                "No school-adjacent crime policy",
            ],
            "Median_Age": [45, 46, 44, 43, 35],
            "Owner_pct": [44, 47, 42, 43, 28],
        })

        st.dataframe(school_precincts, use_container_width=True, hide_index=True)

        st.divider()

        # Universe 4: LGBTQ+ Issue
        st.subheader("🏳️‍🌈 Universe 4 — LGBTQ+ Voters (Issue + Safety Frame)")
        st.caption("Miguel explicitly includes 'safety from discrimination' in his platform")

        lgbtq_precincts = pd.DataFrame({
            "Precinct": [40, 43, 41, 42, 39],
            "Neighborhood": ["Mount Pleasant", "Park View", "Columbia Heights", "Columbia Heights", "Mount Pleasant"],
            "LGBTQ_Context": [
                "Historic Black LGBTQ+ corridor, Shaw/U St anchors",
                "U Street nightlife, queer bars and venues concentrated here",
                "Adams Morgan — diverse LGBTQ+ community, long-established",
                "Adams Morgan — younger queer renters, high transplant population",
                "Columbia Heights — growing LGBTQ+ residential presence",
            ],
            "Deramo_Message": [
                "First Latino on DC Council, second LGBTQ+ — historic AND substantive",
                "Miguel hosted campaign events in neighborhood venues, shows up here",
                "Safety platform explicitly includes 'safety from discrimination'",
                "Record vs Raj: 5 years ANC work vs Raj's zero elected record",
                "Miguel ties LGBTQ+ safety to broader community safety",
            ],
            "2024_Turnout_pct": [30.5, 23.3, 23.2, 27.3, 26.5],
            "Untapped_Voters": [2310, 1343, 2563, 1246, 2873],
        })

        st.dataframe(lgbtq_precincts, use_container_width=True, hide_index=True,
            column_config={
                "Untapped_Voters": st.column_config.ProgressColumn(
                    "Untapped", min_value=0, max_value=3500, format="%d"
                ),
            }
        )

        st.divider()

        # Universe 5: Anti-Nadeau
        st.subheader("📉 Universe 5 — Nadeau Underperformance Precincts")
        st.caption("23% of Ward 1 voters less likely to vote for Nadeau-endorsed candidates, the DSA skeptics among them could open their mind to Trindade Deramo")

        nadeau_precincts = pd.DataFrame({
            "Precinct": [22, 39, 40, 25, 20],
            "Neighborhood": ["U Street", "Mount Pleasant", "Mount Pleasant", "Adams Morgan", "LeDroit Park"],
            "Nadeau_Weakness": [
                "14th St corridor business closures happened on her watch — 12 years, limited action",
                "Columbia Heights Plaza blight, longstanding constituent frustration",
                "U Street safety complaints went unaddressed for years under Nadeau",
                "Housing affordability worsened dramatically during her tenure",
                "Small precinct, high symbolic value in anti-establishment framing",
            ],
            "Deramo_Angle": [
                "I've been your ANC commissioner actually fixing things block by block",
                "Miguel passed resolutions; Nadeau made promises — contrast the records",
                "ANC Home Rule Caucus was Miguel's work, not the council's",
                "Miguel opposes same bad developers Nadeau enabled",
                "Fresh start: 44 years of same leadership, time for change",
            ],
            "Poll_Data": [
                "23% of W1 voters less likely to vote Nadeau-endorsed",
                "Nadeau endorsement net negative among men (-26% vs +12%)",
                "Nadeau less likely among moderates (29% vs 10%)",
                "Among 46-65: 29% less likely with Nadeau endorsement",
                "Anti-establishment voters: Brown's biggest liability is Nadeau's blessing",
            ],
        })

        st.dataframe(nadeau_precincts, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
# TAB 3 — IDENTITY UNIVERSES
# ══════════════════════════════════════════════════════════
with tab3:
    if not unlocked:
        st.info("### 🔒 Access After Meeting\nEnter the access code to view targeting intelligence.\n\n**Contact Thomas Emerick to request access.**")
    else:
        st.subheader("🧬 Identity-Based Targeting — Trindade Deramo's Edge")
        st.markdown("""
        **Theory of the case on identity:**
        Trindade Deramo is a gay Latino candidate in a field with a Black woman (Brown),
        an Indian DSA candidate (Raj), a Salvadoran woman (Reyes Yanes), and a white
        self-identified civic gadfly (Lynch). The standard progressive coalition fractures along identity
        lines in ways that create non-obvious opportunities.

        **Deramo's identity advantages:**
        - Only gay man in the race → LGBTQ+ community, gay male voters specifically
        - Only candidate with Brazilian/Latino heritage still in serious contention → Latino & Hispanic voters
        - Former State Dept / DHS background → moderate and conservative Dems who want competence
        - ANC chairman with 5-year record → white 46+ homeowners who want results not ideology

        **Trindade Deramo's identity vulnerabilities:**
        - Black voters (23% of electorate) → Brown dominates at 15%, Trindade Deramo at 1%
        - College-educated under 45 women → Raj's core, largely locked
        """)

        st.divider()

        # Identity crosstabs
        st.markdown("#### First-Choice Vote Share by Demographic Group")
        st.caption("Source: GGWash/PPP Ward 1 poll March 27-29 2026. Decided voters only.")

        identity_matrix = pd.DataFrame({
            "Demographic Group": [
                "White voters",
                "Black / African-American voters",
                "Hispanic / Latino voters",
                "Other race voters",
                "18-45 years old",
                "46-65 years old",
                "65+ years old",
                "Women",
                "Men",
                "Non-binary",
                "Very liberal",
                "Somewhat liberal",
                "Moderate",
                "Conservative",
                "No college degree",
                "4-year college degree",
                "Post-graduate degree",
                "White moderate voters (est.)",
                "White conservative voters",
            ],
            "Deramo %": [7, 1, 20, 11, 9, 11, 0, 6, 9, 0, 8, 5, 9, 0, 6, 4, 10, 15, 0],
            "Brown %": [9, 15, 20, 23, 10, 10, 21, 17, 7, 22, 8, 8, 24, 38, 33, 5, 9, 20, 38],
            "Raj %": [26, 2, 9, 20, 29, 13, 6, 17, 19, 51, 33, 10, 1, 5, 0, 22, 26, 8, 5],
            "Share_of_Ward1_Dems": [59, 23, 8, 10, 45, 30, 25, 56, 42, 2, 46, 27, 22, 4, 24, 35, 35, 18, 8],
            "Deramo_Opportunity": [
                "🟡 Medium — gap closeable",
                "🔴 Hard — Brown dominates",
                "✅ High — tied with Brown at 20%, Raj only 9%",
                "🟡 Medium — tied with Raj at 20%",
                "🔴 Hard — Raj dominates",
                "✅ Soft target — competitive",
                "⚠️ Problem — Brown 21%, Deramo 0%",
                "🔴 Hard — women break Brown/Raj",
                "✅ Advantage — men break Deramo",
                "⚠️ Problem — Raj dominates",
                "🔴 Hard — Raj at 33%",
                "🟡 Medium — room to grow",
                "✅ Key target — Raj only 1%",
                "✅ Sleeper — Brown leads but Raj irrelevant",
                "✅ Underrated — Raj at 0%",
                "🔴 Hard — Raj and grad-degree voters aligned",
                "🟡 Medium — three-way split",
                "✅ Key target — Raj near zero",
                "⚠️ Brown dominates — RCV transfer play only",
            ],
        })

        identity_matrix["Deramo_vs_Raj"] = identity_matrix["Deramo %"] - identity_matrix["Raj %"]

        st.dataframe(
            identity_matrix,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Deramo %": st.column_config.ProgressColumn("Deramo %", min_value=0, max_value=40, format="%d%%"),
                "Brown %": st.column_config.ProgressColumn("Brown %", min_value=0, max_value=40, format="%d%%"),
                "Raj %": st.column_config.ProgressColumn("Raj %", min_value=0, max_value=40, format="%d%%"),
                "Share_of_Ward1_Dems": st.column_config.NumberColumn("% of Electorate", format="%d%%"),
                "Deramo_vs_Raj": st.column_config.NumberColumn("vs Raj", format="%+d pts"),
            }
        )

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            **✅ Press Hard — Deramo's Strongest Groups**

            **Hispanic/Latino (8% of electorate)**
            Deramo 20%, Brown 20%, Raj 9%
            Only Latino still in serious contention after Reyes Yanes
            First Latino on DC Council if elected

            **Men (42% of electorate)**
            Deramo 9%, Brown 7%, Raj 19%
            Moderate men are the target — DSA net negative among men

            **Moderates (22% of electorate)**
            Deramo 9%, Brown 24%, Raj 1%
            Raj is essentially gone — Deramo + Brown own this lane

            **Whites 46+ (sleeper)**
            46-65: Deramo 11%, Brown 10%, Raj 13% — genuinely competitive
            Columbia Heights/Adams Morgan homeowners: safety, schools, business

            **No college degree (24% of electorate)**
            Brown 33%, Deramo 6%, Raj 0%
            Raj has zero ceiling — Deramo's upside is real
            """)

        with col2:
            st.error("""
            **🔴 Manage, Don't Chase — Problem Groups**

            **Black voters (23% of electorate)**
            Deramo 1%, Brown 15%, Raj 2%
            Brown dominates — ceiling is ~5-8% even with perfect execution
            RCV angle: get Black Brown voters to rank Deramo 2nd

            **Young voters 18-45 (45% of electorate)**
            Raj 29%, Brown 10%, Deramo 9%
            Raj's strongest group — don't chase, be selective
            Young moderates, young Hispanics, young LGBTQ+ men are reachable

            **Women (56% of electorate)**
            Brown 17%, Raj 17%, Deramo 6%
            Focus on women 45+, mothers with school-age kids
            Non-binary → Raj 51%, Deramo 0% — concede

            **Post-grad degree (35% of electorate)**
            Raj 26%, Brown 9%, Deramo 10%
            Raj's educational stronghold — focus elsewhere
            """)

        st.divider()

        # Identity universes
        st.subheader("🗺️ Identity Universe Tables")

        st.markdown("#### 🌎 Identity Universe 1 — Hispanic/Latino Max Turnout")
        identity_universe_1 = pd.DataFrame({
            "Precinct": [39, 40, 23, 24, 25],
            "Neighborhood": ["Mount Pleasant/Columbia Heights", "Mount Pleasant", "Columbia Heights", "Adams Morgan", "Adams Morgan"],
            "Why_Target": [
                "Heart of DC's Salvadoran community — highest Hispanic concentration in Ward 1",
                "Mount Pleasant — historic Latino residential anchor since 1980s",
                "Columbia Heights — large Latino population, community anchors on 14th St",
                "Adams Morgan — Hispanic family density, longtime residents",
                "Adams Morgan — Hispanic renters and homeowners mixed",
            ],
            "Deramo_Edge": [
                "Only Latino w/ double digits in PPP poll, first Latino on DC Council if elected",
                "Speaks Portuguese, Brazilian heritage resonates with Latino voters",
                "Tied with Brown at 20% among Hispanics, Raj only 9%",
                "Business platform resonates with Latino small business owners",
                "Schools + safety message resonates with longer-tenure families",
            ],
            "RCV_Ask": ["Deramo #1, Brown #2"] * 5,
            "Untapped_Voters": [2873, 2310, 2355, 1920, 2804],
            "Priority": ["🚨 Tier 1", "🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2"],
        })
        st.dataframe(identity_universe_1, use_container_width=True, hide_index=True,
            column_config={"Untapped_Voters": st.column_config.ProgressColumn("Untapped", min_value=0, max_value=3500, format="%d")})

        st.divider()
        st.markdown("#### 🏳️‍🌈 Identity Universe 2 — LGBTQ+ Activation")
        identity_universe_2 = pd.DataFrame({
            "Precinct": [40, 43, 41, 42, 39],
            "Neighborhood": ["Mount Pleasant", "Park View", "Columbia Heights", "Columbia Heights", "Mount Pleasant"],
            "LGBTQ_Context": [
                "Historic Black LGBTQ+ corridor",
                "Park View — near Shaw/U St queer nightlife corridor",
                "Adams Morgan w/ established LGBTQ+ residential + nightlife",
                "Columbia Heights — younger queer renters, high density",
                "Columbia Heights w/ growing LGBTQ+ presence",
            ],
            "Deramo_Edge": [
                "2nd out LGBTQ+ on DC Council, first Latino — historic",
                "Record vs Raj: 5 years ANC vs zero elected record",
                "Safety from discrimination explicitly in Miguel's platform",
                "Note: Raj also queer — message must be RECORD not just identity (ideally Blade and Advocate to boost Miguel down stretch)",
                "Cross-universe: LGBTQ+ + crime + business all align here",
            ],
            "RCV_Ask": ["Deramo #1, Brown #2"] * 5,
            "Untapped_Voters": [2310, 1343, 2563, 1246, 2873],
            "Priority": ["🚨 Tier 1", "🚨 Tier 1", "🚨 Tier 1", "🟡 Tier 2", "🟡 Tier 2"],
        })
        st.dataframe(identity_universe_2, use_container_width=True, hide_index=True,
            column_config={"Untapped_Voters": st.column_config.ProgressColumn("Untapped", min_value=0, max_value=3500, format="%d")})

        st.divider()
        st.markdown("#### 👴 Identity Universe 3 — White 46+ Sleeper Vote")
        st.caption("Most underrated universe in the race. Raj is irrelevant. It's Brown vs Deramo.")
        identity_universe_3 = pd.DataFrame({
            "Precinct": [35, 36, 37, 38, 23],
            "Neighborhood": ["Adams Morgan", "Columbia Heights", "Pleasant Plains", "Park View", "Columbia Heights"],
            "Profile": [
                "Highest median age (45) — white long-tenure homeowners",
                "Highest owner-occupancy (47%) — invested, pragmatic, anti-ideology",
                "Park View white 46+ — active on crime and school quality",
                "Park View — school-parent overlap",
                "Mt Pleasant older white homeowners",
            ],
            "Deramo_Edge": [
                "46-65: Deramo 11%, Brown 10% — genuinely competitive",
                "Owner-occupants respond to safety/business record not union politics",
                "McDuffie leads 46-65 on mayor — dual ticket works perfectly",
                "65+ problem (Deramo 0%) but 46-65 is the real target",
                "Tenure 5+ years — long enough to care, short enough to not be locked in",
            ],
            "RCV_Ask": ["Deramo #1, Brown #2"] * 5,
            "Untapped_Voters": [2458, 3080, 2698, 2085, 2355],
            "Priority": ["🚨 Tier 1", "🚨 Tier 1", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
        })
        st.dataframe(identity_universe_3, use_container_width=True, hide_index=True,
            column_config={"Untapped_Voters": st.column_config.ProgressColumn("Untapped", min_value=0, max_value=3500, format="%d")})

        st.divider()
        st.markdown("#### 🗳️ Identity Universe 4 — Moderate + Conservative Dem")
        identity_universe_4 = pd.DataFrame({
            "Precinct": [35, 36, 37, 38, 22],
            "Neighborhood": ["Adams Morgan", "Columbia Heights", "Pleasant Plains", "Park View", "U Street"],
            "Profile": [
                "Adams Morgan — longest tenure residents, moderate Dems",
                "Columbia Heights — homeowners, pragmatic, not ideological",
                "Park View — working class moderate Dems, crime top concern",
                "Park View — Brown's ANC base but Deramo can compete",
                "Columbia Heights — moderate Dems frustrated with progressive performance",
            ],
            "Deramo_Edge": [
                "Moderates: Deramo 9%, Raj 1% — Raj is irrelevant here",
                "Conservative Dems: Brown 38%, Deramo 0% — RCV transfer play only",
                "DSA endorsement net negative among moderates (-27% vs +20%)",
                "Nadeau endorsed Brown — 23% of moderates less likely with Nadeau",
                "The ask: rank Brown or Deramo 1-2, leave Raj unranked",
            ],
            "RCV_Ask": [
                "Deramo #1, Brown #2 — or Brown #1, Deramo #2",
                "Either order — stress RCV math",
                "If Brown voter: Brown #1, Deramo #2, Raj unranked",
                "If Deramo voter: Deramo #1, Brown #2, Raj unranked",
                "Same regardless of preference order",
            ],
            "Untapped_Voters": [2458, 3080, 2698, 2085, 2964],
            "Priority": ["🚨 Tier 1", "🚨 Tier 1", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
        })
        st.dataframe(identity_universe_4, use_container_width=True, hide_index=True,
            column_config={"Untapped_Voters": st.column_config.ProgressColumn("Untapped", min_value=0, max_value=3500, format="%d")})

        st.divider()
        st.markdown("#### 🤝 Identity Universe 5 — Non-Black Minority + Working Class")
        identity_universe_5 = pd.DataFrame({
            "Precinct": [22, 39, 25, 37, 23],
            "Neighborhood": ["U Street", "Mount Pleasant", "Adams Morgan", "Pleasant Plains", "Columbia Heights"],
            "Profile": [
                "Asian, multiracial, mixed-income non-black voters",
                "Other race voters: Deramo 11%, Raj 20% — competitive",
                "Working class renters, no college degree voters",
                "African immigrant community, not Black Dem establishment aligned",
                "Central American community — school/crime concerns",
            ],
            "Deramo_Edge": [
                "Other race: three-way split — Deramo competitive",
                "No college degree: Brown 33%, Deramo 6%, Raj 0%",
                "Working class: crime + business message lands harder than DSA ideology",
                "African immigrants often socially conservative — Raj's platform alienates",
                "Bilingual outreach: Deramo's Portuguese + Spanish-adjacent campaigning",
            ],
            "RCV_Ask": ["Deramo #1, Brown #2"] * 5,
            "Untapped_Voters": [2964, 2873, 2804, 2698, 2355],
            "Priority": ["🟡 Tier 2", "🟡 Tier 2", "🟡 Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
        })
        st.dataframe(identity_universe_5, use_container_width=True, hide_index=True,
            column_config={"Untapped_Voters": st.column_config.ProgressColumn("Untapped", min_value=0, max_value=3500, format="%d")})

        st.divider()
        st.markdown("#### 🦅 Identity Universe 6 — White NonLeft (Moderate + Conservative)")
        st.caption("Most underrated universe. Raj is radioactive here. It's Brown vs Deramo.")
        identity_universe_6 = pd.DataFrame({
            "Precinct": [35, 36, 37, 38, 22],
            "Neighborhood": ["Adams Morgan", "Columbia Heights", "Pleasant Plains", "Park View", "U Street"],
            "Profile": [
                "Long-tenure white homeowners, bought pre-2010, moderate-to-conservative Dems",
                "Highest owner-occupancy, most invested in neighborhood stability",
                "Park View white moderates, active on crime and school quality",
                "Park View: school-parent overlap, Georgia Ave safety concern",
                "14th St corridor white moderates — watched businesses close 12 years",
            ],
            "Poll_Data": [
                "Conservatives: Brown 38%, Raj 5%, Deramo 0% — Brown owns but Raj irrelevant",
                "Moderates: Brown 24%, Deramo 9%, Raj 1% — two-person race",
                "White 46-65 on mayor: McDuffie 52% — these voters exist and align",
                "Nadeau endorsement: moderates 29% less likely — Brown's liability here",
                "DSA endorsement: moderates 27% less likely — Raj radioactive",
            ],
            "Deramo_Message": [
                "'Public safety is foundational' — not ideology, results",
                "Homeowner investment angle: business closures hurt property values",
                "Schools + crime — closures hurt kids, need pragmatism not marching orders",
                "Former State Dept / DHS — competence credential resonates",
                "12 years of Nadeau, businesses still closing — Miguel = change",
            ],
            "RCV_Strategy": [
                "If Brown voter: Brown #1, Deramo #2, Raj unranked",
                "If undecided: Deramo #1, Brown #2 — both beat Raj",
                "Key ask: do NOT rank Raj, her platform is opposite of your values",
                "Conservative Dems may stop at #1, educate on RCV math",
                "White moderate undecideds are the direct Deramo target here",
            ],
            "Untapped_Voters": [2458, 3080, 2698, 2085, 2964],
            "Priority": ["🚨 Tier 1", "🚨 Tier 1", "⭐ Tier 2", "⭐ Tier 2", "⭐ Tier 2"],
        })
        st.dataframe(identity_universe_6, use_container_width=True, hide_index=True,
            column_config={"Untapped_Voters": st.column_config.ProgressColumn("Untapped", min_value=0, max_value=3500, format="%d")})

# ══════════════════════════════════════════════════════════
# TAB 4 — TARGETING MODEL
# ══════════════════════════════════════════════════════════
with tab4:
    if not unlocked:
        st.info("### 🔒 Access After Meeting\nEnter the access code to view targeting intelligence.\n\n**Contact Thomas Emerick to request access.**")
    else:
        st.subheader("🎯 Ward 1 Targeting Model")
        st.markdown("""
        **This is a data-driven canvassing model for Miguel Trindade Deramo — June 16, 2026 primary.**

        Every precinct scored across 9 validated universes — sourced from MPD crime data, DCBOE 2022/2024 election results, DC DLCP business licenses, 2020/2023 Census, and PPP/GGWash poll crosstabs.
        The matrix below tells you exactly where to knock doors and why.

        **The three numbers that matter:**
        """)
        st.markdown("""
        <ul>
        <li>🔴 Red dot = high priority universe for that precinct</li>
        <li>🟡 Yellow dot = medium priority</li>
        <li><span style="display:inline-block;width:20px;height:10px;background:#e74c3c;border-radius:3px;vertical-align:middle;margin-right:6px"></span> Registered Dems = registered Democrats who didn't vote in 2024</li>
        </ul>
        """, unsafe_allow_html=True)
    

        st.subheader("🎯 Combined Issue + Identity Priority Matrix")
        st.caption("Every precinct scored across all 10 universes — 5 issue + 5 identity")



        reg_dems = {20:870, 22:4038, 23:2978, 24:2756, 25:4068, 35:3479,
                    36:3962, 37:3336, 38:2718, 39:3911, 40:3322, 41:3337,
                    42:1713, 43:1751, 137:1110}
        untapped = {40:2310, 41:2563, 39:2873, 35:2458, 36:3080, 23:2355,
                    37:2698, 38:2085, 43:1343, 22:2964, 42:1246, 25:2804,
                    24:1920, 20:671, 137:890}

        scored = pd.read_csv('ward1_scored.csv')
        scored['Reg_Dems'] = scored['Precinct'].map(reg_dems)
        scored['Untapped'] = scored['Precinct'].map(untapped)

        dot_cols = ['Crime_Dot','Business_Dot','Schools_Dot','LGBTQ_Dot',
                    'Anti_Nadeau_Dot','Hispanic_Dot','White_46plus_Dot',
                    'Not_Leftist_Dot','Minrty_NoAlign_Dot']
        for c in dot_cols:
            scored[c + '_num'] = scored[c].map({'🔴': 1, '🟡': 0})
        scored['Red_Count'] = scored[[c + '_num' for c in dot_cols]].sum(axis=1)

        for col in ['Reg_Dems', 'Untapped']:
            mn, mx = scored[col].min(), scored[col].max()
            scored[col + '_norm'] = ((scored[col] - mn) / (mx - mn) * 10).round(2)

        scored['Final_Score'] = (
            scored['Red_Count']     * 0.60 +
            scored['Reg_Dems_norm'] * 0.35 +
            scored['Untapped_norm'] * 0.05
        ).round(3)

        scored = scored.sort_values('Final_Score', ascending=False).reset_index(drop=True)

        def medal(i):
            if i < 3: return f"🥇 #{i+1}"
            elif i < 7: return f"🥈 #{i+1}"
            elif i < 11: return f"🥉 #{i+1}"
            else: return f"  #{i+1}"

        scored['Final_Priority'] = [medal(i) for i in range(len(scored))]

        display_cols = ['Precinct','Neighborhood','Crime_Dot','Business_Dot',
                        'Schools_Dot','LGBTQ_Dot','Anti_Nadeau_Dot','Hispanic_Dot',
                        'White_46plus_Dot','Not_Leftist_Dot','Minrty_NoAlign_Dot',
                        'Reg_Dems','Final_Priority']

        combined = scored[display_cols].rename(columns={
            'Crime_Dot': 'Crime',
            'Business_Dot': 'Business',
            'Schools_Dot': 'Schools',
            'LGBTQ_Dot': 'LGBTQ',
            'Anti_Nadeau_Dot': 'Anti_Nadeau',
            'Hispanic_Dot': 'Hispanic',
            'White_46plus_Dot': 'White_46+',
            'Not_Leftist_Dot': 'Not_Leftist',
            'Minrty_NoAlign_Dot': 'Minrty_NoAlign',
            'Reg_Dems': 'Registered Dems',
            'Final_Priority': 'Final_Priority',
        })

        st.dataframe(
            combined,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Registered Dems": st.column_config.ProgressColumn(
                    "Registered Dems", min_value=0, max_value=4500, format="%d"
                ),
            }
        )


        st.markdown("""
            #### The Theory of the Case:

            Raj has a hard ceiling. Polling says 74% of her base is very liberal, she gets 1% among moderates,
            0% among conservatives, and has no small business or public safety record.
            Brown is strong but Nadeau's endorsement is a liability among the exact voters
            Trindade Deramo needs — moderates, men over 45, anti-establishment whites.
            Trindade Deramo wins by being the only candidate who takes seriously the voters
            Raj ignores and Brown can't fully reach: parents, small business owners,
            crime-weary long-tenure residents, LGBTQ+ voters who want record not just identity,
            and the Latino community that sees two of their own in the race.

            **The RCV math that makes it possible:**
            - 54% of Ward 1 Dems undecided in March, so the race is genuinely open
            - Lynch + Reyes Yanes = 450-550 votes that mostly exhaust, Trindade Deramo needs those transfers
            - Brown's Nadeau endorsement is a net negative among moderates and men over 45
            - Raj's DSA brand is net negative among men, moderates, and conservatives
            - Every door knocked in Columbia Heights and Adams Morgan carries outsized value for Miguel

            **The single most important number: Trindade Deramo must finish above Reyes Yanes in Round 1.**
            If she outperforms him, he's eliminated before the transfers happen.
            Mt Pleasant and the Hispanic universe are existential, not optional.
            """)

            
        st.success("""
            **Path to Victory Plan in One Paragraph:**

            Precinct 39 (Mount Pleasant/Columbia Heights) is Trindade Deramo's #1 target — 7 red dots across crime, business, schools, LGBTQ, Anti-Nadeau, Hispanic, and Not_Leftist universes, with 3,911 registered Dems. Precincts 22 (U Street) and 25 (Adams Morgan) round out the Tier 1 trifecta. Columbia Heights (36) is the sleeper: Largest registered Dem pool in the ward at 3,962 with strong signals from demos of Not_Leftist and Minrty_NoAlign (minority not aligned with base of Raj or Brown). Adams Morgan (35) and Columbia Heights (41) complete Tier 2. Every door knocked in these 6 precincts before June 16 is worth more than two doors anywhere else in the ward.
            """)


# ══════════════════════════════════════════════════════════
# TAB 5 — PRECINCT HEATMAP
# ══════════════════════════════════════════════════════════
    with tab5:
        if not unlocked:
            st.info("### 🔒 Access After Meeting\nEnter the access code to view targeting intelligence.\n\n**Contact Thomas Emerick to request access.**")
        else:
            st.subheader("🗺️ Heatmap of Registered Dems Who Stayed Home Last Cycle")
            st.caption("Darker red = more registered Democrats who didn't vote in the 2024 primary. Hover each precinct for details.")
            
            import streamlit.components.v1 as components
            with open("ward1_heatmap.html", "r") as f:
                html = f.read()
            components.html(html, height=600, scrolling=False)

            st.divider()
            st.markdown("#### 📍 Ward 1 Precinct Quick Reference")
            precinct_ref = pd.DataFrame({
                "Precinct": [20, 22, 23, 24, 25, 35, 36, 37, 38, 39, 40, 41, 42, 43, 137],
                "Neighborhood": ["LeDroit Park", "U Street", "Columbia Heights", "Adams Morgan", "Adams Morgan",
                                "Adams Morgan", "Columbia Heights", "Pleasant Plains", "Park View",
                                "Mt Pleasant/Col Hts", "Mount Pleasant", "Columbia Heights",
                                "Columbia Heights", "Park View", "U Street"],
                "Ward Area": ["Southeast", "South Central", "South Central", "Southwest", "Southwest",
                            "West", "Central", "East", "Northeast",
                            "North", "North", "North",
                            "Northeast", "Northeast", "Southeast"],
                "One_Phrase": [
                    "Historic Black neighborhood, Howard University adjacent",
                    "Restaurants, bars, and residential; heart of U Street corridor",
                    "Latino commercial corridor, Columbia Heights Metro hub",
                    "Dense renters, East side 18th St, Pitchers/ALOHO side",
                    "Rowhouse renters, West side 18th St + Columbia Rd bars/dining",
                    "Upper Adams Morgan, longer-tenure homeowners, Rock Creek edge",
                    "Largest Dem pool in ward, 14th St transit crossroads",
                    "Working-class corridor, crime-focused voters, Pleasant Plains proper",
                    "Transitional rowhouse blocks, family-heavy Park View",
                    "#1 target — multi-issue powerhouse, Mt Pleasant meets Col Hts",
                    "Latino Mount Pleasant, Rock Creek Park edge, family density",
                    "High Hispanic density, working-class families, north Col Hts",
                    "Compact dense blocks, Metro-adjacent, smaller north Col Hts",
                    "Quieter rowhouses, Park View proper, Georgia Ave corridor",
                    "Residential U Street both sides, smaller but high LGBTQ signal",
                ],
                "Boundaries": [
                    "4th to 1st; Rhode Island to Michigan",
                    "16th to 9th; U->S 15th-14th->T->Vermont to Florida",
                    "16th to 11th; Florida to Euclid",
                    "18th to 16th; U to Euclid",
                    "Connecticut to 18th; Florida to Adams Mills",
                    "Rock Creek to 16th; Adams Mill->Euclid to Harvard",
                    "16th-11th; Euclid/Columbia detour Irving 15th-14th",
                    "11th to 4th; Florida to Columbia",
                    "11th to Park Place, Columbia to Park Road",
                    "RockCrk-11th; Harv/Clmbia detour Irv-Lamont/Park",
                    "Rock Creek to 16th; Lamont to Piney Branch",
                    "16th to Holmead; Park to Spring",
                    "Holmead to New Hampshire; Park to Spring",
                    "New Hampshr-Park Plc; Park Rd-Rock Crk Church Rd",
                    "13th to Wiltberger Ave; S to T->Vermont->Florida",
                ],
                "Reg_Dems": [870, 4038, 2978, 2756, 4068, 3479, 3962, 3336, 2718, 3911, 3322, 3337, 1713, 1751, 1110],
            })

            st.dataframe(precinct_ref, use_container_width=True, hide_index=True,
                column_config={
                    "Reg_Dems": st.column_config.ProgressColumn(
                        "Registered Dems", min_value=0, max_value=4500, format="%d"
                    ),
                    "One_Phrase": st.column_config.TextColumn("Description", width="large"),
                    "Boundaries": st.column_config.TextColumn("Street Boundaries", width="large"),
                }
            )
            
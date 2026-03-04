"""
Oscar Predictions 2026 - Complete All Categories with Explanations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# Page config
st.set_page_config(
    page_title="Oscar Predictions 2026 - All Categories",
    page_icon="🏆",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FFD700;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
    }
    
    .category-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FFD700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 8px;
        margin: 20px 0;
        text-align: center;
    }
    
    .winner-box {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 20px;
        border-radius: 10px;
        color: black;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .explanation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 15px 0;
    }
    
    .reason-card {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #FFD700;
        margin: 10px 0;
    }
    
    .positive-factor {
        color: #27AE60;
        font-weight: bold;
    }
    
    .negative-factor {
        color: #E74C3C;
        font-weight: bold;
    }
    
    .confidence-high {
        background: #27AE60;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
    }
    
    .confidence-medium {
        background: #F39C12;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
    }
    
    .confidence-low {
        background: #E74C3C;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# ==================== DATA LOADING ====================

def load_all_predictions():
    """
    Load predictions for all 24 categories
    """
    
    predictions = {
        'Best Picture': pd.DataFrame({
            'nominee': ['One Battle after Another', 'Hamnet', 'Sinners', 'Marty Supreme', 'Frankenstein'],
            'film': ['One Battle after Another', 'Hamnet', 'Sinners', 'Marty Supreme', 'Frankenstein'],
            'win_probability': [0.336, 0.316, 0.142, 0.106, 0.100],
            'won_gg_drama': [0, 1, 0, 0, 0],
            'won_gg_musical': [1, 0, 0, 0, 0],
            'won_bafta': [1, 0, 0, 0, 0],
            'total_nominations': [13, 9, 15, 11, 10]
        }),
        
        'Best Director': pd.DataFrame({
            'nominee': ['Paul Thomas Anderson', 'Ryan Coogler', 'Chloé Zhao', 'Josh Safdie', 'Guillermo del Toro'],
            'film': ['One Battle after Another', 'Sinners', 'Hamnet', 'Marty Supreme', 'Frankenstein'],
            'win_probability': [0.636, 0.210, 0.072, 0.050, 0.032],
            'won_gg': [1, 0, 0, 0, 0],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Actor': pd.DataFrame({
            'nominee': ['Michael B. Jordan', 'Timothée Chalamet', 'Leonardo DiCaprio', 'Ethan Hawke', 'Jesse Plemons'],
            'film': ['Sinners', 'Marty Supreme', 'One Battle after Another', 'Blue Moon', 'Bugonia'],
            'win_probability': [0.548, 0.220, 0.152, 0.050, 0.030],
            'won_gg': [0, 0, 0, 0, 0],
            'won_bafta': [0, 0, 0, 0, 0],
        }),
        
        'Best Actress': pd.DataFrame({
            'nominee': ['Jessie Buckley', 'Emma Stone', 'Renate Reinsve', 'Rose Byrne', 'Kate Hudson'],
            'film': ['Hamnet', 'Bugonia', 'Sentimental Value', 'If I Had Legs I\'d Kick You', 'Song Sung Blue'],
            'win_probability': [0.802, 0.152, 0.046, 0.000, 0.000],
            'won_gg': [1, 0, 0, 0, 0],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Supporting Actor': pd.DataFrame({
            'nominee': ['Delroy Lindo', 'Stellan Skarsgård', 'Sean Penn', 'Paul Mescal', 'Benicio Del Toro'],
            'film': ['Sinners', 'Sentimental Value', 'One Battle after Another', 'Hamnet', 'One Battle after Another'],
            'win_probability': [0.447, 0.217, 0.161, 0.095, 0.080],
            'won_gg': [0, 0, 1, 0, 0],
            'won_bafta': [0, 0, 1, 0, 0],
        }),
        
        'Best Supporting Actress': pd.DataFrame({
            'nominee': ['Wunmi Mosaku', 'Elle Fanning', 'Inga Ibsdotter Lilleaas', 'Teyana Taylor', 'Emily Watson'],
            'film': ['Sinners', 'Marty Supreme', 'Sentimental Value', 'One Battle after Another', 'Hamnet'],
            'win_probability': [0.786, 0.085, 0.085, 0.022, 0.022],
            'won_gg': [0, 0, 0, 1, 0],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Original Screenplay': pd.DataFrame({
            'nominee': ['Sinners', 'Sentimental Value', 'Marty Supreme', 'The Secret Agent', 'I Swear'],
            'film': ['Sinners', 'Sentimental Value', 'Marty Supreme', 'The Secret Agent', 'I Swear'],
            'win_probability': [0.921, 0.044, 0.035, 0.000, 0.000],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Adapted Screenplay': pd.DataFrame({
            'nominee': ['One Battle after Another', 'Frankenstein', 'Hamnet', 'Bugonia', 'Pillion'],
            'film': ['One Battle after Another', 'Frankenstein', 'Hamnet', 'Bugonia', 'Pillion'],
            'win_probability': [0.918, 0.063, 0.018, 0.001, 0.000],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Cinematography': pd.DataFrame({
            'nominee': ['Sinners (Autumn Durald Arkapaw)', 'One Battle after Another', 'Frankenstein', 'Hamnet', 'Marty Supreme'],
            'film': ['Sinners', 'One Battle after Another', 'Frankenstein', 'Hamnet', 'Marty Supreme'],
            'win_probability': [0.468, 0.313, 0.184, 0.035, 0.000],
            'won_bafta': [0, 1, 0, 0, 0],
        }),
        
        'Best Film Editing': pd.DataFrame({
            'nominee': ['Sinners', 'One Battle after Another', 'Marty Supreme', 'Hamnet', 'F1'],
            'film': ['Sinners', 'One Battle after Another', 'Marty Supreme', 'Hamnet', 'F1'],
            'win_probability': [0.634, 0.220, 0.082, 0.032, 0.032],
            'won_bafta': [0, 1, 0, 0, 0],
        }),
        
        'Best Production Design': pd.DataFrame({
            'nominee': ['Sinners', 'Frankenstein', 'Hamnet', 'One Battle after Another', 'Marty Supreme'],
            'film': ['Sinners', 'Frankenstein', 'Hamnet', 'One Battle after Another', 'Marty Supreme'],
            'win_probability': [0.370, 0.264, 0.175, 0.120, 0.071],
            'won_bafta': [0, 1, 0, 0, 0],
        }),
        
        'Best Costume Design': pd.DataFrame({
            'nominee': ['Hamnet', 'Sinners', 'Marty Supreme', 'Frankenstein', 'Wicked: For Good'],
            'film': ['Hamnet', 'Sinners', 'Marty Supreme', 'Frankenstein', 'Wicked: For Good'],
            'win_probability': [0.315, 0.269, 0.256, 0.160, 0.000],
            'won_bafta': [0, 0, 0, 1, 0],
        }),
        
        'Best Makeup & Hair': pd.DataFrame({
            'nominee': ['Sinners', 'Frankenstein', 'Hamnet', 'Marty Supreme', 'Wicked: For Good'],
            'film': ['Sinners', 'Frankenstein', 'Hamnet', 'Marty Supreme', 'Wicked: For Good'],
            'win_probability': [0.675, 0.325, 0.000, 0.000, 0.000],
            'won_bafta': [0, 1, 0, 0, 0],
        }),
        
        'Best Sound': pd.DataFrame({
            'nominee': ['Sinners', 'One Battle after Another', 'Frankenstein', 'F1', 'Warfare'],
            'film': ['Sinners', 'One Battle after Another', 'Frankenstein', 'F1', 'Warfare'],
            'win_probability': [0.716, 0.172, 0.075, 0.037, 0.000],
            'won_bafta': [0, 0, 0, 1, 0],
        }),
        
        'Best Visual Effects': pd.DataFrame({
            'nominee': ['Avatar: Fire and Ash', 'Frankenstein', 'How to Train Your Dragon', 'F1', 'The Lost Bus'],
            'film': ['Avatar: Fire and Ash', 'Frankenstein', 'How to Train Your Dragon', 'F1', 'The Lost Bus'],
            'win_probability': [0.550, 0.250, 0.150, 0.050, 0.000],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Original Score': pd.DataFrame({
            'nominee': ['Sinners (Ludwig Göransson)', 'Frankenstein', 'One Battle after Another', 'Hamnet', 'Bugonia'],
            'film': ['Sinners', 'Frankenstein', 'One Battle after Another', 'Hamnet', 'Bugonia'],
            'win_probability': [0.775, 0.125, 0.053, 0.027, 0.020],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Original Song': pd.DataFrame({
            'nominee': ['"Golden" (KPop Demon Hunters)', '"Never Too Late" (Elton John)', '"Mi Camino" (Emilia Pérez)', 
                       '"The Journey" (The Six Triple Eight)', '"Kiss the Sky" (The Wild Robot)'],
            'film': ['KPop Demon Hunters', 'Elton John: Never Too Late', 'Emilia Pérez', 'The Six Triple Eight', 'The Wild Robot'],
            'win_probability': [0.400, 0.300, 0.200, 0.050, 0.050],
            'won_gg': [1, 0, 0, 0, 0],
        }),
        
        'Best Animated Feature': pd.DataFrame({
            'nominee': ['Zootopia 2', 'KPop Demon Hunters', 'Flow', 'The Wild Robot', 'Wallace & Gromit: Vengeance Most Fowl'],
            'film': ['Zootopia 2', 'KPop Demon Hunters', 'Flow', 'The Wild Robot', 'Wallace & Gromit: Vengeance Most Fowl'],
            'win_probability': [0.450, 0.300, 0.150, 0.070, 0.030],
            'won_gg': [0, 1, 0, 0, 0],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best International Feature': pd.DataFrame({
            'nominee': ['Sentimental Value (Norway)', 'Emilia Pérez (France)', 'The Secret Agent (Brazil)', 
                       'I\'m Still Here (Brazil)', 'Flow (Latvia)'],
            'film': ['Sentimental Value', 'Emilia Pérez', 'The Secret Agent', 'I\'m Still Here', 'Flow'],
            'win_probability': [0.400, 0.350, 0.150, 0.070, 0.030],
            'won_bafta': [1, 0, 0, 0, 0],
        }),
        
        'Best Documentary Feature': pd.DataFrame({
            'nominee': ['No Other Land', 'Soundtrack to a Coup d\'Etat', 'Sugarcane', 'Porcelain War', 'Black Box Diaries'],
            'film': ['No Other Land', 'Soundtrack to a Coup d\'Etat', 'Sugarcane', 'Porcelain War', 'Black Box Diaries'],
            'win_probability': [0.450, 0.300, 0.150, 0.070, 0.030],
        }),
    }
    
    return predictions


def get_category_explanation(category, winner_data, all_data):
    """
    Generate explanation for why a nominee has their probability
    """
    reasons = []
    prob = winner_data['win_probability']
    
    # Category-specific explanations
    if category == 'Best Picture':
        noms = winner_data.get('total_nominations', 0)
        gg_drama = winner_data.get('won_gg_drama', 0)
        gg_musical = winner_data.get('won_gg_musical', 0)
        bafta = winner_data.get('won_bafta', 0)
        
        if noms >= 12:
            reasons.append({'factor': '🎯 High Nomination Count', 'detail': f'{int(noms)} nominations', 'impact': 'Strong', 'type': 'positive'})
        
        if gg_drama:
            reasons.append({'factor': '🏆 Golden Globe Drama Winner', 'detail': '43% historical Oscar rate', 'impact': 'Moderate-Strong', 'type': 'positive'})
        elif gg_musical:
            reasons.append({'factor': '🏆 Golden Globe Musical Winner', 'detail': '22% historical Oscar rate', 'impact': 'Moderate', 'type': 'positive'})
        
        if bafta:
            reasons.append({'factor': '🏆 BAFTA Best Film Winner', 'detail': 'Strongest predictor (~60%)', 'impact': 'Very Strong', 'type': 'positive'})
        
        reasons.append({'factor': '⏳ SAG Outstanding Cast', 'detail': 'Not yet announced', 'impact': 'Critical factor pending', 'type': 'neutral'})
    
    elif category == 'Best Director':
        won_gg = winner_data.get('won_gg', 0)
        won_bafta = winner_data.get('won_bafta', 0)
        
        if won_gg:
            reasons.append({'factor': '🏆 Golden Globe Winner', 'detail': 'Director match with Best Picture', 'impact': 'Strong', 'type': 'positive'})
        
        if won_bafta:
            reasons.append({'factor': '🏆 BAFTA Winner', 'detail': 'BAFTA-Oscar correlation ~70%', 'impact': 'Very Strong', 'type': 'positive'})
        
        reasons.append({'factor': '🎬 Film\'s Overall Strength', 'detail': f'Film: {winner_data.get("film", "Unknown")}', 'impact': 'Indirect boost', 'type': 'positive'})
    
    elif category in ['Best Actor', 'Best Actress', 'Best Supporting Actor', 'Best Supporting Actress']:
        won_gg = winner_data.get('won_gg', 0)
        won_bafta = winner_data.get('won_bafta', 0)
        
        if won_gg and won_bafta:
            reasons.append({'factor': '🔥 Precursor Sweep', 'detail': 'Won both GG and BAFTA', 'impact': 'Almost Guaranteed', 'type': 'positive'})
        elif won_bafta:
            reasons.append({'factor': '🏆 BAFTA Winner', 'detail': 'Strong Oscar predictor', 'impact': 'Very Strong', 'type': 'positive'})
        elif won_gg:
            reasons.append({'factor': '🏆 Golden Globe Winner', 'detail': 'Moderate Oscar predictor', 'impact': 'Moderate', 'type': 'positive'})
        else:
            reasons.append({'factor': '❌ No Major Precursors', 'detail': 'Rare for winner to have none', 'impact': 'Disadvantage', 'type': 'negative'})
        
        reasons.append({'factor': '⏳ SAG Individual Award', 'detail': 'Not yet announced', 'impact': 'Could be decisive', 'type': 'neutral'})
    
    elif category in ['Best Original Screenplay', 'Best Adapted Screenplay']:
        won_bafta = winner_data.get('won_bafta', 0)
        
        if won_bafta:
            reasons.append({'factor': '🏆 BAFTA Screenplay Winner', 'detail': 'Very strong correlation', 'impact': 'Almost Guaranteed', 'type': 'positive'})
        
        reasons.append({'factor': '✍️ WGA (Writers Guild)', 'detail': 'Not yet announced', 'impact': 'Strong predictor pending', 'type': 'neutral'})
    
    elif category in ['Best Cinematography', 'Best Film Editing', 'Best Production Design', 
                     'Best Costume Design', 'Best Makeup & Hair', 'Best Sound', 'Best Visual Effects', 'Best Original Score']:
        won_bafta = winner_data.get('won_bafta', 0)
        film = winner_data.get('film', '')
        
        if won_bafta:
            reasons.append({'factor': '🏆 BAFTA Winner', 'detail': 'Technical BAFTA-Oscar correlation high', 'impact': 'Very Strong', 'type': 'positive'})
        
        if 'Sinners' in film:
            reasons.append({'factor': '🎬 Most Nominated Film', 'detail': 'Sinners leads technical categories', 'impact': 'Strong', 'type': 'positive'})
        
        reasons.append({'factor': '🎨 Technical Excellence', 'detail': 'Based on craft guild recognition', 'impact': 'Moderate', 'type': 'positive'})
    
    elif category == 'Best Animated Feature':
        won_gg = winner_data.get('won_gg', 0)
        won_bafta = winner_data.get('won_bafta', 0)
        
        if won_gg and won_bafta:
            reasons.append({'factor': '🔥 Precursor Sweep', 'detail': 'Won both GG and BAFTA', 'impact': 'Almost Guaranteed', 'type': 'positive'})
        elif won_bafta:
            reasons.append({'factor': '🏆 BAFTA Winner', 'detail': 'Strong animation predictor', 'impact': 'Very Strong', 'type': 'positive'})
        elif won_gg:
            reasons.append({'factor': '🏆 Golden Globe Winner', 'detail': 'Moderate predictor', 'impact': 'Moderate', 'type': 'positive'})
    
    elif category == 'Best International Feature':
        won_bafta = winner_data.get('won_bafta', 0)
        
        if won_bafta:
            reasons.append({'factor': '🏆 BAFTA Winner', 'detail': 'Non-English BAFTA winner', 'impact': 'Very Strong', 'type': 'positive'})
        
        reasons.append({'factor': '🌍 International Recognition', 'detail': 'Festival circuit performance', 'impact': 'Moderate', 'type': 'positive'})
    
    # Add probability-based reasoning
    if prob > 0.70:
        reasons.append({'factor': '📊 Model Confidence', 'detail': 'Very high probability (>70%)', 'impact': 'Clear favorite', 'type': 'positive'})
    elif prob > 0.50:
        reasons.append({'factor': '📊 Model Confidence', 'detail': 'High probability (50-70%)', 'impact': 'Strong favorite', 'type': 'positive'})
    elif prob > 0.30:
        reasons.append({'factor': '📊 Model Confidence', 'detail': 'Moderate probability (30-50%)', 'impact': 'Leading but not guaranteed', 'type': 'neutral'})
    else:
        reasons.append({'factor': '📊 Model Confidence', 'detail': 'Lower probability (<30%)', 'impact': 'Competitive race', 'type': 'neutral'})
    
    return reasons


# ==================== MAIN APP ====================

# Header
st.markdown('<div class="main-header">🏆 OSCAR PREDICTIONS 2026 🏆<br/>ALL 24 CATEGORIES</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Page:",
    [
        "🏠 Overview",
        "🎬 Best Picture",
        "🎭 Acting Categories",
        "✍️ Writing Categories", 
        "🎨 Technical Categories",
        "🎵 Music Categories",
        "🌍 Specialty Categories",
        "🔮 Scenario Simulator",
        "📈 Predictor Analysis",
        "ℹ️ About Model"
    ]
)

# Load all predictions
all_predictions = load_all_predictions()


# ==================== PAGE: OVERVIEW ====================

if page == "🏠 Overview":
    st.header("🏠 Complete Predictions Overview")
    
    st.markdown("""
    ### 📊 All 24 Oscar Categories Predicted
    
    **Status:** Updated after Golden Globes and BAFTA 2026  
    **Pending:** SAG Awards (Late February 2026)
    """)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Categories", "24")
    with col2:
        very_confident = sum(1 for cat, df in all_predictions.items() if df.iloc[0]['win_probability'] > 0.70)
        st.metric("High Confidence (>70%)", very_confident)
    with col3:
        competitive = sum(1 for cat, df in all_predictions.items() if df.iloc[0]['win_probability'] < 0.50)
        st.metric("Competitive Races (<50%)", competitive)
    with col4:
        st.metric("Films Predicted to Win Most", "Sinners (7-8)")
    
    # Category breakdown
    st.subheader("📋 All Categories at a Glance")
    
    summary_data = []
    
    for cat_name, df in all_predictions.items():
        winner = df.iloc[0]
        winner_name = winner['nominee'] if 'nominee' in winner else winner.get('film', 'Unknown')
        prob = winner['win_probability'] * 100
        
        if prob > 70:
            confidence = "🟢 Very High"
        elif prob > 50:
            confidence = "🟡 High"
        elif prob > 30:
            confidence = "🟠 Moderate"
        else:
            confidence = "🔴 Low"
        
        summary_data.append({
            'Category': cat_name,
            'Predicted Winner': winner_name,
            'Probability': f"{prob:.1f}%",
            'Confidence': confidence
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Filter
    confidence_filter = st.multiselect(
        "Filter by Confidence Level:",
        ["🟢 Very High", "🟡 High", "🟠 Moderate", "🔴 Low"],
        default=["🟢 Very High", "🟡 High", "🟠 Moderate", "🔴 Low"]
    )
    
    filtered_df = summary_df[summary_df['Confidence'].isin(confidence_filter)]
    
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    
    # Film domination chart
    st.subheader("🎬 Predicted Wins by Film")
    
    film_wins = {
        'Sinners': 7,
        'One Battle after Another': 4,
        'Hamnet': 2,
        'Frankenstein': 1,
        'Avatar: Fire and Ash': 1,
        'Zootopia 2': 1,
        'Others': 8
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=list(film_wins.keys()),
        values=list(film_wins.values()),
        hole=.3,
        marker=dict(colors=['#E74C3C', '#FFD700', '#2ECC71', '#3498DB', '#9B59B6', '#1ABC9C', '#95A5A6'])
    )])
    
    fig.update_layout(
        title="Distribution of Predicted Oscar Wins",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==================== PAGE: BEST PICTURE ====================

elif page == "🎬 Best Picture":
    st.header("🎬 Best Picture Predictions")
    
    df = all_predictions['Best Picture']
    
    # Top contenders
    st.subheader("🏆 Top 5 Contenders")
    
    for idx, row in df.iterrows():
        film = row['film']
        prob = row['win_probability'] * 100
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            colors = ["#FFD700", "#C0C0C0", "#CD7F32", "#E0E0E0", "#F0F0F0"]
            
            # Precursors
            precursors = []
            if row.get('won_gg_drama'): precursors.append("GG Drama")
            if row.get('won_gg_musical'): precursors.append("GG Musical")
            if row.get('won_bafta'): precursors.append("BAFTA")
            precursor_str = " + ".join(precursors) if precursors else "None yet"
            
            st.markdown(f"""
            <div style="background: {colors[idx]}; padding: 15px; border-radius: 8px; margin: 10px 0; color: black;">
                <h3>#{idx+1} {film}</h3>
                <h2>{prob:.1f}%</h2>
                <p>📊 {int(row['total_nominations'])} nominations | 🏆 {precursor_str}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button(f"Why? 🔍", key=f"bp_{film}"):
                st.session_state.bp_explain = film
    
    # Show explanation
    if hasattr(st.session_state, 'bp_explain'):
        st.markdown("---")
        film_name = st.session_state.bp_explain
        film_data = df[df['film'] == film_name].iloc[0]
        
        reasons = get_category_explanation('Best Picture', film_data, df)
        
        st.markdown(f"""
        <div class="explanation-box">
            <h2>🎯 Why {film_name} has {film_data['win_probability']*100:.1f}% probability</h2>
        </div>
        """, unsafe_allow_html=True)
        
        for reason in reasons:
            icon = "✅" if reason['type'] == 'positive' else ("❌" if reason['type'] == 'negative' else "⏳")
            color_class = "positive-factor" if reason['type'] == 'positive' else ("negative-factor" if reason['type'] == 'negative' else "")
            
            st.markdown(f"""
            <div class="reason-card">
                <h4>{icon} {reason['factor']}</h4>
                <p>{reason['detail']}</p>
                <p class="{color_class}">Impact: {reason['impact']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Visualization
    st.subheader("📈 Race Visualization")
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['film'],
            y=df['win_probability'] * 100,
            text=[f"{p*100:.1f}%" for p in df['win_probability']],
            textposition='outside',
            marker=dict(
                color=['#FFD700', '#C0C0C0', '#CD7F32', '#E0E0E0', '#F0F0F0'],
                line=dict(color='black', width=2)
            )
        )
    ])
    
    fig.update_layout(
        title="Best Picture Probability Distribution",
        xaxis_title="Film",
        yaxis_title="Win Probability (%)",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


# ==================== PAGE: ACTING CATEGORIES ====================

elif page == "🎭 Acting Categories":
    st.header("🎭 Acting Category Predictions")
    
    acting_cats = {
        'Best Actor': all_predictions['Best Actor'],
        'Best Actress': all_predictions['Best Actress'],
        'Best Supporting Actor': all_predictions['Best Supporting Actor'],
        'Best Supporting Actress': all_predictions['Best Supporting Actress']
    }
    
    for cat_name, df in acting_cats.items():
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        
        winner = df.iloc[0]
        prob = winner['win_probability'] * 100
        
        # Winner box
        st.markdown(f"""
        <div class="winner-box">
            🏆 PREDICTED WINNER: {winner['nominee']}<br/>
            ({winner['film']}) - {prob:.1f}%
        </div>
        """, unsafe_allow_html=True)
        
        # Top 3
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write("**Top 3 Predictions:**")
            for idx, row in df.head(3).iterrows():
                st.progress(row['win_probability'])
                st.write(f"**{idx+1}. {row['nominee']}** ({row['film']}): {row['win_probability']*100:.1f}%")
        
        with col2:
            if st.button(f"Explain 🔍", key=f"act_{cat_name}"):
                st.session_state[f'explain_{cat_name}'] = True
        
        # Show explanation
        if st.session_state.get(f'explain_{cat_name}'):
            reasons = get_category_explanation(cat_name, winner, df)
            
            st.markdown("**Why this prediction:**")
            for reason in reasons:
                icon = "✅" if reason['type'] == 'positive' else ("❌" if reason['type'] == 'negative' else "⏳")
                st.markdown(f"{icon} **{reason['factor']}**: {reason['detail']} - *{reason['impact']}*")
        
        st.markdown("---")


# ==================== PAGE: WRITING CATEGORIES ====================

elif page == "✍️ Writing Categories":
    st.header("✍️ Writing Category Predictions")
    
    writing_cats = {
        'Best Original Screenplay': all_predictions['Best Original Screenplay'],
        'Best Adapted Screenplay': all_predictions['Best Adapted Screenplay']
    }
    
    for cat_name, df in writing_cats.items():
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        
        winner = df.iloc[0]
        prob = winner['win_probability'] * 100
        
        st.markdown(f"""
        <div class="winner-box">
            🏆 PREDICTED WINNER: {winner['nominee']}<br/>
            {prob:.1f}% probability
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            for idx, row in df.head(3).iterrows():
                st.progress(row['win_probability'])
                st.write(f"**{idx+1}. {row['nominee']}**: {row['win_probability']*100:.1f}%")
        
        with col2:
            if st.button(f"Why? 🔍", key=f"writ_{cat_name}"):
                st.session_state[f'explain_{cat_name}'] = True
        
        if st.session_state.get(f'explain_{cat_name}'):
            reasons = get_category_explanation(cat_name, winner, df)
            
            st.markdown("**Explanation:**")
            for reason in reasons:
                icon = "✅" if reason['type'] == 'positive' else ("❌" if reason['type'] == 'negative' else "⏳")
                st.markdown(f"{icon} **{reason['factor']}**: {reason['detail']}")
        
        st.markdown("---")


# ==================== PAGE: TECHNICAL CATEGORIES ====================

elif page == "🎨 Technical Categories":
    st.header("🎨 Technical Category Predictions")
    
    st.info("📊 **Note:** Sinners is predicted to dominate technical categories with 7 expected wins!")
    
    technical_cats = {
        'Best Cinematography': all_predictions['Best Cinematography'],
        'Best Film Editing': all_predictions['Best Film Editing'],
        'Best Production Design': all_predictions['Best Production Design'],
        'Best Costume Design': all_predictions['Best Costume Design'],
        'Best Makeup & Hair': all_predictions['Best Makeup & Hair'],
        'Best Sound': all_predictions['Best Sound'],
        'Best Visual Effects': all_predictions['Best Visual Effects']
    }
    
    # Summary chart
    st.subheader("📊 Technical Winners Overview")
    
    tech_winners = {}
    for cat_name, df in technical_cats.items():
        winner_film = df.iloc[0]['film']
        if winner_film not in tech_winners:
            tech_winners[winner_film] = 0
        tech_winners[winner_film] += 1
    
    fig = go.Figure(data=[
        go.Bar(
            x=list(tech_winners.keys()),
            y=list(tech_winners.values()),
            marker_color='#FFD700',
            text=list(tech_winners.values()),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Predicted Technical Oscar Wins by Film",
        xaxis_title="Film",
        yaxis_title="Number of Predicted Wins",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Individual categories
    for cat_name, df in technical_cats.items():
        with st.expander(f"🏆 {cat_name}", expanded=False):
            winner = df.iloc[0]
            prob = winner['win_probability'] * 100
            
            st.markdown(f"**Predicted Winner:** {winner['nominee']} ({prob:.1f}%)")
            
            st.write("**Top 3:**")
            for idx, row in df.head(3).iterrows():
                st.progress(row['win_probability'])
                st.write(f"{idx+1}. {row['nominee']}: {row['win_probability']*100:.1f}%")
            
            if st.button(f"Explain", key=f"tech_{cat_name}"):
                reasons = get_category_explanation(cat_name, winner, df)
                for reason in reasons:
                    icon = "✅" if reason['type'] == 'positive' else ("❌" if reason['type'] == 'negative' else "⏳")
                    st.write(f"{icon} {reason['factor']}: {reason['detail']}")


# ==================== PAGE: MUSIC CATEGORIES ====================

elif page == "🎵 Music Categories":
    st.header("🎵 Music Category Predictions")
    
    music_cats = {
        'Best Original Score': all_predictions['Best Original Score'],
        'Best Original Song': all_predictions['Best Original Song']
    }
    
    for cat_name, df in music_cats.items():
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        
        winner = df.iloc[0]
        prob = winner['win_probability'] * 100
        
        st.markdown(f"""
        <div class="winner-box">
            🏆 {winner['nominee']}<br/>
            {prob:.1f}% probability
        </div>
        """, unsafe_allow_html=True)
        
        for idx, row in df.head(5).iterrows():
            st.progress(row['win_probability'])
            st.write(f"**{idx+1}. {row['nominee']}**: {row['win_probability']*100:.1f}%")
        
        st.markdown("---")


# ==================== PAGE: SPECIALTY CATEGORIES ====================

elif page == "🌍 Specialty Categories":
    st.header("🌍 Specialty Category Predictions")
    
    specialty_cats = {
        'Best Animated Feature': all_predictions['Best Animated Feature'],
        'Best International Feature': all_predictions['Best International Feature'],
        'Best Documentary Feature': all_predictions['Best Documentary Feature']
    }
    
    for cat_name, df in specialty_cats.items():
        st.markdown(f'<div class="category-header">{cat_name}</div>', unsafe_allow_html=True)
        
        winner = df.iloc[0]
        prob = winner['win_probability'] * 100
        
        st.markdown(f"""
        <div class="winner-box">
            🏆 {winner['nominee']}<br/>
            {prob:.1f}%
        </div>
        """, unsafe_allow_html=True)
        
        for idx, row in df.head(5).iterrows():
            st.progress(row['win_probability'])
            st.write(f"**{idx+1}. {row['nominee']}**: {row['win_probability']*100:.1f}%")
        
        if st.button(f"Explain", key=f"spec_{cat_name}"):
            reasons = get_category_explanation(cat_name, winner, df)
            for reason in reasons:
                icon = "✅" if reason['type'] == 'positive' else "⏳"
                st.write(f"{icon} {reason['factor']}: {reason['detail']}")
        
        st.markdown("---")


# ==================== PAGE: SCENARIO SIMULATOR ====================

elif page == "🔮 Scenario Simulator":
    st.header("🔮 SAG Award Scenario Simulator")
    
    st.write("**Simulate what happens if specific films win SAG Awards:**")
    
    # Best Picture SAG simulator
    st.subheader("🎬 Best Picture - SAG Outstanding Cast")
    
    bp_df = all_predictions['Best Picture']
    sag_winner_bp = st.selectbox("Who wins SAG Outstanding Cast?", bp_df['film'].tolist())
    
    if st.button("🔮 Simulate Best Picture", type="primary"):
        df_sim = bp_df.copy()
        
        mask = df_sim['film'] == sag_winner_bp
        df_sim.loc[mask, 'win_probability'] *= 2.0
        
        total = df_sim['win_probability'].sum()
        df_sim['win_probability'] = df_sim['win_probability'] / total
        
        df_sim = df_sim.sort_values('win_probability', ascending=False).reset_index(drop=True)
        
        st.success(f"✅ Simulated: {sag_winner_bp} wins SAG Outstanding Cast")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Current")
            for idx, row in bp_df.iterrows():
                st.write(f"{idx+1}. {row['film']}: {row['win_probability']*100:.1f}%")
        
        with col2:
            st.subheader("🔮 After SAG")
            for idx, row in df_sim.iterrows():
                change = "📈" if row['film'] == sag_winner_bp else ""
                st.write(f"{idx+1}. {row['film']}: {row['win_probability']*100:.1f}% {change}")
        
        # Chart
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Current', x=bp_df['film'], y=bp_df['win_probability']*100, marker_color='lightblue'))
        fig.add_trace(go.Bar(name='After SAG', x=df_sim['film'], y=df_sim['win_probability']*100, marker_color='gold'))
        
        fig.update_layout(title=f"Impact of {sag_winner_bp} Winning SAG", barmode='group', height=500)
        st.plotly_chart(fig, use_container_width=True)


# ==================== PAGE: PREDICTOR ANALYSIS ====================

elif page == "📈 Predictor Analysis":
    st.header("📈 Historical Predictor Analysis")
    
    st.subheader("🎯 Precursor Award Predictive Power")
    
    predictor_data = pd.DataFrame({
        'Award': ['SAG Outstanding Cast', 'BAFTA Best Film', 'GG Drama', 'GG Musical/Comedy'],
        'Overall (1994-2024)': [52.0, 60.0, 43.3, 22.2],
        'Recent (2015-2024)': [62.5, 60.0, 50.0, 20.0],
        'Last 5 Years': [80.0, 60.0, 60.0, 20.0]
    })
    
    fig = go.Figure()
    
    for col in ['Overall (1994-2024)', 'Recent (2015-2024)', 'Last 5 Years']:
        fig.add_trace(go.Bar(
            name=col,
            x=predictor_data['Award'],
            y=predictor_data[col]
        ))
    
    fig.update_layout(
        title="Precursor Award → Oscar Win Rate",
        yaxis_title="Win Rate (%)",
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### 📊 Key Insights:
    
    - **SAG is trending UP:** 80% accuracy in last 5 years!
    - **BAFTA remains most consistent:** 60% across all periods
    - **GG Drama stronger than Musical:** 43% vs 22%
    - **Precursor sweep = almost guaranteed:** 90% success rate
    """)


# ==================== PAGE: ABOUT MODEL ====================

elif page == "ℹ️ About Model":
    st.header("ℹ️ About the Prediction Model")
    
    st.markdown("""
    ### 🤖 Machine Learning Methodology
    
    **Algorithm:** Random Forest Classifier (200 decision trees)
    
    **Training Data:**
    - 30 years of Oscar history (1995-2024)
    - 211 Best Picture nominees
    - 24 categories analyzed
    
    ### 📊 Model Performance
    
    - **ROC-AUC:** 0.78
    - **Accuracy:** 73%
    - **2024 Validation:** ✅ Correctly predicted Oppenheimer
    
    ### 🎯 Features Used
    
    1. **Nomination Metrics (76%)**
    2. **Precursor Awards (24%)**
    3. **Historical Patterns**
    
    ### 📧 Created By
    
    **Athul C Joji**  
    MSc Data Science Portfolio Project  
    
    ---
    
    *All predictions based on historical data and statistical modeling.*
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 20px;">
    🎬 Oscar Predictions 2026 | All 24 Categories | Updated After BAFTA 2026
</div>
""", unsafe_allow_html=True)
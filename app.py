# ╔══════════════════════════════════════════════════════════════════════════╗
# ║              LaunchLens AI  —  Product Launch Intelligence              ║
# ║        UI preserved exactly. Backend fully dynamic. v2.0.0              ║
# ╚══════════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (unchanged from original)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LaunchLens AI | Product Launch Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS  (unchanged from original)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    div[data-testid="stSidebar"] { background-color: #0B0F19; }
    div[data-testid="stSidebar"] * { color: #F3F4F6 !important; }

    .hero-gradient {
        background: linear-gradient(135deg, #6EE7B7 0%, #3B82F6 50%, #8B5CF6 100%);
        padding: 3rem 2rem; border-radius: 16px; color: white; margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.3);
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 16px;
        padding: 1.5rem; margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
    }

    .metric-title  { font-size: 0.875rem; font-weight: 500; color: #6B7280; margin-bottom: 0.25rem; }
    .metric-value  { font-size: 1.75rem;  font-weight: 700; color: #111827; }
    .metric-delta  { font-size: 0.875rem; font-weight: 600; color: #10B981; }

    .badge-purple {
        background-color: #EEF2F6; color: #6366F1;
        padding: 0.25rem 0.75rem; border-radius: 9999px;
        font-size: 0.875rem; font-weight: 500; display: inline-block; margin: 2px;
    }
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# ░░  DYNAMIC BACKEND DATA LAYER  ░░
# ═════════════════════════════════════════════════════════════════════════════

# ── 1. Category configuration table ──────────────────────────────────────────
# CPM  = cost per 1000 impressions (₹)
# CTR  = click-through rate on engagement pool
# CVR  = conversion rate on clicks
# base_demand = starting demand score before modifiers
# price_sweet = the "ideal" price point for the category
CATEGORY_CFG = {
    "Health & Fitness":       {"cpm": 180, "ctr": 0.032, "cvr": 0.050, "base_demand": 82, "price_sweet": 999,  "mkt_pos": "Premium D2C Wellness"},
    "Tech & Gadgets":         {"cpm": 220, "ctr": 0.025, "cvr": 0.035, "base_demand": 78, "price_sweet": 4999, "mkt_pos": "Aspirational Consumer Tech"},
    "Beauty & Personal Care": {"cpm": 160, "ctr": 0.038, "cvr": 0.055, "base_demand": 85, "price_sweet": 699,  "mkt_pos": "Influencer-Led D2C Beauty"},
    "Lifestyle & Fashion":    {"cpm": 170, "ctr": 0.030, "cvr": 0.042, "base_demand": 75, "price_sweet": 1499, "mkt_pos": "Aspirational Urban Fashion"},
    "Food & Beverage":        {"cpm": 150, "ctr": 0.035, "cvr": 0.062, "base_demand": 80, "price_sweet": 499,  "mkt_pos": "Healthy Lifestyle FMCG"},
}

# ── 2. Creator master pool (category-keyed) ───────────────────────────────────
CREATOR_POOL = {
    "Health & Fitness": [
        {"Name": "RohitFit",            "Niche": "Fitness",    "Followers": 500_000, "Engagement": 7.5, "AudienceMatch": 94, "Authenticity": 92},
        {"Name": "Ananya Healthy Eats", "Niche": "Nutrition",  "Followers": 320_000, "Engagement": 6.8, "AudienceMatch": 89, "Authenticity": 95},
        {"Name": "FitWithPriya",        "Niche": "Fitness",    "Followers": 240_000, "Engagement": 8.1, "AudienceMatch": 96, "Authenticity": 91},
        {"Name": "GymBro Amit",         "Niche": "Fitness",    "Followers": 180_000, "Engagement": 9.4, "AudienceMatch": 98, "Authenticity": 94},
        {"Name": "Dietician Meera",     "Niche": "Nutrition",  "Followers": 150_000, "Engagement": 7.2, "AudienceMatch": 91, "Authenticity": 96},
        {"Name": "IronCore Vikas",      "Niche": "Fitness",    "Followers": 710_000, "Engagement": 6.2, "AudienceMatch": 92, "Authenticity": 85},
        {"Name": "Zest & Zeal Yoga",    "Niche": "Wellness",   "Followers": 280_000, "Engagement": 8.5, "AudienceMatch": 95, "Authenticity": 97},
        {"Name": "Mindful Nutritionist","Niche": "Nutrition",  "Followers": 190_000, "Engagement": 6.9, "AudienceMatch": 88, "Authenticity": 93},
        {"Name": "Daily Grind Fitness", "Niche": "Fitness",    "Followers": 360_000, "Engagement": 7.9, "AudienceMatch": 93, "Authenticity": 90},
        {"Name": "Chef Rahul Organic",  "Niche": "Nutrition",  "Followers": 410_000, "Engagement": 5.9, "AudienceMatch": 85, "Authenticity": 87},
        {"Name": "Lifestyle Sneha",     "Niche": "Lifestyle",  "Followers": 620_000, "Engagement": 5.1, "AudienceMatch": 72, "Authenticity": 89},
        {"Name": "Kavya Vlogs",         "Niche": "Lifestyle",  "Followers": 950_000, "Engagement": 3.8, "AudienceMatch": 60, "Authenticity": 82},
        {"Name": "The Wandering Soul",  "Niche": "Travel",     "Followers": 530_000, "Engagement": 4.6, "AudienceMatch": 45, "Authenticity": 90},
        {"Name": "BeautyByBhumika",     "Niche": "Beauty",     "Followers": 440_000, "Engagement": 5.5, "AudienceMatch": 52, "Authenticity": 88},
        {"Name": "TechVibe Kush",       "Niche": "Tech",       "Followers": 850_000, "Engagement": 4.2, "AudienceMatch": 35, "Authenticity": 88},
    ],
    "Tech & Gadgets": [
        {"Name": "TechVibe Kush",       "Niche": "Tech Reviews",   "Followers": 850_000, "Engagement": 4.2, "AudienceMatch": 96, "Authenticity": 88},
        {"Name": "GadgetGuru Raj",      "Niche": "Gadgets",        "Followers": 620_000, "Engagement": 5.8, "AudienceMatch": 93, "Authenticity": 91},
        {"Name": "UnboxIndia Nikhil",   "Niche": "Tech Reviews",   "Followers": 430_000, "Engagement": 6.5, "AudienceMatch": 90, "Authenticity": 90},
        {"Name": "ByteSized Arjun",     "Niche": "Tech",           "Followers": 190_000, "Engagement": 8.3, "AudienceMatch": 88, "Authenticity": 95},
        {"Name": "DevDiaries Aisha",    "Niche": "Coding/Tech",    "Followers": 150_000, "Engagement": 9.0, "AudienceMatch": 85, "Authenticity": 96},
        {"Name": "SmartHome Varun",     "Niche": "Gadgets",        "Followers": 340_000, "Engagement": 6.0, "AudienceMatch": 82, "Authenticity": 87},
        {"Name": "ReviewRacer Samir",   "Niche": "Tech Reviews",   "Followers": 510_000, "Engagement": 5.2, "AudienceMatch": 91, "Authenticity": 86},
        {"Name": "DigitalNomad Rahul",  "Niche": "Productivity",   "Followers": 390_000, "Engagement": 4.9, "AudienceMatch": 78, "Authenticity": 84},
        {"Name": "CodeWithPriya",       "Niche": "Tech",           "Followers": 280_000, "Engagement": 7.1, "AudienceMatch": 86, "Authenticity": 93},
        {"Name": "Gizmo Queen Tara",    "Niche": "Gadgets",        "Followers": 260_000, "Engagement": 7.4, "AudienceMatch": 83, "Authenticity": 89},
        {"Name": "Lifestyle Sneha",     "Niche": "Lifestyle",      "Followers": 620_000, "Engagement": 5.1, "AudienceMatch": 55, "Authenticity": 89},
        {"Name": "TrendTracker Dia",    "Niche": "Lifestyle",      "Followers": 480_000, "Engagement": 5.5, "AudienceMatch": 60, "Authenticity": 85},
        {"Name": "RohitFit",            "Niche": "Fitness",        "Followers": 500_000, "Engagement": 7.5, "AudienceMatch": 40, "Authenticity": 92},
        {"Name": "Kavya Vlogs",         "Niche": "Lifestyle",      "Followers": 950_000, "Engagement": 3.8, "AudienceMatch": 50, "Authenticity": 82},
        {"Name": "The Wandering Soul",  "Niche": "Travel",         "Followers": 530_000, "Engagement": 4.6, "AudienceMatch": 48, "Authenticity": 90},
    ],
    "Beauty & Personal Care": [
        {"Name": "BeautyByBhumika",     "Niche": "Beauty",         "Followers": 440_000, "Engagement": 5.5, "AudienceMatch": 96, "Authenticity": 88},
        {"Name": "GlowUp Riya",         "Niche": "Skincare",       "Followers": 380_000, "Engagement": 7.2, "AudienceMatch": 95, "Authenticity": 92},
        {"Name": "MakeupMaven Sia",     "Niche": "Makeup",         "Followers": 590_000, "Engagement": 6.1, "AudienceMatch": 92, "Authenticity": 90},
        {"Name": "SkinFirst Ananya",    "Niche": "Skincare",       "Followers": 270_000, "Engagement": 8.4, "AudienceMatch": 94, "Authenticity": 95},
        {"Name": "Clean Beauty Pooja",  "Niche": "Beauty",         "Followers": 210_000, "Engagement": 7.8, "AudienceMatch": 93, "Authenticity": 97},
        {"Name": "TrendyTresses Kajal", "Niche": "Haircare",       "Followers": 310_000, "Engagement": 6.7, "AudienceMatch": 88, "Authenticity": 91},
        {"Name": "WellnessGlow Neha",   "Niche": "Wellness",       "Followers": 160_000, "Engagement": 9.1, "AudienceMatch": 87, "Authenticity": 94},
        {"Name": "DermaDiva Priti",     "Niche": "Skincare",       "Followers": 120_000, "Engagement": 9.5, "AudienceMatch": 91, "Authenticity": 96},
        {"Name": "OolaGlow Kezia",      "Niche": "Beauty",         "Followers": 480_000, "Engagement": 5.3, "AudienceMatch": 85, "Authenticity": 86},
        {"Name": "EcoBeauty Shriya",    "Niche": "Sustainable",    "Followers": 200_000, "Engagement": 8.0, "AudienceMatch": 83, "Authenticity": 98},
        {"Name": "Lifestyle Sneha",     "Niche": "Lifestyle",      "Followers": 620_000, "Engagement": 5.1, "AudienceMatch": 70, "Authenticity": 89},
        {"Name": "Kavya Vlogs",         "Niche": "Lifestyle",      "Followers": 950_000, "Engagement": 3.8, "AudienceMatch": 62, "Authenticity": 82},
        {"Name": "FitWithPriya",        "Niche": "Fitness",        "Followers": 240_000, "Engagement": 8.1, "AudienceMatch": 55, "Authenticity": 91},
        {"Name": "Ananya Healthy Eats", "Niche": "Nutrition",      "Followers": 320_000, "Engagement": 6.8, "AudienceMatch": 52, "Authenticity": 95},
        {"Name": "The Wandering Soul",  "Niche": "Travel",         "Followers": 530_000, "Engagement": 4.6, "AudienceMatch": 48, "Authenticity": 90},
    ],
    "Lifestyle & Fashion": [
        {"Name": "Lifestyle Sneha",     "Niche": "Lifestyle",      "Followers": 620_000, "Engagement": 5.1, "AudienceMatch": 97, "Authenticity": 89},
        {"Name": "Kavya Vlogs",         "Niche": "Lifestyle",      "Followers": 950_000, "Engagement": 3.8, "AudienceMatch": 92, "Authenticity": 82},
        {"Name": "Fashion Fwd Maya",    "Niche": "Fashion",        "Followers": 750_000, "Engagement": 4.8, "AudienceMatch": 95, "Authenticity": 85},
        {"Name": "StyleSutra Aditi",    "Niche": "Fashion",        "Followers": 430_000, "Engagement": 6.3, "AudienceMatch": 93, "Authenticity": 91},
        {"Name": "UrbanChic Priya",     "Niche": "Fashion",        "Followers": 310_000, "Engagement": 7.0, "AudienceMatch": 90, "Authenticity": 90},
        {"Name": "OOTDByDivya",         "Niche": "Fashion",        "Followers": 280_000, "Engagement": 7.5, "AudienceMatch": 88, "Authenticity": 93},
        {"Name": "TravelChic Mia",      "Niche": "Travel+Fashion", "Followers": 390_000, "Engagement": 5.8, "AudienceMatch": 85, "Authenticity": 88},
        {"Name": "BohoBabe Isha",       "Niche": "Lifestyle",      "Followers": 170_000, "Engagement": 8.8, "AudienceMatch": 87, "Authenticity": 95},
        {"Name": "MensStyle Rohan",     "Niche": "Men's Fashion",  "Followers": 260_000, "Engagement": 6.9, "AudienceMatch": 83, "Authenticity": 87},
        {"Name": "LuxeLife Roshni",     "Niche": "Luxury",         "Followers": 520_000, "Engagement": 4.5, "AudienceMatch": 79, "Authenticity": 84},
        {"Name": "TrendTracker Dia",    "Niche": "Trends",         "Followers": 480_000, "Engagement": 5.5, "AudienceMatch": 89, "Authenticity": 85},
        {"Name": "DailyDrip Meena",     "Niche": "Lifestyle",      "Followers": 220_000, "Engagement": 7.8, "AudienceMatch": 92, "Authenticity": 92},
        {"Name": "BeautyByBhumika",     "Niche": "Beauty",         "Followers": 440_000, "Engagement": 5.5, "AudienceMatch": 68, "Authenticity": 88},
        {"Name": "The Wandering Soul",  "Niche": "Travel",         "Followers": 530_000, "Engagement": 4.6, "AudienceMatch": 65, "Authenticity": 90},
        {"Name": "GlowUp Riya",         "Niche": "Skincare",       "Followers": 380_000, "Engagement": 7.2, "AudienceMatch": 62, "Authenticity": 92},
    ],
    "Food & Beverage": [
        {"Name": "Chef Rahul Organic",  "Niche": "Food",           "Followers": 410_000, "Engagement": 5.9, "AudienceMatch": 97, "Authenticity": 87},
        {"Name": "Ananya Healthy Eats", "Niche": "Nutrition",      "Followers": 320_000, "Engagement": 6.8, "AudienceMatch": 94, "Authenticity": 95},
        {"Name": "YumYum Priya",        "Niche": "Food",           "Followers": 580_000, "Engagement": 5.4, "AudienceMatch": 93, "Authenticity": 88},
        {"Name": "HomeChef Sangeeta",   "Niche": "Food",           "Followers": 260_000, "Engagement": 7.6, "AudienceMatch": 91, "Authenticity": 94},
        {"Name": "VeggieVibe Pooja",    "Niche": "Vegan Food",     "Followers": 200_000, "Engagement": 8.2, "AudienceMatch": 92, "Authenticity": 96},
        {"Name": "BiteSize Rahul",      "Niche": "Food Reviews",   "Followers": 310_000, "Engagement": 7.0, "AudienceMatch": 90, "Authenticity": 89},
        {"Name": "MasalaMagic Deepa",   "Niche": "Indian Cuisine", "Followers": 350_000, "Engagement": 6.5, "AudienceMatch": 89, "Authenticity": 92},
        {"Name": "HealthyPlate Nisha",  "Niche": "Nutrition",      "Followers": 170_000, "Engagement": 8.7, "AudienceMatch": 95, "Authenticity": 97},
        {"Name": "GourmetGuru Amit",    "Niche": "Food",           "Followers": 490_000, "Engagement": 5.1, "AudienceMatch": 86, "Authenticity": 86},
        {"Name": "FoodieFoot Karan",    "Niche": "Food Travel",    "Followers": 440_000, "Engagement": 6.0, "AudienceMatch": 88, "Authenticity": 90},
        {"Name": "SnackAttack Dev",     "Niche": "Snacks",         "Followers": 230_000, "Engagement": 7.3, "AudienceMatch": 83, "Authenticity": 88},
        {"Name": "Lifestyle Sneha",     "Niche": "Lifestyle",      "Followers": 620_000, "Engagement": 5.1, "AudienceMatch": 70, "Authenticity": 89},
        {"Name": "Kavya Vlogs",         "Niche": "Lifestyle",      "Followers": 950_000, "Engagement": 3.8, "AudienceMatch": 62, "Authenticity": 82},
        {"Name": "FitWithPriya",        "Niche": "Fitness",        "Followers": 240_000, "Engagement": 8.1, "AudienceMatch": 58, "Authenticity": 91},
        {"Name": "The Wandering Soul",  "Niche": "Travel",         "Followers": 530_000, "Engagement": 4.6, "AudienceMatch": 50, "Authenticity": 90},
    ],
}

# ── 3. Persona database (category-keyed, 3 per category) ─────────────────────
PERSONAS = {
    "Health & Fitness": [
        {
            "tab": "Primary Target", "segment": "Active Fitness Enthusiasts",
            "name": "Riya S.", "age": 24, "occ": "Software Engineer",
            "interests": "Gym, Health Reels, Nutrition Tracking",
            "intent": "High", "intent_score": 88,
            "color": "#f3e8ff",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [38,44,14,4],
            "driver1": "Ages 18-35 in Tier 1 & Tier 2 urban centres.",
            "driver2": "Verified formulation transparency and convenient ecosystem compatibility features.",
        },
        {
            "tab": "Secondary Target", "segment": "Busy Corporate Professionals",
            "name": "Armaan K.", "age": 31, "occ": "Product Consultant",
            "interests": "Quick Nutrition, Corporate Wellness, Biohacking",
            "intent": "Medium-High", "intent_score": 72,
            "color": "#e0f2fe",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [10,50,32,8],
            "driver1": "Ages 28-45 busy management professionals.",
            "driver2": "High execution convenience, meal substitution features, and stress optimization.",
        },
        {
            "tab": "Tertiary Target", "segment": "Holistic Wellness Practitioners",
            "name": "Dr. Meera V.", "age": 39, "occ": "Functional Medicine Practitioner",
            "interests": "Preventive Healthcare, Plant-Based Diets, Longevity",
            "intent": "Medium", "intent_score": 55,
            "color": "#ecfdf5",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [5,25,45,25],
            "driver1": "Clean labels, organic-centric lifestyle adapters, health-conscious profiles.",
            "driver2": "High clinical focus, clear verification structures, pure sourcing authenticity.",
        },
    ],
    "Tech & Gadgets": [
        {
            "tab": "Primary Target", "segment": "Early Adopters & Tech Enthusiasts",
            "name": "Aditya R.", "age": 27, "occ": "Backend Developer",
            "interests": "PC Building, AI Tools, Gadget Reviews",
            "intent": "High", "intent_score": 90,
            "color": "#e0f2fe",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [30,48,18,4],
            "driver1": "Ages 22-35 urban tech-forward professionals and students.",
            "driver2": "Performance benchmarks, feature depth, and peer review validation.",
        },
        {
            "tab": "Secondary Target", "segment": "WFH Productivity Seekers",
            "name": "Shreya M.", "age": 32, "occ": "UX Designer",
            "interests": "Productivity Apps, Smart Devices, Remote Setup",
            "intent": "Medium-High", "intent_score": 74,
            "color": "#f3e8ff",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [12,46,34,8],
            "driver1": "Work-from-home professionals seeking efficiency upgrades.",
            "driver2": "Ease of integration, ecosystem compatibility, and time-saving ROI.",
        },
        {
            "tab": "Tertiary Target", "segment": "Budget-Conscious Upgraders",
            "name": "Mohit T.", "age": 21, "occ": "College Student",
            "interests": "Value Tech, YouTube Reviews, Deal Hunting",
            "intent": "Medium", "intent_score": 58,
            "color": "#fef3c7",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [55,35,8,2],
            "driver1": "Price-sensitive first-time buyers in Tier 2/3 cities.",
            "driver2": "Value-for-money ratio, warranty assurance, and influencer trust signals.",
        },
    ],
    "Beauty & Personal Care": [
        {
            "tab": "Primary Target", "segment": "Skincare-First Millennials",
            "name": "Tanya G.", "age": 26, "occ": "Marketing Executive",
            "interests": "Skincare Routines, Clean Beauty, GRWM Reels",
            "intent": "High", "intent_score": 91,
            "color": "#fce7f3",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [35,46,15,4],
            "driver1": "Ages 20-35 urban women with skincare-first purchasing mindset.",
            "driver2": "Ingredient transparency, dermatologist endorsement, and before/after content.",
        },
        {
            "tab": "Secondary Target", "segment": "Trend-Driven Gen Z Shoppers",
            "name": "Kiran P.", "age": 21, "occ": "College Student",
            "interests": "Makeup Trends, Viral Products, Instagram Reels",
            "intent": "High", "intent_score": 85,
            "color": "#f3e8ff",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [50,40,8,2],
            "driver1": "Influencer-driven Gen Z shoppers chasing viral beauty trends.",
            "driver2": "Social proof, limited editions, aesthetic packaging, and creator endorsements.",
        },
        {
            "tab": "Tertiary Target", "segment": "Wellness-Oriented Consumers",
            "name": "Priya N.", "age": 35, "occ": "HR Manager",
            "interests": "Natural Ingredients, Self-Care Rituals, Ayurveda",
            "intent": "Medium", "intent_score": 60,
            "color": "#ecfdf5",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [10,35,42,13],
            "driver1": "Natural and organic seekers prioritising holistic self-care.",
            "driver2": "Cruelty-free certifications, botanical sourcing, and long-term skin health.",
        },
    ],
    "Lifestyle & Fashion": [
        {
            "tab": "Primary Target", "segment": "Urban Fashion Enthusiasts",
            "name": "Naina B.", "age": 25, "occ": "Content Creator",
            "interests": "OOTDs, Street Style, Seasonal Trends",
            "intent": "High", "intent_score": 89,
            "color": "#fef3c7",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [40,44,13,3],
            "driver1": "Ages 18-32 metro-dwelling fashion-forward content consumers.",
            "driver2": "Trend velocity, brand storytelling, and influencer social proof.",
        },
        {
            "tab": "Secondary Target", "segment": "Aspirational Mid-Income Shoppers",
            "name": "Rohan S.", "age": 29, "occ": "Sales Manager",
            "interests": "Brand Value, Style Upgrades, Weekend Fashion",
            "intent": "Medium-High", "intent_score": 71,
            "color": "#e0f2fe",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [18,52,25,5],
            "driver1": "Upwardly mobile professionals seeking quality without overspending.",
            "driver2": "Brand perception, durability, and occasion-readiness of the product.",
        },
        {
            "tab": "Tertiary Target", "segment": "Sustainable Fashion Advocates",
            "name": "Zara K.", "age": 33, "occ": "NGO Program Manager",
            "interests": "Slow Fashion, Ethical Brands, Capsule Wardrobes",
            "intent": "Medium", "intent_score": 54,
            "color": "#ecfdf5",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [15,40,35,10],
            "driver1": "Purpose-driven consumers who prioritise ethics over fast fashion cycles.",
            "driver2": "Supply chain transparency, carbon footprint, and certified sustainable materials.",
        },
    ],
    "Food & Beverage": [
        {
            "tab": "Primary Target", "segment": "Health-Conscious Home Cooks",
            "name": "Sunita R.", "age": 30, "occ": "School Teacher",
            "interests": "Clean Eating, Meal Prep, Nutrition Labels",
            "intent": "High", "intent_score": 87,
            "color": "#fef3c7",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [20,42,30,8],
            "driver1": "Ages 25-45 household decision-makers focused on family nutrition.",
            "driver2": "Ingredient quality, health claims, price-per-serving value.",
        },
        {
            "tab": "Secondary Target", "segment": "Foodie Explorers",
            "name": "Karthik M.", "age": 26, "occ": "Graphic Designer",
            "interests": "Cuisine Discovery, Café Hopping, Food Reels",
            "intent": "High", "intent_score": 82,
            "color": "#e0f2fe",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [35,48,13,4],
            "driver1": "Urban taste explorers driven by discovery and novelty.",
            "driver2": "Unique flavour profiles, brand story, and influencer unboxing content.",
        },
        {
            "tab": "Tertiary Target", "segment": "Convenience-First Shoppers",
            "name": "Leena D.", "age": 38, "occ": "Working Mother",
            "interests": "Quick Meal Solutions, Healthy Packaged Food",
            "intent": "Medium", "intent_score": 62,
            "color": "#ecfdf5",
            "demo_ages": ["18-24","25-34","35-44","45+"], "demo_vals": [8,28,46,18],
            "driver1": "Time-poor urban parents prioritising convenience + nutrition.",
            "driver2": "Ease of preparation, shelf life, and trusted health certifications.",
        },
    ],
}

# ── 4. Recommendations database ───────────────────────────────────────────────
RECOMMENDATIONS = {
    "Health & Fitness": {
        "formats": [
            ("Instagram Reels", 60, "Highest retention for transformation & product demos."),
            ("YouTube Shorts",  30, "Long-tail discovery and deep-dive nutrition content."),
            ("Instagram Stories",10, "Flash sales and swipe-up conversion funnels."),
        ],
        "time": "17:00 – 21:00 IST",
        "duration": "45 Days",
        "cadence": "Top-of-funnel awareness → mid-funnel engagement → conversion retargeting.",
        "split": [("Tier-1 Macro Creators", 40), ("Micro Community Creators", 40), ("Performance Retargeting Ads", 20)],
    },
    "Tech & Gadgets": {
        "formats": [
            ("YouTube Long-Form Reviews", 50, "Benchmark-driven purchase decisions require depth."),
            ("Instagram Reels",           30, "Viral unboxing and feature highlight clips."),
            ("Twitter / X Threads",       20, "Tech community trust-building and early adopters."),
        ],
        "time": "19:00 – 23:00 IST",
        "duration": "30 Days",
        "cadence": "Launch hype → review wave → deal-close retargeting.",
        "split": [("YouTube Creators", 50), ("Tech Blog Sponsorships", 30), ("Display & Search Ads", 20)],
    },
    "Beauty & Personal Care": {
        "formats": [
            ("Instagram Reels & TikTok", 55, "GRWM and skincare routine content drives virality."),
            ("YouTube Tutorials",        30, "Deep dives build product trust and loyalty."),
            ("Pinterest Boards",         15, "High purchase intent discovery platform."),
        ],
        "time": "18:00 – 22:00 IST",
        "duration": "60 Days",
        "cadence": "Seeding → organic buzz → paid amplification → loyalty loop.",
        "split": [("Nano & Micro Influencers", 50), ("Macro Beauty Creators", 30), ("Paid Social Ads", 20)],
    },
    "Lifestyle & Fashion": {
        "formats": [
            ("Instagram Posts & Reels", 60, "Visual storytelling is the primary purchase driver."),
            ("YouTube Lifestyle Vlogs",  25, "Aspirational day-in-the-life format for brand immersion."),
            ("Instagram Stories",        15, "Limited-time offers and poll-based engagement."),
        ],
        "time": "12:00 – 14:00 & 20:00 – 22:00 IST",
        "duration": "45 Days",
        "cadence": "Trend seeding → influencer drops → urgency retargeting.",
        "split": [("Fashion Macro Influencers", 45), ("Micro Style Creators", 35), ("Retargeting Ads", 20)],
    },
    "Food & Beverage": {
        "formats": [
            ("Instagram Reels",    50, "Recipe demos and taste-test content drive impulse buys."),
            ("YouTube Shorts",     30, "Quick recipe clips with product integration."),
            ("Facebook Video Ads", 20, "Reaches older household decision-makers effectively."),
        ],
        "time": "11:00 – 13:00 & 18:00 – 20:00 IST",
        "duration": "30 Days",
        "cadence": "Awareness → recipe discovery → coupon-driven conversion.",
        "split": [("Food & Recipe Creators", 45), ("Micro Health Influencers", 35), ("Search & Display Ads", 20)],
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# ░░  ENGINE FUNCTIONS  ░░
# ═════════════════════════════════════════════════════════════════════════════

def calculate_demand_score(category: str, price: float, description: str) -> int:
    """Dynamic demand score based on category baseline, price positioning, and keyword signals."""
    cfg   = CATEGORY_CFG[category]
    base  = cfg["base_demand"]

    # Price modifier: score highest when price == sweet-spot; penalise large deviations
    ratio = price / cfg["price_sweet"]
    if ratio <= 1.0:
        price_mod = 8 * ratio          # under sweet-spot → ramp up
    else:
        price_mod = 8 / ratio          # over sweet-spot → diminishing returns

    # Description keyword boost (max +10)
    power_words = [
        "organic","premium","ai","smart","sustainable","innovative","natural",
        "pro","advanced","eco","plant-based","clinically","certified","award",
        "patented","cruelty-free","vegan","wireless","fast","ultra",
    ]
    desc_lower  = description.lower()
    kw_score    = sum(2 for w in power_words if w in desc_lower)
    desc_mod    = min(kw_score, 10)

    return min(int(base + price_mod + desc_mod), 100)


def get_creators(category: str) -> pd.DataFrame:
    """Return scored & ranked creator DataFrame for the given category."""
    pool = CREATOR_POOL.get(category, CREATOR_POOL["Health & Fitness"])
    df   = pd.DataFrame(pool)
    # Compatibility Score = weighted sum of four signals
    df["CompatibilityScore"] = (
        df["AudienceMatch"] * 0.40 +
        df["Engagement"]    * 3.50 +
        df["Authenticity"]  * 0.25 +
        df["AudienceMatch"] * 0.05   # niche relevance proxy
    ).clip(upper=100).round(1)
    return df.sort_values("CompatibilityScore", ascending=False).reset_index(drop=True)


def predict_campaign(budget: float, price: float, category: str) -> dict:
    """
    CPM → Impressions → Reach → Engagements → Clicks → Conversions → Revenue → ROI
    All rates are category-specific.
    """
    cfg         = CATEGORY_CFG[category]
    impressions = int((budget / cfg["cpm"]) * 1000)
    reach       = int(impressions * 0.72)              # ~72 % unique reach
    engagements = int(impressions * cfg["ctr"])
    clicks      = int(engagements * 0.35)              # 35 % of engaged users click
    conversions = int(clicks * cfg["cvr"])
    revenue     = conversions * price
    roi         = round(((revenue - budget) / budget) * 100, 1) if budget else 0
    return {
        "impressions": impressions, "reach": reach, "engagements": engagements,
        "clicks": clicks, "conversions": conversions, "revenue": revenue, "roi": roi,
    }


def generate_personas(category: str) -> list:
    return PERSONAS.get(category, PERSONAS["Health & Fitness"])


def generate_recommendations(category: str) -> dict:
    return RECOMMENDATIONS.get(category, RECOMMENDATIONS["Health & Fitness"])


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: glass-card metric block
# ─────────────────────────────────────────────────────────────────────────────
def metric_card(title, value, delta="", delta_color="#10B981"):
    return (
        f"<div class='glass-card'>"
        f"<div class='metric-title'>{title}</div>"
        f"<div class='metric-value'>{value}</div>"
        f"<div class='metric-delta' style='color:{delta_color};'>{delta}</div>"
        f"</div>"
    )


# ═════════════════════════════════════════════════════════════════════════════
# ░░  SESSION STATE  ░░
# ═════════════════════════════════════════════════════════════════════════════
DEFAULTS = {
    "product_analyzed": False,
    "prod_name":        "Organic Protein Shake",
    "prod_cat":         "Health & Fitness",
    "prod_desc":        "Plant-based protein supplement designed for fitness enthusiasts and healthy lifestyle consumers.",
    "prod_price":       999,
    "campaign_budget":  100_000,
    "demand_score":     0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ═════════════════════════════════════════════════════════════════════════════
# ░░  PRE-COMPUTE LIVE METRICS  ░░  (used across pages)
# ═════════════════════════════════════════════════════════════════════════════
cat          = st.session_state.prod_cat
df_creators  = get_creators(cat)
camp         = predict_campaign(st.session_state.campaign_budget, st.session_state.prod_price, cat)
personas     = generate_personas(cat)
demand       = (st.session_state.demand_score if st.session_state.product_analyzed
                else calculate_demand_score(cat, st.session_state.prod_price, st.session_state.prod_desc))
aud_conf     = round(df_creators["AudienceMatch"].head(5).mean(), 1)
cr_match     = round(df_creators["CompatibilityScore"].head(3).mean(), 1)
roi_val      = camp["roi"]


# ═════════════════════════════════════════════════════════════════════════════
# ░░  SIDEBAR  (unchanged from original)  ░░
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<h2 style='color:#F3F4F6; margin-bottom:0;'>✨ LaunchLens AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9CA3AF; font-size:0.85rem; margin-bottom:2rem;'>Launch Intelligence Platform</p>", unsafe_allow_html=True)

    app_mode = st.radio(
        "Navigation",
        ["Dashboard", "Product Analysis", "Audience Discovery",
         "Creator Matching", "Campaign Intelligence", "Insights Report"]
    )

    st.markdown("---")
    st.markdown("<div style='font-size:0.75rem; color:#6B7280;'>Investor Demo Engine v2.0.0</div>", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
if app_mode == "Dashboard":
    st.markdown("""
    <div class='hero-gradient'>
        <h1 style='margin:0; font-size:2.5rem; font-weight:700;'>LaunchLens AI</h1>
        <p style='margin:0.5rem 0 0 0; font-size:1.1rem; opacity:0.9;'>
            Launch smarter. Reach the right audience. Partner with the right creators.
        </p>
    </div>""", unsafe_allow_html=True)

    # — Dynamic KPI cards —
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card(
            "Audience Confidence", f"{aud_conf}%",
            f"↑ Top-5 creator avg match · {cat}"
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card(
            "Creator Match Index", f"{cr_match}/100",
            "↑ Weighted compatibility score"
        ), unsafe_allow_html=True)
    with c3:
        reach_label = f"{camp['reach']/1e6:.1f}M" if camp['reach'] >= 1_000_000 else f"{camp['reach']:,}"
        st.markdown(metric_card(
            "Predicted Gross Reach", reach_label,
            f"Budget ₹{st.session_state.campaign_budget:,}"
        ), unsafe_allow_html=True)
    with c4:
        roi_col = "#10B981" if roi_val > 0 else "#EF4444"
        st.markdown(metric_card(
            "Estimated ROI", f"{roi_val}%",
            "↑ Campaign forecast", delta_color=roi_col
        ), unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)
    with ch1:
        st.markdown("### 📊 Target Audience Demographics")
        fig_pie = px.pie(
            names=[p["segment"] for p in personas],
            values=[50, 30, 20],
            color_discrete_sequence=px.colors.sequential.Plasma_r,
            hole=0.4
        )
        fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig_pie, use_container_width=True)

    with ch2:
        st.markdown("### 📈 Engagement Forecast Trend")
        months = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6']
        base_rate = CATEGORY_CFG[cat]["ctr"] * 100
        eng_rates = [round(base_rate * f, 2) for f in [0.58, 0.72, 0.88, 0.93, 1.02, 1.10]]
        fig_line  = px.line(x=months, y=eng_rates, markers=True,
                            labels={'x': 'Timeline', 'y': 'Engagement Rate (%)'})
        fig_line.update_traces(line_color='#6366F1', line_width=3)
        fig_line.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig_line, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "Product Analysis":
    st.markdown("## 🔍 Product Analysis Engine")
    st.markdown("Submit your product parameters to initialize target scoring and structural layout maps.")

    col_f, col_v = st.columns([1, 1])

    with col_f:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        form_name  = st.text_input("Product Name",        value=st.session_state.prod_name)
        form_cat   = st.selectbox("Product Category",
                                  list(CATEGORY_CFG.keys()),
                                  index=list(CATEGORY_CFG.keys()).index(st.session_state.prod_cat))
        form_desc  = st.text_area("Product Description",  value=st.session_state.prod_desc)
        form_price = st.number_input("Product Price (₹)", min_value=1, value=st.session_state.prod_price)
        st.file_uploader("Product Image Upload (Optional)", type=["png", "jpg", "jpeg"])

        if st.button("Analyze Product", type="primary"):
            st.session_state.prod_name  = form_name
            st.session_state.prod_cat   = form_cat
            st.session_state.prod_desc  = form_desc
            st.session_state.prod_price = form_price
            with st.spinner("Running core AI vectors and market tracking profiles..."):
                time.sleep(1.5)
            st.session_state.demand_score    = calculate_demand_score(form_cat, form_price, form_desc)
            st.session_state.product_analyzed = True
            st.success("Analysis Complete!")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_v:
        if st.session_state.product_analyzed:
            ds  = st.session_state.demand_score
            cfg = CATEGORY_CFG[st.session_state.prod_cat]

            # Market position label
            ratio   = st.session_state.prod_price / cfg["price_sweet"]
            mkt_pos = cfg["mkt_pos"]
            if ratio > 1.4:
                mkt_pos = "Ultra-Premium Niche"
            elif ratio < 0.6:
                mkt_pos = "Value / Entry-Level"

            # Launch potential
            if ds >= 82:
                potential = "🚀 High — Strong launch viability"
            elif ds >= 65:
                potential = "⚡ Medium — Good fundamentals, refine positioning"
            else:
                potential = "🔍 Developing — Revisit pricing or category fit"

            # Key benefits — inferred from category
            benefits_map = {
                "Health & Fitness":       ["High repeat-purchase behaviour", "Clean label & ingredient transparency", "Community-driven virality"],
                "Tech & Gadgets":         ["Early-adopter demand signal", "Review-driven organic discovery", "High shareability & gifting potential"],
                "Beauty & Personal Care": ["Visual product appeal for UGC", "Tutorial-friendly content format", "High brand loyalty ceiling"],
                "Lifestyle & Fashion":    ["Trend-forward seasonal relevance", "Gifting & occasion-ready positioning", "Aspirational brand storytelling"],
                "Food & Beverage":        ["Impulse-buy friendly price point", "Strong word-of-mouth mechanics", "Recipe & content integration ready"],
            }
            benefits = benefits_map.get(st.session_state.prod_cat, [])

            st.markdown(f"### Matrix Profile: {st.session_state.prod_name}")
            st.markdown(f"""
            <div class='glass-card'>
                <h4>Product Summary</h4>
                <p>{st.session_state.prod_desc}</p>
                <span class='badge-purple'>Category: {st.session_state.prod_cat}</span>
                <span class='badge-purple'>Price Structural Index: ₹{st.session_state.prod_price}</span>
            </div>""", unsafe_allow_html=True)

            c_a, c_b = st.columns(2)
            with c_a:
                b_html = "".join(f"<li>{b}</li>" for b in benefits)
                st.markdown(f"""
                <div class='glass-card'>
                    <h5>Key Benefits Identified</h5>
                    <ul>{b_html}</ul>
                </div>""", unsafe_allow_html=True)
            with c_b:
                bar_color = "#10B981" if ds >= 80 else ("#F59E0B" if ds >= 65 else "#EF4444")
                st.markdown(f"""
                <div class='glass-card'>
                    <h5>Market Position</h5>
                    <p>{mkt_pos}</p>
                    <h5>Demand Score</h5>
                    <h2 style='color:{bar_color};'>{ds} / 100</h2>
                    <h5>Launch Potential</h5>
                    <p>{potential}</p>
                </div>""", unsafe_allow_html=True)

            st.markdown("👉 Proceed to **Audience Discovery** in the navigation bar to evaluate specific user personas.")
        else:
            st.info("Complete the product submission details on the left side and choose 'Analyze Product' to view performance analysis.")


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 3 — AUDIENCE DISCOVERY
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "Audience Discovery":
    st.markdown("## 👥 AI Audience Discovery Engine")
    st.markdown(f"Automated customer alignment mapping configured for **{st.session_state.prod_name}**.")

    personas = generate_personas(cat)
    t1, t2, t3 = st.tabs([p["tab"] for p in personas])

    for tab_obj, p in zip([t1, t2, t3], personas):
        with tab_obj:
            st.markdown(f"### Profile: {p['segment']}")
            cx1, cx2 = st.columns([1, 2])
            with cx1:
                intent_color = "#10B981" if p["intent"] == "High" else ("#F59E0B" if "Medium" in p["intent"] else "#6B7280")
                st.markdown(f"""
                <div class='glass-card' style='background: linear-gradient(135deg, #ffffff 0%, {p["color"]} 100%);'>
                    <h4>Persona: {p["name"]}</h4>
                    <p><b>Age:</b> {p["age"]}</p>
                    <p><b>Occupation:</b> {p["occ"]}</p>
                    <p><b>Interests:</b> {p["interests"]}</p>
                    <p><b>Buying Intent:</b> <span style='color:{intent_color}; font-weight:700;'>{p["intent"]}</span></p>
                    <p><b>Intent Score:</b> {p["intent_score"]}/100</p>
                </div>""", unsafe_allow_html=True)
            with cx2:
                st.markdown("#### Segment Strategy Drivers")
                st.markdown(f"* **Core Target Demographics:** {p['driver1']}")
                st.markdown(f"* **Buying Propensity Indices:** {p['driver2']}")
                # Age distribution bar
                fig_age = px.bar(
                    x=p["demo_ages"], y=p["demo_vals"],
                    labels={'x': 'Age Category Bracket', 'y': 'Composition Share (%)'},
                    color_discrete_sequence=['#8B5CF6']
                )
                fig_age.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=220)
                st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("---")
    st.markdown("### Demographics Distribution Weight Matrix")
    # Combined primary age distribution (weighted average across all 3 personas)
    age_labels = personas[0]["demo_ages"]
    combined   = [round(sum(p["demo_vals"][i] * w for p, w in zip(personas, [0.50, 0.30, 0.20])), 1)
                  for i in range(4)]
    fig_bar = px.bar(
        x=age_labels, y=combined,
        labels={'x': 'Age Category Bracket', 'y': 'Core Composition Share (%)'},
        color_discrete_sequence=['#8B5CF6']
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CREATOR MATCHING
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "Creator Matching":
    st.markdown("## 🤖 Creator Discovery Engine")
    st.markdown("Cross-matching engine scores with specialised network profiles based on relevance matrices.")

    st.markdown("### 🏆 Top Automated Matches")
    top_creators = df_creators.head(3)
    c_idx = 1
    for idx, row in top_creators.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
        with col1:
            st.markdown(f"##### #{c_idx} {row['Name']}")
            st.markdown(f"<span class='badge-purple'>{row['Niche']}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Followers**<br>{row['Followers']:,}", unsafe_allow_html=True)
        with col3:
            st.markdown(f"**Engagement**<br>{row['Engagement']}%", unsafe_allow_html=True)
        with col4:
            st.markdown(f"**Authenticity**<br>{row['Authenticity']}/100", unsafe_allow_html=True)
        with col5:
            st.markdown(f"**Compatibility**<br>💎 {row['CompatibilityScore']}", unsafe_allow_html=True)
        st.markdown("---")
        c_idx += 1

    st.markdown("### 📊 Creator Evaluation Matrix")
    st.dataframe(df_creators, use_container_width=True)

    st.markdown("### 📈 Compatibility Score — Top 10")
    fig_cb = px.bar(
        df_creators.head(10), x="Name", y="CompatibilityScore",
        color="CompatibilityScore", color_continuous_scale="Purpor",
        labels={"CompatibilityScore": "Score"}
    )
    fig_cb.update_layout(xaxis_tickangle=-30, height=350, margin=dict(t=10, b=10))
    st.plotly_chart(fig_cb, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 5 — CAMPAIGN INTELLIGENCE
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "Campaign Intelligence":
    st.markdown("## 📊 Predictive Campaign Intelligence")

    budget = st.number_input(
        "Campaign Budget Model (₹)",
        min_value=10_000, max_value=5_000_000,
        value=st.session_state.campaign_budget, step=10_000
    )
    st.session_state.campaign_budget = budget
    c = predict_campaign(budget, st.session_state.prod_price, cat)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(metric_card("Predicted Reach",      f"{c['reach']:,}",      "Unique users exposed"), unsafe_allow_html=True)
    with m2:
        st.markdown(metric_card("Clicks Generated",     f"{c['clicks']:,}",     f"CTR {CATEGORY_CFG[cat]['ctr']*100:.1f}%"), unsafe_allow_html=True)
    with m3:
        st.markdown(metric_card("Target Revenue Stream",f"₹{c['revenue']:,}",   f"{c['conversions']:,} conversions"), unsafe_allow_html=True)
    with m4:
        rc = "#10B981" if c['roi'] > 0 else "#EF4444"
        st.markdown(metric_card("Modeled ROI Index",    f"{c['roi']}%",          "Net return on ad spend", delta_color=rc), unsafe_allow_html=True)

    st.markdown("### 🛒 Campaign Performance Funnel")
    funnel_data = dict(
        number=[c["impressions"], c["reach"], c["engagements"], c["clicks"], c["conversions"]],
        stage =["Impressions",    "Reach",    "Engagements",    "Clicks",    "Conversions"]
    )
    fig_funnel = px.funnel(funnel_data, x='number', y='stage',
                           color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig_funnel, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# PAGE 6 — INSIGHTS REPORT  (Recommendations + Export)
# ═════════════════════════════════════════════════════════════════════════════
elif app_mode == "Insights Report":
    st.markdown("## 👑 Smart Strategic Recommendations")

    rec = generate_recommendations(cat)

    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        fmt_html = "".join(
            f"<li><b>{f[0]} ({f[1]}%):</b> {f[2]}</li>"
            for f in rec["formats"]
        )
        st.markdown(f"""
        <div class='glass-card'>
            <h4>Optimal Media Content Formats</h4>
            <ul>{fmt_html}</ul>
        </div>""", unsafe_allow_html=True)
    with rc2:
        st.markdown(f"""
        <div class='glass-card'>
            <h4>Scheduling & Campaign Frame</h4>
            <p><b>Best Window:</b> {rec['time']}</p>
            <p><b>Target Frame Duration:</b> {rec['duration']}</p>
            <p><b>Cadence Pattern:</b> {rec['cadence']}</p>
        </div>""", unsafe_allow_html=True)
    with rc3:
        split_html = "".join(
            f"<li><b>{s[0]}:</b> {s[1]}%</li>"
            for s in rec["split"]
        )
        st.markdown(f"""
        <div class='glass-card'>
            <h4>Recommended Budget Allocation Matrix</h4>
            <ul>{split_html}</ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📋 Executive Insights Export Engine")
    st.markdown("Generate and compile explicit data matrices for investor pitch tracks.")

    # — Dynamic report text —
    c = predict_campaign(st.session_state.campaign_budget, st.session_state.prod_price, cat)
    personas_live = generate_personas(cat)
    top5_txt = "\n".join(
        f"  #{i+1} {row['Name']} | {row['Niche']} | {row['Followers']:,} followers | Score {row['CompatibilityScore']}"
        for i, (_, row) in enumerate(df_creators.head(5).iterrows())
    )
    fmt_txt   = " | ".join(f"{f[0]} {f[1]}%" for f in rec["formats"])
    split_txt = " | ".join(f"{s[0]} {s[1]}%" for s in rec["split"])

    report_text = f"""LAUNCHLENS AI — EXECUTIVE PORTFOLIO REPORT
==========================================
Product Name   : {st.session_state.prod_name}
Category       : {cat}
Price          : ₹{st.session_state.prod_price}
Demand Score   : {demand}/100
Market Position: {CATEGORY_CFG[cat]['mkt_pos']}

AUDIENCE SEGMENTS
-----------------
Primary   : {personas_live[0]['segment']}  — Intent {personas_live[0]['intent']} ({personas_live[0]['intent_score']}/100)
Secondary : {personas_live[1]['segment']} — Intent {personas_live[1]['intent']} ({personas_live[1]['intent_score']}/100)
Tertiary  : {personas_live[2]['segment']}  — Intent {personas_live[2]['intent']} ({personas_live[2]['intent_score']}/100)

TOP 5 CREATOR MATCHES
---------------------
{top5_txt}

CAMPAIGN FORECAST  (Budget: ₹{st.session_state.campaign_budget:,})
---------------------------------------------------
Impressions  : {c['impressions']:,}
Reach        : {c['reach']:,}
Engagements  : {c['engagements']:,}
Clicks       : {c['clicks']:,}
Conversions  : {c['conversions']:,}
Revenue      : ₹{c['revenue']:,}
ROI          : {c['roi']}%

RECOMMENDATIONS
---------------
Content Formats: {fmt_txt}
Best Time      : {rec['time']}
Duration       : {rec['duration']}
Budget Split   : {split_txt}

Generated by LaunchLens AI v2.0.0  |  Dynamic Engine Build
"""

    st.code(report_text, language="text")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📥 Download Executive Insight Summary (TXT)",
            data=report_text,
            file_name="LaunchLens_Executive_Report.txt",
            mime="text/plain"
        )
    with col_d2:
        csv_data = df_creators.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📊 Export Full Creator Compatibility Metrics (CSV)",
            data=csv_data,
            file_name="LaunchLens_Creator_Matrix.csv",
            mime="text/csv"
        )

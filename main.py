import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import zipfile
import io
from typing import Dict, List, Tuple
import base64

# Configure Streamlit page
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for theme switching */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --background-color: #ffffff;
        --surface-color: #f8fafc;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --border-color: #e5e7eb;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    [data-theme="dark"] {
        --background-color: #0f172a;
        --surface-color: #1e293b;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border-color: #334155;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3), 0 1px 2px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
        background-color: var(--background-color);
        color: var(--text-primary);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Upload section styling */
    .upload-section {
        background: var(--surface-color);
        border: 2px dashed var(--primary-color);
        border-radius: 1rem;
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: var(--secondary-color);
        background: linear-gradient(135deg, var(--surface-color), rgba(99, 102, 241, 0.05));
    }
    
    .upload-title {
        font-size: 2rem;
        font-weight: 600;
        color: var(--primary-color);
        margin-bottom: 1rem;
    }
    
    .upload-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: var(--surface-color);
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* Success/Error message styling */
    .success-message {
        background: var(--success-color);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    .error-message {
        background: var(--error-color);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--surface-color);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed var(--primary-color);
        border-radius: 0.5rem;
        padding: 1rem;
        background: var(--surface-color);
    }
    
    /* Chart containers */
    .chart-container {
        background: var(--surface-color);
        border-radius: 0.75rem;
        padding: 1rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
    }
    
    /* Help section */
    .help-section {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
        border-left: 4px solid var(--primary-color);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Dark mode toggle */
    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        cursor: pointer;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        transform: scale(1.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(135deg, var(--success-color), var(--primary-color));
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: var(--surface-color);
        border-radius: 8px;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

class FinanceDashboard:
    def __init__(self):
        self.transactions_df = None
        self.net_worth_df = None
        self.investments_df = None
        self.goals_df = None
        
    def load_from_zip(self, zip_file):
        """Load data from uploaded ZIP file"""
        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                file_names = zip_ref.namelist()
                
                # Required file names (case insensitive)
                required_files = {
                    'transactions.csv': None,
                    'net_worth.csv': None,
                    'investments.csv': None,
                    'goals.csv': None
                }
                
                # Find matching files
                for file_name in file_names:
                    lower_name = file_name.lower()
                    if lower_name in required_files:
                        required_files[lower_name] = file_name
                
                # Load transactions (required)
                if required_files['transactions.csv']:
                    with zip_ref.open(required_files['transactions.csv']) as f:
                        self.transactions_df = pd.read_csv(f)
                        self.transactions_df['Date'] = pd.to_datetime(self.transactions_df['Date'])
                        self.transactions_df['Month'] = self.transactions_df['Date'].dt.to_period('M')
                else:
                    st.error("❌ Missing required file: transactions.csv")
                    return False
                
                # Load optional files
                if required_files['net_worth.csv']:
                    with zip_ref.open(required_files['net_worth.csv']) as f:
                        self.net_worth_df = pd.read_csv(f)
                        self.net_worth_df['Date'] = pd.to_datetime(self.net_worth_df['Date'])
                
                if required_files['investments.csv']:
                    with zip_ref.open(required_files['investments.csv']) as f:
                        self.investments_df = pd.read_csv(f)
                
                if required_files['goals.csv']:
                    with zip_ref.open(required_files['goals.csv']) as f:
                        self.goals_df = pd.read_csv(f)
                        self.goals_df['Target_Date'] = pd.to_datetime(self.goals_df['Target_Date'])
                
                return True
                
        except Exception as e:
            st.error(f"❌ Error loading ZIP file: {str(e)}")
            return False
    
    def categorize_transactions(self) -> pd.DataFrame:
        """Categorize transactions with enhanced mapping"""
        if self.transactions_df is None:
            return pd.DataFrame()
        
        # Add Category column if it doesn't exist
        if 'Category' not in self.transactions_df.columns:
            self.transactions_df['Category'] = 'other'
        
        # Enhanced category mapping
        category_mapping = {
            'grocery': ['grocery', 'supermarket', 'food', 'walmart', 'target', 'kroger', 'safeway', 'publix', 
                       'whole foods', 'trader joe', 'costco', 'fresh market', 'harris teeter', 'wegmans', 'sprouts'],
            'dining': ['restaurant', 'cafe', 'pizza', 'starbucks', 'mcdonald', 'subway', 'chipotle', 'taco bell',
                      'burger', 'kfc', 'dunkin', 'panera', 'olive garden', 'red lobster', 'five guys', 'domino'],
            'transportation': ['gas station', 'uber', 'lyft', 'metro', 'parking', 'taxi', 'bus', 'train', 'fuel',
                             'shell', 'exxon', 'bp', 'chevron', 'marathon', 'texaco', 'mobil', 'airport'],
            'utilities': ['electric', 'gas', 'water', 'internet', 'phone', 'cable', 'insurance', 'utility',
                         'verizon', 'at&t', 'comcast', 'spectrum'],
            'entertainment': ['movie', 'netflix', 'spotify', 'amazon prime', 'hulu', 'disney', 'hbo', 'theater',
                            'concert', 'game', 'youtube', 'paramount', 'apple music', 'steam'],
            'healthcare': ['hospital', 'pharmacy', 'doctor', 'medical', 'dentist', 'cvs', 'walgreens', 'clinic',
                          'urgent care', 'prescription'],
            'shopping': ['amazon', 'ebay', 'mall', 'clothing', 'electronics', 'best buy', 'apple store', 'nike',
                        'adidas', 'macy', 'target', 'home depot', 'rei', 'gamestop'],
            'salary': ['salary', 'paycheck', 'wages', 'income', 'bonus', 'freelance', 'consulting'],
            'investment': ['dividend', 'interest', 'capital gains', 'stock', 'bond', 'mutual fund', 'reit']
        }
        
        def auto_categorize(description):
            if pd.isna(description):
                return 'other'
            description_lower = str(description).lower()
            for category, keywords in category_mapping.items():
                if any(keyword in description_lower for keyword in keywords):
                    return category
            return 'other'
        
        # Apply auto-categorization
        mask = (self.transactions_df['Category'].isna()) | (self.transactions_df['Category'] == 'other')
        self.transactions_df.loc[mask, 'Category'] = self.transactions_df.loc[mask, 'Description'].apply(auto_categorize)
        
        return self.transactions_df
    
    def calculate_monthly_summary(self) -> pd.DataFrame:
        """Calculate monthly income and expenses"""
        if self.transactions_df is None:
            return pd.DataFrame()
        
        monthly_summary = self.transactions_df.groupby(['Month', 'Type']).agg({
            'Amount': 'sum'
        }).unstack(fill_value=0).round(2)
        
        monthly_summary.columns = monthly_summary.columns.droplevel(0)
        monthly_summary = monthly_summary.reset_index()
        
        # Ensure both income and expense columns exist
        if 'income' not in monthly_summary.columns:
            monthly_summary['income'] = 0
        if 'expense' not in monthly_summary.columns:
            monthly_summary['expense'] = 0
        
        monthly_summary['net_cash_flow'] = monthly_summary['income'] + monthly_summary['expense']
        monthly_summary['Month_str'] = monthly_summary['Month'].astype(str)
        
        return monthly_summary
    
    def get_investment_prices(self) -> Dict:
        """Get simulated investment prices"""
        mock_prices = {
            'AAPL': 175.50, 'GOOGL': 142.30, 'MSFT': 378.85, 'TSLA': 248.42,
            'SPY': 445.67, 'VTI': 235.89, 'NVDA': 455.30, 'AMZN': 155.80,
            'META': 325.40, 'BRK.B': 380.25, 'VOO': 425.60, 'QQQ': 385.90,
            'JNJ': 160.25, 'PG': 148.70, 'KO': 64.15, 'DIS': 92.40,
            'V': 252.80, 'JPM': 168.90, 'UNH': 492.15, 'HD': 328.60
        }
        return mock_prices
    
    def calculate_portfolio_value(self) -> pd.DataFrame:
        """Calculate portfolio performance"""
        if self.investments_df is None:
            return pd.DataFrame()
        
        current_prices = self.get_investment_prices()
        portfolio = self.investments_df.copy()
        
        portfolio['Current_Price'] = portfolio['Symbol'].map(current_prices).fillna(0)
        portfolio['Current_Value'] = portfolio['Shares'] * portfolio['Current_Price']
        portfolio['Total_Cost'] = portfolio['Shares'] * portfolio['Purchase_Price']
        portfolio['Gain_Loss'] = portfolio['Current_Value'] - portfolio['Total_Cost']
        portfolio['Gain_Loss_Pct'] = np.where(portfolio['Total_Cost'] > 0, 
                                            (portfolio['Gain_Loss'] / portfolio['Total_Cost'] * 100).round(2), 0)
        
        return portfolio
    
    def calculate_goal_progress(self) -> pd.DataFrame:
        """Calculate goal progress"""
        if self.goals_df is None:
            return pd.DataFrame()
        
        goals = self.goals_df.copy()
        current_date = datetime.now()
        
        goals['Progress_Pct'] = np.where(goals['Target_Amount'] > 0,
                                       (goals['Current_Amount'] / goals['Target_Amount'] * 100).round(2), 0)
        
        goals['Days_Remaining'] = (goals['Target_Date'] - current_date).dt.days
        
        goals['Required_Monthly_Savings'] = np.where(
            goals['Days_Remaining'] > 0,
            (goals['Target_Amount'] - goals['Current_Amount']) / (goals['Days_Remaining'] / 30.44),
            0
        ).round(2)
        
        return goals

def create_sample_zip():
    """Create downloadable sample ZIP file"""
    zip_buffer = io.BytesIO()
    
    # Sample data
    transactions_data = """Date,Description,Amount,Type,Category
2024-01-01,Salary Payment,5000.00,income,salary
2024-01-02,Whole Foods Market,-156.89,expense,grocery
2024-01-03,Shell Gas Station,-65.42,expense,transportation
2024-01-04,Netflix Subscription,-15.99,expense,entertainment
2024-01-05,Chipotle Mexican Grill,-12.85,expense,dining
2024-01-06,Electric Company Bill,-134.67,expense,utilities
2024-01-07,Amazon Purchase,-289.99,expense,shopping
2024-01-08,Starbucks Coffee,-6.75,expense,dining
2024-01-09,Uber Ride,-45.30,expense,transportation
2024-01-10,CVS Pharmacy,-25.99,expense,healthcare"""
    
    net_worth_data = """Date,Assets,Liabilities
2024-01-31,85420.50,32150.75
2024-02-29,87890.25,31980.50
2024-03-31,91250.80,31750.25
2024-04-30,94560.40,31520.00"""
    
    investments_data = """Symbol,Name,Shares,Purchase_Price,Purchase_Date
AAPL,Apple Inc.,50,145.30,2024-01-15
GOOGL,Alphabet Inc.,25,128.50,2024-01-22
MSFT,Microsoft Corporation,40,352.80,2024-02-05
SPY,SPDR S&P 500 ETF,100,398.45,2024-01-08"""
    
    goals_data = """Goal_Name,Target_Amount,Current_Amount,Target_Date
Emergency Fund,25000,12500,2024-12-31
House Down Payment,80000,35000,2026-06-30
Retirement Fund,1000000,125000,2055-12-31
Vacation Fund,8000,3200,2025-06-15"""
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('transactions.csv', transactions_data)
        zip_file.writestr('net_worth.csv', net_worth_data)
        zip_file.writestr('investments.csv', investments_data)
        zip_file.writestr('goals.csv', goals_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def show_upload_interface():
    """Show the main upload interface"""
    st.markdown("""
    <div class="upload-section">
        <div class="upload-title">📁 Upload Your Financial Data</div>
        <div class="upload-subtitle">Upload a ZIP file containing your CSV files or use individual file uploads</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for upload options
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗜️ ZIP File Upload (Recommended)")
        st.markdown("Upload a single ZIP file containing all your CSV files")
        
        zip_file = st.file_uploader(
            "Choose ZIP file",
            type=['zip'],
            help="Upload a ZIP file containing: transactions.csv (required), net_worth.csv, investments.csv, goals.csv",
            key="zip_upload"
        )
        
        if zip_file:
            return 'zip', zip_file, None, None, None
    
    with col2:
        st.subheader("📄 Individual File Upload")
        st.markdown("Upload CSV files individually")
        
        transactions_file = st.file_uploader(
            "📊 Transactions CSV (Required)",
            type=['csv'],
            help="Required: Date, Description, Amount, Type columns",
            key="trans_upload"
        )
        
        net_worth_file = st.file_uploader(
            "💎 Net Worth CSV (Optional)",
            type=['csv'],
            help="Required: Date, Assets, Liabilities columns",
            key="net_upload"
        )
        
        investments_file = st.file_uploader(
            "📈 Investments CSV (Optional)",
            type=['csv'],
            help="Required: Symbol, Name, Shares, Purchase_Price columns",
            key="inv_upload"
        )
        
        goals_file = st.file_uploader(
            "🎯 Goals CSV (Optional)",
            type=['csv'],
            help="Required: Goal_Name, Target_Amount, Current_Amount, Target_Date columns",
            key="goals_upload"
        )
        
        if transactions_file:
            return 'individual', transactions_file, net_worth_file, investments_file, goals_file
    
    return None, None, None, None, None

def show_file_requirements():
    """Show detailed file requirements"""
    st.markdown("---")
    
    with st.expander("📋 **File Requirements & Help**", expanded=False):
        
        st.markdown("### 🗂️ ZIP File Structure")
        st.code("""
financial_data.zip
├── transactions.csv    (REQUIRED)
├── net_worth.csv      (optional)  
├── investments.csv    (optional)
└── goals.csv          (optional)
        """)
        
        st.markdown("### 📊 File Formats")
        
        # Transactions format
        st.markdown("#### 1. transactions.csv (Required)")
        st.code("""
Date,Description,Amount,Type,Category
2024-01-01,Salary Payment,5000.00,income,salary
2024-01-02,Grocery Store,-150.25,expense,grocery
2024-01-03,Gas Station,-65.80,expense,transportation
        """)
        st.markdown("**Required columns:** Date, Description, Amount, Type  \n**Optional:** Category (auto-generated)")
        
        # Net worth format
        st.markdown("#### 2. net_worth.csv (Optional)")
        st.code("""
Date,Assets,Liabilities
2024-01-31,52500.00,25000.00
2024-02-29,54200.00,24800.00
        """)
        
        # Investments format
        st.markdown("#### 3. investments.csv (Optional)")
        st.code("""
Symbol,Name,Shares,Purchase_Price,Purchase_Date
AAPL,Apple Inc.,25,150.00,2024-01-15
GOOGL,Alphabet Inc.,15,120.00,2024-02-10
        """)
        
        # Goals format
        st.markdown("#### 4. goals.csv (Optional)")
        st.code("""
Goal_Name,Target_Amount,Current_Amount,Target_Date
Emergency Fund,15000,8500,2025-12-31
House Down Payment,50000,15000,2026-06-30
        """)
        
        st.markdown("### 💡 **Tips for Success**")
        st.markdown("""
        - **File names must be exact:** transactions.csv, net_worth.csv, investments.csv, goals.csv
        - **Date format:** YYYY-MM-DD preferred (but flexible)
        - **Amount format:** Positive for income, negative for expenses
        - **No empty rows** in the middle of your data
        - **UTF-8 encoding** recommended for special characters
        """)

def show_sample_download():
    """Show sample data download section"""
    st.markdown("---")
    st.subheader("📥 Download Sample Data")
    st.markdown("Don't have your data ready? Download our sample files to test the dashboard:")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**🗜️ Complete Sample ZIP**")
        st.markdown("Contains all 4 CSV files with realistic financial data")
        
        sample_zip = create_sample_zip()
        st.download_button(
            label="📦 Download Sample ZIP",
            data=sample_zip,
            file_name="sample_financial_data.zip",
            mime="application/zip",
            help="Download sample ZIP file with all CSV files"
        )
    
    with col2:
        st.markdown("**📖 Instructions**")
        st.markdown("""
        1. Download the sample ZIP file
        2. Extract and examine the CSV files
        3. Replace with your own data
        4. Re-zip and upload to the dashboard
        """)

def create_beautiful_metrics(dashboard):
    """Create beautiful metric cards"""
    if dashboard.transactions_df is None:
        return
    
    # Calculate metrics
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_income = dashboard.transactions_df[
        (dashboard.transactions_df['Type'] == 'income') & 
        (dashboard.transactions_df['Date'].dt.month == current_month) &
        (dashboard.transactions_df['Date'].dt.year == current_year)
    ]['Amount'].sum()
    
    monthly_expenses = abs(dashboard.transactions_df[
        (dashboard.transactions_df['Type'] == 'expense') & 
        (dashboard.transactions_df['Date'].dt.month == current_month) &
        (dashboard.transactions_df['Date'].dt.year == current_year)
    ]['Amount'].sum())
    
    net_flow = monthly_income - monthly_expenses
    
    # Net worth
    latest_net_worth = 0
    if dashboard.net_worth_df is not None and not dashboard.net_worth_df.empty:
        latest_net_worth = dashboard.net_worth_df.iloc[-1]['Assets'] - dashboard.net_worth_df.iloc[-1]['Liabilities']
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        (col1, "💰", "Monthly Income", f"${monthly_income:,.0f}", "var(--success-color)"),
        (col2, "💸", "Monthly Expenses", f"${monthly_expenses:,.0f}", "var(--warning-color)"),
        (col3, "📊", "Net Cash Flow", f"${net_flow:,.0f}", "var(--primary-color)" if net_flow >= 0 else "var(--error-color)"),
        (col4, "💎", "Net Worth", f"${latest_net_worth:,.0f}", "var(--secondary-color)")
    ]
    
    for col, icon, label, value, color in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

def create_enhanced_charts(dashboard):
    """Create enhanced interactive charts"""
    
    # Expense Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💸 Expense Breakdown")
        
        if dashboard.transactions_df is not None:
            expense_data = dashboard.transactions_df[
                dashboard.transactions_df['Type'] == 'expense'
            ].groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)
            
            if not expense_data.empty:
                fig_pie = px.pie(
                    values=expense_data.values, 
                    names=expense_data.index,
                    title="",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig_pie.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
                )
                fig_pie.update_layout(
                    showlegend=True,
                    legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=400
                )
                st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Cash Flow Trend")
        
        if dashboard.transactions_df is not None:
            monthly_summary = dashboard.calculate_monthly_summary()
            if not monthly_summary.empty:
                fig_cashflow = go.Figure()
                
                fig_cashflow.add_trace(go.Scatter(
                    x=monthly_summary['Month_str'],
                    y=monthly_summary['income'],
                    mode='lines+markers',
                    name='Income',
                    line=dict(color='#10b981', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>Income</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
                ))
                
                fig_cashflow.add_trace(go.Scatter(
                    x=monthly_summary['Month_str'],
                    y=monthly_summary['expense'].abs(),
                    mode='lines+markers',
                    name='Expenses',
                    line=dict(color='#ef4444', width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>Expenses</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
                ))
                
                fig_cashflow.update_layout(
                    title="",
                    xaxis_title="Month",
                    yaxis_title="Amount ($)",
                    hovermode='x unified',
                    margin=dict(t=0, b=0, l=0, r=0),
                    height=400,
                    showlegend=True,
                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
                )
                
                st.plotly_chart(fig_cashflow, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard_content(dashboard):
    """Show the main dashboard content"""
    # Beautiful metrics
    create_beautiful_metrics(dashboard)
    
    st.markdown("---")
    
    # Enhanced charts
    create_enhanced_charts(dashboard)
    
    # Navigation tabs
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💳 Transactions", 
        "💰 Cash Flow", 
        "📈 Investments", 
        "💎 Net Worth", 
        "🎯 Goals"
    ])
    
    with tab1:
        show_transactions_tab(dashboard)
    
    with tab2:
        show_cash_flow_tab(dashboard)
    
    with tab3:
        show_investments_tab(dashboard)
    
    with tab4:
        show_net_worth_tab(dashboard)
    
    with tab5:
        show_goals_tab(dashboard)

def show_transactions_tab(dashboard):
    """Enhanced transactions analysis tab"""
    if dashboard.transactions_df is None:
        st.warning("No transaction data available")
        return
    
    # Categorize transactions
    categorized_df = dashboard.categorize_transactions()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_transactions = len(categorized_df)
    date_range_days = (categorized_df['Date'].max() - categorized_df['Date'].min()).days
    total_income = categorized_df[categorized_df['Type'] == 'income']['Amount'].sum()
    total_expenses = abs(categorized_df[categorized_df['Type'] == 'expense']['Amount'].sum())
    
    with col1:
        st.metric("Total Transactions", f"{total_transactions:,}")
    with col2:
        st.metric("Date Range", f"{date_range_days} days")
    with col3:
        st.metric("Total Income", f"${total_income:,.0f}")
    with col4:
        st.metric("Total Expenses", f"${total_expenses:,.0f}")
    
    st.markdown("---")
    
    # Interactive filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_categories = st.multiselect(
            "Filter by Category",
            options=sorted(categorized_df['Category'].unique()),
            default=sorted(categorized_df['Category'].unique()),
            key="trans_cat_filter"
        )
    
    with col2:
        selected_types = st.multiselect(
            "Filter by Type",
            options=categorized_df['Type'].unique(),
            default=categorized_df['Type'].unique(),
            key="trans_type_filter"
        )
    
    with col3:
        amount_range = st.slider(
            "Amount Range",
            min_value=float(categorized_df['Amount'].min()),
            max_value=float(categorized_df['Amount'].max()),
            value=(float(categorized_df['Amount'].min()), float(categorized_df['Amount'].max())),
            key="trans_amount_filter"
        )
    
    # Apply filters
    filtered_df = categorized_df[
        (categorized_df['Category'].isin(selected_categories)) &
        (categorized_df['Type'].isin(selected_types)) &
        (categorized_df['Amount'] >= amount_range[0]) &
        (categorized_df['Amount'] <= amount_range[1])
    ]
    
    # Enhanced transaction table
    st.subheader("📊 Transaction Details")
    
    if not filtered_df.empty:
        # Format the dataframe for better display
        display_df = filtered_df.copy()
        display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df[['Date', 'Description', 'Amount', 'Type', 'Category']].sort_values('Date', ascending=False),
            use_container_width=True,
            height=400
        )
        
        # Category analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📊 Spending by Category")
            category_totals = filtered_df[filtered_df['Type'] == 'expense'].groupby('Category')['Amount'].sum().abs().sort_values(ascending=True)
            
            if not category_totals.empty:
                fig_bar = px.bar(
                    x=category_totals.values,
                    y=category_totals.index,
                    orientation='h',
                    title="",
                    color=category_totals.values,
                    color_continuous_scale='Viridis'
                )
                fig_bar.update_layout(
                    xaxis_title="Amount ($)",
                    yaxis_title="Category",
                    height=400,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("📈 Transaction Timeline")
            daily_totals = filtered_df.groupby('Date')['Amount'].sum().reset_index()
            
            if not daily_totals.empty:
                fig_timeline = px.line(
                    daily_totals,
                    x='Date',
                    y='Amount',
                    title="",
                    line_shape='spline'
                )
                fig_timeline.update_traces(line=dict(width=3))
                fig_timeline.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Net Amount ($)",
                    height=400
                )
                st.plotly_chart(fig_timeline, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.info("No transactions match the selected filters")

def show_cash_flow_tab(dashboard):
    """Enhanced cash flow analysis tab"""
    if dashboard.transactions_df is None:
        st.warning("No transaction data available")
        return
    
    monthly_summary = dashboard.calculate_monthly_summary()
    
    if monthly_summary.empty:
        st.warning("No monthly summary data available")
        return
    
    # Cash flow metrics
    avg_income = monthly_summary['income'].mean()
    avg_expenses = abs(monthly_summary['expense'].mean())
    avg_savings = monthly_summary['net_cash_flow'].mean()
    savings_rate = (avg_savings / avg_income * 100) if avg_income > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Avg Monthly Income", f"${avg_income:,.0f}")
    with col2:
        st.metric("Avg Monthly Expenses", f"${avg_expenses:,.0f}")
    with col3:
        st.metric("Avg Monthly Savings", f"${avg_savings:,.0f}")
    with col4:
        st.metric("Savings Rate", f"{savings_rate:.1f}%")
    
    st.markdown("---")
    
    # Enhanced cash flow visualization
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💰 Monthly Cash Flow Analysis")
    
    fig_cashflow = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Cash Flow Trends', 'Net Cash Flow'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Main cash flow chart
    fig_cashflow.add_trace(
        go.Bar(
            x=monthly_summary['Month_str'],
            y=monthly_summary['income'],
            name='Income',
            marker_color='#10b981',
            hovertemplate='<b>Income</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig_cashflow.add_trace(
        go.Bar(
            x=monthly_summary['Month_str'],
            y=monthly_summary['expense'],
            name='Expenses',
            marker_color='#ef4444',
            hovertemplate='<b>Expenses</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Net cash flow
    fig_cashflow.add_trace(
        go.Scatter(
            x=monthly_summary['Month_str'],
            y=monthly_summary['net_cash_flow'],
            mode='lines+markers',
            name='Net Cash Flow',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=8),
            hovertemplate='<b>Net Cash Flow</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig_cashflow.update_layout(
        height=600,
        barmode='group',
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    
    fig_cashflow.update_xaxes(title_text="Month", row=2, col=1)
    fig_cashflow.update_yaxes(title_text="Amount ($)", row=1, col=1)
    fig_cashflow.update_yaxes(title_text="Net Amount ($)", row=2, col=1)
    
    st.plotly_chart(fig_cashflow, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Cash flow table
    st.subheader("📊 Monthly Summary Table")
    display_summary = monthly_summary[['Month_str', 'income', 'expense', 'net_cash_flow']].copy()
    display_summary.columns = ['Month', 'Income', 'Expenses', 'Net Cash Flow']
    display_summary['Income'] = display_summary['Income'].apply(lambda x: f"${x:,.2f}")
    display_summary['Expenses'] = display_summary['Expenses'].apply(lambda x: f"${x:,.2f}")
    display_summary['Net Cash Flow'] = display_summary['Net Cash Flow'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(display_summary, use_container_width=True)

def show_investments_tab(dashboard):
    """Enhanced investments analysis tab"""
    if dashboard.investments_df is None:
        st.warning("No investment data available. Upload an investments.csv file to see your portfolio analysis.")
        return
    
    portfolio = dashboard.calculate_portfolio_value()
    
    if portfolio.empty:
        st.warning("No investment data available")
        return
    
    # Portfolio summary metrics
    total_value = portfolio['Current_Value'].sum()
    total_cost = portfolio['Total_Cost'].sum()
    total_gain_loss = portfolio['Gain_Loss'].sum()
    total_gain_loss_pct = (total_gain_loss / total_cost * 100) if total_cost > 0 else 0
    num_positions = len(portfolio)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Portfolio Value", f"${total_value:,.0f}")
    with col2:
        st.metric("Total Invested", f"${total_cost:,.0f}")
    with col3:
        st.metric("Total Gain/Loss", f"${total_gain_loss:,.0f}")
    with col4:
        st.metric("Total Return", f"{total_gain_loss_pct:.1f}%")
    with col5:
        st.metric("Positions", f"{num_positions}")
    
    st.markdown("---")
    
    # Portfolio visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Portfolio Allocation")
        
        fig_allocation = px.pie(
            portfolio, 
            values='Current_Value', 
            names='Symbol',
            title="",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_allocation.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Value: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
        )
        fig_allocation.update_layout(
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02),
            height=400
        )
        st.plotly_chart(fig_allocation, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Performance by Holding")
        
        # Sort by gain/loss percentage for better visualization
        portfolio_sorted = portfolio.sort_values('Gain_Loss_Pct', ascending=True)
        
        fig_performance = px.bar(
            portfolio_sorted,
            x='Gain_Loss_Pct',
            y='Symbol',
            orientation='h',
            title="",
            color='Gain_Loss_Pct',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0
        )
        fig_performance.update_layout(
            xaxis_title="Gain/Loss (%)",
            yaxis_title="Symbol",
            height=400,
            coloraxis_showscale=False
        )
        fig_performance.update_traces(
            hovertemplate='<b>%{y}</b><br>Return: %{x:.1f}%<extra></extra>'
        )
        st.plotly_chart(fig_performance, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed portfolio table
    st.subheader("📈 Portfolio Details")
    
    # Format portfolio data for display
    display_portfolio = portfolio.copy()
    display_portfolio['Current_Price'] = display_portfolio['Current_Price'].apply(lambda x: f"${x:.2f}")
    display_portfolio['Purchase_Price'] = display_portfolio['Purchase_Price'].apply(lambda x: f"${x:.2f}")
    display_portfolio['Current_Value'] = display_portfolio['Current_Value'].apply(lambda x: f"${x:,.0f}")
    display_portfolio['Total_Cost'] = display_portfolio['Total_Cost'].apply(lambda x: f"${x:,.0f}")
    display_portfolio['Gain_Loss'] = display_portfolio['Gain_Loss'].apply(lambda x: f"${x:,.0f}")
    display_portfolio['Gain_Loss_Pct'] = display_portfolio['Gain_Loss_Pct'].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        display_portfolio[['Symbol', 'Name', 'Shares', 'Purchase_Price', 'Current_Price', 
                         'Total_Cost', 'Current_Value', 'Gain_Loss', 'Gain_Loss_Pct']],
        use_container_width=True
    )

def show_net_worth_tab(dashboard):
    """Enhanced net worth tracking tab"""
    if dashboard.net_worth_df is None:
        st.warning("No net worth data available. Upload a net_worth.csv file to track your financial progress.")
        return
    
    # Calculate net worth if not present
    if 'Net_Worth' not in dashboard.net_worth_df.columns:
        dashboard.net_worth_df['Net_Worth'] = dashboard.net_worth_df['Assets'] - dashboard.net_worth_df['Liabilities']
    
    # Net worth metrics
    latest_net_worth = dashboard.net_worth_df.iloc[-1]['Net_Worth']
    latest_assets = dashboard.net_worth_df.iloc[-1]['Assets']
    latest_liabilities = dashboard.net_worth_df.iloc[-1]['Liabilities']
    
    if len(dashboard.net_worth_df) > 1:
        previous_net_worth = dashboard.net_worth_df.iloc[-2]['Net_Worth']
        net_worth_change = latest_net_worth - previous_net_worth
        net_worth_change_pct = (net_worth_change / previous_net_worth * 100) if previous_net_worth != 0 else 0
    else:
        net_worth_change = 0
        net_worth_change_pct = 0
    
    # Growth rate calculation
    if len(dashboard.net_worth_df) > 1:
        first_net_worth = dashboard.net_worth_df.iloc[0]['Net_Worth']
        months = len(dashboard.net_worth_df) - 1
        if first_net_worth > 0 and months > 0:
            monthly_growth_rate = ((latest_net_worth / first_net_worth) ** (1/months) - 1) * 100
        else:
            monthly_growth_rate = 0
    else:
        monthly_growth_rate = 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Net Worth", f"${latest_net_worth:,.0f}")
    with col2:
        st.metric("Assets", f"${latest_assets:,.0f}")
    with col3:
        st.metric("Liabilities", f"${latest_liabilities:,.0f}")
    with col4:
        st.metric("Monthly Change", f"${net_worth_change:,.0f}", f"{net_worth_change_pct:+.1f}%")
    with col5:
        st.metric("Growth Rate", f"{monthly_growth_rate:+.1f}%/month")
    
    st.markdown("---")
    
    # Enhanced net worth visualization
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💎 Net Worth Timeline")
    
    fig_net_worth = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Assets vs Liabilities', 'Net Worth Trend'),
        vertical_spacing=0.1,
        row_heights=[0.6, 0.4]
    )
    
    # Assets vs Liabilities
    fig_net_worth.add_trace(
        go.Scatter(
            x=dashboard.net_worth_df['Date'],
            y=dashboard.net_worth_df['Assets'],
            mode='lines+markers',
            name='Assets',
            line=dict(color='#10b981', width=3),
            marker=dict(size=6),
            hovertemplate='<b>Assets</b><br>Date: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig_net_worth.add_trace(
        go.Scatter(
            x=dashboard.net_worth_df['Date'],
            y=dashboard.net_worth_df['Liabilities'],
            mode='lines+markers',
            name='Liabilities',
            line=dict(color='#ef4444', width=3),
            marker=dict(size=6),
            hovertemplate='<b>Liabilities</b><br>Date: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Net Worth
    fig_net_worth.add_trace(
        go.Scatter(
            x=dashboard.net_worth_df['Date'],
            y=dashboard.net_worth_df['Net_Worth'],
            mode='lines+markers',
            name='Net Worth',
            line=dict(color='#6366f1', width=4),
            marker=dict(size=8),
            fill='tonexty' if len(dashboard.net_worth_df) > 1 else None,
            hovertemplate='<b>Net Worth</b><br>Date: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
        ),
        row=2, col=1
    )
    
    fig_net_worth.update_layout(
        height=600,
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    
    fig_net_worth.update_xaxes(title_text="Date", row=2, col=1)
    fig_net_worth.update_yaxes(title_text="Amount ($)", row=1, col=1)
    fig_net_worth.update_yaxes(title_text="Net Worth ($)", row=2, col=1)
    
    st.plotly_chart(fig_net_worth, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Net worth history table
    st.subheader("📊 Net Worth History")
    display_nw = dashboard.net_worth_df.copy()
    display_nw['Date'] = display_nw['Date'].dt.strftime('%Y-%m-%d')
    display_nw['Assets'] = display_nw['Assets'].apply(lambda x: f"${x:,.0f}")
    display_nw['Liabilities'] = display_nw['Liabilities'].apply(lambda x: f"${x:,.0f}")
    display_nw['Net_Worth'] = display_nw['Net_Worth'].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(display_nw.sort_values('Date', ascending=False), use_container_width=True)

def show_goals_tab(dashboard):
    """Enhanced financial goals tracking tab"""
    if dashboard.goals_df is None:
        st.warning("No goals data available. Upload a goals.csv file to track your financial objectives.")
        return
    
    goals_progress = dashboard.calculate_goal_progress()
    
    if goals_progress.empty:
        st.warning("No goals data available")
        return
    
    # Goals summary metrics
    total_goals = len(goals_progress)
    completed_goals = len(goals_progress[goals_progress['Progress_Pct'] >= 100])
    on_track_goals = len(goals_progress[(goals_progress['Progress_Pct'] >= 50) & (goals_progress['Progress_Pct'] < 100)])
    behind_goals = len(goals_progress[goals_progress['Progress_Pct'] < 50])
    total_target = goals_progress['Target_Amount'].sum()
    total_current = goals_progress['Current_Amount'].sum()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Goals", f"{total_goals}")
    with col2:
        st.metric("Completed", f"{completed_goals}", f"{completed_goals/total_goals*100:.0f}%")
    with col3:
        st.metric("On Track", f"{on_track_goals}", f"{on_track_goals/total_goals*100:.0f}%")
    with col4:
        st.metric("Behind", f"{behind_goals}", f"{behind_goals/total_goals*100:.0f}%")
    with col5:
        st.metric("Progress", f"{total_current/total_target*100:.0f}%")
    
    st.markdown("---")
    
    # Enhanced goals visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🎯 Goals Progress Overview")
        
        fig_goals = px.bar(
            goals_progress,
            x='Goal_Name',
            y='Progress_Pct',
            title="",
            color='Progress_Pct',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=50
        )
        fig_goals.add_hline(y=100, line_dash="dash", line_color="green", annotation_text="Target")
        fig_goals.add_hline(y=50, line_dash="dash", line_color="orange", annotation_text="Halfway")
        
        fig_goals.update_layout(
            xaxis_title="Goals",
            yaxis_title="Progress (%)",
            height=400,
            xaxis_tickangle=-45,
            coloraxis_showscale=False
        )
        fig_goals.update_traces(
            hovertemplate='<b>%{x}</b><br>Progress: %{y:.1f}%<extra></extra>'
        )
        st.plotly_chart(fig_goals, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💰 Goal Amounts")
        
        fig_amounts = go.Figure()
        
        fig_amounts.add_trace(go.Bar(
            x=goals_progress['Goal_Name'],
            y=goals_progress['Current_Amount'],
            name='Current Amount',
            marker_color='#6366f1',
            hovertemplate='<b>%{x}</b><br>Current: $%{y:,.0f}<extra></extra>'
        ))
        
        fig_amounts.add_trace(go.Bar(
            x=goals_progress['Goal_Name'],
            y=goals_progress['Target_Amount'] - goals_progress['Current_Amount'],
            name='Remaining Amount',
            marker_color='#e5e7eb',
            hovertemplate='<b>%{x}</b><br>Remaining: $%{y:,.0f}<extra></extra>'
        ))
        
        fig_amounts.update_layout(
            barmode='stack',
            xaxis_title="Goals",
            yaxis_title="Amount ($)",
            height=400,
            xaxis_tickangle=-45,
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
        )
        
        st.plotly_chart(fig_amounts, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Individual goal progress
    st.subheader("🎯 Individual Goal Progress")
    
    for _, goal in goals_progress.iterrows():
        with st.container():
            st.markdown(f"### {goal['Goal_Name']}")
            
            progress = min(goal['Progress_Pct'] / 100, 1.0)
            st.progress(progress)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Progress", f"{goal['Progress_Pct']:.1f}%")
            
            with col2:
                st.metric("Current / Target", f"${goal['Current_Amount']:,.0f} / ${goal['Target_Amount']:,.0f}")
            
            with col3:
                if goal['Days_Remaining'] > 0:
                    st.metric("Days Remaining", f"{goal['Days_Remaining']:,}")
                else:
                    st.metric("Status", "⚠️ Overdue")
            
            with col4:
                if goal['Required_Monthly_Savings'] > 0:
                    st.metric("Monthly Savings Needed", f"${goal['Required_Monthly_Savings']:,.0f}")
                else:
                    st.metric("Status", "✅ Complete")
            
            st.markdown("---")

def show_theme_toggle():
    """Add theme toggle functionality"""
    if st.sidebar.button("🌓 Toggle Theme"):
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.experimental_rerun()

def apply_theme():
    """Apply the selected theme"""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    if st.session_state.dark_mode:
        st.markdown("""
        <script>
        document.documentElement.setAttribute('data-theme', 'dark');
        </script>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <script>
        document.documentElement.setAttribute('data-theme', 'light');
        </script>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Load custom CSS and apply theme
    load_custom_css()
    apply_theme()
    
    # App header
    st.markdown("""
    <div class="main-header">
        <h1>💰 Personal Finance Dashboard</h1>
        <p>Transform your financial data into actionable insights with beautiful visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle in sidebar
    st.sidebar.markdown("### 🎨 Theme")
    theme_col1, theme_col2 = st.sidebar.columns(2)
    
    with theme_col1:
        if st.button("☀️ Light", key="light_theme"):
            st.session_state.dark_mode = False
            st.experimental_rerun()
    
    with theme_col2:
        if st.button("🌙 Dark", key="dark_theme"):
            st.session_state.dark_mode = True
            st.experimental_rerun()
    
    st.sidebar.markdown("---")
    
    # Initialize dashboard
    dashboard = FinanceDashboard()
    
    # File upload interface
    upload_type, file1, file2, file3, file4 = show_upload_interface()
    
    # Show file requirements help
    show_file_requirements()
    
    # Show sample download section
    show_sample_download()
    
    # Process uploaded files
    data_loaded = False
    
    if upload_type == 'zip' and file1 is not None:
        with st.spinner("🔄 Processing ZIP file..."):
            if dashboard.load_from_zip(file1):
                data_loaded = True
                st.markdown("""
                <div class="success-message">
                    ✅ ZIP file loaded successfully! Your financial data is ready for analysis.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="error-message">
                    ❌ Failed to load ZIP file. Please check the file format and try again.
                </div>
                """, unsafe_allow_html=True)
    
    elif upload_type == 'individual' and file1 is not None:
        with st.spinner("🔄 Processing CSV files..."):
            try:
                # Load transactions (required)
                dashboard.transactions_df = pd.read_csv(file1)
                dashboard.transactions_df['Date'] = pd.to_datetime(dashboard.transactions_df['Date'])
                dashboard.transactions_df['Month'] = dashboard.transactions_df['Date'].dt.to_period('M')
                
                # Load optional files
                if file2 is not None:
                    dashboard.net_worth_df = pd.read_csv(file2)
                    dashboard.net_worth_df['Date'] = pd.to_datetime(dashboard.net_worth_df['Date'])
                
                if file3 is not None:
                    dashboard.investments_df = pd.read_csv(file3)
                
                if file4 is not None:
                    dashboard.goals_df = pd.read_csv(file4)
                    dashboard.goals_df['Target_Date'] = pd.to_datetime(dashboard.goals_df['Target_Date'])
                
                data_loaded = True
                st.markdown("""
                <div class="success-message">
                    ✅ CSV files loaded successfully! Your financial data is ready for analysis.
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error loading CSV files: {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    # Show dashboard content or welcome message
    if data_loaded:
        st.markdown("---")
        
        # Add data summary
        st.sidebar.markdown("### 📊 Data Summary")
        
        if dashboard.transactions_df is not None:
            st.sidebar.success(f"✅ Transactions: {len(dashboard.transactions_df):,} records")
        
        if dashboard.net_worth_df is not None:
            st.sidebar.success(f"✅ Net Worth: {len(dashboard.net_worth_df)} months")
        
        if dashboard.investments_df is not None:
            st.sidebar.success(f"✅ Investments: {len(dashboard.investments_df)} positions")
        
        if dashboard.goals_df is not None:
            st.sidebar.success(f"✅ Goals: {len(dashboard.goals_df)} objectives")
        
        st.sidebar.markdown("---")
        
        # Navigation
        st.sidebar.markdown("### 🧭 Quick Navigation")
        nav_option = st.sidebar.radio(
            "Jump to section:",
            ["📊 Overview", "💳 Transactions", "💰 Cash Flow", "📈 Investments", "💎 Net Worth", "🎯 Goals"],
            key="nav_radio"
        )
        
        # Show the selected content
        if nav_option == "📊 Overview":
            show_dashboard_content(dashboard)
        elif nav_option == "💳 Transactions":
            show_transactions_tab(dashboard)
        elif nav_option == "💰 Cash Flow":
            show_cash_flow_tab(dashboard)
        elif nav_option == "📈 Investments":
            show_investments_tab(dashboard)
        elif nav_option == "💎 Net Worth":
            show_net_worth_tab(dashboard)
        elif nav_option == "🎯 Goals":
            show_goals_tab(dashboard)
    
    else:
        # Welcome screen
        st.markdown("---")
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <div class="metric-label">TRANSACTION ANALYSIS</div>
                <p style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                    Automatically categorize and analyze your spending patterns with beautiful visualizations
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
                <div class="metric-label">INVESTMENT TRACKING</div>
                <p style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                    Monitor your portfolio performance with real-time valuations and gain/loss analysis
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <div class="metric-label">GOAL TRACKING</div>
                <p style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                    Set and monitor progress towards your financial objectives with timeline tracking
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Getting started guide
        st.markdown("## 🚀 Getting Started")
        
        with st.container():
            st.markdown("""
            <div class="help-section">
                <h3>📝 Step-by-Step Guide</h3>
                <ol style="margin-left: 1rem;">
                    <li><strong>Prepare Your Data:</strong> Export CSV files from your bank, investment accounts, or create them manually</li>
                    <li><strong>Create ZIP File:</strong> Combine your CSV files into a single ZIP file with the exact names: transactions.csv, net_worth.csv, investments.csv, goals.csv</li>
                    <li><strong>Upload & Analyze:</strong> Upload your ZIP file and explore your financial data through interactive dashboards</li>
                    <li><strong>Generate Insights:</strong> Use filters, charts, and reports to understand your financial health</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick tips
        st.markdown("### 💡 Pro Tips")
        
        tip_col1, tip_col2 = st.columns(2)
        
        with tip_col1:
            st.markdown("""
            **📁 File Organization:**
            - Use exact file names (case-sensitive)
            - Include at least transactions.csv
            - Date format: YYYY-MM-DD preferred
            - UTF-8 encoding recommended
            """)
        
        with tip_col2:
            st.markdown("""
            **📊 Better Analysis:**
            - Include 6-12 months of data
            - Use consistent category names
            - Update data monthly
            - Keep backup copies
            """)
        
        # Sample data section
        st.markdown("---")
        st.markdown("### 📥 Don't Have Data Ready?")
        st.markdown("Download our sample ZIP file to test the dashboard with realistic financial data:")
        
        sample_zip = create_sample_zip()
        st.download_button(
            label="🎁 Download Sample Data ZIP",
            data=sample_zip,
            file_name="sample_financial_data.zip",
            mime="application/zip",
            help="Complete sample dataset with transactions, net worth, investments, and goals"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: var(--text-secondary); padding: 2rem;">
        <p>💰 Personal Finance Dashboard • Built with Streamlit & Plotly • Your data stays private on your device</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
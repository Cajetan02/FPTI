# 💰 Personal Finance Dashboard - CSV Upload Version

A comprehensive Streamlit-based personal finance dashboard that allows users to upload their own CSV files and generate insightful financial reports and visualizations.

## 🚀 Key Features

### File Upload System
- **Easy CSV Upload**: Upload your financial data through a user-friendly interface
- **Real-time Validation**: Automatic validation of CSV file formats and structures
- **Sample Templates**: Download sample CSV templates to get started quickly
- **Flexible Format Support**: Supports various date formats and handles missing optional columns

### Core Functionality
- **Transaction Analysis**: Automatically categorize and analyze uploaded transactions
- **Cash Flow Tracking**: Monitor monthly income, expenses, and net cash flow
- **Net Worth Monitoring**: Track assets, liabilities, and net worth over time
- **Investment Portfolio**: Monitor investment performance with simulated real-time valuations
- **Goal Tracking**: Set and monitor progress towards financial goals
- **Comprehensive Reports**: Generate detailed financial reports and export processed data

### Enhanced Features
- **Smart Categorization**: Automatic transaction categorization using keyword matching
- **Interactive Visualizations**: Professional charts and graphs using Plotly
- **Multi-page Navigation**: Organized sections for different financial aspects
- **Data Export**: Download processed reports in CSV format
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Error Handling**: Robust error handling and user-friendly error messages

## 📁 Required CSV File Formats

### 1. Transactions CSV (Required for core functionality)
```csv
Date,Description,Amount,Type,Category
2024-01-01,Salary Payment,5000.00,income,salary
2024-01-02,Grocery Store,-150.25,expense,grocery
2024-01-03,Gas Station,-65.80,expense,transportation
```
**Required columns:** `Date`, `Description`, `Amount`, `Type`  
**Optional columns:** `Category` (auto-generated if missing)  
**Notes:** 
- Amount: Positive for income, negative for expenses
- Type: 'income' or 'expense'
- Date: Various formats supported (YYYY-MM-DD recommended)

### 2. Net Worth CSV (Optional)
```csv
Date,Assets,Liabilities
2024-01-31,52500.00,25000.00
2024-02-29,54200.00,24800.00
```
**Required columns:** `Date`, `Assets`, `Liabilities`  
**Notes:** Net Worth is calculated automatically

### 3. Investments CSV (Optional)
```csv
Symbol,Name,Shares,Purchase_Price,Purchase_Date
AAPL,Apple Inc.,25,150.00,2024-01-15
GOOGL,Alphabet Inc.,15,120.00,2024-02-10
```
**Required columns:** `Symbol`, `Name`, `Shares`, `Purchase_Price`  
**Optional columns:** `Purchase_Date`

### 4. Goals CSV (Optional)
```csv
Goal_Name,Target_Amount,Current_Amount,Target_Date
Emergency Fund,15000,8500,2025-12-31
House Down Payment,50000,15000,2026-06-30
```
**Required columns:** `Goal_Name`, `Target_Amount`, `Current_Amount`, `Target_Date`

## 🛠 Installation & Setup

1. **Install Python dependencies**:
   ```bash
      pip install -r requirements.txt
         ```

         2. **Run the application**:
            ```bash
               streamlit run finance_dashboard.py
                  ```

                  3. **Open in browser**: Navigate to `http://localhost:8501`

                  ## 📊 How to Use

                  ### Step 1: Upload Your Data
                  1. Use the sidebar file uploaders to upload your CSV files
                  2. Start with at least a transactions CSV for basic functionality
                  3. Add other files (net worth, investments, goals) for additional insights
                  4. Download sample templates if you need examples

                  ### Step 2: Data Validation
                  - The app automatically validates your CSV structure
                  - Error messages guide you to fix any formatting issues
                  - Successfully uploaded files show a green success message

                  ### Step 3: Explore Your Data
                  Navigate through different sections:
                  - **📊 Overview**: High-level financial summary
                  - **💳 Transactions**: Detailed transaction analysis with filtering
                  - **💰 Cash Flow**: Monthly income vs expense trends
                  - **📈 Investments**: Portfolio performance and allocation
                  - **💎 Net Worth**: Assets, liabilities, and net worth tracking
                  - **🎯 Goals**: Financial goal progress monitoring
                  - **📋 Reports**: Comprehensive reports and data export

                  ### Step 4: Generate Reports
                  - View interactive charts and visualizations
                  - Filter data by date ranges, categories, and types
                  - Export processed data for external analysis
                  - Download detailed financial reports

                  ## 🎯 Dashboard Sections

                  ### Overview Page
                  - Key financial metrics at a glance
                  - Expense breakdown by category (pie chart)
                  - Net worth trend visualization
                  - Current month's financial summary

                  ### Transactions Page
                  - Complete transaction history with search and filtering
                  - Transaction trends over time
                  - Category-wise spending analysis
                  - Data validation and cleaning status

                  ### Cash Flow Page
                  - Monthly income vs expenses comparison
                  - Net cash flow trends
                  - Average monthly financial flows
                  - Visual cash flow analysis

                  ### Investments Page
                  - Portfolio allocation pie chart
                  - Individual investment performance
                  - Gain/loss analysis with percentages
                  - Total portfolio value and returns

                  ### Net Worth Page
                  - Assets, liabilities, and net worth over time
                  - Historical trend analysis
                  - Month-over-month changes
                  - Financial health indicators

                  ### Goals Page
                  - Progress bars for each financial goal
                  - Days remaining and required monthly savings
                  - Goal achievement timeline
                  - Visual progress tracking

                  ### Reports Page
                  - Comprehensive financial summaries
                  - Category-wise expense analysis
                  - Monthly averages and totals
                  - Export functionality for all data

                  ## 🧮 Automatic Calculations

                  The dashboard automatically calculates:
                  - **Net Worth**: Assets - Liabilities
                  - **Cash Flow**: Monthly income - Monthly expenses
                  - **Investment Performance**: Current value vs purchase price
                  - **Goal Progress**: (Current amount / Target amount) × 100
                  - **Required Savings**: (Remaining amount) / (Days remaining / 30.44)
                  - **Category Totals**: Spending by category with percentages

                  ## 🔧 Advanced Features

                  ### Smart Transaction Categorization
                  Automatically categorizes transactions based on description keywords:
                  - **Grocery**: Walmart, Target, Kroger, Safeway, etc.
                  - **Dining**: Restaurant, Starbucks, McDonald's, etc.
                  - **Transportation**: Gas station, Uber, Metro, etc.
                  - **Utilities**: Electric, Internet, Phone, Insurance, etc.
                  - **Entertainment**: Netflix, Movies, Spotify, etc.
                  - And many more categories...

                  ### Data Validation & Error Handling
                  - Validates CSV structure before processing
                  - Handles missing optional columns gracefully
                  - Provides clear error messages for formatting issues
                  - Supports multiple date formats
                  - Handles edge cases and data inconsistencies

                  ### Export Capabilities
                  - Download original uploaded data
                  - Export processed data with calculations
                  - Generate formatted reports
                  - Save charts and visualizations

                  ## 🔒 Data Privacy & Security

                  - **Local Processing**: All data processing happens locally on your machine
                  - **No External Servers**: Your financial data never leaves your computer
                  - **No Data Storage**: Files are processed in memory, not stored permanently
                  - **Privacy First**: Complete control over your sensitive financial information

                  ## 🚀 Customization Options

                  ### Adding New Categories
                  Modify the `category_mapping` dictionary to add new transaction categories or keywords.

                  ### Investment Price Integration
                  Replace the mock price feed with real APIs:
                  - Yahoo Finance API
                  - Alpha Vantage
                  - IEX Cloud
                  - Polygon.io

                  ### Custom Visualizations
                  The modular design allows easy addition of new charts and analysis features.

                  ## 🤝 Contributing

                  Contributions welcome! Areas for enhancement:
                  - Additional chart types and visualizations
                  - New financial metrics and KPIs
                  - Integration with banking APIs
                  - Mobile app development
                  - Machine learning for spending predictions
                  - Multi-currency support
                  - Budget planning features

                  ## 📝 License

                  Open source under the MIT License.

                  ---

                  *Transform your financial data into actionable insights with this powerful, privacy-focused dashboard!*
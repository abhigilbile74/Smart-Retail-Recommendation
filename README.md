# 🛒 Smart Market Basket Recommendation System

A Streamlit-based web application that discovers product associations using the **Apriori Algorithm** and **Association Rule Mining**. Perfect for retailers to understand customer purchasing patterns and boost cross-selling strategies.

## Features

✨ **Key Features**
- Market Basket Analysis using Apriori Algorithm
- Association Rule Mining with confidence and lift metrics
- Interactive product recommendation engine
- Real-time visualization of associations
- Top-selling products analysis
- Support/Confidence scatter plot analysis
- Downloadable association rules

## Project Structure

```
groceries/
├── app/
│   └── app.py              # Main Streamlit application
├── src/
│   ├── apriori_model.py    # Apriori algorithm implementation
│   ├── preprocess.py       # Data preprocessing utilities
│   ├── recommend.py        # Recommendation engine
│   └── visualize.py        # Visualization functions
├── data/
│   └── grocerie.csv        # Transaction data
├── notebooks/
│   └── analysis.ipynb      # Analysis notebook
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd groceries
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Locally

```bash
streamlit run app/app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Adjust Model Settings** - Use the sidebar to set:
   - Minimum Support: Controls the frequency threshold
   - Minimum Confidence: Controls the rule strength

2. **Select a Product** - Choose from the dropdown to get recommendations

3. **View Insights** - Explore visualizations and metrics:
   - Top Selling Products
   - Association Rule Insights
   - Rules Table with downloadable CSV

4. **Download Results** - Export association rules as CSV

## Dependencies

The project uses the following Python packages:

- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `numpy` - Numerical computations
- `mlxtend` - Machine learning extensions (Apriori algorithm)
- `plotly` - Interactive visualizations
- `matplotlib` - Additional visualization support
- `seaborn` - Statistical data visualization
- `networkx` - Network analysis (optional)

See [requirements.txt](requirements.txt) for complete list.

## Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your repository
4. Choose the branch and path: `app/app.py`
5. Click "Deploy"

### Deploy to Heroku

1. Create a Heroku account and install Heroku CLI
2. Run:
   ```bash
   heroku create <app-name>
   git push heroku main
   ```

### Deploy to Other Platforms

- **AWS**: Use AWS Lambda + API Gateway with container
- **Docker**: Build a Docker image for containerization
- **Azure**: Deploy using Azure App Service

## Configuration

### Streamlit Configuration

The app uses default Streamlit settings. To customize:
1. Create `.streamlit/config.toml` in the project root
2. Configure as needed (see [Streamlit docs](https://docs.streamlit.io/library/advanced-features/configuration))

### Data Path

By default, the app expects data at `data/grocerie.csv`. Ensure this file exists with columns:
- Column 0: Transaction ID (or index)
- Columns 1+: Product items in each transaction

## How It Works

### Algorithm Overview

1. **Data Preprocessing**
   - Load transaction data from CSV
   - Convert to one-hot encoded format
   - Create binary matrix (True/False for item presence)

2. **Frequent Itemsets Mining (Apriori)**
   - Find all itemsets exceeding minimum support
   - Support = Frequency of itemset / Total transactions

3. **Association Rule Generation**
   - Extract rules from frequent itemsets
   - Calculate confidence, lift, and support metrics
   - Filter by minimum confidence threshold

4. **Recommendation Engine**
   - Match selected product against rule antecedents
   - Return recommended consequent items
   - Rank by lift score

### Key Metrics

- **Support**: How often items appear together (0-1)
- **Confidence**: Probability of consequent given antecedent (0-1)
- **Lift**: How much more likely items are purchased together (>1 is strong)

## Example Use Cases

🛒 **Retail Stores**
- Improve store layout based on associations
- Create targeted bundle promotions
- Optimize shelf placement

🌾 **Grocery Chains**
- Cross-selling strategies
- Customer basket analysis
- Seasonal product associations

📊 **E-commerce**
- Personalized recommendations
- "Frequently bought together" features
- Marketing campaign optimization

## Troubleshooting

### Data File Not Found
- Ensure `data/grocerie.csv` exists in the correct location
- Check file permissions

### Module Import Errors
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility (3.8+)

### Slow Performance
- Reduce dataset size for testing
- Lower minimum support threshold incrementally
- Monitor memory usage on large datasets

## Performance Tips

- **Large Datasets**: Consider sampling transactions first
- **High Support Values**: Faster computation with fewer rules
- **Memory Issues**: Process data in chunks for massive files

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Push to GitHub
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## References

- [Streamlit Documentation](https://docs.streamlit.io)
- [MLxtend Apriori](http://rasbt.github.io/mlxtend/user_guide/frequent_patterns/apriori/)
- [Association Rule Mining](https://en.wikipedia.org/wiki/Association_rule_learning)

---

**Last Updated**: May 2026

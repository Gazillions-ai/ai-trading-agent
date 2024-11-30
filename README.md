# 🚀 AI Crypto Trading Signal System

An advanced AI-powered platform for analyzing cryptocurrency trading signals using social media sentiment and machine learning techniques.

## 🎯 Project Overview

This system analyzes social media trends and sentiment to generate cryptocurrency trading signals, combining natural language processing with technical analysis for informed trading decisions.

### Key Features

- 📊 Real-time social media sentiment analysis
- 🤖 Advanced signal generation algorithm
- 📈 Interactive dashboard visualization
- ⚡ High-performance data processing
- 🔄 Multi-platform data integration

## 🛠️ Technical Architecture

### Data Acquisition
- Twitter trends analysis via RapidAPI
- CoinGecko market data integration
- Configurable data collection parameters

### Analysis Engine
- VADER sentiment analysis
- Multi-factor signal generation
- Engagement impact calculation
- Batch processing capabilities

### Visualization
- Interactive Streamlit dashboard
- Real-time signal monitoring
- Performance metrics tracking

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Gazillions-ai/ai-trading-agent.git
   cd ai-trading-agent
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   env\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up configuration:
   - Copy `config.example.py` to `config.py`
   - Add your API keys and customize settings

### Running the System

1. Start data collection:
   ```bash
   python main.py collect
   ```

2. Generate signals:
   ```bash
   python main.py analyze
   ```

3. Launch dashboard:
   ```bash
   python -m streamlit run dashboard/crypto_dashboard.py
   ```

## 📁 Project Structure

```
ai-trading-agent/
├── data/                  # Data storage
│   ├── raw/              # Raw API data
│   ├── processed/        # Processed data
│   ├── analysis/         # Analysis results
│   └── signals/          # Trading signals
├── data_acquisition/     # Data collection
│   ├── parse_twitter_trends.py
│   ├── coingecko_api.py
│   └── rapidapi_twitter135.py
├── analysis/            # Analysis modules
│   ├── sentiment_analyzer.py
│   ├── signal_generator.py
│   └── __init__.py
├── dashboard/          # Visualization
│   └── crypto_dashboard.py
├── utils/             # Utilities
│   └── logger.py
├── config.py          # Configuration
├── main.py            # Main script
└── requirements.txt   # Dependencies
```

## 🔧 Configuration

Key configuration options in `config.py`:
- API credentials
- Data collection parameters
- Signal generation thresholds
- Performance optimization settings

## 📊 Performance Metrics

- Processing time: ~0.01-0.02 seconds per batch
- Memory efficient design
- Scalable architecture

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- VADER Sentiment for NLP analysis
- Streamlit for dashboard framework
- Plotly for interactive visualizations

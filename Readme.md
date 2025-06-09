# Real-Time Bidding (RTB) Bidding System

This repository contains our submission for the RTB Hackathon. Our system leverages historical data to predict CTR, CVR, and the market price of ad impressions. Based on these predictions, the bidding engine makes real-time bid decisions under budget constraints.

------------------------------------------------------------
Team: Access Denied (+91 83750 80625)
------------------------------------------------------------
Members: 
1. Samay Jain (23/MC/128)
2. Ibrahim Haneef (23/IT/72)
3. Mohd Hassan (23/IT/100)
4. Hemant Singh (23/IT/69)

------------------------------------------------------------
Table of Contents
------------------------------------------------------------
1. Project Overview
2. File Descriptions
3. Installation & Setup
4. Usage Instructions
5. Testing the Bidding Engine
6. Additional Information

------------------------------------------------------------
1. Project Overview
------------------------------------------------------------
Our RTB system processes bid requests in real time by:
- Predicting CTR: The probability that an ad impression results in a click.
- Predicting CVR: The probability that a click leads to a conversion.
- Estimating Market Price: The expected second-highest bid (i.e., the price paid in a second-price auction).

Using these predictions, we calculate the Expected Value (EV) for a bid as follows:

    EV = CTR + N * CVR

For example, for a Tire company (AdvertiserID = "3476") where the conversion weight N = 10, the overall score becomes:

    Score = Clicks + 10 * Conversions

If the EV (or the EV-to-market-price ratio) exceeds a defined threshold, the system bids slightly above the predicted market price.

------------------------------------------------------------
2. File Descriptions
------------------------------------------------------------
- bid.py
  Implements the Bid class. This class:
    - Loads pre-trained models and preprocessing objects.
    - Extracts features from a bid request.
    - Predicts CTR, CVR, and market price.
    - Computes EV and makes a bid decision (returns a bid price or -1 if no bid).

- bidder.py
  Defines the Bidder interface with the abstract method getBidPrice(bidRequest: BidRequest) -> int. The Bid class inherits from this interface.

- bidrequest.py
  Contains the BidRequest class that encapsulates all the information related to a bid request (e.g., bidId, timestamp, visitorId, userAgent, ad slot attributes, etc.). Note: BidID is used as the primary key for merging data across logs.

- model_training.ipynb
  A Jupyter Notebook that:
    - Loads bid, impression, click, and conversion logs in chunks (100,000 rows per chunk).
    - Extracts features in batches of 50,000 rows.
    - Performs data cleaning, feature engineering, and memory optimization.
    - Trains three LightGBM models (CTR, CVR, and Market Price) and evaluates them.
    - Saves the models and preprocessing objects to disk.

- test_bid.py
  A test script that simulates sample bid requests. It:
    - Instantiates a BidRequest with realistic sample data.
    - Creates an instance of the Bid class.
    - Calls getBidPrice() and prints the resulting bid price.
    
    Organizers can run this script to quickly verify the functionality of our bidding engine.

- ctr_model.pkl, cvr_model.pkl, market_price_model.pkl
  Pre-trained LightGBM models for predicting CTR, CVR, and market price, respectively.

- label_encoders.pkl
  Contains the saved label encoders used to transform categorical features.

- scaler.pkl
  Contains the saved scaler used for normalizing numerical features.

- requirements.txt
  Lists all Python dependencies (e.g., pandas, numpy, scikit-learn, lightgbm, joblib, tqdm).
------------------------------------------------------------
NOTE: The models used for prediction have only been trained on a single day's data i.e. 06.06.2023 due to resource and time constraint. Training our model on the entire dataset would greatly benefit in increasing accuracy and improving prediction reliability.

------------------------------------------------------------
3. Installation & Setup
------------------------------------------------------------
1. Clone or extract the ZIP file.
2. Install dependencies by running:

       pip install -r requirements.txt

------------------------------------------------------------
4. Usage Instructions
------------------------------------------------------------
### Training (Optional)
If you wish to retrain the models, open and run the model_training.ipynb notebook. Running this notebook will process the data in chunks (100,000 rows per chunk for loading and 50,000 rows per chunk for feature extraction), perform feature engineering (using BidID as the primary key), and save the following files:
    - ctr_model.pkl
    - cvr_model.pkl
    - market_price_model.pkl
    - label_encoders.pkl
    - scaler.pkl

### Running the Bidding Engine
The bid.py file contains the implementation of the bidding logic, which can be integrated into a larger real-time system. It relies on the saved model files and preprocessing objects.

------------------------------------------------------------
5. Testing the Bidding Engine
------------------------------------------------------------
To test our system with sample bid requests, run the test script after going to the directory of bidding folder:

       python test_bid.py

This script creates a sample BidRequest, passes it to our Bid class, and prints out the resulting bid price. This allows the users to verify that our system is working as expected.

------------------------------------------------------------
6. Additional Information
------------------------------------------------------------
- Model & Feature Engineering Justification:
    Our feature engineering includes:
      - Time-based features (hour, day of week, is_weekend) to capture user activity patterns.
      - User-Agent derived features (is_mobile, is_chrome, is_firefox, is_safari) to determine device and browser types.
      - Ad slot features (ad_area computed from adSlotWidth and adSlotHeight, adSlotFloorPrice, and is_premium_ad) that affect the ad’s performance.
      - Categorical features (Region, City, Adexchange, Domain, URL, AdslotID, Adslotvisibility, Adslotformat, CreativeID, AdvertiserID) are label encoded.
    
    These features were selected based on domain expertise and validated through exploratory data analysis (EDA). Detailed EDA findings and visualizations are provided in the Documentation_Access_Denied document.
    
- Performance Metrics:
    - CTR Model: ROC AUC, PR-AUC
    - CVR Model: ROC AUC, PR-AUC
    - Market Price Model: RMSE
    (Full evaluation details are available in model_training.ipynb.)
    
- Budget Pacing & Bid Decision:
    Our bidding engine ensures that bids are only placed if sufficient budget remains. When the computed expected value (EV) exceeds the threshold, the system bids slightly above the predicted market price.

------------------------------------------------------------
For any questions or further clarifications, please refer to the code comments or contact our team.


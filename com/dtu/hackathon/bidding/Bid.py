from BidRequest import BidRequest
from Bidder import Bidder
import joblib
import numpy as np
import os
from datetime import datetime
import pandas as pd

def extract_features_from_bidrequest(bidRequest, label_encoders, scaler):
    from datetime import datetime
    import pandas as pd

    data = {}
    try:
        ts = datetime.strptime(bidRequest.timestamp, '%Y%m%d%H%M%S%f')
    except Exception:
        ts = None

    if ts:
        data['hour'] = ts.hour
        data['day_of_week'] = ts.weekday()
        data['is_weekend'] = 1 if ts.weekday() in [5, 6] else 0
    else:
        data['hour'] = -1
        data['day_of_week'] = -1
        data['is_weekend'] = 0
    ua = bidRequest.userAgent if bidRequest.userAgent else 'unknown'
    data['is_mobile'] = 1 if ('Mobile' in ua or 'Android' in ua or 'iOS' in ua) else 0
    data['is_chrome'] = 1 if 'Chrome' in ua else 0
    data['is_firefox'] = 1 if 'Firefox' in ua else 0
    data['is_safari'] = 1 if 'Safari' in ua else 0
    try:
        width = float(bidRequest.adSlotWidth)
    except Exception:
        width = 0.0
    try:
        height = float(bidRequest.adSlotHeight)
    except Exception:
        height = 0.0
    data['Adslotwidth'] = width
    data['Adslotheight'] = height
    data['ad_area'] = width * height
    try:
        data['Adslotfloorprice'] = float(bidRequest.adSlotFloorPrice)
    except Exception:
        data['Adslotfloorprice'] = 0.0
    data['is_premium_ad'] = 1 if (width * height) >= 100000 else 0


    cat_features = ['Region', 'City', 'Adexchange', 'Domain', 'URL',
                    'AdslotID', 'Adslotvisibility', 'Adslotformat', 'CreativeID', 'AdvertiserID']
    data['Region'] = bidRequest.region if bidRequest.region else 'unknown'
    data['City'] = bidRequest.city if bidRequest.city else 'unknown'
    data['Adexchange'] = bidRequest.adExchange if bidRequest.adExchange else 'unknown'
    data['Domain'] = bidRequest.domain if bidRequest.domain else 'unknown'
    data['URL'] = bidRequest.url if bidRequest.url else 'unknown'
    data['AdslotID'] = bidRequest.adSlotID if bidRequest.adSlotID else 'unknown'
    data['Adslotvisibility'] = bidRequest.adSlotVisibility if bidRequest.adSlotVisibility else 'unknown'
    data['Adslotformat'] = bidRequest.adSlotFormat if bidRequest.adSlotFormat else 'unknown'
    data['CreativeID'] = bidRequest.creativeID if bidRequest.creativeID else 'unknown'
    data['AdvertiserID'] = bidRequest.advertiserId if bidRequest.advertiserId else 'unknown'

    for col in cat_features:
        if col in label_encoders:
            encoder = label_encoders[col]
            try:
                data[col] = int(encoder.transform([data[col]])[0])
            except Exception:
                data[col] = 0
        else:
            data[col] = 0

    data['Biddingprice'] = 0.0 
    df = pd.DataFrame([data])
    # print("Features being used:", df.columns.tolist())

    num_cols = ['Adslotwidth', 'Adslotheight', 'ad_area', 'Adslotfloorprice']
    df[num_cols] = scaler.transform(df[num_cols])
    
    return df

class Bid(Bidder):

    def __init__(self):
        # Bidder parameters, you can adjust these as needed
        self.bidRatio = 50  # This can be used to randomize bidding if desired
        self.fixedBidPrice = 300  # Fallback fixed bid price

    
        # Budget information (for example, $10,000)
        self.initial_budget = 10000.0
        self.remaining_budget = self.initial_budget

        # Load models and preprocessing objects.
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
        
        # Load the pre-trained models and preprocessing objects from the root folder.
        self.ctr_model = joblib.load(os.path.join(base_path, 'ctr_model.pkl'))
        self.cvr_model = joblib.load(os.path.join(base_path, 'cvr_model.pkl'))
        self.market_price_model = joblib.load(os.path.join(base_path, 'market_price_model.pkl'))
        self.label_encoders = joblib.load(os.path.join(base_path, 'label_encoders.pkl'))
        self.scaler = joblib.load(os.path.join(base_path,'scaler.pkl'))


        self.advertiser_conversion_weight = {
            "3476": 10 ,
            "1458": 0,
            "3358":2,
            "3386":0,
            "3427":0
            
        }
    
    def getBidPrice(self, bidRequest: BidRequest) -> int:
        
        #Given a BidRequest, return the bid price in dollars (as an integer) if a bid is placed,
        #or -1 if no bid is placed.
       
        # Check budget pacing: if not enough budget, do not bid.
        if self.remaining_budget <= 0:
            return -1
        
        # Extract features from the bid request.
        features = extract_features_from_bidrequest(bidRequest, self.label_encoders, self.scaler)
        print(features.shape)  # Should match model n_features_ (23)

        
        ctr = self.ctr_model.predict_proba(features)[:, 1][0]      # probability of click
        cvr = self.cvr_model.predict_proba(features)[:, 1][0]        # probability of conversion given click
        market_price_pred = self.market_price_model.predict(features)[0]  # predicted market price
        
        # Get conversion weight (N) for the advertiser; default to 1 if not defined.
        N = self.advertiser_conversion_weight.get(bidRequest.advertiserId, 1)
        
        # Compute the expected value (EV) for the bid.
        ev = ctr + N * cvr  
        
        # Decide whether to bid.
        threshold = 0.05
        ratio = ev / market_price_pred if market_price_pred > 0 else 0

        # Debug prints can be removed in production to meet the execution time requirement.
        # uncommented below print statement only if you want to see the CVR ,CTR and Market Value 
        print(f"CTR: {ctr}, CVR: {cvr}, Market Price: {market_price_pred}, EV: {ev}, Ratio: {ratio}")

        if ratio > threshold:
            # Place a bid.
            # Set the bid price slightly above the predicted market price.
            bid_price = market_price_pred * 1.02  # For example, 2% higher.
            if bid_price > self.remaining_budget:
                return -1
            return int(round(bid_price))
        else:
            return -1

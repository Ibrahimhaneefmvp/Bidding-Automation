from BidRequest import BidRequest
from Bid import Bid

def main():
    #Create a sample bid request.
    bid_request = BidRequest()
    
    # Populate the bid request with example data.
    bid_request.bidId = "01460000800000000000000000000001"
    bid_request.timestamp = "202310101200000000"
    bid_request.visitorId = "35605620124522340227135"
    bid_request.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    bid_request.ipAddress = "118.81.189.1"
    bid_request.region = "15"
    bid_request.city = "16"
    bid_request.adExchange = "2"
    bid_request.domain = "e80f4ac7c01ad1a049"
    bid_request.url = "hz55b010003d6f274121"
    bid_request.adSlotID = "21476898764813"
    bid_request.adSlotWidth = "300"
    bid_request.adSlotHeight = "250"
    bid_request.adSlotVisibility = "SecondView"
    bid_request.adSlotFormat = "Fixed"
    bid_request.adSlotFloorPrice = "0"
    bid_request.creativeID = "e39e178dfd1ee56acd"
    bid_request.advertiserId = "3476"
    bidder = Bid()
    bid_price = bidder.getBidPrice(bid_request)
    print(f"\nBid Price: {bid_price}")

   # Second Request 
    bid_request = BidRequest()
    bid_request.bidId = "01460000800000000000000000000001"
    bid_request.timestamp = "202310101200000000" #peak hour time
    bid_request.visitorId = "35605620124522340227135"
    bid_request.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    bid_request.ipAddress = "118.81.189.1"
    bid_request.region = "1"
    bid_request.city = "1"
    bid_request.adExchange = "1"
    bid_request.domain = "premium_domain_123"
    bid_request.url = "premium_url_456"
    bid_request.adSlotID = "premium_slot_789"
    bid_request.adSlotWidth = "728"
    bid_request.adSlotHeight = "90"
    bid_request.adSlotVisibility = "FirstView"
    bid_request.adSlotFormat = "Fixed"
    bid_request.adSlotFloorPrice = "5"
    bid_request.creativeID = "premium_creative_xyz"
    bid_request.advertiserId = "3476"
    bidder = Bid()
    bid_price = bidder.getBidPrice(bid_request)
    print(f"\nBid Price: {bid_price}")


# Third Request 
    bid_request = BidRequest()
    bid_request.bidId = "c7654fe86bc7f66d75242d5e12a6aad4"
    bid_request.timestamp = "20130606000110312"
    bid_request.visitorId = "Vh1OPiSeP2kfQGj"
    bid_request.userAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1"
    bid_request.ipAddress = "49.223.203.*"
    bid_request.region = "40"
    bid_request.city = "42"
    bid_request.adExchange = "1"
    bid_request.domain = "trqRTvpogNlyDok4JKTI"
    bid_request.url = "97dca58e0df8652a255d11ddb5732483"
    bid_request.adSlotID = "mm_10032051_2374052_9577342"
    bid_request.adSlotWidth = "950"
    bid_request.adSlotHeight = "900"
    bid_request.adSlotVisibility = "1"
    bid_request.adSlotFormat = "1"
    bid_request.adSlotFloorPrice = "3"
    bid_request.creativeID = "c938195f9e404b4f38c7e71bf50263e5"
    bid_request.advertiserId = "3476"
    bidder = Bid()
    bid_price = bidder.getBidPrice(bid_request)
    print(f"\nBid Price: {bid_price}")


if __name__ == "__main__":
    main()
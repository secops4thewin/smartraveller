# smartraveller
This python script is used to scrape smartraveller.gov.au to pull out information and risk rating as it pertains to the safety of travel.  The csv will be updated daily so that you can integrate the data with your SIEM and proactively email users of VPNs to alert them of any dangers of their visit.

If you import this into Splunk then a simple script can be performed below.

index=main sourcetype="vpn" | head 100 | iplocation srcip | lookup smartraveller Country OUTPUTNEW | stats values(src_ip) by Country, City, risk_rating, text

Note: In your lookup definition untick case sensitive matches

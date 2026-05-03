"""
Complete NSE F&O Stock List - Updated May 2026
Contains all actively traded F&O stocks with proper Yahoo Finance tickers
"""

NSE_FNO_STOCKS = [
    # Nifty 50 Core
    'RELIANCE.NS',      # Reliance Industries
    'HDFCBANK.NS',      # HDFC Bank
    'BHARTIARTL.NS',    # Bharti Airtel
    'SBIN.NS',          # State Bank of India
    'ICICIBANK.NS',     # ICICI Bank
    'TCS.NS',           # Tata Consultancy Services
    'BAJFINANCE.NS',    # Bajaj Finance
    'LT.NS',            # Larsen & Toubro
    'HINDUNILVR.NS',    # Hindustan Unilever
    'LICI.NS',          # LIC of India
    'INFY.NS',          # Infosys
    'SUNPHARMA.NS',     # Sun Pharmaceutical
    'ADANIPOWER.NS',    # Adani Power
    'MARUTI.NS',        # Maruti Suzuki
    'ITC.NS',           # ITC
    'AXISBANK.NS',      # Axis Bank
    'TITAN.NS',         # Titan
    'NTPC.NS',          # NTPC
    'M&M.NS',           # Mahindra & Mahindra
    'ADANIPORTS.NS',    # Adani Ports & SEZ
    'KOTAKBANK.NS',     # Kotak Bank
    'ONGC.NS',          # Oil & Natural Gas Corporation
    'ULTRACEMCO.NS',    # UltraTech Cement
    'HCLTECH.NS',       # HCL Technologies
    'BEL.NS',           # Bharat Electronics
    'ADANIENT.NS',      # Adani Enterprises
    'JSWSTEEL.NS',      # JSW Steel
    'DMART.NS',         # Avenue Supermarts DMart
    'COALINDIA.NS',     # Coal India
    'POWERGRID.NS',     # Power Grid Corporation
    'HAL.NS',           # Hindustan Aeronautics
    'NESTLEIND.NS',     # Nestle
    'BAJAJFINSV.NS',    # Bajaj Finserv
    'BAJAJ-AUTO.NS',    # Bajaj Auto
    'TATASTEEL.NS',     # Tata Steel
    'HINDZINC.NS',      # Hindustan Zinc
    'ETERNALIT.NS',     # Eternal (IT Services)
    'ASIANPAINT.NS',    # Asian Paints
    'HINDALCO.NS',      # Hindalco Industries
    'SHRIRAMFIN.NS',    # Shriram Finance
    'WIPRO.NS',         # Wipro
    'ADANIGREEN.NS',    # Adani Green Energy
    'IOC.NS',           # Indian Oil Corporation
    'EICHERMOT.NS',     # Eicher Motors
    'GRASIM.NS',        # Grasim Industries
    'SBILIFE.NS',       # SBI Life Insurance
    'VBL.NS',           # Varun Beverages
    'DIVISLAB.NS',      # Divis Laboratories
    'INDIGO.NS',        # Interglobe Aviation
    'TVSMOTOR.NS',      # TVS Motors

    # Additional F&O Stocks
    'ADANIENSOL.NS',    # Adani Energy Solutions
    'JIOFIN.NS',        # Jio Financial Services
    'ABB.NS',           # ABB
    'POWERINDIA.NS',    # Hitachi Energy (formerly ABB Power)
    'BSE.NS',           # BSE
    'PFC.NS',           # Power Finance Corporation
    'HYUNDAI.NS',       # Hyundai Motor India
    'TRENT.NS',         # Trent
    'CUMMINSIND.NS',    # Cummins
    'DLF.NS',           # DLF
    'TECHM.NS',         # Tech Mahindra
    'TATAPOWER.NS',     # Tata Power
    'TORNTPHARM.NS',    # Torrent Pharmaceuticals
    'PIDILITIND.NS',    # Pidilite Industries
    'SOLARINDS.NS',     # Solar Industries
    'BRITANNIA.NS',     # Britannia Industries
    'MUTHOOTFIN.NS',    # Muthoot Finance
    'BANKBARODA.NS',    # Bank of Baroda
    'IRFC.NS',          # IRFC
    'SIEMENS.NS',       # Siemens
    'CHOLAFIN.NS',      # Cholamandalam Investment
    'BPCL.NS',          # Bharat Petroleum
    'CGPOWER.NS',       # CG Power & Industrial Solutions
    'MOTHERSON.NS',     # Samvardhana Motherson International
    'UNIONBANK.NS',     # Union Bank of India
    'HDFCLIFE.NS',      # HDFC Life Insurance
    'LTIM.NS',          # LTIMindtree
    'TATAMTRDVR.NS',    # Tata Motors DVR
    'PNB.NS',           # Punjab National Bank
    'JINDALSTEL.NS',    # Jindal Steel
    'BHEL.NS',          # Bharat Heavy Electricals
    'CANBK.NS',         # Canara Bank
    'POLYCAB.NS',       # Polycab
    'HDFCAMC.NS',       # HDFC AMC
    'INDIANB.NS',       # Indian Bank
    'BAJAJHLDNG.NS',    # Bajaj Holdings & Investments
    'TATACONSUM.NS',    # Tata Consumer Products
    'IDEA.NS',          # Vodafone Idea
    'DRREDDY.NS',       # Dr Reddys Laboratories
    'MAZAGON.NS',       # Mazagon Dock Shipbuilders
    'APOLLOHOSP.NS',    # Apollo Hospitals
    'AMBUJACEM.NS',     # Ambuja Cements
    'GODREJCP.NS',      # Godrej Consumer Products
    'INDUSTOWER.NS',    # Indus Towers
    'GAIL.NS',          # GAIL
    'VEDL.NS',          # Vedanta
    'BOSCHLTD.NS',      # Bosch
    'CIPLA.NS',         # Cipla
    'LUPIN.NS',         # Lupin
    'HEROMOTOCO.NS',    # Hero Motocorp
    'GMR.NS',           # GMR Airports (GMR Infra)
    'MARICO.NS',        # Marico
    'JSWENERGY.NS',     # JSW Energy
    'MAXHEALTH.NS',     # Max Healthcare Institute
    'MCDOWELL-N.NS',    # United Spirits
    'ASHOKLEY.NS',      # Ashok Leyland
    'RECLTD.NS',        # REC
    'MANKIND.NS',       # Mankind Pharma
    'INDHOTEL.NS',      # Indian Hotels Company
    'ABCAPITAL.NS',     # Aditya Birla Capital
    'BEL.NS',           # Bharat Forge (duplicate check needed)
    'ZYDUSLIFE.NS',     # Zydus Life Science
    'WAAREEENER.NS',    # Waaree Energies
    'LODHA.NS',         # Lodha Developers (Macrotech Developers)
    'ICICIGI.NS',       # ICICI Lombard General Insurance
    'SHREECEM.NS',      # Shree Cement
    'OFSS.NS',          # Oracle Financial Services Software
    'NHPC.NS',          # NHPC
    'AUROPHARMA.NS',    # Aurobindo Pharma
    'OIL.NS',           # Oil India
    'HINDPETRO.NS',     # Hindustan Petroleum
    'NMDC.NS',          # NMDC
    'DABUR.NS',         # Dabur India
    'HAVELLS.NS',       # Havells
    'POLICYBZR.NS',     # PB FinTech
    'SAIL.NS',          # Steel Authority of India
    'SUZLON.NS',        # Suzlon Energy
    'AUBANK.NS',        # AU Small Finance Bank
    'NYKAA.NS',         # Nykaa
    'MCX.NS',           # MCX
    'PERSISTENT.NS',    # Persistent Systems
    'SRF.NS',           # SRF
    'SWIGGY.NS',        # Swiggy
    'ICICIPRULI.NS',    # ICICI Prudential Life Insurance
    'NATIONALUM.NS',    # NALCO
    'INDUSINDBK.NS',    # Indusind Bank
    'FEDERALBNK.NS',    # Federal Bank
    'PAYTM.NS',         # One 97 Communications (Paytm)
    'L&TFH.NS',         # L&T Finance
    'FORTIS.NS',        # Fortis Healthcare
    'GLENMARK.NS',      # Glenmark Pharmaceuticals
    'DIXON.NS',         # Dixon Technologies
    'ALKEM.NS',         # Alkem Laboratories
    'NAM-INDIA.NS',     # Nippon Life India AMC
    'UNOMINDA.NS',      # UNO Minda
    'BANKINDIA.NS',     # Bank of India
    'PHOENIXLTD.NS',    # Phoenix Mills
    'NAUKRI.NS',        # Info Edge
    'YESBANK.NS',       # Yes Bank
    'RVNL.NS',          # Rail Vikas Nigam
    'SBICARD.NS',       # SBI Cards
    'PRESTIGE.NS',      # Prestige Estates Projects
    'OBEROIRLTY.NS',    # Oberoi Realty
    'IDFCFIRSTB.NS',    # IDFC First Bank
    'LAURUSLABS.NS',    # Laurus Labs
    'BIOCON.NS',        # Biocon
    'VLMM.NS',          # Vishal Mega Mart
    'TIINDIA.NS',       # Tube Investment
    'COLPAL.NS',        # Colgate Palmolive
    'GODREJPROP.NS',    # Godrej Properties
    'MFSL.NS',          # Max Financial Services
    'UPL.NS',           # UPL
    'APLAPOLLO.NS',     # APL Apollo Tubes
    'BDL.NS',           # Bharat Dynamics
    'PATANJALI.NS',     # Patanjali Foods
    'MOTILALOFS.NS',    # Motilal Oswal Financial Services
    'VOLTAS.NS',        # Voltas
    'KEIIND.NS',        # KEI Industries
    'PIIND.NS',         # PI Industries
    'PREMIERENE.NS',    # Premier Energies
    'SUPREMEIND.NS',    # Supreme Industries
    'COCHINSHIP.NS',    # Cochin Shipyard
    'MPHASIS.NS',       # Mphasis
    'KALYANKJIL.NS',    # Kalyan Jewellers
    '360ONE.NS',        # 360 One WAM
    'PETRONET.NS',      # Petronet LNG
    'ASTRAL.NS',        # Astral
    'PAGEIND.NS',       # Page Industries
    'COFORGE.NS',       # Coforge
    'CONCOR.NS',        # Container Corporation of India
    'IREDA.NS',         # IREDA
    'SONACOMS.NS',      # Sona BLW Precision Forgings
    'BLUESTARCO.NS',    # Blue Star
    'DALBHARAT.NS',     # Dalmia Bharat
    'GODFRYPHLP.NS',    # Godfrey Phillips
    'DELHIVERY.NS',     # Delhivery
    'BANDHANBNK.NS',    # Bandhan Bank
    'JUBLFOOD.NS',      # Jubilant FoodWorks
    'EXIDEIND.NS',      # Exide Industries
    'LICHSGFIN.NS',     # LIC Housing Finance
    'AMBER.NS',         # Amber Enterprises
    'ANGELONE.NS',      # Angel One
    'PNBHOUSING.NS',    # PNB Housing Finance
    'KAYNES.NS',        # Kaynes Technology India
    'CDSL.NS',          # CDSL
    'FORCEMOT.NS',      # Force Motors
    'TATAELXSI.NS',     # Tata Elxsi
    'MANAPPURAM.NS',    # Manappuram Finance
    'NBCC.NS',          # NBCC
    'NUVAMA.NS',        # Nuvama Wealth Management
    'KPITTECH.NS',      # KPIT Technologies
    'RBLBANK.NS',       # RBL Bank
    'CAMS.NS',          # CAMS
    'CROMPTON.NS',      # Crompton Greaves
    'INOXWIND.NS',      # Inox Wind
    'SAMMAAN.NS',       # Sammaan Capital
    'KFINTECH.NS',      # KFin Technologies
    'PGEL.NS',          # PG Electroplast
    'IEX.NS',           # Indian Energy Exchange
]

# Remove duplicates and sort
NSE_FNO_STOCKS = sorted(list(set(NSE_FNO_STOCKS)))

# Create version without .NS suffix for Upstox/other APIs
NSE_FNO_SYMBOLS = [stock.replace('.NS', '') for stock in NSE_FNO_STOCKS]

if __name__ == "__main__":
    print(f"Total F&O stocks: {len(NSE_FNO_STOCKS)}")
    print(f"Total symbols: {len(NSE_FNO_SYMBOLS)}")

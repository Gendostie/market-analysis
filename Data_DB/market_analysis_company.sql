-- MySQL dump 10.13  Distrib 5.7.12, for Win32 (AMD64)
--
-- Host: localhost    Database: market_analysis
-- ------------------------------------------------------
-- Server version	5.7.15-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `symbol` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `is_in_snp500` tinyint(1) DEFAULT '0',
  `last_update_historic` datetime DEFAULT NULL,
  PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES ('A','Agilent Technologies Inc',1,NULL),('AAL','American Airlines Group',1,NULL),('AAP','Advance Auto Parts',1,NULL),('AAPL','Apple Inc.',1,NULL),('ABBV','AbbVie',1,NULL),('ABC','AmerisourceBergen Corp',1,NULL),('ABT','Abbott Laboratories',1,NULL),('ACN','Accenture plc',1,NULL),('ADBE','Adobe Systems Inc',1,NULL),('ADI','Analog Devices, Inc.',1,NULL),('ADM','Archer-Daniels-Midland Co',1,NULL),('ADP','Automatic Data Processing',1,NULL),('ADS','Alliance Data Systems',1,NULL),('ADSK','Autodesk Inc',1,NULL),('AEE','Ameren Corp',1,NULL),('AEP','American Electric Power',1,NULL),('AES','AES Corp',1,NULL),('AET','Aetna Inc',1,NULL),('AFL','AFLAC Inc',1,NULL),('AGN','Allergan plc',1,NULL),('AIG','American International Group, Inc.',1,NULL),('AIV','Apartment Investment & Mgmt',1,NULL),('AIZ','Assurant Inc',1,NULL),('AJG','Arthur J. Gallagher & Co.',1,NULL),('AKAM','Akamai Technologies Inc',1,NULL),('ALB','Albemarle Corp',1,NULL),('ALK','Alaska Air Group Inc',1,NULL),('ALL','Allstate Corp',1,NULL),('ALLE','Allegion',1,NULL),('ALXN','Alexion Pharmaceuticals',1,NULL),('AMAT','Applied Materials Inc',1,NULL),('AME','Ametek',1,NULL),('AMG','Affiliated Managers Group Inc',1,NULL),('AMGN','Amgen Inc',1,NULL),('AMP','Ameriprise Financial',1,NULL),('AMT','American Tower Corp A',1,NULL),('AMZN','Amazon.com Inc',1,NULL),('AN','AutoNation Inc',1,NULL),('ANTM','Anthem Inc.',1,NULL),('AON','Aon plc',1,NULL),('APA','Apache Corporation',1,NULL),('APC','Anadarko Petroleum Corp',1,NULL),('APD','Air Products & Chemicals Inc',1,NULL),('APH','Amphenol Corp A',1,NULL),('ARNC','Arconic Inc',1,NULL),('ATVI','Activision Blizzard',1,NULL),('AVB','AvalonBay Communities, Inc.',1,NULL),('AVGO','Broadcom',1,NULL),('AVY','Avery Dennison Corp',1,NULL),('AWK','American Water Works Company Inc',1,NULL),('AXP','American Express Co',1,NULL),('AYI','Acuity Brands Inc',1,NULL),('AZO','AutoZone Inc',1,NULL),('BA','Boeing Company',1,NULL),('BAC','Bank of America Corp',1,NULL),('BAX','Baxter International Inc.',1,NULL),('BBBY','Bed Bath & Beyond',1,NULL),('BBT','BB&T Corporation',1,NULL),('BBY','Best Buy Co. Inc.',1,NULL),('BCR','Bard (C.R.) Inc.',1,NULL),('BDX','Becton Dickinson',1,NULL),('BEN','Franklin Resources',1,NULL),('BF-B','Brown-Forman Corporation',1,NULL),('BHI','Baker Hughes Inc',1,NULL),('BIIB','BIOGEN IDEC Inc.',1,NULL),('BK','The Bank of New York Mellon Corp.',1,NULL),('BLK','BlackRock',1,NULL),('BLL','Ball Corp',1,NULL),('BMY','Bristol-Myers Squibb',1,NULL),('BRK-B','Berkshire Hathaway',1,NULL),('BSX','Boston Scientific',1,NULL),('BWA','BorgWarner',1,NULL),('BXP','Boston Properties',1,NULL),('C','Citigroup Inc.',1,NULL),('CA','CA, Inc.',1,NULL),('CAG','ConAgra Foods Inc.',1,NULL),('CAH','Cardinal Health Inc.',1,NULL),('CAT','Caterpillar Inc.',1,NULL),('CB','Chubb Limited',1,NULL),('CBG','CBRE Group',1,NULL),('CBS','CBS Corp.',1,NULL),('CCI','Crown Castle International Corp.',1,NULL),('CCL','Carnival Corp.',1,NULL),('CELG','Celgene Corp.',1,NULL),('CERN','Cerner',1,NULL),('CF','CF Industries Holdings Inc',1,NULL),('CFG','Citizens Financial Group',1,NULL),('CHD','Church & Dwight',1,NULL),('CHK','Chesapeake Energy',1,NULL),('CHRW','C. H. Robinson Worldwide',1,NULL),('CHTR','Charter Communications',1,NULL),('CI','CIGNA Corp.',1,NULL),('CINF','Cincinnati Financial',1,NULL),('CL','Colgate-Palmolive',1,NULL),('CLX','The Clorox Company',1,NULL),('CMA','Comerica Inc.',1,NULL),('CMCSA','Comcast A Corp',1,NULL),('CME','CME Group Inc.',1,NULL),('CMG','Chipotle Mexican Grill',1,NULL),('CMI','Cummins Inc.',1,NULL),('CMS','CMS Energy',1,NULL),('CNC','Centene Corporation',1,NULL),('CNP','CenterPoint Energy',1,NULL),('COF','Capital One Financial',1,NULL),('COG','Cabot Oil & Gas',1,NULL),('COH','Coach Inc.',1,NULL),('COL','Rockwell Collins',1,NULL),('COO','The Cooper Companies',1,NULL),('COP','ConocoPhillips',1,NULL),('COST','Costco Co.',1,NULL),('COTY','Coty, Inc',1,NULL),('CPB','Campbell Soup',1,NULL),('CRM','Salesforce.com',1,NULL),('CSCO','Cisco Systems',1,NULL),('CSRA','CSRA Inc.',1,NULL),('CSX','CSX Corp.',1,NULL),('CTAS','Cintas Corporation',1,NULL),('CTL','CenturyLink Inc',1,NULL),('CTSH','Cognizant Technology Solutions',1,NULL),('CTXS','Citrix Systems',1,NULL),('CVS','CVS Health',1,NULL),('CVX','Chevron Corp.',1,NULL),('CXO','Concho Resources',1,NULL),('D','Dominion Resources',1,NULL),('DAL','Delta Air Lines',1,NULL),('DD','Du Pont (E.I.)',1,NULL),('DE','Deere & Co.',1,NULL),('DFS','Discover Financial Services',1,NULL),('DG','Dollar General',1,NULL),('DGX','Quest Diagnostics',1,NULL),('DHI','D. R. Horton',1,NULL),('DHR','Danaher Corp.',1,NULL),('DIS','The Walt Disney Company',1,NULL),('DISCA','Discovery Communications-A',1,NULL),('DISCK','Discovery Communications-C',1,NULL),('DLPH','Delphi Automotive',1,NULL),('DLR','Digital Realty Trust',1,NULL),('DLTR','Dollar Tree',1,NULL),('DNB','Dun & Bradstreet',1,NULL),('DOV','Dover Corp.',1,NULL),('DOW','Dow Chemical',1,NULL),('DPS','Dr Pepper Snapple Group',1,NULL),('DRI','Darden Restaurants',1,NULL),('DTE','DTE Energy Co.',1,NULL),('DUK','Duke Energy',1,NULL),('DVA','DaVita Inc.',1,NULL),('DVN','Devon Energy Corp.',1,NULL),('EA','Electronic Arts',1,NULL),('EBAY','eBay Inc.',1,NULL),('ECL','Ecolab Inc.',1,NULL),('ED','Consolidated Edison',1,NULL),('EFX','Equifax Inc.',1,NULL),('EIX','Edison Int\'l',1,NULL),('EL','Estee Lauder Cos.',1,NULL),('EMN','Eastman Chemical',1,NULL),('EMR','Emerson Electric Company',1,NULL),('ENDP','Endo International',1,NULL),('EOG','EOG Resources',1,NULL),('EQIX','Equinix',1,NULL),('EQR','Equity Residential',1,NULL),('EQT','EQT Corporation',1,NULL),('ES','Eversource Energy',1,NULL),('ESRX','Express Scripts',1,NULL),('ESS','Essex Property Trust Inc',1,NULL),('ETFC','E*Trade',1,NULL),('ETN','Eaton Corporation',1,NULL),('ETR','Entergy Corp.',1,NULL),('EW','Edwards Lifesciences',1,NULL),('EXC','Exelon Corp.',1,NULL),('EXPD','Expeditors Int\'l',1,NULL),('EXPE','Expedia Inc.',1,NULL),('EXR','Extra Space Storage',1,NULL),('F','Ford Motor',1,NULL),('FAST','Fastenal Co',1,NULL),('FB','Facebook',1,NULL),('FBHS','Fortune Brands Home & Security',1,NULL),('FCX','Freeport-McMoran Cp & Gld',1,NULL),('FDX','FedEx Corporation',1,NULL),('FE','FirstEnergy Corp',1,NULL),('FFIV','F5 Networks',1,NULL),('FIS','Fidelity National Information Services',1,NULL),('FISV','Fiserv Inc',1,NULL),('FITB','Fifth Third Bancorp',1,NULL),('FL','Foot Locker Inc',1,NULL),('FLIR','FLIR Systems',1,NULL),('FLR','Fluor Corp.',1,NULL),('FLS','Flowserve Corporation',1,NULL),('FMC','FMC Corporation',1,NULL),('FOX','Twenty-First Century Fox Class B',1,NULL),('FOXA','Twenty-First Century Fox Class A',1,NULL),('FRT','Federal Realty Investment Trust',1,NULL),('FSLR','First Solar Inc',1,NULL),('FTI','FMC Technologies Inc.',1,NULL),('FTR','Frontier Communications',1,NULL),('FTV','Fortive Corp',1,NULL),('GD','General Dynamics',1,NULL),('GE','General Electric',1,NULL),('GGP','General Growth Properties Inc.',1,NULL),('GILD','Gilead Sciences',1,NULL),('GIS','General Mills',1,NULL),('GLW','Corning Inc.',1,NULL),('GM','General Motors',1,NULL),('GOOG','Alphabet Inc Class C',1,NULL),('GOOGL','Alphabet Inc Class A',1,NULL),('GPC','Genuine Parts',1,NULL),('GPN','Global Payments Inc',1,NULL),('GPS','Gap (The)',1,NULL),('GRMN','Garmin Ltd.',1,NULL),('GS','Goldman Sachs Group',1,NULL),('GT','Goodyear Tire & Rubber',1,NULL),('GWW','Grainger (W.W.) Inc.',1,NULL),('HAL','Halliburton Co.',1,NULL),('HAR','Harman Int\'l Industries',1,NULL),('HAS','Hasbro Inc.',1,NULL),('HBAN','Huntington Bancshares',1,NULL),('HBI','Hanesbrands Inc',1,NULL),('HCA','HCA Holdings',1,NULL),('HCN','Welltower Inc.',1,NULL),('HCP','HCP Inc.',1,NULL),('HD','Home Depot',1,NULL),('HES','Hess Corporation',1,NULL),('HIG','Hartford Financial Svc.Gp.',1,NULL),('HOG','Harley-Davidson',1,NULL),('HOLX','Hologic',1,NULL),('HON','Honeywell Int\'l Inc.',1,NULL),('HP','Helmerich & Payne',1,NULL),('HPE','Hewlett Packard Enterprise',1,NULL),('HPQ','HP Inc.',1,NULL),('HRB','Block H&R',1,NULL),('HRL','Hormel Foods Corp.',1,NULL),('HRS','Harris Corporation',1,NULL),('HSIC','Henry Schein',1,NULL),('HST','Host Hotels & Resorts',1,NULL),('HSY','The Hershey Company',1,NULL),('HUM','Humana Inc.',1,NULL),('IBM','International Bus. Machines',1,NULL),('ICE','Intercontinental Exchange',1,NULL),('IFF','Intl Flavors & Fragrances',1,NULL),('ILMN','Illumina Inc',1,NULL),('INTC','Intel Corp.',1,NULL),('INTU','Intuit Inc.',1,NULL),('IP','International Paper',1,NULL),('IPG','Interpublic Group',1,NULL),('IR','Ingersoll-Rand PLC',1,NULL),('IRM','Iron Mountain Incorporated',1,NULL),('ISRG','Intuitive Surgical Inc.',1,NULL),('ITW','Illinois Tool Works',1,NULL),('IVZ','Invesco Ltd.',1,NULL),('JBHT','J. B. Hunt Transport Services',1,NULL),('JCI','Johnson Controls International Plc',1,NULL),('JEC','Jacobs Engineering Group',1,NULL),('JNJ','Johnson & Johnson',1,NULL),('JNPR','Juniper Networks',1,NULL),('JPM','JPMorgan Chase & Co.',1,NULL),('JWN','Nordstrom',1,NULL),('K','Kellogg Co.',1,NULL),('KEY','KeyCorp',1,NULL),('KHC','Kraft Heinz Co',1,NULL),('KIM','Kimco Realty',1,NULL),('KLAC','KLA-Tencor Corp.',1,NULL),('KMB','Kimberly-Clark',1,NULL),('KMI','Kinder Morgan',1,NULL),('KMX','Carmax Inc',1,NULL),('KO','Coca Cola Company',1,NULL),('KORS','Michael Kors Holdings',1,NULL),('KR','Kroger Co.',1,NULL),('KSS','Kohl\'s Corp.',1,NULL),('KSU','Kansas City Southern',1,NULL),('L','Loews Corp.',1,NULL),('LB','L Brands Inc.',1,NULL),('LEG','Leggett & Platt',1,NULL),('LEN','Lennar Corp.',1,NULL),('LH','Laboratory Corp. of America Holding',1,NULL),('LKQ','LKQ Corporation',1,NULL),('LLL','L-3 Communications Holdings',1,NULL),('LLTC','Linear Technology Corp.',1,NULL),('LLY','Lilly (Eli) & Co.',1,NULL),('LM','Legg Mason',1,NULL),('LMT','Lockheed Martin Corp.',1,NULL),('LNC','Lincoln National',1,NULL),('LNT','Alliant Energy Corp',1,NULL),('LOW','Lowe\'s Cos.',1,NULL),('LRCX','Lam Research',1,NULL),('LUK','Leucadia National Corp.',1,NULL),('LUV','Southwest Airlines',1,NULL),('LVLT','Level 3 Communications',1,NULL),('LYB','LyondellBasell',1,NULL),('M','Macy\'s Inc.',1,NULL),('MA','Mastercard Inc.',1,NULL),('MAC','Macerich',1,NULL),('MAR','Marriott Int\'l.',1,NULL),('MAS','Masco Corp.',1,NULL),('MAT','Mattel Inc.',1,NULL),('MCD','McDonald\'s Corp.',1,NULL),('MCHP','Microchip Technology',1,NULL),('MCK','McKesson Corp.',1,NULL),('MCO','Moody\'s Corp',1,NULL),('MDLZ','Mondelez International',1,NULL),('MDT','Medtronic plc',1,NULL),('MET','MetLife Inc.',1,NULL),('MHK','Mohawk Industries',1,NULL),('MJN','Mead Johnson',1,NULL),('MKC','McCormick & Co.',1,NULL),('MLM','Martin Marietta Materials',1,NULL),('MMC','Marsh & McLennan',1,NULL),('MMM','3M Company',1,NULL),('MNK','Mallinckrodt Plc',1,NULL),('MNST','Monster Beverage',1,NULL),('MO','Altria Group Inc',1,NULL),('MON','Monsanto Co.',1,NULL),('MOS','The Mosaic Company',1,NULL),('MPC','Marathon Petroleum',1,NULL),('MRK','Merck & Co.',1,NULL),('MRO','Marathon Oil Corp.',1,NULL),('MS','Morgan Stanley',1,NULL),('MSFT','Microsoft Corp.',1,NULL),('MSI','Motorola Solutions Inc.',1,NULL),('MTB','M&T Bank Corp.',1,NULL),('MTD','Mettler Toledo',1,NULL),('MU','Micron Technology',1,NULL),('MUR','Murphy Oil',1,NULL),('MYL','Mylan N.V.',1,NULL),('NAVI','Navient',1,NULL),('NBL','Noble Energy Inc',1,NULL),('NDAQ','NASDAQ OMX Group',1,NULL),('NEE','NextEra Energy',1,NULL),('NEM','Newmont Mining Corp. (Hldg. Co.)',1,NULL),('NFLX','Netflix Inc.',1,NULL),('NFX','Newfield Exploration Co',1,NULL),('NI','NiSource Inc.',1,NULL),('NKE','Nike',1,NULL),('NLSN','Nielsen Holdings',1,NULL),('NOC','Northrop Grumman Corp.',1,NULL),('NOV','National Oilwell Varco Inc.',1,NULL),('NRG','NRG Energy',1,NULL),('NSC','Norfolk Southern Corp.',1,NULL),('NTAP','NetApp',1,NULL),('NTRS','Northern Trust Corp.',1,NULL),('NUE','Nucor Corp.',1,NULL),('NVDA','Nvidia Corporation',1,NULL),('NWL','Newell Rubbermaid Co.',1,NULL),('NWS','News Corp. Class B',1,NULL),('NWSA','News Corp. Class A',1,NULL),('O','Realty Income Corporation',1,NULL),('OI','Owens-Illinois Inc',1,NULL),('OKE','ONEOK',1,NULL),('OMC','Omnicom Group',1,NULL),('ORCL','Oracle Corp.',1,NULL),('ORLY','O\'Reilly Automotive',1,NULL),('OXY','Occidental Petroleum',1,NULL),('PAYX','Paychex Inc.',1,NULL),('PBCT','People\'s United Financial',1,NULL),('PBI','Pitney-Bowes',1,NULL),('PCAR','PACCAR Inc.',1,NULL),('PCG','PG&E Corp.',1,NULL),('PCLN','Priceline.com Inc',1,NULL),('PDCO','Patterson Companies',1,NULL),('PEG','Public Serv. Enterprise Inc.',1,NULL),('PEP','PepsiCo Inc.',1,NULL),('PFE','Pfizer Inc.',1,NULL),('PFG','Principal Financial Group',1,NULL),('PG','Procter & Gamble',1,NULL),('PGR','Progressive Corp.',1,NULL),('PH','Parker-Hannifin',1,NULL),('PHM','Pulte Homes Inc.',1,NULL),('PKI','PerkinElmer',1,NULL),('PLD','Prologis',1,NULL),('PM','Philip Morris International',1,NULL),('PNC','PNC Financial Services',1,NULL),('PNR','Pentair Ltd.',1,NULL),('PNW','Pinnacle West Capital',1,NULL),('PPG','PPG Industries',1,NULL),('PPL','PPL Corp.',1,NULL),('PRGO','Perrigo',1,NULL),('PRU','Prudential Financial',1,NULL),('PSA','Public Storage',1,NULL),('PSX','Phillips 66',1,NULL),('PVH','PVH Corp.',1,NULL),('PWR','Quanta Services Inc.',1,NULL),('PX','Praxair Inc.',1,NULL),('PXD','Pioneer Natural Resources',1,NULL),('PYPL','PayPal',1,NULL),('QCOM','QUALCOMM Inc.',1,NULL),('QRVO','Qorvo',1,NULL),('R','Ryder System',1,NULL),('RAI','Reynolds American Inc.',1,NULL),('RCL','Royal Caribbean Cruises Ltd',1,NULL),('REGN','Regeneron',1,NULL),('RF','Regions Financial Corp.',1,NULL),('RHI','Robert Half International',1,NULL),('RHT','Red Hat Inc.',1,NULL),('RIG','Transocean',1,NULL),('RL','Polo Ralph Lauren Corp.',1,NULL),('ROK','Rockwell Automation Inc.',1,NULL),('ROP','Roper Industries',1,NULL),('ROST','Ross Stores',1,NULL),('RRC','Range Resources Corp.',1,NULL),('RSG','Republic Services Inc',1,NULL),('RTN','Raytheon Co.',1,NULL),('SBUX','Starbucks Corp.',1,NULL),('SCG','SCANA Corp',1,NULL),('SCHW','Charles Schwab Corporation',1,NULL),('SE','Spectra Energy Corp.',1,NULL),('SEE','Sealed Air',1,NULL),('SHW','Sherwin-Williams',1,NULL),('SIG','Signet Jewelers',1,NULL),('SJM','JM Smucker',1,NULL),('SLB','Schlumberger Ltd.',1,NULL),('SLG','SL Green Realty',1,NULL),('SNA','Snap-On Inc.',1,NULL),('SNI','Scripps Networks Interactive Inc.',1,NULL),('SO','Southern Co.',1,NULL),('SPG','Simon Property Group Inc',1,NULL),('SPGI','S&P Global, Inc.',1,NULL),('SPLS','Staples Inc.',1,NULL),('SRCL','Stericycle Inc',1,NULL),('SRE','Sempra Energy',1,NULL),('STI','SunTrust Banks',1,NULL),('STJ','St Jude Medical',1,NULL),('STT','State Street Corp.',1,NULL),('STX','Seagate Technology',1,NULL),('STZ','Constellation Brands',1,NULL),('SWK','Stanley Black & Decker',1,NULL),('SWKS','Skyworks Solutions',1,NULL),('SWN','Southwestern Energy',1,NULL),('SYF','Synchrony Financial',1,NULL),('SYK','Stryker Corp.',1,NULL),('SYMC','Symantec Corp.',1,NULL),('SYY','Sysco Corp.',1,NULL),('T','AT&T Inc',1,NULL),('TAP','Molson Coors Brewing Company',1,NULL),('TDC','Teradata Corp.',1,NULL),('TDG','TransDigm Group',1,NULL),('TEL','TE Connectivity Ltd.',1,NULL),('TGNA','Tegna',1,NULL),('TGT','Target Corp.',1,NULL),('TIF','Tiffany & Co.',1,NULL),('TJX','TJX Companies Inc.',1,NULL),('TMK','Torchmark Corp.',1,NULL),('TMO','Thermo Fisher Scientific',1,NULL),('TRIP','TripAdvisor',1,NULL),('TROW','T. Rowe Price Group',1,NULL),('TRV','The Travelers Companies Inc.',1,NULL),('TSCO','Tractor Supply Company',1,NULL),('TSN','Tyson Foods',1,NULL),('TSO','Tesoro Petroleum Co.',1,NULL),('TSS','Total System Services',1,NULL),('TWX','Time Warner Inc.',1,NULL),('TXN','Texas Instruments',1,NULL),('TXT','Textron Inc.',1,NULL),('UA','Under Armour',1,NULL),('UA.C','Under Armour',1,NULL),('UAL','United Continental Holdings',1,NULL),('UDR','UDR Inc',1,NULL),('UHS','Universal Health Services, Inc.',1,NULL),('ULTA','Ulta Salon Cosmetics & Fragrance Inc',1,NULL),('UNH','United Health Group Inc.',1,NULL),('UNM','Unum Group',1,NULL),('UNP','Union Pacific',1,NULL),('UPS','United Parcel Service',1,NULL),('URBN','Urban Outfitters',1,NULL),('URI','United Rentals, Inc.',1,NULL),('USB','U.S. Bancorp',1,NULL),('UTX','United Technologies',1,NULL),('V','Visa Inc.',1,NULL),('VAR','Varian Medical Systems',1,NULL),('VFC','V.F. Corp.',1,NULL),('VIAB','Viacom Inc.',1,NULL),('VLO','Valero Energy',1,NULL),('VMC','Vulcan Materials',1,NULL),('VNO','Vornado Realty Trust',1,NULL),('VRSK','Verisk Analytics',1,NULL),('VRSN','Verisign Inc.',1,NULL),('VRTX','Vertex Pharmaceuticals Inc',1,NULL),('VTR','Ventas Inc',1,NULL),('VZ','Verizon Communications',1,NULL),('WAT','Waters Corporation',1,NULL),('WBA','Walgreens Boots Alliance',1,NULL),('WDC','Western Digital',1,NULL),('WEC','Wisconsin Energy Corporation',1,NULL),('WFC','Wells Fargo',1,NULL),('WFM','Whole Foods Market',1,NULL),('WHR','Whirlpool Corp.',1,NULL),('WLTW','Willis Towers Watson',1,NULL),('WM','Waste Management Inc.',1,NULL),('WMB','Williams Cos.',1,NULL),('WMT','Wal-Mart Stores',1,NULL),('WRK','Westrock Co',1,NULL),('WU','Western Union Co',1,NULL),('WY','Weyerhaeuser Corp.',1,NULL),('WYN','Wyndham Worldwide',1,NULL),('WYNN','Wynn Resorts Ltd',1,NULL),('XEC','Cimarex Energy',1,NULL),('XEL','Xcel Energy Inc',1,NULL),('XL','XL Capital',1,NULL),('XLNX','Xilinx Inc',1,NULL),('XOM','Exxon Mobil Corp.',1,NULL),('XRAY','Dentsply Sirona',1,NULL),('XRX','Xerox Corp.',1,NULL),('XYL','Xylem Inc.',1,NULL),('YHOO','Yahoo Inc.',1,NULL),('YUM','Yum! Brands Inc',1,NULL),('ZBH','Zimmer Biomet Holdings',1,NULL),('ZION','Zions Bancorp',1,NULL),('ZTS','Zoetis',1,NULL);
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-11-08 13:01:47

# ----------------------------------------------------------
# this code is for filtering hbond data by
# xray exp. parameters, resolution 3.5, R free 0.3
# ----------------------------------------------------------

# ----------------------------------------------------------
# import
# ----------------------------------------------------------

# ----------------------------------------------------------
# constants
# ----------------------------------------------------------
input_file = '/Users/tkimura/Desktop/RNP/check_contact/non_redun_positives.txt'
output_file = '/Users/tkimura/Desktop/RNP/check_contact/filtered_xray_positives.txt'
pdb_list = ['1A34', '1AV6', '1B23', '1B2M', '1B7F', '1C0A', '1C9S', '1DDL', '1DFU', '1DI2', '1DK1', '1DRZ', '1DUL',
			'1E8O', '1EC6', '1EFW', '1EIY', '1EUQ', '1EUY', '1EXD', '1F7U', '1F7V', '1F7Y', '1F8V', '1FEU', '1FFK',
			'1FFY', '1FJG', '1FXL', '1G1X', '1G2E', '1G59', '1GAX', '1GTF', '1GTN', '1H2C', '1H3E', '1H4Q', '1H4S',
			'1HC8', '1HNW', '1HNX', '1HNZ', '1HQ1', '1HR0', '1I6U', '1I94', '1IBK', '1IBL', '1IBM', '1IL2', '1IVS',
			'1J1U', '1J2B', '1J5E', '1JBR', '1JBS', '1JBT', '1JID', '1JJ2', '1K73', '1K8A', '1K8W', '1K9M', '1KC8',
			'1KD1', '1KNZ', '1KOG', '1KQ2', '1KQS', '1L9A', '1LAJ', '1LNG', '1M1K', '1M5K', '1M5O', '1M5P', '1M5V',
			'1M8V', '1M8W', '1M8X', '1M8Y', '1M90', '1MFQ', '1MJI', '1MMS', '1MZP', '1N1H', '1N32', '1N33', '1N35',
			'1N38', '1N77', '1N78', '1N8R', '1NB7', '1NJI', '1NJP', '1NKW', '1O0B', '1O0C', '1OB2', '1OB5', '1OOA',
			'1Q2R', '1Q2S', '1Q7Y', '1Q81', '1Q82', '1Q86', '1QF6', '1QTQ', '1QU2', '1QVF', '1QVG', '1R3E', '1R9F',
			'1RC7', '1RLG', '1RPU', '1S03', '1S72', '1SDS', '1SJ3', '1SJ4', '1SJF', '1TFW', '1TFY', '1TTT', '1U0B',
			'1U1Y', '1U6B', '1UN6', '1UTD', '1UVI', '1UVJ', '1UVL', '1UVM', '1UVN', '1VBX', '1VBY', '1VBZ', '1VC0',
			'1VC6', '1VFG', '1VQ4', '1VQ5', '1VQ6', '1VQ7', '1VQ8', '1VQ9', '1VQK', '1VQL', '1VQM', '1VQN', '1VQO',
			'1VQP', '1VVJ', '1VY4', '1VY5', '1VY6', '1VY7', '1W2B', '1WMQ', '1WNE', '1WPU', '1WRQ', '1WSU', '1XMO',
			'1XMQ', '1XNQ', '1XNR', '1XOK', '1XPR', '1XPU', '1Y39', '1YHQ', '1YI2', '1YIJ', '1YIT', '1YJ9', '1YJN',
			'1YJW', '1YTU', '1YTY', '1YVP', '1YYK', '1YYO', '1YZ9', '1ZBH', '1ZH5', '1ZHO', '1ZJW', '1ZL3', '1ZSE',
			'2A1R', '2A8V', '2AB4', '2AKE', '2ANN', '2ANR', '2ASB', '2ATW', '2AZ0', '2AZ2', '2AZX', '2B2D', '2B2E',
			'2B2G', '2B3J', '2BGG', '2BH2', '2BNY', '2BQ5', '2BS0', '2BS1', '2BTE', '2BU1', '2BX2', '2BYT', '2C0B',
			'2C4Q', '2C4Y', '2C4Z', '2C50', '2C51', '2CT8', '2CV0', '2CV1', '2CV2', '2D6F', '2DB3', '2DER', '2DLC',
			'2DR2', '2DR5', '2DR7', '2DR8', '2DR9', '2DRA', '2DRB', '2DU3', '2DU4', '2DU5', '2DVI', '2DXI', '2E9R',
			'2E9T', '2E9Z', '2EC0', '2EZ6', '2F8K', '2F8T', '2FK6', '2FMT', '2FZ2', '2G4B', '2GJW', '2GXB', '2HHH',
			'2HVY', '2HW8', '2HYI', '2I82', '2I91', '2IX1', '2IY5', '2IZ8', '2IZ9', '2IZM', '2IZN', '2J0Q', '2J0S',
			'2JEA', '2JLU', '2JLV', '2JLW', '2JLX', '2JLY', '2JLZ', '2NQP', '2NUE', '2NUF', '2NUG', '2NZ4', '2OIH',
			'2OJ3', '2OTJ', '2OTL', '2OZB', '2PJP', '2PLY', '2PO1', '2PXB', '2PXD', '2PXE', '2PXL', '2PXP', '2PXT',
			'2PY9', '2Q66', '2QA4', '2QEX', '2QUX', '2R7R', '2R7S', '2R7T', '2R7U', '2R7V', '2R7W', '2R7X', '2R8S',
			'2RD2', '2RE8', '2UU9', '2UUA', '2UUB', '2UUC', '2UWM', '2UXC', '2UXD', '2V3C', '2VNU', '2VOD', '2VON',
			'2VOO', '2VOP', '2VPL', '2VQE', '2VQF', '2W2H', '2WJ8', '2X1A', '2X1F', '2XB2', '2XBM', '2XD0', '2XDB',
			'2XDD', '2XGJ', '2XLI', '2XLJ', '2XLK', '2XNR', '2XS2', '2XS5', '2XS7', '2XZL', '2XZO', '2Y8W', '2Y8Y',
			'2Y9H', '2YKG', '2ZH1', '2ZH2', '2ZH3', '2ZH4', '2ZH5', '2ZH6', '2ZH7', '2ZH8', '2ZH9', '2ZHA', '2ZHB',
			'2ZI0', '2ZKO', '2ZM5', '2ZNI', '2ZUE', '2ZUF', '2ZXU', '2ZZM', '2ZZN', '3ADB', '3ADC', '3ADD', '3ADL',
			'3AEV', '3AF6', '3AGV', '3AHU', '3AKZ', '3AL0', '3AM1', '3AMT', '3AVT', '3AVU', '3AVV', '3AVW', '3AVX',
			'3AVY', '3B0U', '3BO4', '3BOY', '3BSB', '3BSN', '3BSO', '3BSX', '3BT7', '3BX2', '3CC2', '3CC4', '3CC7',
			'3CCE', '3CCJ', '3CCL', '3CCM', '3CCQ', '3CCR', '3CCS', '3CCU', '3CCV', '3CD6', '3CMA', '3CME', '3CPW',
			'3CUL', '3CXC', '3CZ3', '3D2S', '3DD2', '3DH3', '3DLL', '3EGZ', '3EPH', '3EPJ', '3EPK', '3EQT', '3ER9',
			'3EX7', '3FHT', '3FOZ', '3FTE', '3FTF', '3G0H', '3G4S', '3G6E', '3G71', '3G9Y', '3GIB', '3GPQ', '3H5X',
			'3H5Y', '3HAX', '3HHN', '3HJW', '3HL2', '3HSB', '3HTX', '3I55', '3I56', '3I5X', '3I5Y', '3I61', '3I62',
			'3IAB', '3ICE', '3ICQ', '3IE1', '3IEM', '3IEV', '3IRW', '3IVK', '3IWN', '3K0J', '3K49', '3K4E', '3K5Q',
			'3K5Y', '3K5Z', '3K61', '3K62', '3K64', '3KFU', '3KLV', '3KMQ', '3KMS', '3KNA', '3KOA', '3KS8', '3KTW',
			'3L25', '3L26', '3LQX', '3LRN', '3LRR', '3LWO', '3LWP', '3LWQ', '3LWR', '3LWV', '3M7N', '3M85', '3MDG',
			'3MDI', '3MJ0', '3MOJ', '3MQK', '3MUM', '3MUR', '3MUT', '3MUV', '3MXH', '3NCU', '3NDB', '3NL0', '3NMA',
			'3NMR', '3NMU', '3NNA', '3NNC', '3NNH', '3NVI', '3NVK', '3O3I', '3O7V', '3O8C', '3O8R', '3OG8', '3OIJ',
			'3OIN', '3OL6', '3OL7', '3OL8', '3OL9', '3OLA', '3OLB', '3OUY', '3OV7', '3OVA', '3OVB', '3OVS', '3OW2',
			'3P6Y', '3PEW', '3PEY', '3PF4', '3PF5', '3PIO', '3PLA', '3PTX', '3PU0', '3PU4', '3Q0L', '3Q0M', '3Q0N',
			'3Q0O', '3Q0P', '3Q0Q', '3Q0R', '3Q0S', '3Q2T', '3QG9', '3QGB', '3QGC', '3QJJ', '3QJL', '3QJP', '3QRP',
			'3QSU', '3R1H', '3R1L', '3R2C', '3R2D', '3R9W', '3R9X', '3RC8', '3RER', '3RW6', '3SIU', '3SIV', '3SN2',
			'3SNP', '3SQW', '3SQX', '3T1H', '3T1Y', '3T3N', '3T3O', '3T5N', '3T5Q', '3TRZ', '3TS0', '3TS2', '3TUP',
			'3U2E', '3U4M', '3U56', '3UCU', '3UCZ', '3UD3', '3UD4', '3UMY', '3V6Y', '3V71', '3V74', '3V7E', '3VJR',
			'3VNV', '3VYX', '3VYY', '3W3S', '3WBM', '3WFR', '3WFS', '3WQY', '3WQZ', '3WZI', '3ZC0', '3ZD6', '3ZD7',
			'3ZGZ', '3ZJT', '3ZJU', '3ZJV', '3ZLA', '4AFY', '4AL5', '4AL6', '4AL7', '4ALP', '4AM3', '4AQ7', '4AQY',
			'4ARC', '4ARI', '4AS1', '4ATO', '4AY2', '4B3G', '4B3M', '4B3R', '4B3S', '4B3T', '4BA2', '4BHH', '4BPB',
			'4BW0', '4C4W', '4C7O', '4C8Y', '4C8Z', '4C9D', '4CQN', '4CSF', '4D25', '4D26', '4DB2', '4DR2', '4DR3',
			'4DR5', '4DR6', '4DUY', '4DV6', '4DV7', '4DWA', '4E78', '4ED5', '4EJT', '4ERD', '4EYA', '4F02', '4F1N',
			'4F3T', '4FVU', '4G0A', '4G9Z', '4GCW', '4GHA', '4GHL', '4GKJ', '4GKK', '4GV3', '4GV6', '4H5P', '4HOR',
			'4HOS', '4HOT', '4HT8', '4HT9', '4I67', '4IFD', '4IG8', '4II9', '4IJS', '4ILL', '4ILM', '4IO9', '4IOA',
			'4IQX', '4J1G', '4J39', '4J5V', '4J7L', '4J7M', '4JGN', '4JI0', '4JI1', '4JI3', '4JI7', '4JK0', '4JNG',
			'4JNX', '4JV5', '4JVY', '4JXX', '4JXZ', '4JYA', '4JYZ', '4JZU', '4JZV', '4K0K', '4K4S', '4K4T', '4K4U',
			'4K4V', '4K4W', '4K4X', '4K4Y', '4K4Z', '4K50', '4KHP', '4KNQ', '4KQ0', '4KR2', '4KR3', '4KR6', '4KR7',
			'4KR9', '4KRE', '4KRF', '4KTG', '4KXT', '4KZD', '4KZE', '4L47', '4L8H', '4L8R', '4LCK', '4LF4', '4LF6',
			'4LF7', '4LF8', '4LF9', '4LFB', '4LG2', '4LGT', '4LJ0', '4LMZ', '4LNT', '4LQ3', '4LSK', '4LT8', '4M2Z',
			'4M30', '4M4O', '4M59', '4M6D', '4M7A', '4M7D', '4MDX', '4N0T', '4N2Q', '4N2S', '4N48', '4NGB', '4NGC',
			'4NGD', '4NGF', '4NGG', '4NH3', '4NH5', '4NH6', '4NIA', '4NKU', '4NL3', '4O26', '4O8J', '4OAU', '4OAV',
			'4OE1', '4OHY', '4OHZ', '4OI0', '4OI1', '4OLA', '4OLB', '4OO1', '4OOG', '4OQ8', '4OQ9', '4P3E', '4PDB',
			'4PEH', '4PEI', '4PJO', '4PKD', '4PMI', '4PMW', '4PR6', '4PRF', '4Q9Q', '4Q9R', '4QEI', '4QG3', '4QI2',
			'4QIK', '4QIL', '4QM6', '4QOZ', '4QPX', '4QQB', '4QU6', '4QU7', '4QVC', '4QVD', '4QVI', '4R3I', '4R8I',
			'4RCJ', '4RCM', '4RDX', '4RMO', '4RWN', '4RWO', '4RWP', '4S2X', '4S2Y', '4S3N', '4TU0', '4TUE', '4TUW',
			'4TV0', '4TVX', '4TYW', '4TYY', '4TZ0', '4TZ6', '4U1U', '4U1V', '4U20', '4U24', '4U25', '4U26', '4U27',
			'4U3M', '4U3N', '4U3U', '4U4N', '4U4Q', '4U4R', '4U4U', '4U4Y', '4U4Z', '4U50', '4U51', '4U52', '4U53',
			'4U55', '4U56', '4U6F', '4U7U', '4U8T', '4UYJ', '4UYK', '4V2S', '4V4F', '4V5C', '4V5D', '4V5E', '4V5J',
			'4V5K', '4V5L', '4V5P', '4V5Q', '4V5R', '4V5S', '4V6C', '4V6F', '4V6G', '4V7J', '4V7L', '4V7M', '4V7S',
			'4V7T', '4V7U', '4V7V', '4V7W', '4V7X', '4V7Y', '4V7Z', '4V83', '4V84', '4V85', '4V87', '4V88', '4V8A',
			'4V8B', '4V8C', '4V8D', '4V8E', '4V8F', '4V8G', '4V8H', '4V8I', '4V8N', '4V8Q', '4V8X', '4V90', '4V95',
			'4V99', '4V9A', '4V9B', '4V9C', '4V9D', '4V9E', '4V9F', '4V9H', '4V9I', '4V9N', '4V9O', '4V9P', '4V9Q',
			'4V9R', '4V9S', '4W2F', '4W2G', '4W2H', '4W2I', '4W4G', '4W5N', '4W5O', '4W5Q', '4W5R', '4W5T', '4W90',
			'4W92', '4WAL', '4WAN', '4WC2', '4WC3', '4WF1', '4WF9', '4WFA', '4WFB', '4WJ4', '4WKR', '4WOI', '4WPO',
			'4WQ1', '4WQF', '4WQR', '4WQU', '4WQY', '4WR6', '4WRA', '4WRO', '4WRT', '4WSA', '4WSB', '4WSD', '4WT8',
			'4WTA', '4WTC', '4WTD', '4WTE', '4WTF', '4WTG', '4WTI', '4WTJ', '4WTK', '4WTL', '4WTM', '4WU1', '4WWW',
			'4WZD', '4WZM', '4WZO', '4WZQ', '4X2B', '4X4N', '4X4O', '4X4P', '4X4Q', '4X4R', '4X4S', '4X4T', '4X4U',
			'4X4V', '4X62', '4X64', '4X65', '4X66', '4X9E', '4XBF', '4XCO', '4XJN', '4XWW', '4Y4O', '4Y4P', '4Y91',
			'4YB1', '4YBB', '4YCO', '4YCP', '4YHH', '4YHW', '4YOE', '4YPB', '4YVI', '4YVJ', '4YVK', '4YYE', '4YZV',
			'4Z0C', '4Z31', '4Z3S', '4Z4C', '4Z4D', '4Z4E', '4Z4F', '4Z4G', '4Z4H', '4Z4I', '4Z7L', '4Z8C', '4ZCF',
			'4ZDO', '4ZDP', '4ZER', '4ZLD', '4ZLR', '4ZT0', '4ZT9', '5A0T', '5A0V', '5AH5', '5AMQ', '5AMR', '5AOR',
			'5AOX', '5AXM', '5AXN', '5B63', '5BR8', '5BS3', '5BTE', '5BUD', '5BYM', '5BZ1', '5BZ5', '5BZU', '5BZV',
			'5C0Y', '5C9H', '5CCB', '5CCX', '5CD4', '5CZP', '5D0A', '5D0B', '5D6G', '5D8H', '5DAR', '5DAT', '5DDO',
			'5DDP', '5DDQ', '5DDR', '5DE5', '5DE8', '5DEA', '5DET', '5DFE', '5DGE', '5DGV', '5DM6', '5DNO', '5DO4',
			'5DOX', '5DOY', '5DTO', '5DV7', '5E08', '5E3H', '5E6M', '5E7K', '5E81', '5ED1', '5ED2', '5EEU', '5EEV',
			'5EEW', '5EEX', '5EEY', '5EEZ', '5EF0', '5EF1', '5EF2', '5EF3', '5EIM', '5EL4', '5EL5', '5EL6', '5EL7',
			'5ELH', '5ELK', '5ELR', '5ELS', '5ELT', '5ELX', '5EMO', '5EN1', '5EX7', '5F5F', '5F5H', '5F6C', '5F8G',
			'5F8H', '5F8I', '5F8J', '5F8K', '5F8L', '5F8M', '5F8N', '5F98', '5F9F', '5F9H', '5FCI', '5FCJ', '5FDU',
			'5FDV', '5FJ4', '5FMZ', '5G4U', '5G4V', '5GIP', '5GJB', '5GMF', '5GMG', '5GUH', '5GXH', '5GXI', '5H1K',
			'5H1L', '5H3U', '5HAB', '5HAU', '5HC9', '5HCP', '5HCQ', '5HCR', '5HD1', '5HJZ', '5HK0', '5HKC', '5HO4',
			'5HP2', '5HP3', '5HR6', '5HR7', '5HSW', '5I4A', '5I4L', '5I9D', '5I9F', '5I9G', '5I9H', '5IB7', '5IB8',
			'5IBB', '5ID6', '5IT8', '5IWA', '5J30', '5J3C', '5J4B', '5J4C', '5J4D', '5J5B', '5J7L', '5J88', '5J8A',
			'5J8B', '5J91', '5JAJ', '5JB2', '5JBG', '5JC3', '5JC9', '5JCH', '5JEA', '5JJI', '5JJK', '5JJL', '5JJU',
			'5JRC', '5JS1', '5JS2', '5JVG', '5JXS', '5K36', '5K77', '5K78', '5KAL', '5KI6', '5KLA', '5L2L', '5LTA',
			'5LYB', '5M0I', '5M0J', '5M3H', '5M3J', '5M73', '5MEI', '5MFX', '5MJV', '5MSF', '5N94', '5NDJ', '5NDK',
			'5NDV', '5NEW', '5NG6', '5NPM', '5NRG', '5NS3', '5NS4', '5O1Y', '5O1Z', '5O58', '5O7H', '5OBM', '5OC6',
			'5OMW', '5ON2', '5ON3', '5ON6', '5ONH', '5SUP', '5SZE', '5T16', '5T7B', '5T8Y', '5TBW', '5TF6', '5TGA',
			'5THE', '5TSN', '5UD5', '5UDI', '5UDJ', '5UDK', '5UDL', '5UDZ', '5UJ2', '5UK4', '5V6X', '5V7C', '5V8I',
			'5VM9', '5VOE', '5VOF', '5VP2', '5VPO', '5VSU', '5VW1', '5VZJ', '5W0M', '5W0O', '5W1H', '5W1I', '5W3V',
			'5W4K', '5W5H', '5W5I', '5W6V', '5WEA', '5WIS', '5WIT', '5WLH', '5WNP', '5WNQ', '5WNR', '5WNS', '5WNT',
			'5WNU', '5WNV', '5WQE', '5WS2', '5WT1', '5WT3', '5WTK', '5WTY', '5WWE', '5WWF', '5WWG', '5WWR', '5WWS',
			'5WWT', '5WWW', '5WWX', '5WZG', '5WZH', '5WZI', '5WZJ', '5WZK', '5X6B', '5X70', '5XBL', '5XC6', '5XJ2',
			'5XTM', '5XWP', '5Y58', '5Y6Z', '5Y7M', '5YKI', '5YTS', '5YTT', '5YTV', '5YTX', '5YYN', '5Z4A', '5Z4D',
			'5Z4J', '5Z9X', '5ZC9', '5ZQ0', '5ZQ1', '5ZSA', '5ZSB', '5ZSC', '5ZSD', '5ZSE', '5ZSL', '5ZSM', '5ZSN',
			'5ZTH', '5ZTM', '5ZUU', '5ZW4', '6A4E', '6A6J', '6A6L', '6AAX', '6AAY', '6AJK', '6ASO', '6B14', '6B3K',
			'6BJG', '6BJH', '6BJV', '6BUW', '6BZ6', '6C5L', '6C6K', '6CAE', '6CAO', '6CAP', '6CAQ', '6CAR', '6CAS',
			'6CBD', '6CF2', '6CFJ', '6CFK', '6CFL', '6CMN', '6CYT', '6CZR', '6D06', '6D12', '6D1V', '6D2Z', '6D30',
			'6DB8', '6DB9', '6DCB', '6DCC', '6DCL', '6DTD', '6DU4', '6DU5', '6E0O', '6E4P', '6EEN', '6EVK', '6F3H',
			'6F4G', '6F4H', '6FHH', '6FHI', '6FKR', '6FPQ', '6FPX', '6FQ3', '6FQL', '6FQR', '6G2K', '6GC5', '6GD2',
			'6GD3', '6GPG', '6GSJ', '6GSK', '6GVY', '6GX6', '6H9H', '6H9I', '6HAU', '6HCT', '6HHQ', '6HTU', '6HYU',
			'6I0T', '6I0U', '6I0V', '6I3P', '6I7V', '6IFN', '6IFO', '6IS0', '6IV8', '6IV9', '6J7Z', '6JIM', '6M7K',
			'6MDZ', '6MFN', '6MKN', '6MPF', '6MPI', '6MSF', '6MWN', '6N4O', '6N6A', '6N6C', '6N6D', '6N6E', '6N6F',
			'6N6G', '6N6H', '6N6I', '6N6J', '6N6K', '6ND5', '6NOC', '6NOD', '6NOF', '6NOH', '6NY5', '6O16', '6O5F',
			'6O6V', '6O6X', '6O75', '6O7B', '6O97', '6OF1', '6OON', '6OTR', '6OV0', '6OXA', '6OXI', '6PUN', '6Q8U',
			'6QCV', '6QCW', '6QCX', '6QIC', '6QNQ', '6QNR', '6R9J', '6R9M', '6R9Q', '6RA4', '6S0M', '7MSF']

# ----------------------------------------------------------
# functions
# ----------------------------------------------------------

# ----------------------------------------------------------
# main
# ----------------------------------------------------------
with open(output_file, 'w') as fo:
	with open(input_file) as f:
		for lines in f.readlines():
			if lines[0:4].upper() in pdb_list:
				fo.writelines(lines)
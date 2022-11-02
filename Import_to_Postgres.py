import pandas as pd
df = pd.read_csv(r"C:\Users\wausa\Work\Data\Object_Fields\Contact_Fields_All_Data.csv")
df.columns = [c.lower() for c in df.columns] # PostgreSQL doesn't like capitals or spaces



accounts_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Accounts_All_Data.csv")
contacts_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Contacts_All_Data.csv")
sales_leads_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Sales_Leads_All_Data.csv")
opportunities_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Opportunities_All_Data.csv")
market_intelligence_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Market_Intelligence_All_Data.csv")
line_items_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Line_Items_All_Data.csv")
po_orders_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\PO_Orders_All_Data.csv")
campaign_member_all_data = pd.read_csv(r"C:\Users\wausa\Work\Data\SF_Data\Campaign_Member_Field_History_All_Data.csv")

# PostgreSQL doesn't like capitals or spaces
accounts_all_data.columns = [c.lower() for c in accounts_all_data.columns]
contacts_all_data.columns = [c.lower() for c in contacts_all_data.columns]
sales_leads_all_data.columns = [c.lower() for c in sales_leads_all_data.columns]
opportunities_all_data.columns = [c.lower() for c in opportunities_all_data.columns]
market_intelligence_all_data.columns = [c.lower() for c in market_intelligence_all_data.columns]
line_items_all_data.columns = [c.lower() for c in line_items_all_data.columns]
po_orders_all_data.columns = [c.lower() for c in po_orders_all_data.columns]
campaign_member_all_data.columns = [c.lower() for c in campaign_member_all_data.columns]



from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:@localhost:5432/postgres')

# df.to_sql('contact_fields', engine)

accounts_all_data.to_sql('accounts_all_data', engine) # make contacts one
contacts_all_data.to_sql('contacts_all_data', engine)
sales_leads_all_data.to_sql('sales_leads_all_data', engine)
opportunities_all_data.to_sql('opportunities_all_data', engine)
market_intelligence_all_data.to_sql('market_intelligence_all_data', engine)
line_items_all_data.to_sql('line_items_all_data', engine)
po_orders_all_data.to_sql('po_orders_all_data', engine)
campaign_member_all_data.to_sql('campaign_members_all_data', engine)





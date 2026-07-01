from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


app=FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=False,
                   allow_headers=["*"],
                   allow_methods=["*"])

class Userdata(BaseModel):
    comm_name:str
    fno:str
    date:str
    



@app.post("/send_data")
def getdata(Userdata:Userdata):
    name=Userdata.comm_name
    leave_type=Userdata.fno
    date=Userdata.date
    date = datetime.strptime(Userdata.date, "%Y-%m-%d").strftime("%d-%b-%Y")
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
    creds=Credentials.from_service_account_file("credentials.json",scopes=scopes)
    client=gspread.authorize(creds)

    sheet_id="1SBj6p6g0U4iZ77r20hqkyflaTIVMEsGguq3ufjQRaHk"

    sheet=client.open_by_key(sheet_id).sheet1
    values=sheet.get_all_values()
    headers=values[0]
    try:
        col=headers.index(name)+1
    except ValueError:
        print("Employee not found")
    row=None
    for i,record in enumerate(values[1:],start=2):
        if record[0]==date:
            row=i
            break

    if row is None:
        print("No date found")
    else:
        sheet.update_cell(row,col,leave_type)    
    # print(name," ",types," ",date," ",type(date))
    # print("2026-07-01"==date)

















































"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import gspread
from google.oauth2.service_account import Credentials

scopes=["https://www.googleapis.com/auth/spreadsheets"]
creds=Credentials.from_service_account_file("credentials.json",scopes=scopes)
client=gspread.authorize(creds)

sheet_id="1SBj6p6g0U4iZ77r20hqkyflaTIVMEsGguq3ufjQRaHk"

sheet=client.open_by_key(sheet_id).sheet1
values=sheet.get_all_values()
headers=values[0]
app=FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=False,
                   allow_headers=["*"],
                   allow_methods=["*"])

class Userdata(BaseModel):
    comm_name:str
    fno:str
    date:str
    



@app.post("/send_data")
def getdata(Userdata:Userdata):
    name=Userdata.comm_name
    leave_type=Userdata.fno
    date=Userdata.date
    try:
        col=headers.index(name)+1
    except ValueError:
        print("Employee not found")
    row=None
    for i,record in enumerate(values[1:],start=2):
        if record[0]==date:
            row=i
            break

    if row is None:
        print("No date found")
    sheet.update_cell(row,col,leave_type)    
    # print(name," ",types," ",date," ",type(date))
    # print("2026-07-01"==date)




"""
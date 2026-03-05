import requests
import bs4
from fake_useragent import UserAgent
import time
import re
import csv
import random
branch_shorthand=input("Input shorthand of your branch\n(for example bec for electronics) :  ").strip().upper()
start_range=int(input("Enter starting roll no. : "))
end_range=int(input("Enter ending roll no. : "))
with open("result.csv","w") as f:
    fieldname=["ROLL NUMBER","NAME","CG"]
    data=csv.DictWriter(f,fieldnames=fieldname)
    data.writeheader()
obj=UserAgent()
for i in range(start_range,end_range+1):
    roll="25"+branch_shorthand+str(f"{i:03}")
    data={"RollNumber":roll}
    headers={'user-agent':obj.chrome}
    response=requests.post("http://results.nith.ac.in/scheme25/studentresult/result.asp",data=data,headers=headers)
    with open("data.html","w+") as f:
        f.write(response.text)
    with open("data.html","r") as f:
        content=f.read()
    try:
        soup_object=bs4.BeautifulSoup(content,"html.parser")
        data=soup_object.find('p',class_="formSetting",string=r"STUDENT NAME").next_sibling.next_sibling
        name=data.text.strip()
        cg_data=soup_object.find('p',class_="formSetting",string=re.compile(r"\d+/\d+=\d+(\.\d+)?"))
        cg_text=cg_data.text.strip()
        pattern=r"=(\d+(\.\d+)?)"
        cg=re.findall(pattern,cg_text)
        real_cg=cg[0]
        roll_data=soup_object.find('p',class_="formSetting",string=re.compile(roll))
        roll_text=roll_data.text.strip()
        with open("result.csv","a") as f:
            data=csv.DictWriter(f,fieldnames=fieldname)
            data.writerow({"ROLL NUMBER":roll_text,"CG":float(real_cg[0]),"NAME":name})    
        time.sleep(random.uniform(0.3,0.4))
    except AttributeError:
        print("Check your input details once again")
    














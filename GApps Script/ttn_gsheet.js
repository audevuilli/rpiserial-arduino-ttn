/*  
    Script by Uspizig - TTN-Google-Script

    Idea is to export Data from TTN to a Google Sheet using Webhook Integration
    https://www.thethingsindustries.com/docs/getting-started/migrating/major-changes/

    How to use the script? 
    1. Create a new google sheet. 
    2. Save your google sheet id -> https://docs.google.com/spreadsheets/d/YOUR-SHEET-ID/edit*gitd=0 
    3. Replace YOUR-SHEET-ID in the code below. 
    4. Deploy Script as Web App - Select Access to Everyone 
    5. Copy the URL Address and add it to TTN Integration Custom Webhook Base URL

    Parameters can be modifiy in the below script if you are interested to save more parameters from the TTN messages. See Uspizig GitHub repository https://github.com/Uspizig/Ttn-gooogle-script/tree/master for more configuraiton options.
*/

function test(e){
    var sheet = SpreadsheetApp.openById("YOUR-SHEET-ID");
    var firstSheet = sheet.getSheets()[0];
    sheet.setName("YOUR-SHEET-NAME");
  }
  
  // Function to retrieve Messages from TTN
  function doPost(e) {
    
    Logger.log("I was called")
    if(typeof e !== 'undefined')
    Logger.log(e.parameter);
    
    // Parameters to access the Google Sheet
    var sheet = SpreadsheetApp.openById("YOUR-SHEET-ID");
    var firstSheet = sheet.getSheets()[0];
    firstSheet.setName("YOUR-SHEET-NAME");
    
    // Fill in the 1st row
    firstSheet.getRange(1, 1).setValue('New Messages from TTN.');
    //firstSheet.getRange(1, 3).setValue(JSON.parse(e.postData.contents));
    firstSheet.getRange(2,1).setValue(['Timestamp']);
    firstSheet.getRange(2,2).setValue(['Message']);
    firstSheet.getRange(2,3).setValue(['Raw Message']);
    firstSheet.getRange(2,4).setValue(['Port:']); 
    firstSheet.getRange(2,5).setValue(['Packet#']);
    //firstSheet.getRange(2,6).setValue(['RSSI']);
    //firstSheet.getRange(2,7).setValue(['SNR']);
    
    // Fill in the subsequent rows
    var jsonData = JSON.parse(e.postData.contents);
    firstSheet.appendRow([jsonData.received_at,jsonData.uplink_message.decoded_payload.msg, jsonData.uplink_message.frm_payload, jsonData.uplink_message.f_port, jsonData.uplink_message.f_cnt]);
    
    // Create message data into Google Sheet
    return ContentService.createTextOutput(JSON.stringify(e))
  }
  